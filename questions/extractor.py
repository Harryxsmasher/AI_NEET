"""
=========================================================
AI_NEET

Question Extraction Engine

Author : Praveen Mark

Description
-----------
Reads cached NEET JSON files and extracts
multiple-choice questions into structured
Question objects.

This parser uses a deterministic state-machine
instead of regex-only parsing to improve
reliability.

=========================================================
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List


class QuestionExtractor:

    QUESTION_PATTERN = re.compile(
    r"^\s*(\d+)[\.\)]?\s*(.*)$"
    )
    OPTION_PATTERN = re.compile(
    r"^\s*\(?([1-4])\)?[\.\)]?\s*(.*)$"
)

    STATE_FIND_QUESTION = "find_question"
    STATE_READ_QUESTION = "read_question"
    STATE_READ_OPTION_1 = "read_option_1"
    STATE_READ_OPTION_2 = "read_option_2"
    STATE_READ_OPTION_3 = "read_option_3"
    STATE_READ_OPTION_4 = "read_option_4"

    def __init__(self):

        self.questions: List[Dict] = []

        self.current_question = None

        self.current_state = self.STATE_FIND_QUESTION

    # --------------------------------------------------

    def load_json(self, json_file: str):

        with open(
            json_file,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # --------------------------------------------------

    def extract_file(self, json_file: str):

        document = self.load_json(json_file)

        self.questions = []

        exam_year = self.detect_year(
            document["file_name"]
        )

        source_file = (
            Path(document["file_name"]).stem + ".pdf"
        )

        for page in document["pages"]:

            self.parse_page(

                page["text"],

                page["page_number"],

                exam_year,

                source_file

            )

        self.finalize_current_question()

        return self.questions

    # --------------------------------------------------

    @staticmethod
    def detect_year(file_name: str):

        match = re.search(r"20\d\d", file_name)

        if match:

            return int(match.group())

        return None

    # --------------------------------------------------

    def new_question(

        self,

        question_number,

        page_number,

        exam_year,

        source_file

    ):

        self.current_question = {

            "question_number": question_number,

            "question_text": "",

            "option_a": "",

            "option_b": "",

            "option_c": "",

            "option_d": "",

            "correct_answer": "",

            "subject": "",

            "chapter": "",

            "topic": "",

            "exam_year": exam_year,

            "page_number": page_number,

            "source_file": source_file,

            "image_path": "",

            "repeat_count": 1,

            "difficulty": "",

            "verified": 0

        }

        self.current_state = self.STATE_READ_QUESTION

            # --------------------------------------------------

    def parse_page(

            self,

            text,

            page_number,

            exam_year,

            source_file

        ):

    # --------------------------------------------------
    # Skip Answer Key Pages
    # --------------------------------------------------

        lower_text = text.lower()

        if (
            "1 2 3 4 5 6 7 8 9 10" in lower_text
            or "ans section" in lower_text
            or "answer key" in lower_text
        ):
            return

        # --------------------------------------------------

        lines = text.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Ignore subject headings

            if line.upper() in (

                "BIOLOGY",
                "CHEMISTRY",
                "PHYSICS"

            ):

                continue

            # Ignore chapter titles

            if len(line.split()) <= 6 and not any(

                ch.isdigit() for ch in line

            ):

                if line.istitle() or line.isupper():

                    continue

            # ------------------------------------------

            question_match = self.QUESTION_PATTERN.match(
                line
            )

            if question_match:

                number = int(
                    question_match.group(1)
                )

                remaining = question_match.group(2).strip()

                # Question number without text?
                # Example:
                #
                # 1.
                #
                # Which...
                #
                if not remaining:

                    self.finalize_current_question()

                    self.new_question(

                        number,

                        page_number,

                        exam_year,

                        source_file

                    )

                    continue

                # Avoid parsing option lines as questions

                if number in (1, 2, 3, 4):

                    if (
                        self.current_question is not None
                        and self.current_state != self.STATE_READ_QUESTION
                    ):

                        pass

                    else:

                        self.finalize_current_question()

                        self.new_question(

                            number,

                            page_number,

                            exam_year,

                            source_file

                        )

                        self.append_text(remaining)

                    continue

                self.finalize_current_question()

                self.new_question(

                    number,

                    page_number,

                    exam_year,

                    source_file

                )

                self.append_text(remaining)

                continue

            # ------------------------------------------

            option_match = self.OPTION_PATTERN.match(
                line
            )

            if option_match:

                option_number = option_match.group(1)

                option_text = option_match.group(2).strip()

                self.start_option(

                    option_number,

                    option_text

                )

                continue

            # ------------------------------------------

            self.append_text(line)

    # --------------------------------------------------

    def start_option(

        self,

        option_number,

        option_text

    ):

        if self.current_question is None:

            return

        if option_number == "1":

            self.current_question["option_a"] = option_text

            self.current_state = self.STATE_READ_OPTION_1

        elif option_number == "2":

            self.current_question["option_b"] = option_text

            self.current_state = self.STATE_READ_OPTION_2

        elif option_number == "3":

            self.current_question["option_c"] = option_text

            self.current_state = self.STATE_READ_OPTION_3

        elif option_number == "4":

            self.current_question["option_d"] = option_text

            self.current_state = self.STATE_READ_OPTION_4

    # --------------------------------------------------

    def append_text(self, line):

        if self.current_question is None:

            return

        if self.current_state == self.STATE_READ_QUESTION:

            if self.current_question["question_text"]:

                self.current_question["question_text"] += " "

            self.current_question["question_text"] += line

            return

        if self.current_state == self.STATE_READ_OPTION_1:

            if self.current_question["option_a"]:

                self.current_question["option_a"] += " "

            self.current_question["option_a"] += line

            return

        if self.current_state == self.STATE_READ_OPTION_2:

            if self.current_question["option_b"]:

                self.current_question["option_b"] += " "

            self.current_question["option_b"] += line

            return

        if self.current_state == self.STATE_READ_OPTION_3:

            if self.current_question["option_c"]:

                self.current_question["option_c"] += " "

            self.current_question["option_c"] += line

            return

        if self.current_state == self.STATE_READ_OPTION_4:

            if self.current_question["option_d"]:

                self.current_question["option_d"] += " "

            self.current_question["option_d"] += line
        # --------------------------------------------------

    def finalize_current_question(self):

        if self.current_question is None:
            return

        self.current_question["question_text"] = (
            self.current_question["question_text"].strip()
        )

        self.current_question["option_a"] = (
            self.current_question["option_a"].strip()
        )

        self.current_question["option_b"] = (
            self.current_question["option_b"].strip()
        )

        self.current_question["option_c"] = (
            self.current_question["option_c"].strip()
        )

        self.current_question["option_d"] = (
            self.current_question["option_d"].strip()
        )

        # Ignore incomplete questions
        if not self.is_valid_question(
            self.current_question
        ):

            self.current_question = None
            self.current_state = self.STATE_FIND_QUESTION

            return

        self.questions.append(
            self.current_question
        )

        self.current_question = None

        self.current_state = self.STATE_FIND_QUESTION

    # --------------------------------------------------

    def is_valid_question(

        self,

        question

    ):

        if not question["question_text"]:
            return False

        if not question["option_a"]:
            return False

        if not question["option_b"]:
            return False

        if not question["option_c"]:
            return False

        if not question["option_d"]:
            return False

        return True

    # --------------------------------------------------

    def extract_folder(

        self,

        folder="cache/extracted"

    ):

        folder = Path(folder)

        files = sorted(
            folder.glob("neet_*.json")
        )

        all_questions = []

        print()

        print("=" * 70)
        print("QUESTION EXTRACTION")
        print("=" * 70)

        for index, file in enumerate(
            files,
            start=1
        ):

            print(
                f"[{index:02d}/{len(files)}] "
                f"{file.name}"
            )

            questions = self.extract_file(
                str(file)
            )

            print(
                f"Questions : {len(questions)}"
            )

            all_questions.extend(
                questions
            )

        print("=" * 70)

        return all_questions

    # --------------------------------------------------

    def statistics(

        self,

        questions

    ):

        years = {}

        for question in questions:

            year = question["exam_year"]

            years.setdefault(year, 0)

            years[year] += 1

        print()

        print("=" * 70)
        print("QUESTION EXTRACTION SUMMARY")
        print("=" * 70)

        for year in sorted(years):

            print(
                f"{year} : "
                f"{years[year]} Questions"
            )

        print("-" * 70)

        print(
            f"Total Questions : "
            f"{len(questions)}"
        )

        print("=" * 70)

        return years
    
        # --------------------------------------------------

    def remove_duplicates(self, questions):

        """
        Remove duplicate questions within the extracted set.
        """

        unique_questions = []
        seen = set()

        for question in questions:

            key = (
                question["question_text"]
                .strip()
                .lower()
            )

            if key in seen:
                continue

            seen.add(key)

            unique_questions.append(question)

        return unique_questions

    # --------------------------------------------------

    def export_json(

        self,

        questions,

        output_folder="cache/generated"

    ):

        output_folder = Path(output_folder)

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
            output_folder /
            "question_bank.json"
        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                questions,

                file,

                indent=4,

                ensure_ascii=False

            )

        print()

        print("=" * 70)
        print("QUESTION BANK SAVED")
        print("=" * 70)

        print(
            f"Output : {output_file}"
        )

        print("=" * 70)

    # --------------------------------------------------

    def process(self):

        """
        Complete Question Extraction Pipeline
        """

        questions = self.extract_folder()

        before = len(questions)

        questions = self.remove_duplicates(
            questions
        )

        after = len(questions)

        self.statistics(questions)

        print()

        print(
            f"Duplicates Removed : "
            f"{before-after}"
        )

        print(
            f"Final Questions : "
            f"{after}"
        )

        self.export_json(questions)

        return questions

    # --------------------------------------------------

    def __len__(self):

        return len(self.questions)