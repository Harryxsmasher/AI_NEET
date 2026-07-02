"""
=========================================================
AI_NEET

AI Question Parser

Author : Praveen Mark

Converts OCR Text
↓

Structured JSON

=========================================================
"""

import json

from ai.prompts import PromptLibrary


class AIQuestionParser:

    def __init__(

        self,

        llm

    ):

        self.llm = llm

    # --------------------------------------------------

    def parse(

        self,

        ocr_text

    ):

        prompt = PromptLibrary.question_parser(

            ocr_text

        )

        response = self.llm.generate(

            prompt

        )

        return self.parse_json(

            response

        )

    # --------------------------------------------------

    def parse_json(

        self,

        response

    ):

        if not response:

            return {

                "questions": []

            }

        response = response.strip()

        # Remove markdown fences

        response = response.replace(

            "```json",

            ""

        )

        response = response.replace(

            "```",

            ""

        )

        start = response.find("{")

        end = response.rfind("}")

        if start == -1 or end == -1:

            return {

                "questions": []

            }

        response = response[start:end + 1]

        try:

            return json.loads(

                response

            )

        except Exception as e:

            print()

            print("=" * 70)
            print("AI JSON ERROR")
            print("=" * 70)
            print(e)
            print("=" * 70)

            return {

                "questions": []

            }

    # --------------------------------------------------

    def parse_document(

        self,

        pages

    ):

        all_questions = []

        total_pages = len(

            pages

        )

        print()

        print("=" * 70)
        print("AI DOCUMENT PARSER")
        print("=" * 70)

        for index, page in enumerate(

            pages,

            start=1

        ):

            text = page.get(

                "text",

                ""

            )

            if not text.strip():

                continue

            print(

                f"[{index}/{total_pages}]"

            )

            result = self.parse(

                text

            )

            questions = result.get(

                "questions",

                []

            )

            all_questions.extend(

                questions

            )

        print()

        print("=" * 70)
        print("AI PARSER SUMMARY")
        print("=" * 70)
        print(f"Questions : {len(all_questions)}")
        print("=" * 70)

        return all_questions

    # --------------------------------------------------

    def classify_subject(

        self,

        question

    ):

        prompt = PromptLibrary.subject_classifier(

            question

        )

        return self.llm.generate(

            prompt

        ).strip()

    # --------------------------------------------------

    def classify_chapter(

        self,

        question

    ):

        prompt = PromptLibrary.chapter_classifier(

            question

        )

        return self.llm.generate(

            prompt

        ).strip()

    # --------------------------------------------------

    def classify_difficulty(

        self,

        question

    ):

        prompt = PromptLibrary.difficulty_classifier(

            question

        )

        return self.llm.generate(

            prompt

        ).strip()