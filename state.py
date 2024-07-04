from dataclasses import dataclass, field
from typing import List, Dict, Set

@dataclass
class State:
    authenticated: bool = False
    search_done: bool = False
    selected_results: Set[int] = field(default_factory=set)
    mrn: str = ""
    search_options: List[str] = field(default_factory=list)
    query: str = ""
    results: List[Dict] = field(default_factory=list)
    past_searches: List[Dict] = field(default_factory=list)
    delete_mode: bool = False

    @classmethod
    def initialize(cls, st):
        if 'app_state' not in st.session_state:
            st.session_state.app_state = cls()
        return st.session_state.app_state
