import streamlit as st
from PIL import Image


def show_success_page(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date, image):
    st.success("Food posted successfully!")
    st.header("Thank you for posting your food donation.")

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

    # Display a button to navigate to the 'Past Donations' page
    if st.button("Go Back to Home"):
        st.session_state.page = 'Home'
        st.session_state.form_submitted = False
    # Display a button to navigate to the 'Past Donations' page
    if st.button("View Past Donations"):
        st.session_state.page = 'Past Donations'
        st.session_state.form_submitted = False
