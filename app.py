import streamlit as st

from src.donor.qr_code_scan_handler import handle_qr_scan
from src.donor.donor_utils import generate_qr_code
from src.donor.donor_entry import init_donor_page
from src.donor.home import run_home_page
from src.recipients.recipients_entry import init_recipient_page


# Global Vars


def run():
    query_params = st.query_params
    if query_params:
        scan = query_params.get("scan", "False").lower() == "true"
        # either individual or ngo
        collection_type = query_params.get("collection_type", None)
        inventory_id = query_params.get("inventory_id", None)
        if scan and inventory_id and collection_type:
            handle_qr_scan(collection_type, inventory_id)
    else:
        if st.session_state.role == 'donor':
            init_donor_page()
        elif st.session_state.role == 'receiver':
            init_recipient_page()
