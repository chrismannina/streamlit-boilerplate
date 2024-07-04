import streamlit as st
import random
from typing import List, Dict
from datetime import datetime

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

def add_to_past_searches(mrn: str, search_options: List[str], query: str, results: List[Dict]):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_data = {
        "timestamp": timestamp,
        "mrn": mrn,
        "search_options": search_options,
        "query": query,
        "results": results
    }
    st.session_state.past_searches.insert(0, search_data) 
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