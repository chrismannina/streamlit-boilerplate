import streamlit as st
from config import APP_CONFIG
from components.authentication import is_authenticated, login_user, logout_user
from components.navigation import render_navigation
from utils.helpers import CSSLoader, JSLoader
from state import State

def main():
    st.set_page_config(
        page_title=APP_CONFIG.APP_NAME,
        page_icon=APP_CONFIG.PAGE_ICON,
        layout=APP_CONFIG.LAYOUT
    )

    CSSLoader.load(APP_CONFIG.CSS_FILE)
    JSLoader.load(APP_CONFIG.JS_FILE)

    state = State.initialize(st)

    if not state.authenticated:
        if APP_CONFIG.USE_AUTHENTICATION:
            login_user()
        else:
            state.authenticated = True

    if state.authenticated:
        render_navigation()
        
        st.title(f"Welcome to {APP_CONFIG.APP_NAME}")
        if APP_CONFIG.USE_AUTHENTICATION:
            st.write(f"Hello, {st.session_state.username}!")
        else: 
            st.write("Hello!")
        st.write("This is the main page of your application.")
        st.write("Use the navigation to explore other pages.")
        if APP_CONFIG.USE_AUTHENTICATION and APP_CONFIG.SHOW_NAVBAR:
            if st.button("Logout", key="navbar_logout", use_container_width=True):
                logout_user()
                
if __name__ == "__main__":
    main()