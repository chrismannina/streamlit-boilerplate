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
        .search-result {
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .search-result h3 {
            margin-top: 0;
        }
        .search-result .score {
            font-size: 0.8em;
            color: #666;
        }
        .stExpander {
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .stExpander > div:first-child {
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)

def load_js():
    # Add any JavaScript you want to load here
    pass