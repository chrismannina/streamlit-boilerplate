import streamlit as st
from config import APP_CONFIG
from utils.helpers import CSSLoader, JSLoader
from components.navigation import render_navigation
from components.search_components import Sidebar, ResultList, SourceDetail
from utils.search_functions import DummySearch, add_to_past_searches
from state import State
from utils.error_handling import handle_error


@handle_error
def search_page():
    st.set_page_config(
        page_title=APP_CONFIG.APP_NAME,
        page_icon=APP_CONFIG.PAGE_ICON,
        layout=APP_CONFIG.LAYOUT,
    )
    state = State.initialize(st)

    if APP_CONFIG.USE_AUTHENTICATION and not state.authenticated:
        st.warning("Please log in to access this page.")
        st.stop()

    CSSLoader.load()
    JSLoader.load()

    render_navigation()
    Sidebar().render()

    st.title("Clinical Search")

    if not state.search_done:
        with st.form(key='search_form'):
            col1, col2 = st.columns([1, 2])
            with col1:
                mrn = st.text_input("Enter Patient MRN", value=state.mrn, key="search-mrn")
            with col2:
                search_options = st.multiselect(
                    "Select search options",
                    ["Notes", "Labs", "Medication Orders", "Diagnoses"],
                    default=state.search_options if state.search_options else ["Notes"],
                    key="search-options"
                )
            query = st.text_input("Enter your search query", value=state.query, key="search-query")
            submitted = st.form_submit_button("Search", use_container_width=True)

            if submitted:
                if mrn and search_options and query:
                    state.search_done = True
                    state.mrn = mrn
                    state.search_options = search_options
                    state.query = query
                    search_strategy = DummySearch()  # Or RealSearch() in production
                    state.results = search_strategy.search(mrn, search_options, query)
                    add_to_past_searches(mrn, search_options, query, state.results)
                    st.rerun()
                else:
                    st.warning("Please fill in all fields (MRN, Search Options, and Query)")

    if state.search_done:
        st.subheader("Search Results")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(
                f"""
                <div class="info-box">
                    <b>MRN:</b> {state.mrn}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
                <div class="info-box">
                    <b>Search Options:</b> {', '.join(state.search_options)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        query_col, reset_col = st.columns([8, 1])
        with query_col:
            st.markdown(
                f"""
                <div class="info-box">
                    <b>Query:</b> {state.query}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with reset_col:
            if st.button("Reset", key="reset_search_button"):
                state.search_done = False
                state.mrn = ""
                state.query = ""
                state.selected_results = set()
                st.rerun()

        col1, col2 = st.columns([1, 3])

        with col1:
            ResultList(state.results).render()

        with col2:
            SourceDetail(state.results).render()
        
    
    


if __name__ == "__main__":
    search_page()
