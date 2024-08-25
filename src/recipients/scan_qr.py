import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

def scan_qr():
    st.header("Scan QR Code to Confirm Pick Up")
    st.session_state.page = 'Scan QR'

    # QR code scanning input
    qr_code = qrcode_scanner(key='qrcode_scanner')

    if qr_code:
        # Create a button-like hyperlink using HTML and Markdown with custom CSS styling
        button_style = """
        <style>
        .button {
            display: inline-block;
            padding: 0.75em 1.5em;
            font-size: 16px;
            font-weight: bold;
            color: #000000;  /* Text color black */
            background-color: #FFFFFF;  /* Green button */
            border: none;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            text-decoration: none;  /* No underline */
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #FFFFFF;  /* Darker green on hover */
        }
        </style>
        """

        st.markdown(button_style, unsafe_allow_html=True)  # Inject custom CSS styling

        # Render the styled button as a hyperlink
        st.markdown(
            f'<a href="{qr_code}" target="_self" class="button">Click to confirm food collection!</a>',
            unsafe_allow_html=True
        )

    # Back button to navigate to the previous page
    if st.button("Back"):
        st.session_state.page = 'PreviousPage'  # Set this to the actual page state you want to go back to
        st.rerun()  # Refresh the page to navigate
