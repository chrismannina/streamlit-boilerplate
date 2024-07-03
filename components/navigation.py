import streamlit as st
from config import APP_CONFIG
from components.authentication import logout_user
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.source_util import get_pages

def render_navigation():
    if APP_CONFIG.SHOW_NAVBAR:
        render_nav_items(is_sidebar=False)
    if APP_CONFIG.SHOW_SIDEBAR:
        with st.sidebar:
            st.title("Navigation")
            render_nav_items(is_sidebar=True)

def render_nav_items(is_sidebar=False):
    cols = st.columns(len(APP_CONFIG.PAGES) + 1) if not is_sidebar else [st.sidebar]
    
    for idx, (page_name, settings) in enumerate(APP_CONFIG.PAGES.items()):
        icon = settings.get("icon")
        page_number = settings.get("page_number")
        page_path = f"pages/{page_number}_{page_name.lower()}" if page_name.lower() != "home" else "main"

        if is_sidebar:
            st.page_link(f"{page_path}.py", label=f":{icon}: {page_name}", use_container_width=True)
        else:
            with cols[idx]:
                st.page_link(f"{page_path}.py", label=f":{icon}: {page_name}", use_container_width=True)
    
    # Logout button for sidebar
    if is_sidebar and APP_CONFIG.USE_AUTHENTICATION:
        if st.button("Logout", key="sidebar_logout", use_container_width=True):
            logout_user()

