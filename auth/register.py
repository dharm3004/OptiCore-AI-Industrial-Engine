import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


def register():

    st.subheader("📝 Register New User")

    # Load config
    with open("auth/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    new_username = st.text_input("Username")
    new_name = st.text_input("Full Name")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["viewer", "analyst"])

    if st.button("Register"):

        # check if user exists
        if new_username in config["credentials"]["usernames"]:
            st.error("❌ Username already exists")
            return

        # hash password
        hashed_password = stauth.Hasher().hash(new_password)

        # add user
        config["credentials"]["usernames"][new_username] = {
            "name": new_name,
            "email": new_email,
            "password": hashed_password,
            "role": role
        }

        # save config
        with open("auth/config.yaml", "w") as file:
            yaml.dump(config, file)

        st.success("✅ User Registered Successfully")