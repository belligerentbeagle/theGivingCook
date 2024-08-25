import streamlit as st
import pandas as pd
from src.db_utils.db_donors import DatabaseConnector

def view_donations_page():
    # TODO: Check user is logged in and have vendor role
    st.session_state.post_food_form_submitted = False
    db_connector = DatabaseConnector()

    st.write("Here is a list of the food items you have donated so far.")

    try:
        # TODO: retrieve vendor_id
        donations = db_connector.get_vendor_donations(4)
        if donations:
            donations_df = pd.DataFrame(donations, columns=[
                "id", "Food Name", "Food Type", "Description", "Is Halal", 
                "Is Vegetarian", "Expiry Date", "Date of Entry", 
                "Total Quantity", "Qty Left After Booking", "Qty Left After Scanning", "QR Code"
            ])
            donations_df["Is Halal"] = donations_df["Is Halal"].apply(lambda x: "True" if x == 1 else "False")
            donations_df["Is Vegetarian"] = donations_df["Is Vegetarian"].apply(lambda x: "True" if x == 1 else "False")
            donations_df.index = donations_df.index + 1

            table_html = "<table border=\"1\" class=\"dataframe\">"

            table_html += "<thead><tr>"
            for col in donations_df.columns.drop("QR Code"):
                table_html += f"<th>{col}</th>"
            table_html += "<th>Edit</th>"
            table_html += "</tr></thead>"

            table_html += "<tbody>"
            for _, row in donations_df.iterrows():
                table_html += "<tr>"
                for col in donations_df.columns.drop("QR Code"):
                    table_html += f"<td>{row[col]}</td>"
                edit_link = f"<td><a href=\"?inventory_id={row['id']}\" target=\"_self\">Edit</a></td>"
                table_html += edit_link
                table_html += "</tr>"
            table_html += "</tbody>"

            table_html += "</table>"

            st.markdown(table_html, unsafe_allow_html=True)

        else:
            st.write("No donations found or failed to retrieve donations.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
