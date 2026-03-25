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
            stored_password = user.get("password", "")
            role = user.get("role", "viewer")

            try:
                if bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
                    st.sidebar.success(f"Welcome {username} 👋")
                    return username, role
                else:
                    st.error("❌ Invalid username or password")
                    return None, None
            except Exception:
                st.error("⚠ Password format error in database. Re-register this user.")
                return None, None

        else:
            st.error("❌ Invalid username or password")
            return None, None

    return None, None