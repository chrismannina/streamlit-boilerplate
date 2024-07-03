import streamlit as st

def load_css():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp {
            background-color: #f0f2f6;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

def load_js():
    # Add any JavaScript you want to load here
    pass