import streamlit as st
from database import users_collection
import bcrypt


def register():

    st.subheader("📝 Register New User")

    new_username = st.text_input("Username")
    new_name = st.text_input("Full Name")
    new_email = st.text_input("Email")
    new_password = st.text_input("Password", type="password")

    role = st.selectbox("Role", ["viewer", "analyst"])

    if st.button("Register"):

        existing_user = users_collection.find_one({"username": new_username})

        if existing_user:
            st.error("❌ Username already exists")
            return

        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        users_collection.insert_one({
            "username": new_username,
            "name": new_name,
            "email": new_email,
            "password": hashed_password,
            "role": role
        })

        st.success("✅ User Registered Successfully")