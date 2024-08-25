import os
import qrcode
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

def generate_qr_code(link):
    host = os.getenv("HOST", "http://localhost:8501/")
    full_link = f"{host}/{link}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(full_link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im