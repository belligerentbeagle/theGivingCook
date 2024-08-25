import streamlit as st


def run_home_page():
    st.session_state.post_food_form_submitted = False
    st.header("Welcome, donor! 🧑‍🍳")

