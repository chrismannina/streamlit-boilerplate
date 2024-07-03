import streamlit as st
from components.authentication import is_authenticated
from components.navigation import render_navigation
from config import APP_CONFIG
from typing import List, Dict
import random
import json
from datetime import datetime

# Initialize session state for past searches
if 'past_searches' not in st.session_state:
    st.session_state.past_searches = []
if 'delete_mode' not in st.session_state:
    st.session_state.delete_mode = False

def add_to_past_searches(mrn: str, search_options: List[str], query: str, results: List[Dict]):
    timestamp = datetime.now().strftime("%#m/%#d/%y %H:%M")
    search_data = {
        "timestamp": timestamp,
        "mrn": mrn,
        "search_options": search_options,
        "query": query,
        "results": results
    }
    st.session_state.past_searches.insert(0, search_data)  # Add new search to the beginning
    st.session_state.past_searches = st.session_state.past_searches[:10]  # Keep only the 10 most recent searches

def delete_selected_searches(selected_indices):
    for index in sorted(selected_indices, reverse=True):
        del st.session_state.past_searches[index]
    if st.session_state.search_done and not st.session_state.past_searches:
        # If the current search is deleted and no past searches are available, reset search state
        st.session_state.search_done = False
        st.session_state.mrn = ""
        st.session_state.search_options = []
        st.session_state.query = ""
        st.session_state.results = []
        st.session_state.selected_results = set()
        st.rerun()

def render_sidebar():
    st.sidebar.title("Search History")
    
    if not st.session_state.past_searches:
        st.sidebar.write("No past searches.")
        return

    for i, search in enumerate(st.session_state.past_searches):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            if st.button(f"{search['query'][:20]} [{search['timestamp']}]", key=f"past_search_{i}"):
                # Load this past search
                st.session_state.search_done = True
                st.session_state.mrn = search['mrn']
                st.session_state.search_options = search['search_options']
                st.session_state.query = search['query']
                st.session_state.results = search['results']
                st.session_state.selected_results = set()  # Reset selected results
                st.experimental_rerun()
        with col2:
            if st.button("🗑️", key=f"delete_search_{i}"):
                del st.session_state.past_searches[i]
                if not st.session_state.past_searches or i == 0:
                    # If deleting the current search, reset the search state
                    st.session_state.search_done = False
                    st.session_state.mrn = ""
                    st.session_state.search_options = []
                    st.session_state.query = ""
                    st.session_state.results = []
                    st.session_state.selected_results = set()
                st.rerun()

    if st.sidebar.button("Clear All History"):
        st.session_state.past_searches = []
        # Reset search state
        st.session_state.search_done = False
        st.session_state.mrn = ""
        st.session_state.search_options = []
        st.session_state.query = ""
        st.session_state.results = []
        st.session_state.selected_results = set()
        st.rerun()
        
def dummy_search(mrn: str, search_options: List[str], query: str) -> List[Dict]:
    # This is a dummy function to simulate search results
    results = []
    for _ in range(10):
        score = random.uniform(0.5, 1.0)
        source_type = random.choice(search_options)
        result = {
            "score": score,
            "snippet": f"This is a snippet of the result for patient MRN {mrn}...",
            "source_type": source_type,
            "source_content": f"Detailed content for {source_type} result. Patient MRN: {mrn}, Query: {query}\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        }
        results.append(result)
    
    # Sort results by score in descending order
    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)
    
    # Assign IDs based on sorted order
    for i, result in enumerate(sorted_results):
        result["id"] = i
        source_type = str(result["source_type"])
        result["title"] = f"Result {i + 1} ({source_type})"
    
    return sorted_results

def render_result_list(results: List[Dict]):
    for result in results:
        is_selected = result['id'] in st.session_state.selected_results
        
        result_number = str(result['id'] + 1)
        result_title = str(result['title'])
        result_button = result_number + ". " + result_title
        
        # Create a button that looks like text
        if st.button(result_button, key=f"result_{result['id']}", use_container_width=True, type="primary"):
            if is_selected:
                st.session_state.selected_results.remove(result['id'])
            else:
                st.session_state.selected_results.add(result['id'])
            st.rerun()

    # Apply custom CSS to style the buttons
    st.markdown("""
    <style>
    .stButton > button[kind="primary"] {
        display: block !important;
        width: 100% !important;
        padding: 8px 12px !important;
        text-align: left !important;
        background-color: transparent !important;
        border: none !important;
        font-size: 16px !important;
        color: inherit !important;
        cursor: pointer !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #f0f0f0 !important;
    }
    .stButton > button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    .stButton > button[kind="primary"] > div {
        text-align: left !important;
        justify-content: flex-start !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
def render_source_detail(results: List[Dict]):
    if 'selected_results' in st.session_state and st.session_state.selected_results:
        for result_id in st.session_state.selected_results:
            result = next((r for r in results if r['id'] == result_id), None)
            if result:
                st.markdown(
                    f"""
                    <div style='padding: 15px; border: 2px solid #ddd; background-color: #f9f9f9; margin-top: 10px;'>
                    <h4>Result {result['id'] + 1}</h4>
                    <p><b>Type:</b> {result['source_type']}</p>
                    <p>{result['source_content']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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
        if st.button("New Search"):
            st.session_state.search_done = False
            st.session_state.selected_results = set()
            st.rerun()

        st.subheader("Search Results")

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

        # Display Query on its own row
        st.markdown(
            f"""
            <div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                <b>Query:</b> {st.session_state.query}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([1, 3])

        with col1:
            render_result_list(st.session_state.results)

        with col2:
            render_source_detail(st.session_state.results)

if __name__ == "__main__":
    search_page()
