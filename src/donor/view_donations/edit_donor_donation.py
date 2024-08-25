import pandas as pd
import streamlit as st
from PIL import Image
from io import BytesIO

from src.db_utils.db_donors import update_inventory_item
from src.db_utils.image_to_blob_util import blob_to_image


def edit_or_view_post(row):
    st.header("Edit Your Item")

    with st.form(key='edit_form'):
        # Display and edit each attribute of the item within a form
        food_name = st.text_input("Food Name", value=row['Food Name'])
        food_type = st.selectbox("Food Type", options=["Cooked", "Packaged"],
                                 index=["Cooked", "Packaged"].index(row['Food Type']))
        description = st.text_area("Description", value=row['Description'])
        is_halal = st.selectbox("Is Halal", options=["True", "False"], index=[1, 0].index(row['Is Halal'] == "True"))
        is_vegetarian = st.selectbox("Is Vegetarian", options=["True", "False"],
                                     index=[1, 0].index(row['Is Vegetarian'] == "True"))
        expiry_date = st.date_input("Expiry Date", value=pd.to_datetime(row['Expiry Date']))

        st.subheader("QR Code")
        if row['QR Code'] is not None:
            qr_code_image = blob_to_image(row['QR Code'])
            if qr_code_image:
                st.image(qr_code_image, caption="QR Code", use_column_width=True)
            else:
                st.write("Failed to load QR code")
        else:
            st.write("No QR code available")

        col1, col2 = st.columns(2)
        with col1:
            # Form submission buttons
            submitted = st.form_submit_button(label="Update")
        with col2:
            cancelled = st.form_submit_button(label="Cancel")

    if submitted:
        is_halal_value = 1 if is_halal == "True" else 0
        is_vegetarian_value = 1 if is_vegetarian == "True" else 0

        success = update_inventory_item(
            int(row['id']), food_name, food_type, description,
            is_halal_value, is_vegetarian_value, expiry_date
        )

        if success:
            st.success("Changes saved successfully!")
            st.session_state.edit_id = -1  # Reset the edit_id or handle as needed
        else:
            st.error("Failed to save changes. Please try again.")

    if cancelled:
        st.session_state.edit_id = -1  # Reset the edit_id
        st.rerun()  # Refresh the page to go back to the main view
