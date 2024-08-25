import streamlit as st
from src.donor.donor_home import run_home_page
from src.donor.post_food.post_food_main import post_food
from src.donor.view_donations.donor_donations import view_donations_page


def init_donor_page():
    if st.session_state.page == 'Log In':
        st.session_state.page = 'Home'
    name = st.session_state['name']
    st.sidebar.image("src/data/assets/logo.png")
    st.sidebar.title(f"Welcome Back, {name}!")

    if st.sidebar.button("Home", use_container_width=True):
        st.session_state.page = 'Home'
    if st.sidebar.button("Post Food", use_container_width=True):
        st.session_state.page = 'Post Food'
    if st.sidebar.button("View Donations", use_container_width=True):
        st.session_state.page = 'View Donations'
    if st.session_state.page == 'Home':
        run_home_page()
    elif st.session_state.page == 'Post Food':
        post_food()
    elif st.session_state.page == "View Donations":
        view_donations_page()
