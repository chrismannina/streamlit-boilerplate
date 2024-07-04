import streamlit as st
from components.authentication import is_authenticated
from components.navigation import render_navigation
from config import APP_CONFIG
from typing import List, Dict
import random

def dummy_search(mrn: str, search_options: List[str], query: str) -> List[Dict]:
    # This is a dummy function to simulate search results
    results = []
    for i in range(10):
        score = random.uniform(0.5, 1.0)
        source_type = random.choice(search_options)
        result = {
            "id": i,
            "score": score,
            "title": f"Result {i+1} for {query} in {source_type}",
            "snippet": f"This is a snippet of the result {i+1} for patient MRN {mrn}...",
            "source_type": source_type,
            "source_content": f"Detailed content for {source_type} result {i+1}. Patient MRN: {mrn}, Query: {query}\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        }
        results.append(result)
    return sorted(results, key=lambda x: x["score"], reverse=True)

def render_result_cards(results: List[Dict], cols: int = 3):
    # Calculate the number of rows needed
    rows = (len(results) + cols - 1) // cols
    for row in range(rows):
        cols_layout = st.columns(cols)
        for col in range(cols):
            idx = row * cols + col
            if idx < len(results):
                result = results[idx]
                if f"expanded_{result['id']}" not in st.session_state:
                    st.session_state[f"expanded_{result['id']}"] = False

                with cols_layout[col]:
                    expanded = st.session_state[f"expanded_{result['id']}"]
                    with st.expander(label=f"{result['id'] + 1}. {result['snippet']} ({result['source_type']})", expanded=False):
                        st.write(result['snippet'])
                        if expanded:
                            st.write(f"**Type:** {result['source_type']}")
                            st.write(result['source_content'])
                        st.session_state[f"expanded_{result['id']}"] = not expanded
                    st.write("---")

def search_page():
    if APP_CONFIG.USE_AUTHENTICATION and not is_authenticated():
        st.warning("Please log in to access this page.")
        st.stop()

    render_navigation()

    st.title("Clinical Search")

    if 'search_done' not in st.session_state:
        st.session_state.search_done = False

    if not st.session_state.search_done:
        col1, col2 = st.columns(2)
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
            else:
                st.warning("Please fill in all fields (MRN, Search Options, and Query)")

    if st.session_state.search_done:
        st.subheader("Search Summary")
        st.write(f"**Patient MRN:** {st.session_state.mrn}")
        st.write(f"**Search Options:** {', '.join(st.session_state.search_options)}")
        st.write(f"**Query:** {st.session_state.query}")

        st.subheader("Search Results")
        render_result_cards(st.session_state.results, cols=3)

if __name__ == "__main__":
    search_page()
