"""
=========================================================
AI_NEET

Database Manager

Author : Praveen Mark
=========================================================
"""

import sqlite3
from pathlib import Path

from core.config import ConfigManager
from core.logger import Logger
from database.schema import SCHEMA


class DatabaseManager:

    def __init__(self):

        self.logger = Logger.get_logger()

        self.config = ConfigManager()

        self.database_path = Path(
            self.config.get("database.sqlite")
        )

        self.connection = None
        self.cursor = None

    # --------------------------------------------------

    def connect(self):

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.logger.info(
            f"SQLite Connected : {self.database_path}"
        )

    # --------------------------------------------------

    def initialize(self):

        self.connect()

        self.logger.info("Creating Database Schema...")

        for query in SCHEMA:

            self.cursor.execute(query)

        self.connection.commit()

        self.logger.info("Database Ready.")

    # --------------------------------------------------

    def insert_book(self, document: dict):

        query = """
        INSERT INTO books
        (
            title,
            subject,
            class_level,
            source_type,
            file_name,
            file_path,
            total_pages,
            processed
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?
        )
        """

        existing = self.fetchone(

            """
            SELECT id
            FROM books
            WHERE file_path = ?
            """,

            (document["file_path"],)

        )

        if existing:
            return existing["id"]

        self.execute(

            query,

            (

                document["title"],

                document["subject"],

                document["class_level"],

                document["source_type"],

                document["file_name"],

                document["file_path"],

                document["page_count"],

                int(document["processed"])

            )

        )

        return self.cursor.lastrowid
    
        # --------------------------------------------------

    def insert_document(self, document: dict):

        query = """
        INSERT INTO documents
        (
            book_id,
            source_file,
            source_type,
            exam_year,
            total_pages,
            processing_status
        )
        VALUES
        (
            ?,?,?,?,?,?
        )
        """

        existing = self.fetchone(

            """
            SELECT id
            FROM documents
            WHERE source_file = ?
            """,

            (
                document["file_name"],
            )

        )

        if existing:

            return existing["id"]

        self.execute(

            query,

            (

                document.get(
                    "book_id"
                ),

                document["file_name"],

                document["source_type"],

                document.get(
                    "exam_year"
                ),

                document["page_count"],

                "REGISTERED"

            )

        )

        return self.cursor.lastrowid

    # --------------------------------------------------
        # --------------------------------------------------

    def insert_chunk(self, chunk: dict):

        query = """
        INSERT INTO knowledge_chunks
        (
            book_id,
            page_number,
            chunk_index,
            chunk_text,
            embedding_id
        )
        VALUES
        (
            ?,?,?,?,?
        )
        """

        self.execute(

            query,

            (

                chunk["book_id"],

                chunk["page_number"],

                chunk["chunk_index"],

                chunk["chunk_text"],

                chunk.get(

                    "embedding_id",

                    None

                )

            )

        )

        return self.cursor.lastrowid

    def execute(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        self.connection.commit()

    # --------------------------------------------------

    def fetchone(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        return self.cursor.fetchone()

    # --------------------------------------------------

    def fetchall(self, query, parameters=()):

        self.cursor.execute(query, parameters)

        return self.cursor.fetchall()

    # --------------------------------------------------

    def table_count(self):

        result = self.fetchone(

            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type='table'
            AND name NOT LIKE 'sqlite_%'
            """

        )

        return result[0]

    # --------------------------------------------------

    def book_count(self):

        result = self.fetchone(

            """
            SELECT COUNT(*)
            FROM books
            """

        )

        return result[0]

    # --------------------------------------------------

        # --------------------------------------------------

    def document_count(self):

        result = self.fetchone(

            """
            SELECT COUNT(*)
            FROM documents
            """

        )

        return result[0]
    
    #-----------------------------------------------------
        # --------------------------------------------------

    def chunk_count(self):

        result = self.fetchone(

            """
            SELECT COUNT(*)
            FROM knowledge_chunks
            """

        )

        return result[0]
    #-----------------------------------------------------------

        # --------------------------------------------------

    def knowledge_count(self):

        result = self.fetchone(

            """
            SELECT COUNT(*)

            FROM knowledge_objects
            """

        )

        return result[0]

    def close(self):

        if self.connection:

            self.connection.close()

            self.logger.info(
                "SQLite Connection Closed."
            )