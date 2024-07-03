import streamlit as st
from components.authentication import is_authenticated
from components.navigation import render_navigation

if not is_authenticated():
    st.warning("Please log in to access this page.")
    st.stop()

render_navigation()

st.title("Dashboard")
st.write("This is the dashboard page. Add your dashboard content here.")