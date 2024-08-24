import streamlit as st
from PIL import Image
import datetime


def post_food():
    st.title("Post Food")

    st.write("Fill out the form below to post food details available at your restaurant.")

    with st.form(key='food_form'):
        food_name = st.text_input("Food Name", placeholder="Enter the food name")
        food_type = st.selectbox("Food Type", options=["Cooked", "Packaged"])
        description = st.text_area("Description", placeholder="Enter a brief description of the food")
        is_halal = st.checkbox("Halal", value=False)
        is_vegetarian = st.checkbox("Vegetarian", value=False)
        quantity = st.number_input("Quantity Available", min_value=1, step=1)
        expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())
        image = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not food_name or not food_type or not description or not image:
            st.warning("Please fill in all required fields and upload an image.")
        else:
            st.success("Food posted successfully!")
            st.write(f"**Food Name**: {food_name}")
            st.write(f"**Food Type**: {food_type}")
            st.write(f"**Description**: {description}")
            st.write(f"**Halal**: {'Yes' if is_halal else 'No'}")
            st.write(f"**Vegetarian**: {'Yes' if is_vegetarian else 'No'}")
            st.write(f"**Quantity Available**: {quantity}")
            st.write(f"**Expiry Date**: {expiry_date.strftime('%Y-%m-%d')}")

            # Display the uploaded image
            if image is not None:
                image_display = Image.open(image)
                st.image(image_display, caption='Uploaded Image', use_column_width=True)
