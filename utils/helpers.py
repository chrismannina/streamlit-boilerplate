import streamlit as st
from config import APP_CONFIG

def load_css():
    with open(APP_CONFIG.CSS_FILE, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_js():
    with open(APP_CONFIG.JS_FILE, "r") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)