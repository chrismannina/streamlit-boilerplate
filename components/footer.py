import streamlit as st
from config import APP_CONFIG

def footer():
    if APP_CONFIG.SHOW_FOOTER:
        st.markdown(
            f"""
            <div class="footer">
                <p>{APP_CONFIG.FOOTER_TEXT}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
