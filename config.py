from dataclasses import dataclass, field

@dataclass
class AppConfig:
    APP_NAME: str = "Streamlit Starter Template"
    PAGE_ICON: str = ":rocket:"
    LAYOUT: str = "wide"
    THEME_COLOR: str = "#3366cc"
    FONT_FAMILY: str = "sans serif"
    USE_AUTHENTICATION: bool = False
    AUTH_METHOD: str = "in_memory"  # Options: "in_memory", "database", "api"
    SHOW_NAVBAR: bool = False
    SHOW_SIDEBAR: bool = True
    PAGES: dict = field(default_factory=lambda: {
        "Home": {"icon": "house", "page_number": ""},
        "Dashboard": {"icon": "bar_chart", "page_number": "1"},
        "Settings": {"icon": "gear", "page_number": "2"},
    })

APP_CONFIG = AppConfig()