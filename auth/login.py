import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


def login():

    with open("auth/config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    # login widget
    authenticator.login(location="main")

    authentication_status = st.session_state["authentication_status"]
    username = st.session_state["username"]
    name = st.session_state["name"]

    if authentication_status is False:
        st.error("❌ Username or password incorrect")
        return None

    if authentication_status is None:
        st.warning("⚠ Please enter your username and password")
        return None

    if authentication_status:

        authenticator.logout("Logout", location="sidebar")

        st.sidebar.success(f"Welcome {name}")

        role = config["credentials"]["usernames"][username]["role"]

        return username, role