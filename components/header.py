import streamlit as st
from config import APP_CONFIG

def header():
    if APP_CONFIG.SHOW_HEADER:
        st.markdown(
            f"""
            <div class="custom-header">
                <div>
                    <h1>{APP_CONFIG.HEADER_TITLE}</h1>
                    <h2>{APP_CONFIG.HEADER_SUBTITLE}</h2>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )