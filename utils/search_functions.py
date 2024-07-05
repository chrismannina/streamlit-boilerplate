import streamlit as st
import random
from typing import List, Dict
from datetime import datetime
from abc import ABC, abstractmethod


class SearchStrategy(ABC):
    @abstractmethod
    def search(self, mrn: str, search_options: List[str], query: str) -> List[Dict]:
        pass


class DummySearch(SearchStrategy):
    def search(self, mrn: str, search_options: List[str], query: str) -> List[Dict]:
        results = []
        for _ in range(10):
            score = random.uniform(0.5, 1.0)
            source_type = random.choice(search_options)
            result = {
                "score": score,
                "snippet": f"This is a snippet of the result for patient MRN {mrn}...",
                "source_type": source_type,
                "source_content": f"Detailed content for {source_type} result. Patient MRN: {mrn}, Query: {query}\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit.",
            }
            results.append(result)

        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

        for i, result in enumerate(sorted_results):
            result["id"] = i
            result["title"] = f"Result {i + 1} ({result['source_type']})"

        return sorted_results


class RealSearch(SearchStrategy):
    def search(self, mrn: str, search_options: List[str], query: str) -> List[Dict]:
        # Implement real search logic here
        pass


def add_to_past_searches(
    mrn: str, search_options: List[str], query: str, results: List[Dict]
):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    search_data = {
        "timestamp": timestamp,
        "mrn": mrn,
        "search_options": search_options,
        "query": query,
        "results": results,
    }
    st.session_state.app_state.past_searches.insert(0, search_data)
    st.session_state.app_state.past_searches = st.session_state.app_state.past_searches[
        :10
    ]  # Keep only the 10 most recent searches


def delete_selected_searches(selected_indices):
    for index in sorted(selected_indices, reverse=True):
        del st.session_state.app_state.past_searches[index]
    if (
        st.session_state.app_state.search_done
        and not st.session_state.app_state.past_searches
    ):
        # If the current search is deleted and no past searches are available, reset search state
        st.session_state.app_state.search_done = False
        st.session_state.app_state.mrn = ""
        st.session_state.app_state.search_options = []
        st.session_state.app_state.query = ""
        st.session_state.app_state.results = []
        st.session_state.app_state.selected_results = set()
        st.rerun()
