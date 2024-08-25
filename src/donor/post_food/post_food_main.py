import datetime

import streamlit as st

from src.donor.post_food.post_food_success import show_success_page


def post_food():
    if st.session_state.post_food_form_submitted:
        show_success_page(
            st.session_state.food_name,
            st.session_state.food_type,
            st.session_state.description,
            st.session_state.is_halal,
            st.session_state.is_vegetarian,
            st.session_state.quantity,
            st.session_state.expiry_date,
            st.session_state.recipient,
            st.session_state.image
        )
    else:
        show_form_page()


def show_form_page():
    st.title("Post Food")

    st.write("Fill out the form below to post food details available at your restaurant.")

    with st.form(key='food_form'):
        food_name = st.text_input("Food Name", placeholder="Enter the food name")
        food_type = st.selectbox("Food Type", options=["Cooked", "Packaged"])
        description = st.text_area("Description", placeholder="Enter a brief description of the food")
        is_halal = st.checkbox("Halal", value=False)
        is_vegetarian = st.checkbox("Vegetarian", value=False)
        quantity = st.slider("Total quantity/pax servable", 1, 200, 1)
        expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())
        recipient = st.selectbox("Select who to donate to:", options=["NGOs", "Individuals"])
        image = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not food_name or not food_type or not description or not image or not recipient:
            st.warning("Please fill in all required fields, upload an image, and select a recipient.")
        else:
            # Store form data in session state
            st.session_state.food_name = food_name
            st.session_state.food_type = food_type
            st.session_state.description = description
            st.session_state.is_halal = is_halal
            st.session_state.is_vegetarian = is_vegetarian
            st.session_state.quantity = quantity
            st.session_state.expiry_date = expiry_date
            st.session_state.image = image
            st.session_state.recipient = recipient
            st.session_state.post_food_form_submitted = True
            st.rerun()





