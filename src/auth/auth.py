import streamlit as st
import sqlite3
import streamlit_authenticator as stauth
import time

from src.db_utils.db_auth import query_db, register_user

# Load configuration from the database
def load_config():
    config = {"credentials": {"usernames": {}}, "cookie": {"name": "auth_cookie", "key": str(time.time()), "expiry_days": 0}}
    
    # Query the vendor, ngo, and user tables
    vendors = query_db("SELECT id, username, name, hp_number, address, cuisine, description, password FROM vendor")
    ngos = query_db("SELECT id, username, name, hp_number, address, number_of_ppl, password FROM ngo")
    users = query_db("SELECT id, username, first_name, last_name, hp_number, age, sex, password FROM user")
    
    # Load vendor users
    for vendor in vendors:
        user_id, username, name, hp_number, address, cuisine, description, password = vendor
        config["credentials"]["usernames"][username] = {"name": name, "password": password, "role": "vendor", "user_id": user_id}
    
    # Load NGO users
    for ngo in ngos:
        user_id, username, name, hp_number, address, number_of_ppl, password = ngo
        config["credentials"]["usernames"][username] = {"name": name, "password": password, "role": "ngo", "user_id": user_id}
    
    # Load individual users
    for user in users:
        user_id, username, first_name, last_name, hp_number, age, sex, password = user
        config["credentials"]["usernames"][username] = {"name": username, "password": password, "role": "user", "user_id": user_id}
    
    return config

def create_authenticator():
    config = load_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    return authenticator, config

def show_login_page():
    authenticator, config = create_authenticator()
    st.session_state.authenticator = authenticator
    st.session_state.authenticator_config = config
    
    # Check if this is the first load (before any login attempt)
    if "authentication_status" not in st.session_state:
        st.session_state.authentication_status = None

    # Attempt login only if user has tried to log in
    if st.session_state.authentication_status is None:
        st.session_state.username = None
        name, authentication_status, username = authenticator.login(key="1234")
        st.session_state.authentication_status = authentication_status

        if authentication_status:
            role, user_id = get_user_role_and_id(username)
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.user_id = user_id  # Store the user ID in session
            st.session_state.authentication_status = True
            st.stop()
        elif authentication_status is False:
            st.error('Username or password is incorrect')
            if st.button('No Account yet? Create an Account instead'):
                st.session_state.page = 'Create an Account'
                st.stop()
        else:
            # No login attempt yet, prompt user to log in
            st.warning('Please enter your username and password')
            if st.button('No Account yet? Create an Account instead'):
                st.session_state.page = 'Create an Account'
                st.stop()

# Updated get_user_role function to also return the user ID
def get_user_role_and_id(username):
    if "authenticator" not in st.session_state:
        authenticator, config = create_authenticator()
        st.session_state.authenticator = authenticator
        st.session_state.authenticator_config = config
    else:
        authenticator = st.session_state.authenticator
        config = st.session_state.authenticator_config

    role = config['credentials']['usernames'][username]['role']
    user_id = config['credentials']['usernames'][username]['user_id']
    return role, user_id

# Adjust your signup functions to use the database
def show_signup_donor():
    st.title("Register as a Donor")
    name = st.text_input("Organization Name")
    hp_number = st.text_input("Phone Number")
    address = st.text_input("Address")
    cuisine = st.text_input("Cuisine")
    password = st.text_input("Password", type="password")
    password_confirmation = st.text_input("Confirm Password", type="password")
    username = name.replace(" ", "").lower()

    params_dict = {
        "name": name,
        "username" : username,
        "hp_number": hp_number,
        "address": address,
        "cuisine": cuisine,
        "password": password,
        "description": "",
        "role": "vendor"}
    
    if st.button("Register"):
        if password == password_confirmation:
            register_user(params_dict)
            st.success(f"User '{username}' registered successfully as {params_dict['role']}.")
        else:
            st.error("Passwords do not match")

def show_signup_beneficiaries():
    st.title("Register as a Receiver")
    genre = st.radio("Are you an individual/family or Organization?", ["Individual/Family", "Organization"])

    if genre == "Individual/Family":
        uploaded_file = st.file_uploader("Upload proof of an Organizations' Member")
        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")
        hp_number = st.text_input("Phone Number")
        age = st.number_input("age", step=1, format="%d", min_value=1)
        sex = st.radio("Gender", ["M", "F"])
        name = firstname + lastname
        username = name.replace(" ", "").lower()

        params_dict = {
            "username" : username,
            "first_name": firstname,
            "last_name": lastname,
            "hp_number": hp_number,
            "age": age,
            "sex": sex,
            "credit_value": 100,
            "role": "user"}
        
        password = st.text_input("Password", type="password")
        password_confirmation = st.text_input("Confirm Password", type="password")

        params_dict['password'] = password
        if st.button("Register"):
            if uploaded_file is not None:
                if password == password_confirmation:
                    register_user(params_dict)
                    st.success(f"User '{username}' registered successfully as {params_dict['role']}.")
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please Upload Proof")
    else:
        name = st.text_input("Organization Name")
        hp_number = st.text_input("Phone Number")
        address = st.text_input("Address")
        number_of_ppl = st.number_input("Number of People in Organisation", step=10, format="%d",min_value=1)
        username = name.replace(" ", "").lower()

        params_dict = {
            "username" : username,
            "role": "ngo",
            "name": name,
            "hp_number": hp_number,
            "address": address,
            "number_of_ppl": number_of_ppl,
            "credit_value": 100 * number_of_ppl}
        
        password = st.text_input("Password", type="password")
        password_confirmation = st.text_input("Confirm Password", type="password")

        params_dict['password'] = password
        if st.button("Register"):
            if password == password_confirmation:
                register_user(params_dict)
                st.success(f"User '{username}' registered successfully as {params_dict['role']}.")
            else:
                st.error("Passwords do not match")
