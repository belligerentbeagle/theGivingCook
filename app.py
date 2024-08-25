#Main logics of the application goes here, calling diff modules depending on the user state
import streamlit as st
import time
import pandas as pd
from src.recipients import recipients_entry

## Global Vars


def run():
    st.title("App is running!")
    recipients_entry.init_recipient_page()

    with st.sidebar:
        st.header("Welcome to The Giving Cook! 🧑‍🍳")
        someProcess = st.button("Click me!")


    
    if someProcess:
        with st.spinner("Running some process..."):
            time.sleep(1)
            st.write("Process completed!")
            st.dataframe(pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]}))

    
