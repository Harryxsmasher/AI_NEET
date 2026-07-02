"""
=========================================================
AI_NEET

Question Repository

Author : Praveen Mark

Description
-----------
Handles all SQLite operations for
Question Bank.

=========================================================
"""

from database.database import DatabaseManager


class QuestionRepository:

    def __init__(self, database):

        self.database = database
        



    # --------------------------------------------------

    def question_exists(

        self,

        question_text

    ):

        row = self.database.fetchone(

            """
            SELECT id

            FROM questions

            WHERE question_text = ?

            LIMIT 1
            """,

            (

                question_text,

            )

        )

        return row is not None

    # --------------------------------------------------

    def insert_question(

        self,

        question

    ):

        if self.question_exists(

            question["question_text"]

        ):

            return False

        self.database.execute(

            """
            INSERT INTO questions
            (

                question_number,

                question_text,

                option_a,

                option_b,

                option_c,

                option_d,

                correct_answer,

                subject,

                chapter,

                topic,

                exam_year,

                page_number,

                source_file,

                image_path,

                repeat_count,

                difficulty,

                verified

            )

            VALUES

            (

                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

            )

            """,

            (

                question["question_number"],

                question["question_text"],

                question["option_a"],

                question["option_b"],

                question["option_c"],

                question["option_d"],

                question["correct_answer"],

                question["subject"],

                question["chapter"],

                question["topic"],

                question["exam_year"],

                question["page_number"],

                question["source_file"],

                question["image_path"],

                question["repeat_count"],

                question["difficulty"],

                question["verified"]

            )

        )

        return True
    
        # --------------------------------------------------

        # --------------------------------------------------
    # AI Question Support
    # --------------------------------------------------

    def insert_ai_question(

        self,

        question

    ):

        database_question = {

            "question_number":

                question.get(

                    "question_number",

                    0

                ),

            "question_text":

                question.get(

                    "question",

                    ""

                ),

            "option_a":

                question.get(

                    "options",

                    {}

                ).get(

                    "1",

                    ""

                ),

            "option_b":

                question.get(

                    "options",

                    {}

                ).get(

                    "2",

                    ""

                ),

            "option_c":

                question.get(

                    "options",

                    {}

                ).get(

                    "3",

                    ""

                ),

            "option_d":

                question.get(

                    "options",

                    {}

                ).get(

                    "4",

                    ""

                ),

            "correct_answer":

                question.get(

                    "correct_answer",

                    ""

                ),

            "subject":

                question.get(

                    "subject",

                    "Unknown"

                ),

            "chapter":

                question.get(

                    "chapter",

                    "Unknown"

                ),

            "topic":

                question.get(

                    "topic",

                    ""

                ),

            "exam_year":

                question.get(

                    "exam_year",

                    0

                ),

            "page_number":

                question.get(

                    "page_number",

                    0

                ),

            "source_file":

                question.get(

                    "source_file",

                    ""

                ),

            "image_path":"",

            "repeat_count":0,

            "difficulty":

                question.get(

                    "difficulty",

                    "Medium"

                ),

            "verified":1

        }

        return self.insert_question(

            database_question

        )

    def insert_many(self, questions):

        inserted = 0

        skipped = 0

        total = len(questions)

        print()

        print("=" * 70)
        print("INSERTING QUESTION BANK")
        print("=" * 70)

        for index, question in enumerate(
            questions,
            start=1
        ):

            success = self.insert_question(
                question
            )

            if success:

                inserted += 1

            else:

                skipped += 1

            if index % 50 == 0 or index == total:

                print(
                    f"[{index}/{total}]"
                )

        print()

        print(f"Inserted : {inserted}")

        print(f"Skipped  : {skipped}")

        print("=" * 70)

        return inserted

    # --------------------------------------------------

        # --------------------------------------------------
    # AI Bulk Insert
    # --------------------------------------------------

    def insert_ai_questions(

        self,

        questions

    ):

        inserted = 0

        skipped = 0

        total = len(questions)

        print()

        print("=" * 70)
        print("AI QUESTION INSERTION")
        print("=" * 70)

        for index, question in enumerate(

            questions,

            start=1

        ):

            success = self.insert_ai_question(

                question

            )

            if success:

                inserted += 1

            else:

                skipped += 1

            if index % 25 == 0 or index == total:

                print(

                    f"[{index}/{total}]"

                )

        print()

        print("=" * 70)
        print("AI INSERT SUMMARY")
        print("=" * 70)
        print(f"Inserted : {inserted}")
        print(f"Skipped  : {skipped}")
        print("=" * 70)

        return inserted

    def search(

        self,

        keyword

    ):

        return self.database.fetchall(

            """
            SELECT *

            FROM questions

            WHERE question_text LIKE ?

            ORDER BY exam_year
            """,

            (

                f"%{keyword}%",

            )

        )

    # --------------------------------------------------

    def get_questions_by_year(

        self,

        year

    ):

        return self.database.fetchall(

            """
            SELECT *

            FROM questions

            WHERE exam_year=?

            ORDER BY question_number
            """,

            (

                year,

            )

        )

    # --------------------------------------------------

    def random_questions(

        self,

        limit=10

    ):

        return self.database.fetchall(

            f"""
            SELECT *

            FROM questions

            ORDER BY RANDOM()

            LIMIT {limit}
            """

        )

    # --------------------------------------------------

    def count(self):

        row = self.database.fetchone(

            """
            SELECT COUNT(*)

            FROM questions
            """
        )

        return row[0]

    # --------------------------------------------------

    def clear(self):

        self.database.execute(

            """
            DELETE FROM questions
            """
        )

    # --------------------------------------------------

    def close(self):

        self.database.close()