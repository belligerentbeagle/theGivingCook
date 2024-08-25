import streamlit as st
from src.donor.home import run_home_page
from src.donor.post_food.post_food_main import post_food
from src.donor.donor_donations import view_donations_page


def init_donor_page():
    if st.session_state.page == 'Log In':
        st.session_state.page = 'Home'
    name = st.session_state['name']
    st.sidebar.title(f"Welcome Back, {name}!")

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home'
    if st.sidebar.button("Post Food"):
        st.session_state.page = 'Post Food'
    if st.sidebar.button("View Donations"):
        st.session_state.page = 'View Donations'
    if st.session_state.page == 'Home':
        run_home_page()
    elif st.session_state.page == 'Post Food':
        post_food()
    elif st.session_state.page == "View Donations":
        view_donations_page()