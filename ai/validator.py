"""
=========================================================
AI_NEET

AI Question Validator

Author : Praveen Mark

Validates AI generated questions before
they are inserted into SQLite.

=========================================================
"""


class AIValidator:

    def __init__(self):

        self.required_subjects = {

            "Biology",

            "Physics",

            "Chemistry"

        }

    # --------------------------------------------------

    def validate(self, question):

        if not isinstance(question, dict):

            return False

        if not self.validate_number(question):

            return False

        if not self.validate_question(question):

            return False

        if not self.validate_options(question):

            return False

        if not self.validate_subject(question):

            return False

        if not self.validate_chapter(question):

            return False

        return True

    # --------------------------------------------------

    def validate_number(self, question):

        number = question.get(

            "question_number"

        )

        return isinstance(number, int)

    # --------------------------------------------------

    def validate_question(self, question):

        text = question.get(

            "question",

            ""

        )

        if not isinstance(text, str):

            return False

        return len(text.strip()) > 10

    # --------------------------------------------------

    def validate_options(self, question):

        options = question.get(

            "options"

        )

        if not isinstance(options, dict):

            return False

        required = [

            "1",

            "2",

            "3",

            "4"

        ]

        for key in required:

            value = options.get(

                key,

                ""

            )

            if len(

                str(value).strip()

            ) == 0:

                return False

        return True

    # --------------------------------------------------

    def validate_subject(self, question):

        subject = question.get(

            "subject",

            ""

        )

        if not subject:

            return False

        return subject in self.required_subjects

    # --------------------------------------------------

    def validate_chapter(self, question):

        chapter = question.get(

            "chapter",

            ""

        )

        return len(

            str(chapter).strip()

        ) > 0

    # --------------------------------------------------

    def validate_all(

        self,

        questions

    ):

        valid = []

        invalid = []

        seen = set()

        for question in questions:

            if not self.validate(question):

                invalid.append(question)

                continue

            key = (

                question["question_number"],

                question["question"]

            )

            if key in seen:

                continue

            seen.add(key)

            valid.append(question)

        print()

        print("=" * 70)
        print("AI VALIDATION")
        print("=" * 70)
        print(f"Valid Questions   : {len(valid)}")
        print(f"Invalid Questions : {len(invalid)}")
        print("=" * 70)

        return valid