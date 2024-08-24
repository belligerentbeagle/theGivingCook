import streamlit as st

from src.db_utils.db_donors import DatabaseConnector

def handle_qr_scan(collection_type, inventory_id):
    # TODO: perform some auth that scanner is correct 
    db_connector = DatabaseConnector()
    conn = db_connector.connect()
    if not conn:
        return False
    cur = conn.cursor()
    try:
        status = db_connector.update_inventory_qty(collection_type, inventory_id)
        if status:
            st.success("Scan success")
        else:
            st.error("Scan unsuccessful. Please approach the restaurant with proof of booking")

    except Exception as e:
        return None
    
    finally:
        conn.close()
    
    return True