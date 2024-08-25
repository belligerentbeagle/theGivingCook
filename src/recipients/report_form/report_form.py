import streamlit as st
from datetime import datetime
import sqlite3
from src.recipients.report_form.report_form_success import show_success_page
from src.gmail.EmailSender import send_message


database_loc = "../data/theGivingCook.db"
email = "e0968802@u.nus.edu "

def file_report():

    if 'report_submitted' not in st.session_state:
        st.session_state.report_submitted = False

    if st.session_state.report_submitted:
        show_success_page(
            st.session_state.report_order,
            st.session_state.report_description,
        )
    else:
        show_report_form_page()

def insert_report(order, description):
    try:    
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vendor_reports(vendor_id, description, time)
            VALUES(?, ?, ?)
        """, (order[3], description, datetime.now()))
        conn.commit()

        cur.execute("""
            SELECT COUNT(*) FROM vendor_reports
            WHERE id = ?
        """, (order[3],))
        count = cur.fetchone()

        cur.execute("""
            SELECT name FROM vendor
            WHERE id = ?
        """, (order[3],))
        vendor_name = cur.fetchone()

        if (count >= 1):
            send_warning_email(vendor_name, order[1], count)

        send_report(vendor_name, order[1], description)
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def show_report_form_page():

    st.title("File Report")
    order = getItemsAndVendors()
    if order:
        st.write("Fill out the form below to file a report on the unsafe food provided")
        item_id, item_name, vendor_id, dates = order
    else:
        st.write("Make your first order now!")
        return None
    options = [(f"Order {name}: {date}", [name, date, id, vendor_id]) for name, date, id, vendor_id in zip(item_name, dates, item_id, vendor_id)]

    with st.form(key='report_form'):
        order = st.selectbox("Order", options=options, format_func=lambda x: x[0])  
        description = st.text_area("Description", placeholder="Enter a brief description of the situation")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if not order or not description:
                st.warning("Please fill in all required fields")
            else:
                # Store form data in session state                
                insert_report(order, description)

                st.session_state.report_order = order
                st.session_state.report_description = description
                st.session_state.report_submitted = True

def getItemsAndVendors():
    try:
        # Assuming 'user_id' is stored in session_state
        user_id = st.session_state.user_id 
        conn = sqlite3.connect(database_loc)
        cur = conn.cursor()
        cur.execute("""
            SELECT item_id FROM orders
            WHERE user_id = ?
        """, (user_id,))
        item_ids = cur.fetchall()

        cur.execute("""
            SELECT food_id, food_name, vendor_id, date_of_entry 
            FROM inventory 
            WHERE id IN ({})
        """.format(','.join('?' * len(item_ids))), item_ids)

        result = cur.fetchall()

        conn.close()

        if result:
            return result
        # else:
        #     item_id, item_name, vendor_id, dates = None, None, None, None 
        # return item_id, item_name, vendor_id, dates
    except Exception as e:
        print(e)
        return None
    
def send_warning_email(vendor, time, count):
    subject = "Urgent Alert: Potential Food Safety Issue Reported!"
    body = f"We have received {count} report(s) regarding food safety associated with food collected from {vendor} on {time}. Please take immediate action to investigate and address these concerns."  
    send_message(email, subject, body)
    
def send_report(vendor, time, description):
    subject = "Food Safety Report Filed"
    body = f"We have received a report regarding food safety associated with food collected from {vendor} on {time}. The report is as follow \n {description}"