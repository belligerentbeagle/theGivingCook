import streamlit as st
from PIL import Image

from src.db_utils.db_donors import DatabaseConnector
from src.donor.donor_donations import view_donations_page
from src.donor.home import run_home_page


def show_success_page(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient,
                      image):
    add_item_logic(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient, image)
    st.success("Food posted successfully!")
    st.header("Thank you for posting your food donation.")

    st.write(f"**Food Name**: {food_name}")
    st.write(f"**Food Type**: {food_type}")
    st.write(f"**Description**: {description}")
    st.write(f"**Halal**: {'Yes' if is_halal else 'No'}")
    st.write(f"**Vegetarian**: {'Yes' if is_vegetarian else 'No'}")
    st.write(f"**Serves**: {quantity} pax")
    st.write(f"**Expiry Date**: {expiry_date.strftime('%Y-%m-%d')}")
    st.write(f"**Beneficiary**: {recipient}")

    if image is not None:
        image_display = Image.open(image)
        st.image(image_display, caption='Uploaded Image', use_column_width=True)

    home = st.button("Go Back to Home")
    view_others = st.button("View Past Donations")

    if home:
        st.session_state.page = 'Home'
    if view_others:
        st.session_state.page = 'View Donations'


# updates db by calling corresponding db functions
# returns the qr code to be displayed
def add_item_logic(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient, image):
    vendor_id = st.session_state['user_id']  # CHANGE THIS SOON
    for_ngo = 1 if recipient == 'NGOs' else 0
    link = 'http://localhost:8501/?scan=True&collection_type=individual&inventory_id=2'
    dbconnect = DatabaseConnector()
    inventory_id = dbconnect.add_new_inventory_item_without_qrcode(food_name, food_type, description, is_halal, is_vegetarian, expiry_date, quantity, for_ngo, vendor_id, image)
    return inventory_id
