"""
=========================================================
AI_NEET

Knowledge Graph Engine

Author : Praveen Mark

Description
-----------
Builds relationships between subjects,
chapters, concepts, topics and keywords.

=========================================================
"""

from collections import defaultdict

class KnowledgeGraph:

    def __init__(self):

        self.subjects = defaultdict(list)

        self.chapters = defaultdict(list)

        self.topics = defaultdict(list)

        self.keywords = defaultdict(list)

        self.graph = {}

        # --------------------------------------------------

    def build(

        self,

        knowledge_objects

    ):

        print()

        print("=" * 70)
        print("KNOWLEDGE GRAPH")
        print("=" * 70)

        for item in knowledge_objects:

            subject = item["subject"]

            chapter = item["chapter"]

            topics = item["topics"]

            keywords = item["keywords"]

            self.subjects[subject].append(

                chapter

            )

            self.chapters[chapter].extend(

                topics

            )

            for topic in topics:

                self.topics[topic].extend(

                    keywords

                )

        print(

            f"Subjects : {len(self.subjects)}"

        )

        print(

            f"Chapters : {len(self.chapters)}"

        )

        print(

            f"Topics : {len(self.topics)}"

        )

        print("=" * 70)

        # --------------------------------------------------

    def get_subjects(self):

        return self.subjects

    # --------------------------------------------------

    def get_chapters(self):

        return self.chapters

    # --------------------------------------------------

    def get_topics(self):

        return self.topics
        # --------------------------------------------------

    def chapter_topics(

        self,

        chapter

    ):

        return self.chapters.get(

            chapter,

            []

        )
    
        # --------------------------------------------------

    def print_summary(self):

        print()

        print("=" * 70)
        print("KNOWLEDGE GRAPH SUMMARY")
        print("=" * 70)

        print(

            f"Subjects : {len(self.subjects)}"

        )

        print(

            f"Chapters : {len(self.chapters)}"

        )

        print(

            f"Topics : {len(self.topics)}"

        )

        print("=" * 70)

    