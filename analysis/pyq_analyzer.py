"""
=========================================================
AI_NEET

Previous Year Question Intelligence Engine

Author : Praveen Mark

Description
-----------
Analyzes NEET previous year questions.

Provides

✓ Chapter Frequency
✓ Topic Frequency
✓ Concept Frequency
✓ Repeated Questions
✓ Repeated Concepts
✓ Year-wise Analysis
✓ Importance Ranking

=========================================================
"""

from collections import defaultdict

class PYQAnalyzer:

    def __init__(self):

        self.chapter_frequency = defaultdict(int)

        self.topic_frequency = defaultdict(int)

        self.concept_frequency = defaultdict(int)

        self.question_frequency = defaultdict(list)

        self.year_frequency = defaultdict(list)

    
        # --------------------------------------------------

    def analyze(

        self,

        questions

    ):

        print()

        print("=" * 70)
        print("PYQ INTELLIGENCE ENGINE")
        print("=" * 70)

        for question in questions:

            chapter = question["chapter"]

            topic = question["topic"]

            concept = question.get(

                "concept",

                ""

            )

            year = question["exam_year"]

            text = question["question_text"]

            self.chapter_frequency[chapter] += 1

            self.topic_frequency[topic] += 1

            self.concept_frequency[concept] += 1

            self.question_frequency[text].append(

                year

            )

            self.year_frequency[chapter].append(

                year

            )

        # --------------------------------------------------

    def repeated_questions(self):

        repeated = []

        for question, years in self.question_frequency.items():

            if len(years) > 1:

                repeated.append(

                    {

                        "question": question,

                        "years": sorted(years),

                        "count": len(years)

                    }

                )

        return repeated
    
        # --------------------------------------------------

    def chapter_report(

        self,

        chapter

    ):

        return {

            "chapter": chapter,

            "questions": self.chapter_frequency.get(

                chapter,

                0

            ),

            "years": sorted(

                self.year_frequency.get(

                    chapter,

                    []

                )

            )

        }
    
    