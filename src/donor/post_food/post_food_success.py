import os
from io import BytesIO

import streamlit as st
from PIL import Image

from src.db_utils.db_donors import add_new_inventory_item_without_qrcode, update_inventory_item_with_qr_code, add_item_price
from src.donor.donor_donations import view_donations_page
from src.donor.generate_qr import generate_qr_code
from src.donor.home import run_home_page
from src.donor.post_food.food_price_algo import get_item_price


def show_success_page(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient,
                      image):
    qr_img = add_item_logic(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient, image)
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

    st.write("**Please get the recipient to scan this QR Code to receive the item:**")
    if qr_img is not None:
        st.image(qr_img, caption="Scan this QR code to collect the food item", width=500)


# updates db by calling corresponding db functions
# returns the byte image of qr code to be displayed
def add_item_logic(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, recipient, image):
    vendor_id = st.session_state['user_id']  # CHANGE THIS SOON
    for_ngo = 1 if recipient == 'NGOs' else 0
    type = 'ngo' if for_ngo else 'individual'

    inventory_id = add_new_inventory_item_without_qrcode(food_name, food_type, description, is_halal, is_vegetarian, expiry_date, quantity, for_ngo, vendor_id, image)

    # qrcode logic
    link = os.getenv("QR_LINK").format(collection_type=type, inventory_id=inventory_id)
    qr_img = generate_qr_code(link)
    buffered = BytesIO()
    qr_img.save(buffered, format="PNG")
    byte_img = buffered.getvalue()

    # upload qr code to db
    update_inventory_item_with_qr_code(inventory_id, qr_img)

    # add new price for the item
    add_item_price(inventory_id, get_item_price())

    return byte_img
