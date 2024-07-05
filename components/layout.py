import streamlit as st
from config import APP_CONFIG

def page_container(content_func):
    st.markdown(
        f"""
        <div class="custom-header">
            <h1>{APP_CONFIG.HEADER_TITLE}</h1>
            <h2>{APP_CONFIG.HEADER_SUBTITLE}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    content_func()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="custom-footer">
            {APP_CONFIG.FOOTER_TEXT}
        </div>
        """,
        unsafe_allow_html=True
    )