import logging
import streamlit as st

def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            st.error("An unexpected error occurred. Please try again later.")
    return wrapper