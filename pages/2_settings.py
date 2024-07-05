import streamlit as st
from config import APP_CONFIG
from utils.helpers import CSSLoader, JSLoader
from components.authentication import change_password, change_username
from components.navigation import render_navigation
from state import State
from utils.error_handling import handle_error


@handle_error
def settings_page():
    state = State.initialize(st)

    if APP_CONFIG.USE_AUTHENTICATION and not state.authenticated:
        st.warning("Please log in to access this page.")
        st.stop()

    CSSLoader.load()
    JSLoader.load()
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
                st.error(
                    "Failed to change password. Please check your current password."
                )

        st.subheader("Change Username")
        new_username = st.text_input("New Username")
        if st.button("Change Username"):
            if change_username(new_username):
                st.success("Username changed successfully!")
                st.experimental_rerun()
            else:
                st.error(
                    "Failed to change username. This username might already be taken."
                )


if __name__ == "__main__":
    settings_page()
