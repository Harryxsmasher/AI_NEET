"""
=========================================
AI_NEET
Constants

Author : Praveen Mark
=========================================
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

CACHE_DIR = PROJECT_ROOT / "cache"

DATABASE_DIR = PROJECT_ROOT / "database"

VECTOR_DB_DIR = PROJECT_ROOT / "vectordb"

OUTPUT_DIR = PROJECT_ROOT / "output"

LOG_DIR = PROJECT_ROOT / "logs"

TEMPLATE_DIR = PROJECT_ROOT / "templates"

ASSET_DIR = PROJECT_ROOT / "assets"

CONFIG_FILE = PROJECT_ROOT / "config.yaml"

DATABASE_FILE = DATABASE_DIR / "ai_neet.db"

APP_NAME = "AI_NEET"

VERSION = "1.0.0"

AUTHOR = "Praveen Mark"