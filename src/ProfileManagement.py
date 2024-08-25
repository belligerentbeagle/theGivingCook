import streamlit as st
from db_utils.db_recipients import updateUser, updateNgo
from db_utils.db_donors import updateVendor

# Profile management for users, NGOs, and vendors
def profile_management():
    st.title("Profile Management")

    option = st.selectbox("Select profile to edit", ("User", "NGO", "Vendor"))

    if option == "User":
        user_id = st.number_input("User ID", min_value=1, step=1)
        first_name = st.text_input("First Name", placeholder="Enter first name")
        last_name = st.text_input("Last Name", placeholder="Enter last name")
        hp_number = st.text_input("HP Number", placeholder="Enter phone number")
        age = st.number_input("Age", min_value=1, max_value=120, step=1, placeholder="Enter age")
        sex = st.selectbox("Sex", ["M", "F"], index=0)

        if st.button("Update User"):
            updateUser(user_id, first_name, last_name, hp_number, age, sex)
            st.success(f"User {user_id} updated successfully.")

    elif option == "NGO":
        ngo_id = st.number_input("NGO ID", min_value=1, step=1)
        name = st.text_input("Name", placeholder="Enter NGO name")
        hp_number = st.text_input("HP Number", placeholder="Enter phone number")
        address = st.text_input("Address", placeholder="Enter address")
        number_of_ppl = st.number_input("Number of People", min_value=1, step=1, placeholder="Enter number of people")
        credit_id = st.number_input("Credit ID", min_value=1, step=1, placeholder="Enter credit ID")

        if st.button("Update NGO"):
            updateNgo(ngo_id, name, hp_number, address, number_of_ppl, credit_id)
            st.success(f"NGO {ngo_id} updated successfully.")

    elif option == "Vendor":
        vendor_id = st.number_input("Vendor ID", min_value=1, step=1)
        name = st.text_input("Name", placeholder="Enter vendor name")
        hp_number = st.text_input("HP Number", placeholder="Enter phone number")
        address = st.text_input("Address", placeholder="Enter address")
        cuisine = st.text_input("Cuisine", placeholder="Enter type of cuisine")
        description = st.text_area("Description", placeholder="Enter description")

        if st.button("Update Vendor"):
            updateVendor(vendor_id, name, hp_number, address, cuisine, description)
            st.success(f"Vendor {vendor_id} updated successfully.")


# Run the profile management page
if __name__ == "__main__":
    profile_management()
