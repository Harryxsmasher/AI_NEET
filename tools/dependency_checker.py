"""
=========================================================
AI_NEET

Dependency Checker

Author : Praveen Mark

Description
-----------
Checks whether all required Python packages
for AI_NEET are installed.

=========================================================
"""

import importlib

REQUIRED_PACKAGES = {

    # Core
    "numpy": "numpy",
    "requests": "requests",
    "faiss": "faiss-cpu",
    "sentence_transformers": "sentence-transformers",

    # AI
    "torch": "torch",
    "transformers": "transformers",

    # PDF
    "fitz": "PyMuPDF",
    "pdfplumber": "pdfplumber",

    # Database
    "sqlite3": "Built-in",

    # API (Future)
    "fastapi": "fastapi",
    "uvicorn": "uvicorn",
    "jinja2": "jinja2",

    # Utilities
    "yaml": "pyyaml",
    "tqdm": "tqdm"

}


def check():

    print()
    print("=" * 70)
    print("AI_NEET DEPENDENCY CHECKER")
    print("=" * 70)

    missing = []

    for module, package in REQUIRED_PACKAGES.items():

        try:

            importlib.import_module(module)

            print(f"[ OK ] {module}")

        except Exception:

            print(f"[MISS] {module:<25} Install -> pip install {package}")

            missing.append(package)

    print("=" * 70)

    if missing:

        print("\nMissing Packages\n")

        for package in sorted(set(missing)):

            print(package)

    else:

        print("\nEverything Required Is Installed.")

    print("=" * 70)


if __name__ == "__main__":

    check()