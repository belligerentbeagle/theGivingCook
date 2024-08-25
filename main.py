import app
import streamlit as st
from src.auth.auth import show_login_page, show_signup_donor, show_signup_beneficiaries, get_user_role_and_id

st.set_page_config(page_title="The Giving Cook", page_icon="🍲")

def main():
    if st.session_state.get('authentication_status', False):
        role, user_id = get_user_role_and_id(st.session_state.username)
        st.session_state.role = role
        st.session_state.user_id = user_id
        st.session_state.authenticator.logout('Logout', 'sidebar')  # Ensure the logout button is visible
        app.run()
    else:
        if 'page' not in st.session_state:
            st.session_state.page = 'Log In'

        if st.sidebar.button("Log In"):
            st.session_state.page = 'Log In'
        if st.sidebar.button("Create an Account"):
            st.session_state.page = 'Create an Account'
        if st.sidebar.button("Be a Registered Donor"):
            st.session_state.page = 'Register as Donor'

        if st.session_state.page == 'Log In':
            show_login_page()
        elif st.session_state.page == 'Create an Account':
            show_signup_beneficiaries()
        elif st.session_state.page == 'Register as Donor':
            show_signup_donor()


if __name__ == "__main__":
    main()
