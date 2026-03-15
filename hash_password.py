import streamlit_authenticator as stauth

password = "admin123"

hashed_password = stauth.Hasher().hash(password)

print(hashed_password)