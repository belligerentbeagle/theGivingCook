import streamlit as st
import sqlite3
from src.db_utils.db_donors import DatabaseConnector
# TODO
# need check user id and that user actually made a booking, query the booking table and ensure that the inventory id is the same as the one in the ordertable

def handle_qr_scan(collection_type, inventory_id):
 db_connector = DatabaseConnector()

 user_id = st.session_state.user_id

 if db_connector.validateIfUserMadeBookingWithInventoryId(inventory_id, user_id):

    try:
        if collection_type.lower() == "ngo":
            st.write("Please enter the total quantity that you are collecting.")
            with st.form(key="collection_form"):
                qty = st.number_input("Quantity", min_value=1, step=1)
                submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                status = db_connector.update_inventory_qty_ngo(inventory_id, qty)
                if status:
                    st.success("Scan success")
                else:
                    st.error("Scan unsuccessful. Please approach the restaurant with proof of booking")
        else:
            status = db_connector.update_inventory_qty_individual(inventory_id)
            if status:
                st.success("Scan success")
            else:
                st.error("Scan unsuccessful. Please approach the restaurant with proof of booking")

    except Exception as e:
        return None
    
    return True
 else:
    st.error("User has not made a booking with the inventory id in question")
    return False