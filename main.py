import streamlit as st
import app

def main():
    st.title("Hello World!")
    st.write("This is a simple Streamlit app.")
    auth = True

    if auth:
        app.run()

if __name__ == "__main__":
    main()