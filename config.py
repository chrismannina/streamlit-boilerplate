import os
from dataclasses import dataclass, field


@dataclass
class AppConfig:
    APP_NAME: str = "UM Rx Analytics"
    PAGE_ICON: str = ":medical_symbol:"
    LAYOUT: str = "wide"
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
    CSS_FILE: str = "static/css/modern.css"
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
