import streamlit as st
from config import APP_CONFIG
from components.authentication import is_authenticated, login_user, logout_user
from components.navigation import render_navigation
from utils.helpers import load_css, load_js

def main():
    st.set_page_config(
        page_title=APP_CONFIG.APP_NAME,
        page_icon=APP_CONFIG.PAGE_ICON,
        layout=APP_CONFIG.LAYOUT
    )

    load_css()
    load_js()

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not is_authenticated():
        login_user()
    else:
        render_navigation()
        
        st.title(f"Welcome to {APP_CONFIG.APP_NAME}")
        st.write(f"Hello, {st.session_state.username}!")
        st.write("This is the main page of your application.")
        st.write("Use the navigation to explore other pages.")
        if APP_CONFIG.SHOW_NAVBAR:
            if st.button("Logout", key="navbar_logout", use_container_width=True):
                logout_user()
                
if __name__ == "__main__":
    main()