import app
import streamlit as st

st.set_page_config(page_title="The Giving Cook", page_icon="🍲")

def main():
    auth = True

    if auth:
        app.run()


if __name__ == "__main__":
    main()
