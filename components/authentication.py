import streamlit as st
from config import APP_CONFIG

# User database
# For in-memory authentication, add or modify users here
USERS = {
    "admin": {"password": "admin123", "username": "admin"},
    "user": {"password": "user123", "username": "user"}
}

def is_authenticated():
    return st.session_state.app_state.authenticated

def login_user():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.app_state.authenticated = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout_user():
    st.session_state.app_state.authenticated = False
    st.session_state.username = None
    st.rerun()

def authenticate_user(username, password):
    if APP_CONFIG.AUTH_METHOD == "in_memory":
        return username in USERS and USERS[username]["password"] == password
    elif APP_CONFIG.AUTH_METHOD == "database":
        # Implement database authentication logic
        pass
    elif APP_CONFIG.AUTH_METHOD == "api":
        # Implement API authentication logic
        pass
    return False

def change_password(current_password, new_password):
    username = st.session_state.username
    if authenticate_user(username, current_password):
        USERS[username]["password"] = new_password
        return True
    return False

def change_username(new_username):
    old_username = st.session_state.username
    if new_username not in USERS:
        USERS[new_username] = USERS.pop(old_username)
        USERS[new_username]["username"] = new_username
        st.session_state.username = new_username
        return True
    return False

# Function to add a new user (for admin use)
def add_user(username, password):
    if username not in USERS:
        USERS[username] = {"password": password, "username": username}
        return True
    return False

# Function to remove a user (for admin use)
def remove_user(username):
    if username in USERS:
        del USERS[username]
        return True
    return False