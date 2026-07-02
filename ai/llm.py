"""
=========================================================
AI_NEET

Local LLM Engine

Author : Praveen Mark

Supports

✓ Ollama
✓ Offline AI
✓ JSON Responses
✓ Question Parsing
✓ Question Generation

=========================================================
"""

import requests

from core.config import ConfigManager


class LocalLLM:

    def __init__(self):

        self.config = ConfigManager()

        self.model = self.config.get(
            "llm.model",
            "qwen2.5:7b"
        )

        self.host = self.config.get(
            "llm.host",
            "http://localhost:11434"
        )

        self.timeout = self.config.get(
            "llm.timeout",
            300
        )

        self.temperature = self.config.get(
            "llm.temperature",
            0.1
        )

        self.num_ctx = self.config.get(
            "llm.num_ctx",
            4096
        )

        self.num_predict = self.config.get(
            "llm.num_predict",
            1024
        )

        self.api = f"{self.host}/api/generate"

        print()

        print("=" * 70)
        print("LOCAL AI ENGINE")
        print("=" * 70)
        print(f"Model       : {self.model}")
        print(f"Host        : {self.host}")
        print(f"Timeout     : {self.timeout}")
        print(f"Temperature : {self.temperature}")
        print(f"Context     : {self.num_ctx}")
        print("=" * 70)

    # --------------------------------------------------

    def generate(

        self,

        prompt

    ):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": self.temperature,

                "num_ctx": self.num_ctx,

                "num_predict": self.num_predict

            }

        }

        try:

            response = requests.post(

                self.api,

                json=payload,

                timeout=self.timeout

            )

            response.raise_for_status()

            result = response.json()

            return result["response"]

        except Exception as e:

            print()

            print("=" * 70)
            print("OLLAMA ERROR")
            print("=" * 70)
            print(e)
            print("=" * 70)

            return ""

    # --------------------------------------------------

    def health(self):

        try:

            response = requests.get(

                self.host,

                timeout=5

            )

            return response.status_code == 200

        except Exception:

            return False

    # --------------------------------------------------

    def ask(

        self,

        prompt

    ):

        print()

        print("=" * 70)
        print("PROMPT")
        print("=" * 70)

        print(prompt[:500])

        print()

        print("=" * 70)
        print("GENERATING...")
        print("=" * 70)

        answer = self.generate(prompt)

        print()

        print("=" * 70)
        print("AI RESPONSE")
        print("=" * 70)

        print(answer)

        print("=" * 70)

        return answer