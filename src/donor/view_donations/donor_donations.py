import streamlit as st
import pandas as pd
from src.db_utils.db_donors import get_vendor_donations
from src.db_utils.image_to_blob_util import blob_to_image
from src.donor.view_donations.edit_donor_donation import edit_or_view_post


def view_donations_page():
    if st.session_state.authentication_status == True and st.session_state.role == 'vendor':
        st.session_state.post_food_form_submitted = False

        # st.session_state.edit_id = -1
        if 'edit_id' not in st.session_state:
            st.session_state.edit_id = -1

        try:
            vendor_id = st.session_state.user_id
            donations = get_vendor_donations(vendor_id)
            if donations:
                # Convert donations to DataFrame
                donations_df = pd.DataFrame(donations, columns=[
                    "id", "Food Name", "Food Type", "Description", "Is Halal",
                    "Is Vegetarian", "Expiry Date", "Date of Entry",
                    "Total Quantity", "Qty Left After Booking", "Qty Left After Scanning", "Photo", "QR Code"
                ])
                if st.session_state.edit_id == -1:
                    process_donations_list(donations_df)
                else:
                    edit_or_view_post(donations_df.loc[donations_df['id'] == st.session_state.edit_id].iloc[0])
            else:
                st.header("No donations found or failed to retrieve donations.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("User is not logged in or is not a vendor.")

def process_donations_list(donations_df):
    st.header("Here is a list of the food items you have donated so far.")
    count = 0

    # Create tiles for each donation
    for idx, row in donations_df.iterrows():
        col1, col2 = st.columns(2)  # Create two columns for side-by-side layout

        with col1:
            st.subheader("Item: " + row['Food Name'])  # Display Food Name
            st.write("Expiry Date: " + row['Expiry Date'])
            st.write("Quantity / Pax Servable: " + str(row['Total Quantity']))

        with col2:
            if row['Photo'] is not None:
                # Convert binary data to image using your blob_to_image function
                image = blob_to_image(row['Photo'])
                if image:
                    st.image(image, use_column_width=True)
                else:
                    st.write("Failed to load image")
            else:
                st.write("No image available")

        count += 1
        edit_link = f"<td><a href=\"?inventory_id={row['id']}\" target=\"_self\">Edit</a></td>"
        if st.button(f"View QR Code or Edit Item {count}"):
            st.session_state.edit_id = row['id']

            st.rerun()

        st.divider()
