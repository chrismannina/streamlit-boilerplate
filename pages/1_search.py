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

        col1, col2 = st.columns([1, 2])
        with col1:
            mrn = st.text_input("Enter Patient MRN", value=state.mrn)
        with col2:
            search_options = st.multiselect(
                "Select search options",
                ["Notes", "Labs", "Medication Orders", "Diagnoses"],
                default=state.search_options if state.search_options else ["Notes"],
            )

        query = st.text_input("Enter your search query", value=state.query)

        if st.button("Search") or query:
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
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <b>MRN:</b> {state.mrn}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <b>Search Options:</b> {', '.join(state.search_options)}
                </div>
                """,
                unsafe_allow_html=True,
            )

        query_col, reset_col = st.columns([8, 1])
        with query_col:
            st.markdown(
                f"""
                <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
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
