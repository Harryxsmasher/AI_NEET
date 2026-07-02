"""
=========================================================
AI_NEET
Configuration Manager

Author : Praveen Mark
Python : 3.12+

Loads configuration from config.yaml
Provides strongly typed access to configuration values.
=========================================================
"""

from pathlib import Path
from typing import Any

import yaml

from core.constants import CONFIG_FILE


class ConfigManager:
    """
    Singleton configuration manager.

    Example
    -------
    config = ConfigManager()

    database = config.get("database.sqlite")

    model = config.get("embedding.model")
    """

    _instance = None
    _config: dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()

        return cls._instance

    def _load(self) -> None:

        config_path = Path(CONFIG_FILE)

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found:\n{config_path}"
            )

        with open(config_path, "r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file)

    def reload(self) -> None:
        """Reload configuration from disk."""
        self._load()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Read nested configuration.

        Example
        -------
        config.get("database.sqlite")

        config.get("embedding.model")
        """

        keys = key.split(".")

        value = self._config

        for item in keys:

            if isinstance(value, dict) and item in value:
                value = value[item]
            else:
                return default

        return value

    @property
    def data(self) -> dict[str, Any]:
        """Return complete configuration dictionary."""
        return self._config

    def print_summary(self) -> None:

        print()

        print("=" * 60)
        print("AI_NEET Configuration")
        print("=" * 60)

        print(f"Application : {self.get('application.name')}")
        print(f"Version     : {self.get('application.version')}")
        print(f"Author      : {self.get('application.author')}")

        print("-" * 60)

        print(f"Database    : {self.get('database.sqlite')}")
        print(f"Vector DB   : {self.get('vector_db.folder')}")
        print(f"Embedding   : {self.get('embedding.model')}")
        print(f"LLM         : {self.get('llm.provider')}")
        print(f"Mode        : {self.get('application.mode')}")

        print("=" * 60)