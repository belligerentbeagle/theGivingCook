import streamlit as st

# Profile management for users, NGOs, and vendors
def profile_management():
    st.title("Profile Management")

    option = st.session_state.role

    if option == "user":
        # user_id = st.number_input("User ID", min_value=1, step=1)
        first_name = st.text_input("First Name", placeholder="Enter first name", value=st.session_state.get('name', 'Guest'))
        last_name = st.text_input("Last Name", placeholder="Enter last name", value = "")
        hp_number = st.text_input("HP Number", placeholder="Enter phone number", value="+65 91327543")
        age = st.number_input("Age", min_value=16, max_value=120, step=1, placeholder="Enter age")
        sex = st.selectbox("Sex", ["M", "F"], index=0)

        if st.button("Update User"):
            # updateUser(user_id, first_name, last_name, hp_number, age, sex)
            st.success(f"User {first_name} {last_name} updated successfully.")

    elif option == "ngo":
        # ngo_id = st.number_input("NGO ID", min_value=1, step=1)
        name = st.text_input("Name", placeholder="Enter NGO name", value=st.session_state.get('name', 'Guest'))
        hp_number = st.text_input("HP Number", placeholder="Enter phone number", value="+65 91327543")
        address = st.text_input("Address", placeholder="Enter address", value="125 Marine Parade Ave 2 #01-22/23")
        number_of_ppl = st.number_input("Number of People", min_value=1, step=1, placeholder="Enter number of people")

        if st.button("Update NGO"):
            # updateNgo(ngo_id, name, hp_number, address, number_of_ppl, credit_id)
            st.success(f"NGO {name} updated successfully.")

    elif option == "vendor":
        # vendor_id = st.number_input("Vendor ID", min_value=1, step=1)
        name = st.text_input("Name", placeholder="Enter vendor name", value=st.session_state.get('name', 'Guest'))
        hp_number = st.text_input("HP Number", placeholder="Enter phone number", value="+65 91327543")
        address = st.text_input("Address", placeholder="Enter address", value="125 Bedok South Ave 2 #01-22/23")
        cuisine = st.text_input("Cuisine", placeholder="Enter type of cuisine", value="Western")
        description = st.text_area("Description", placeholder="Enter description", value=f"{st.session_state.get('name', 'Guest')} combines cooking and great ingredients to serve up quality Western food that is accessible to everyone.")

        if st.button("Update Vendor"):
            # updateVendor(vendor_id, name, hp_number, address, cuisine, description)
            st.success(f"Vendor {name} updated successfully.")

# Run the profile management page
if __name__ == "__main__":
    profile_management()
