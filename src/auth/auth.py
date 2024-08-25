import streamlit as st
import streamlit_authenticator as stauth
import yaml

# Load configuration
def load_config():
    with open('src/auth/config.yaml') as file:
        config = yaml.safe_load(file)
    return config

def create_authenticator():
    config = load_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['pre-authorized']  # This ensures that cookies are managed properly
    )
    return authenticator, config

def get_user_role(username):
    config = load_config()
    return config['credentials']['usernames'][username]['role']

def show_login_page():
    if "authenticator" not in st.session_state:
        authenticator, config = create_authenticator()
        st.session_state.authenticator = authenticator
        st.session_state.authenticator_config = config
    else:
        authenticator = st.session_state.authenticator

    name, authentication_status, username = authenticator.login()

    if authentication_status:
        role = get_user_role(username)
        st.session_state.username = username  # Store the username in session
        st.sidebar.success(f"Welcome {name} (Role: {role})")
        st.session_state.authenticator.logout('Logout', 'sidebar')
        # st.session_state.authenticated = True  # Set the session state to authenticated
        st.stop()  # Stop execution to allow the main script to refresh
    elif authentication_status is False:
        st.error('Username or password is incorrect')
        if st.button('No Account yet? Create an Account instead'):
            st.session_state.page = 'Create an Account'
            st.stop()
        # st.page_link("pages/Create_an_Account.py", label="Do not have an Account? Create an Account here")
    else:
        st.warning('Please enter your username and password')
        if st.button('No Account yet? Create an Account instead'):
            st.session_state.page = 'Create an Account'
            st.stop()
    if st.session_state.page == 'Create an Account':
        show_signup_beneficiaries()
        # st.page_link("pages/Create_an_Account.py", label="Do not have an Account? Create an Account here")

def show_signup_donor():
    if "authenticator" not in st.session_state:
        authenticator, config = create_authenticator()
        st.session_state.authenticator = authenticator
        st.session_state.authenticator_config = config
    else:
        authenticator = st.session_state.authenticator

    st.title("Register as a Donor")

    username = st.text_input("Username")
    uen = st.text_input("UEN")
    name = st.text_input("Organization Name")
    password = st.text_input("Password", type="password")
    password_confirmation = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password == password_confirmation:
            # Here, you would typically hash the password and save the new user
            hashed_password = authenticator.hash_password(password)
            config['usernames'][username] = {"name": name, "password": hashed_password, "role": "donor"}

            st.success("User registered successfully")
        else:
            st.error("Passwords do not match")

def show_signup_beneficiaries():
    if "authenticator" not in st.session_state:
        authenticator, config = create_authenticator()
        st.session_state.authenticator = authenticator
        st.session_state.authenticator_config = config
    else:
        authenticator = st.session_state.authenticator

    st.title("Register as a Receiver")

    genre = st.radio(
    "Are you an individual/family or Organization?",
    ["Individual/Family", "Organization"],
    captions=[
        "Register as Individual Member",
        "Register as Organization",
    ],
)
    st.divider()
    if genre == "Individual/Family":
        uploaded_file = st.file_uploader("Upload proof of an Organizations' Member")
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()

        username = st.text_input("Username")
        name = st.text_input("Name")
        password = st.text_input("Password", type="password")
        password_confirmation = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if password == password_confirmation:
                # Here, you would typically hash the password and save the new user
                hashed_password = authenticator.hash_password(password)
                config['usernames'][username] = {"name": name, "password": hashed_password, "role": "receiver"}

                st.success("User registered successfully")
            else:
                st.error("Passwords do not match")
    elif genre == "Organization":
        username = st.text_input("Username")
        uen = st.text_input("UEN")
        name = st.text_input("Organization Name")
        password = st.text_input("Password", type="password")
        password_confirmation = st.text_input("Confirm Password", type="password")

        if st.button("Register"):
            if password == password_confirmation:
                # Here, you would typically hash the password and save the new user
                hashed_password = authenticator.hash_password(password)
                config['usernames'][username] = {"name": name, "password": hashed_password, "role": "receiver"}

                st.success("User registered successfully")
            else:
                st.error("Passwords do not match")

