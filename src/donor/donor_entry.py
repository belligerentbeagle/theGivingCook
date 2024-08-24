import streamlit as st
from src.donor.home import run_home_page
from src.donor.post_food.post_food_main import post_food


def init_donor_page():
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'

    st.sidebar.title("Welcome Back, Donor_Name!")

    if st.sidebar.button("Home"):
        st.session_state.page = 'Home'
    if st.sidebar.button("Post Food"):
        st.session_state.page = 'Post Food'
    if st.sidebar.button("Past Donations"):
        st.session_state.page = 'Past Donations'

    if st.session_state.page == 'Home':
        run_home_page()
    elif st.session_state.page == 'Post Food':
        post_food()
