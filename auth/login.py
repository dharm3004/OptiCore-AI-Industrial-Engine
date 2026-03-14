import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


def login():

    # config load
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("❌ Username or password incorrect")

    if authentication_status == None:
        st.warning("⚠ Please enter your username and password")

    if authentication_status:

        authenticator.logout("Logout", "sidebar")

        st.sidebar.success(f"Welcome {name}")

        role = config["credentials"]["usernames"][username]["role"]

        return username, role