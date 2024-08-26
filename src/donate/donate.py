import streamlit as st

def show_donate_page():
    st.title("Donate to Our Cause")
    st.image("src/data/assets/KidsEat.jpg", caption="One more meal, one more Smile!")

    # Name input field
    name = st.text_input("Full Name", placeholder="Required")

    # Email input field
    email = st.text_input("Email Address", placeholder="Required")

    # Amount input field
    st.write("Select Donation Amount")
    amounts = [5, 10, 20, 50, 100, 200, 500, 1000, "Others"]
    amount = st.radio("Donation Amount", amounts, horizontal=True)
    if amount == "Others":
        st.number_input("Enter Other Amount: ($)", step=10.00, min_value=1.00, format="%0.2f")
    # Payment type selection
    payment_type = st.selectbox("Payment Type", ["Credit/Debit Card", "PayNow", "PayPal", "Bank Transfer"])

    # Donation button
    if st.button("Donate", key="123"):
        if name and email and amount > 0:
            st.success(f"Thank you, {name}, for your donation of SGD {amount:.2f} via {payment_type}!")
        else:
            st.error("Please fill in all fields before submitting.")
