import streamlit_authenticator as stauth

passwords = "admin123"

hashed_passwords = stauth.Hasher().hash(passwords)

print(hashed_passwords)