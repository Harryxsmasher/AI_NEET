"""
=========================================================
AI_NEET

Knowledge Repository

Author : Praveen Mark

Description
-----------
Handles all SQLite operations for
Knowledge Objects.

=========================================================
"""

import json

from database.database import DatabaseManager

class KnowledgeRepository:

    def __init__(self):

        self.database = DatabaseManager()

        self.database.initialize()

        # --------------------------------------------------

    def knowledge_exists(

        self,

        chunk_id

    ):

        row = self.database.fetchone(

            """
            SELECT id

            FROM knowledge_objects

            WHERE chunk_id = ?

            LIMIT 1
            """,

            (

                chunk_id,

            )

        )

        return row is not None
    
        # --------------------------------------------------

    def insert_knowledge(

        self,

        chunk

    ):

        knowledge = chunk["knowledge"]

        chunk_id = chunk.get(

            "chunk_id",

            0

        )

        if self.knowledge_exists(

            chunk_id

        ):

            return False

        self.database.execute(

            """
            INSERT INTO knowledge_objects
            (

                chunk_id,

                subject,

                chapter,

                topics,

                keywords,

                summary

            )

            VALUES

            (

                ?,?,?,?,?,?

            )
            """,

            (

                chunk_id,

                knowledge["subject"],

                knowledge["chapter"],

                json.dumps(

                    knowledge["topics"]

                ),

                json.dumps(

                    knowledge["keywords"]

                ),

                knowledge["summary"]

            )

        )

        return True
    
        # --------------------------------------------------

    def insert_many(

        self,

        knowledge_objects

    ):

        inserted = 0

        skipped = 0

        total = len(knowledge_objects)

        print()

        print("=" * 70)
        print("INSERTING KNOWLEDGE OBJECTS")
        print("=" * 70)

        for index, knowledge in enumerate(

            knowledge_objects,

            start=1

        ):

            success = self.insert_knowledge(

                knowledge

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

    def get_by_subject(

        self,

        subject

    ):

        return self.database.fetchall(

            """
            SELECT *

            FROM knowledge_objects

            WHERE subject = ?

            ORDER BY chapter
            """,

            (

                subject,

            )

        )
    
        # --------------------------------------------------

    def get_by_chapter(

        self,

        subject,

        chapter

    ):

        return self.database.fetchall(

            """
            SELECT *

            FROM knowledge_objects

            WHERE subject = ?

            AND chapter = ?

            """,

            (

                subject,

                chapter,

            )

        )
    
        # --------------------------------------------------

    def search(

        self,

        keyword

    ):

        return self.database.fetchall(

            """
            SELECT *

            FROM knowledge_objects

            WHERE

                summary LIKE ?

                OR keywords LIKE ?

                OR topics LIKE ?

            """,

            (

                f"%{keyword}%",

                f"%{keyword}%",

                f"%{keyword}%"

            )

        )
    
        # --------------------------------------------------

    def count(

        self

    ):

        row = self.database.fetchone(

            """
            SELECT COUNT(*)

            FROM knowledge_objects
            """

        )

        return row[0]
    
        # --------------------------------------------------

    def clear(

        self

    ):

        self.database.execute(

            """
            DELETE FROM knowledge_objects
            """

        )

        # --------------------------------------------------

    def close(

        self

    ):

        self.database.close()

    
        # --------------------------------------------------

    def get_all(self):

        rows = self.database.fetchall(

            """
            SELECT *

            FROM knowledge_objects
            """

        )

        knowledge = []

        import json

        for row in rows:

            knowledge.append(

                {

                    "chunk_id": row["chunk_id"],

                    "subject": row["subject"],

                    "chapter": row["chapter"],

                    "topics": json.loads(

                        row["topics"]

                    ),

                    "keywords": json.loads(

                        row["keywords"]

                    ),

                    "summary": row["summary"]

                }

            )

        return knowledge
    
