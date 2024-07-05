import streamlit as st
from config import APP_CONFIG
import logging


class CSSLoader:
    @staticmethod
    def load(file_path=APP_CONFIG.CSS_FILE):
        try:
            with open(file_path, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            logging.error(f"CSS file not found: {file_path}")


class JSLoader:
    @staticmethod
    def load(file_path=APP_CONFIG.JS_FILE):
        try:
            with open(file_path, "r") as f:
                st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)
        except FileNotFoundError:
            logging.error(f"JS file not found: {file_path}")
