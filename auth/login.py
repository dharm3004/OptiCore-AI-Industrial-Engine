import streamlit as st
import bcrypt
from database import users_collection


def login():

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = users_collection.find_one({"username": username})

        if user:

            stored_password = user["password"]

            if bcrypt.checkpw(password.encode(), stored_password.encode()):

                role = user["role"]

                st.sidebar.success(f"Welcome {username}")

                return username, role

            else:
                st.error("❌ Invalid password")
                return None

        else:
            st.error("❌ User not found")
            return None