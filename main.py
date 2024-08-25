import app
import streamlit as st
from src.auth.auth import show_login_page, show_signup_donor, show_signup_beneficiaries, get_user_role_and_id
from itertools import cycle
from streamlit_carousel import carousel
from src.donate.donate import show_donate_page

st.set_page_config(page_title="The Giving Cook", page_icon="🍲")

def show_home_page():
    test_items = [
        dict(
            title="",
            text="",
            img="https://i.postimg.cc/SRWrYwbk/background.png",
            link="https://foodbank.sg/",
        ),
        dict(
            title="",
            text="",
            img="https://foodbank.sg/wp-content/uploads/2022/09/IMG_3204.png",
            link="https://foodbank.sg/juniors-club-2022/",
        ),
        dict(
            title="",
            text="",
            img="https://foodbank.sg/wp-content/uploads/2022/03/DSC03237.jpg",
            link="https://foodbank.sg/bank-card-programme/",
        ),
        dict(
            title="",
            text="",
            img="https://res.cloudinary.com/dmajhtvmd/image/upload/w_800,c_scale/avwejrllnrak0eimpu4r.jpg",
            link="https://foodbank.sg/donate/",
        ),
        dict(
            title="",
            text="",
            img="https://i.postimg.cc/KzcFWyQs/photo-2024-08-26-00-46-56.jpg",
            link="https://foodbank.sg/time-based/",
        ),
    ]

    carousel(items=test_items)
    
    
def main():
    if st.session_state.get('authentication_status', False):
        role, user_id = get_user_role_and_id(st.session_state.username)
        st.session_state.role = role
        st.session_state.user_id = user_id
        st.session_state.authenticator.logout('Logout', 'sidebar')  # Ensure the logout button is visible
        app.run()
    else:
        with st.container():
            # Adding CSS for the animation and the heading
            st.markdown("""
                <style>
                /* Define the keyframes for the animation */
                @keyframes fadeInUp {
                    0% {
                        opacity: 0;
                        transform: translateY(20px);
                    }
                    100% {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                /* Apply the animation to the h1 element */
                .animated-heading {
                    animation: fadeInUp 3s ease-out;
                }
                </style>
            """, unsafe_allow_html=True)

            # Heading with animation and bold text
            st.markdown("<h1 class='animated-heading' style='text-align: center; font-weight: bold;'>The Giving Cook 👨‍🍳</h1>", unsafe_allow_html=True)

            # Divider
            st.markdown(
            """
            <div style="
                height: 5px; 
                background: linear-gradient(to right, #3f8a46, #66bb6a);
                margin-bottom: 20px;">
            </div>
            """, 
            unsafe_allow_html=True
            )
   
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'
        
        st.sidebar.image("src/data/assets/logo.png")
        if st.sidebar.button("Home"):
            st.session_state.page = 'Home'
        if st.sidebar.button("Log In"):
            st.session_state.page = 'Log In'
        if st.sidebar.button("Create an Account"):
            st.session_state.page = 'Create an Account'
        if st.sidebar.button("Be a Registered Donor"):
            st.session_state.page = 'Register as Donor'
        if st.sidebar.button("Donate"):
            st.session_state.page = 'Donate'

        if st.session_state.page == 'Home':
            show_home_page()
        elif st.session_state.page == 'Log In':
            show_login_page()
        elif st.session_state.page == 'Create an Account':
            show_signup_beneficiaries()
        elif st.session_state.page == 'Register as Donor':
            show_signup_donor()
        elif st.session_state.page == 'Donate':
            show_donate_page()

if __name__ == "__main__":
    main()
