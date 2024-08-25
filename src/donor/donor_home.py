import streamlit as st


def run_home_page():
    # Reset any form submission flags
    st.session_state.post_food_form_submitted = False

    # Page header
    st.header("Thank you for partnering with us! 🧑‍🍳")

    # Introduction and Motivation
    st.write("""
    At The Giving Cook, we believe in the power of community and the impact of sharing. 
    We are thrilled to have you as a partner in our mission to reduce food waste and feed those in need.
    """)
    st.image("src/data/assets/foodbank.png", use_column_width=True, caption="Credits: Photo taken from https://www.facebook.com/thefoodbanksingapore/")
    # Information from The Food Bank Singapore
    st.subheader("Why Donate Food?")
    st.write("""
    Food insecurity is a pressing issue in Singapore, with many families struggling to access sufficient, safe, and nutritious food. 
    Food waste in Singapore amounts to more than 800,000 tonnes annually, 
    while thousands of individuals and families face food insecurity. By donating your surplus food, you can:
    - Help reduce food waste and its environmental impact.
    - Support those in need by providing access to nutritious meals.
    - Enhance your corporate social responsibility and community engagement.
    """)

    # Information about the Good Samaritan Food Donation Bill
    st.subheader("Good Samaritan Food Donation Bill")
    st.write("""
    The recently introduced [Good Samaritan Food Donation Bill](https://www.parliament.gov.sg/docs/default-source/bills-introduced/good-samaritan-food-donation-bill-22-2024.pdf?sfvrsn=83d45608_3) 
    in Singapore provides legal protection for food donors and recipient organizations, encouraging more businesses to donate surplus food. 
    Key highlights of the Bill include:
    - Protection from liability for donors who donate food in good faith, ensuring that the food is safe for consumption.
    - Encouragement of food donation as a sustainable practice to reduce waste and support social causes.
    - Promoting a culture of giving and solidarity within the community.
    """)

    # Call to Action
    st.subheader("Join Us in Making a Difference")
    st.write("""
    Your donations make a direct impact on the lives of those in need. 
    Together, we can make a significant difference by reducing food waste and supporting vulnerable communities.
    **Partner with us today and start making a difference!**
    """)

