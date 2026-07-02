"""
=========================================================
AI_NEET

Entry Point

Author : Praveen Mark
=========================================================
"""

from core.orchestrator import AINEETSystem


def main():

    system = AINEETSystem()

    system.initialize()

    system.run()


if __name__ == "__main__":
    main()