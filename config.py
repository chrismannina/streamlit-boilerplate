import os
from dataclasses import dataclass, field


@dataclass
class AppConfig:
    APP_NAME: str = "Streamlit Starter Template"
    PAGE_ICON: str = ":rocket:"
    LAYOUT: str = "wide"
    THEME_COLOR: str = "#3366cc"
    FONT_FAMILY: str = "sans serif"
    USE_AUTHENTICATION: bool = False
    AUTH_METHOD: str = "in_memory"
    SHOW_NAVBAR: bool = False
    SHOW_SIDEBAR: bool = True
    PAGES: dict = field(
        default_factory=lambda: {
            "Home": {"icon": "house", "page_number": ""},
            "Search": {"icon": "mag", "page_number": "1"},
            "Settings": {"icon": "gear", "page_number": "2"},
        }
    )
    CSS_FILE: str = "static/css/main.css"
    JS_FILE: str = "static/js/main.js"
    ENVIRONMENT: str = field(
        default_factory=lambda: os.getenv("APP_ENVIRONMENT", "development")
    )

    @classmethod
    def load_config(cls):
        config = cls()
        if config.ENVIRONMENT == "production":
            # Load production-specific settings
            config.USE_AUTHENTICATION = True
            # Add other production-specific settings
        elif config.ENVIRONMENT == "staging":
            # Load staging-specific settings
            pass
        return config


APP_CONFIG = AppConfig.load_config()
