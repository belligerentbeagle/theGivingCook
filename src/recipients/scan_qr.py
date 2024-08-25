import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner


def scan_qr():
    st.header("Scan QR Code to Confirm Pick Up")
    qr_code = qrcode_scanner(key='qrcode_s canner')

    if qr_code:
        st.write(qr_code)

    st.button("Back")
