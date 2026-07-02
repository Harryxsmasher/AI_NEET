"""
=========================================================
AI_NEET

Prompt Library

Author : Praveen Mark

=========================================================
"""


class PromptLibrary:

    # --------------------------------------------------

    @staticmethod
    @staticmethod
    def question_parser(ocr_text):

        return f"""
    You are an expert OCR document parser for NEET examination papers.

    Your ONLY task is to convert OCR text into structured JSON.

    =========================================================
    STRICT RULES
    =========================================================

    DO NOT explain anything.

    DO NOT answer the questions.

    DO NOT summarize.

    DO NOT rewrite.

    Return ONLY valid JSON.

    =========================================================
    IGNORE
    =========================================================

    Ignore

    • page numbers
    • headers
    • footers
    • section titles
    • answer keys
    • instructions
    • figure captions
    • tables
    • image labels
    • watermarks
    • repeated text

    =========================================================
    QUESTION RULES
    =========================================================

    Extract ONLY multiple choice questions.

    A question begins with

    1.
    2.
    3.

    etc.

    A question ends after Option 4.

    Do NOT merge text from another question.

    Do NOT merge tables into questions.

    If OCR contains unrelated text after option 4,
    ignore it.

    =========================================================
    OPTIONS
    =========================================================

    Extract exactly four options.

    Supported formats

    (1)

    1)

    1.

    A)

    A.

    (a)

    =========================================================
    SUBJECT
    =========================================================

    Automatically identify

    Biology

    Physics

    Chemistry

    =========================================================
    OUTPUT
    =========================================================

    Return ONLY JSON.

    {{
        "questions":
        [
            {{
                "question_number":1,

                "subject":"Biology",

                "chapter":"Plant Kingdom",

                "question":"...",

                "options":
                {{
                    "1":"...",

                    "2":"...",

                    "3":"...",

                    "4":"..."
                }}
            }}
        ]
    }}

    =========================================================
    OCR TEXT
    =========================================================

    {ocr_text}

    =========================================================
    """

    # --------------------------------------------------

    @staticmethod
    def subject_classifier(question):

        return f"""
Identify the subject of this NEET question.

Possible values

Biology
Physics
Chemistry

Return ONLY the subject.

Question

{question}
"""

    # --------------------------------------------------

    @staticmethod
    def chapter_classifier(question):

        return f"""
Identify the NCERT chapter.

Return ONLY chapter name.

Question

{question}
"""

    # --------------------------------------------------

    @staticmethod
    def difficulty_classifier(question):

        return f"""
Classify difficulty.

Possible values

Easy
Medium
Hard

Return ONLY one word.

Question

{question}
"""

    # --------------------------------------------------

    @staticmethod
    def generate_question(topic):

        return f"""
Generate one NEET level MCQ.

Topic

{topic}

Return JSON

{{
    "question":"",
    "options":
    {{
        "1":"",
        "2":"",
        "3":"",
        "4":""
    }},
    "correct_answer":""
}}
"""