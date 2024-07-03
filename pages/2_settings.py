import streamlit as st
from components.authentication import is_authenticated, change_password, change_username
from components.navigation import render_navigation
from config import APP_CONFIG

if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

render_navigation()

st.title("Settings")
st.write("This is the settings page. Add your settings content here.")


if APP_CONFIG.USE_AUTHENTICATION:
    st.title("User Profile")
    st.write(f"Current username: {st.session_state.username}")
    
    st.subheader("Change Password")
    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    if st.button("Change Password"):
        if change_password(current_password, new_password):
            st.success("Password changed successfully!")
        else:
            st.error("Failed to change password. Please check your current password.")

    st.subheader("Change Username")
    new_username = st.text_input("New Username")
    if st.button("Change Username"):
        if change_username(new_username):
            st.success("Username changed successfully!")
            st.experimental_rerun()
        else:
            st.error("Failed to change username. This username might already be taken.")