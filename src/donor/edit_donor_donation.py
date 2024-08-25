import streamlit as st
import pandas as pd
from PIL import Image
import io
from src.db_utils.db_donors import DatabaseConnector

def edit_donation_page(item_id):
    # TODO: Check user is logged in and have vendor role
    
    db_connector = DatabaseConnector()

    try:
        donation = db_connector.get_donation_by_id(item_id)
        if donation:
            row = donation

            st.write(f"Editing item: {row[1]}")

            new_food_name = st.text_input("Food Name", value=row[1], key=f"food_name_{item_id}")
            new_food_type = st.text_input("Food Type", value=row[2], key=f"food_type_{item_id}")
            new_description = st.text_area("Description", value=row[3], key=f"description_{item_id}")
            new_is_halal = st.selectbox("Is Halal", options=["True", "False"], index=0 if row[4] == 1 else 1, key=f"is_halal_{item_id}")
            new_is_vegetarian = st.selectbox("Is Vegetarian", options=["True", "False"], index=0 if row[5] == 1 else 1, key=f"is_vegetarian_{item_id}")
            new_expiry_date = st.date_input("Expiry Date", value=pd.to_datetime(row[6]), key=f"expiry_date_{item_id}")
            new_total_qty = st.number_input("Total Quantity", min_value=1, value=row[8], key=f"total_qty_{item_id}")
            new_curr_qty = st.number_input("Current Quantity", min_value=0, value=row[9], key=f"curr_qty_{item_id}")

            if new_curr_qty > new_total_qty:
                st.error("Current Quantity cannot be greater than Total Quantity.")
            elif st.button("Update"):
                is_halal_value = 1 if new_is_halal == "True" else 0
                is_vegetarian_value = 1 if new_is_vegetarian == "True" else 0
                
                success = db_connector.update_inventory_item(
                    item_id, new_food_name, new_food_type, new_description, 
                    is_halal_value, is_vegetarian_value, new_expiry_date, new_total_qty, new_curr_qty
                )
                if success:
                    st.success(f"Item \"{new_food_name}\" updated successfully.")
                else:
                    st.error(f"Failed to update \"{new_food_name}\".")

        else:
            st.write("Donation not found or failed to retrieve donation.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
