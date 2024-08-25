'''
donor either request for individuals or beneficiaries to come down
QR code generated will be displayed on restaurant's end
'''

import os

import qrcode
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def generate_qr_code(link):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill='black', back_color='white')

    return img
