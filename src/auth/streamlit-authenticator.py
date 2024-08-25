import streamlit_authenticator as stauth

# List of plain-text passwords
passwords = ["password"]

# Hash the passwords
hashed_passwords = stauth.Hasher(passwords).generate()

for i, password in enumerate(passwords):
    print(f"Original: {password}, Hashed: {hashed_passwords[i]}")
