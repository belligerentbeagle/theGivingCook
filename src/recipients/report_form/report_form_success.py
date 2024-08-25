import streamlit as st

def show_success_page(order, description):
    st.success("Food posted successfully!")
    st.header("Thank you for posting your food donation.")

    st.write(f"**Order**: {order[1]}: {order[2]}")
    st.write(f"**Description**: {description}")

    if st.button("Go Back to Home"):
        st.session_state.page = 'Home'
        st.session_state.form_submitted = False