import streamlit as st
from config import APP_CONFIG
from components.authentication import is_authenticated
from components.navigation import render_navigation
from components.search_components import render_sidebar, render_result_list, render_source_detail
from utils.search_functions import dummy_search, add_to_past_searches

# Initialize session state for past searches
if 'past_searches' not in st.session_state:
    st.session_state.past_searches = []
if 'delete_mode' not in st.session_state:
    st.session_state.delete_mode = False

def search_page():
    if APP_CONFIG.USE_AUTHENTICATION and not is_authenticated():
        st.warning("Please log in to access this page.")
        st.stop()

    # Initialize session state variables
    if 'search_done' not in st.session_state:
        st.session_state.search_done = False
    if 'selected_results' not in st.session_state:
        st.session_state.selected_results = set()
    if 'mrn' not in st.session_state:
        st.session_state.mrn = ""
    if 'search_options' not in st.session_state:
        st.session_state.search_options = []
    if 'query' not in st.session_state:
        st.session_state.query = ""
    if 'results' not in st.session_state:
        st.session_state.results = []
    
    render_navigation()
    render_sidebar()

    st.title("Clinical Search")

    if not st.session_state.search_done:
        col1, col2 = st.columns([1, 2])
        with col1:
            mrn = st.text_input("Enter Patient MRN")
        with col2:
            search_options = st.multiselect(
                "Select search options",
                ["Notes", "Labs", "Medication Orders", "Diagnoses"],
                default=["Notes"]
            )
        query = st.text_input("Enter your search query")

        if st.button("Search") or query:
            if mrn and search_options and query:
                st.session_state.search_done = True
                st.session_state.mrn = mrn
                st.session_state.search_options = search_options
                st.session_state.query = query
                st.session_state.results = dummy_search(mrn, search_options, query)
                add_to_past_searches(mrn, search_options, query, st.session_state.results)
                st.rerun()
            else:
                st.warning("Please fill in all fields (MRN, Search Options, and Query)")

    if st.session_state.search_done:
        

        # Display MRN and Search Options
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <b>MRN:</b> {st.session_state.mrn}
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <b>Search Options:</b> {', '.join(st.session_state.search_options)}
                </div>
                """,
                unsafe_allow_html=True
            )

                # Display MRN and Search Options
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(
            f"""
            <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <b>Query:</b> {st.session_state.query}
            </div>
            """,
            unsafe_allow_html=True
        )
        with col2:
            if st.button("Reset", key="reset_search_button"):
                st.session_state.search_done = False
                st.session_state.selected_results = set()
                st.rerun()
        
        st.subheader("Search Results")

        col1, col2 = st.columns([1, 3])

        with col1:
            render_result_list(st.session_state.results)

        with col2:
            render_source_detail(st.session_state.results)

if __name__ == "__main__":
    search_page()
