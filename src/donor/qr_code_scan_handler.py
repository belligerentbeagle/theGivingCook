import streamlit as st

from src.db_utils.db_donors import DatabaseConnector

def handle_qr_scan(collection_type, inventory_id):
    db_connector = DatabaseConnector()
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