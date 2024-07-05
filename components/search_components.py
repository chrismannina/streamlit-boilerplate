import streamlit as st
from typing import List, Dict
from components.base import BaseComponent


class Sidebar(BaseComponent):
    def render(self):
        st.sidebar.title("Search History")

        if not st.session_state.app_state.past_searches:
            st.sidebar.write("No past searches.")
            return

        for i, search in enumerate(st.session_state.app_state.past_searches):
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                if st.button(
                    f"{search['query'][:20]} [{search['mrn']}]", key=f"past_search_{i}"
                ):
                    # Load this past search
                    st.session_state.app_state.search_done = True
                    st.session_state.app_state.mrn = search["mrn"]
                    st.session_state.app_state.search_options = search["search_options"]
                    st.session_state.app_state.query = search["query"]
                    st.session_state.app_state.results = search["results"]
                    st.session_state.app_state.selected_results = (
                        set()
                    )  # Reset selected results
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_search_{i}"):
                    del st.session_state.app_state.past_searches[i]
                    if not st.session_state.app_state.past_searches or i == 0:
                        # If deleting the current search, reset the search state
                        st.session_state.app_state.search_done = False
                        st.session_state.app_state.mrn = ""
                        st.session_state.app_state.search_options = []
                        st.session_state.app_state.query = ""
                        st.session_state.app_state.results = []
                        st.session_state.app_state.selected_results = set()
                    st.rerun()

        if st.sidebar.button("Clear History"):
            st.session_state.app_state.past_searches = []
            # Reset search state
            st.session_state.app_state.search_done = False
            st.session_state.app_state.mrn = ""
            st.session_state.app_state.search_options = []
            st.session_state.app_state.query = ""
            st.session_state.app_state.results = []
            st.session_state.app_state.selected_results = set()
            st.rerun()


class ResultList(BaseComponent):
    def __init__(self, results: List[Dict]):
        self.results = results

    def render(self):
        for result in self.results:
            is_selected = result["id"] in st.session_state.app_state.selected_results

            result_number = str(result["id"] + 1)
            result_title = str(result["title"])
            result_button = result_number + ". " + result_title

            if st.button(
                result_button,
                key=f"result_{result['id']}",
                use_container_width=True,
                type="primary",
            ):
                if is_selected:
                    st.session_state.app_state.selected_results.remove(result["id"])
                else:
                    st.session_state.app_state.selected_results.add(result["id"])
                st.rerun()


class SourceDetail(BaseComponent):
    def __init__(self, results: List[Dict]):
        self.results = results

    def render(self):
        if st.session_state.app_state.selected_results:
            for result_id in st.session_state.app_state.selected_results:
                result = next((r for r in self.results if r["id"] == result_id), None)
                if result:
                    st.markdown(
                        f"""
                        <div style='padding: 15px; border: 2px solid #ddd; background-color: #f9f9f9; margin-top: 10px;'>
                        <h4>Result {result['id'] + 1}</h4>
                        <p><b>Type:</b> {result['source_type']}</p>
                        <p>{result['source_content']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
