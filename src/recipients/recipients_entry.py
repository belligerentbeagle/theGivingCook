import streamlit as st
from src.recipients import search_food
from src.recipients.report_form.report_form import file_report
from src.ProfileManagement import profile_management

def init_recipient_page():
    # Get user's name from session state and set default page if not set
    name = st.session_state.get('name', 'Guest')
    
    if 'page' not in st.session_state:
        st.session_state.page = 'Search Food'    

    st.sidebar.title(f"Welcome Back, {name}!")

    if st.sidebar.button("Search Food"):
        st.session_state.page = 'Search Food'
    if st.sidebar.button("Manage Profile"):
        st.session_state.page = 'Manage Profile'
    if st.sidebar.button("File Report"):
        st.session_state.page = 'File Report'
    if st.sidebar.button("Scan QR"):
        st.session_state.page = 'Scan QR'

    if st.session_state.page == 'Search Food':
        search_food.view_postings()
    elif st.session_state.page == 'Manage Profile':
        profile_management()
        print("manage profile")
    elif st.session_state.page == 'Past Donations':
        print("past donations")
    elif st.session_state.page == 'File Report':
        file_report()
    elif st.session_state.page == 'Scan QR':
        st.write("Scan QR")