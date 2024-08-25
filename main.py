import app
import streamlit as st
from src.auth.auth import show_login_page, show_signup_donor, show_signup_beneficiaries, get_user_role_and_id
from src.donate.donate import show_donate_page

st.set_page_config(page_title="The Giving Cook", page_icon="🍲")

def show_home_page():
    pass
    

    
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

            # Rainbow divider
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
            st.image("src/data/assets/background.png")

            st.markdown("<h1 class='animated-heading' style='text-align: center; font-weight: bold;'> Your superapp for fighting food waste</h1>", unsafe_allow_html=True)


           

   
        if 'page' not in st.session_state:
            st.session_state.page = 'Home'
        
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
