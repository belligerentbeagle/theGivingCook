import streamlit as st
from streamlit_modal import Modal
from PIL import Image
import datetime

def post_food():
    # Initialize session state for navigation and form submission if not already set
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    if st.session_state.form_submitted:
        show_success_modal()
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
        quantity = st.number_input("Quantity Available", min_value=1, step=1)
        expiry_date = st.date_input("Expiry Date", min_value=datetime.date.today())
        image = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not food_name or not food_type or not description or not image:
            st.warning("Please fill in all required fields and upload an image.")
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

            show_success_modal()

def show_success_modal():
    # Create a modal for the success message
    modal = Modal("Success Modal", key="succ-modal",)
    with st.modal("Success", key="success_modal"):
        st.success("Food posted successfully!")
        st.header("Thank you for posting your food donation.")

        st.write(f"**Food Name**: {st.session_state.food_name}")
        st.write(f"**Food Type**: {st.session_state.food_type}")
        st.write(f"**Description**: {st.session_state.description}")
        st.write(f"**Halal**: {'Yes' if st.session_state.is_halal else 'No'}")
        st.write(f"**Vegetarian**: {'Yes' if st.session_state.is_vegetarian else 'No'}")
        st.write(f"**Quantity Available**: {st.session_state.quantity}")
        st.write(f"**Expiry Date**: {st.session_state.expiry_date.strftime('%Y-%m-%d')}")

        # Display the uploaded image
        if st.session_state.image is not None:
            image_display = Image.open(st.session_state.image)
            st.image(image_display, caption='Uploaded Image', use_column_width=True)

        # Display buttons to navigate to different pages
        if st.button("Go Back to Home"):
            st.session_state.page = 'Home'
            st.session_state.form_submitted = False

        if st.button("View Past Donations"):
            st.session_state.page = 'Past Donations'
            st.session_state.form_submitted = False

# Main execution
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

if st.session_state.page == 'Home':
    post_food()
elif st.session_state.page == 'Past Donations':
    st.write("This is the Past Donations page.")
    # Add your Past Donations page logic here
