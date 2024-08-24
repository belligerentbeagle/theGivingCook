'''
donor either request for individuals or beneficiaries to come down
QR code generated will be displayed on restaurant's end
'''

import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

print(os.getenv("HOST"))

def generate_qr_page():
    host = os.getenv("HOST")
    st.title("Generate QR Code")
    st.write("This is where the QR code generation will happen.")
    # Add more logic related to QR code generation here
