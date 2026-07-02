"""
=========================================================
AI_NEET

Application Orchestrator

Author : Praveen Mark

Description
-----------
Central controller for the AI_NEET system.

=========================================================
"""

from pathlib import Path
import json
from core.config import ConfigManager
from core.logger import Logger

from database.database import DatabaseManager

from ingestion.pdf_loader import PDFLoader
from ingestion.text_extractor import TextExtractor
from questions.repository import QuestionRepository
from ai.llm import LocalLLM
from ai.parser import AIQuestionParser
from ai.validator import AIValidator
from ai.document_assembler import DocumentAssembler
from core.document_registry import DocumentRegistry
from ai.knowledge_parser import KnowledgeParser

input_folder = Path("data")

output_folder = Path("cache/extracted")

class AINEETSystem:

    def __init__(self):

        # ------------------------------------
        # AI Document Engine
        # ------------------------------------

        self.document_assembler = DocumentAssembler()

        # ------------------------------------
        # Document Registry
        # ------------------------------------

        self.document_registry = DocumentRegistry()

        # ------------------------------------
        # Core
        # ------------------------------------

        self.config = ConfigManager()

        self.logger = Logger.get_logger()

        self.database = DatabaseManager()

        # ------------------------------------
        # Engines
        # ------------------------------------

        self.pdf_loader = PDFLoader()

        self.text_extractor = TextExtractor()

                # ------------------------------------
        # AI Engine
        # ------------------------------------

        self.llm = LocalLLM()

        self.ai_parser = AIQuestionParser(
            self.llm
        )

        self.ai_validator = AIValidator()

        # ------------------------------------
        # Knowledge Engine
        # ------------------------------------

        self.knowledge_parser = KnowledgeParser(
            self.llm
        )

        # ------------------------------------
        # Question Engine
        # ------------------------------------

        self.question_repository = QuestionRepository(
            self.database
        )

        self.logger.info(
            "Application Controller Created."
        )
    # ==================================================

    def initialize(self):

        self.show_banner()

        self.logger.info(
            "Initializing AI_NEET..."
        )

        self.database.initialize()

        self.logger.info(
            "Database Initialized."
        )

        self.verify_folders()

        self.logger.info(
            "Folder Verification Complete."
        )

        self.system_summary()

        self.logger.info(
            "Initialization Complete."
        )

    # ==================================================

    def show_banner(self):

        print()

        print("=" * 70)

        print("                     AI_NEET")

        print("          Offline AI Examination Platform")

        print("=" * 70)

        print(
            f"Version : {self.config.get('application.version')}"
        )

        print(
            f"Author  : {self.config.get('application.author')}"
        )

        print("=" * 70)

    # ==================================================

    def verify_folders(self):

        folders = [

            "cache",

            "cache/extracted",

            "cache/processed",

            "cache/generated",

            "vectordb",

            "logs",

            "output",

            "database"

        ]

        for folder in folders:

            Path(folder).mkdir(
                parents=True,
                exist_ok=True
            )

    # ==================================================

    def system_summary(self):

        print()

        print("-" * 70)

        print("SYSTEM STATUS")

        print("-" * 70)

        print("[ OK ] Configuration")

        print("[ OK ] Logger")

        print("[ OK ] SQLite")

        print("[ OK ] Database")

        print("[ OK ] Folder Structure")

        print("-" * 70)

        print(
            f"Tables : {self.database.table_count()}"
        )

        print("-" * 70)

    # ==================================================

    def run(self):

        self.logger.info(
            "Starting AI_NEET Main Loop."
        )

        while True:

            self.show_menu()

            choice = input(
                "\nEnter Choice : "
            ).strip()

            if choice == "1":

                self.generate_mock_test()

            elif choice == "2":

                self.analyze_previous_papers()

            elif choice == "3":

                self.build_knowledge_base()

            elif choice == "4":

                self.search_questions()

            elif choice == "5":

                self.student_history()

            elif choice == "6":

                self.shutdown()
                break

            elif choice == "7":

                self.test_ai_parser()

            elif choice == "8":

                self.test_document_assembler()
                
                

            else:

                print("\nInvalid Choice.")

                self.logger.warning(
                    "Invalid Menu Choice."
                )

        # ==================================================

    def show_menu(self):

        print()

        print("=" * 70)
        print("MAIN MENU")
        print("=" * 70)

        print("1. Generate Mock Test")
        print("2. Analyze Previous Papers")
        print("3. Build Knowledge Base")
        print("4. Question Search")
        print("5. Student History")
        print("6. Exit")
        print("7. Test AI Parser")
        print("8. Test Document Assembler")
        

        print("=" * 70)

    # ==================================================

    def build_knowledge_base(self):

        self.logger.info(
            "Knowledge Base Build Started."
        )

        print()
        print("=" * 70)
        print("STEP 1 : SCANNING DOCUMENTS")
        print("=" * 70)

        documents = self.pdf_loader.scan()

        # ------------------------------------
        # Register Documents
        # ------------------------------------

        registered_documents = self.document_registry.register_documents(
            documents
        )

        self.document_registry.print_summary()

        summary = self.pdf_loader.summary()

        self.logger.info(
            f"PDFs Found : {summary['Total PDFs']}"
        )

        self.logger.info(
            f"Pages Found : {summary['Total Pages']}"
        )

        print()
        print("=" * 70)
        print("STEP 2 : REGISTERING BOOKS")
        print("=" * 70)

        inserted = 0

        for index, document in enumerate(
            documents,
            start=1
        ):

            print(
                f"[{index:03d}/{len(documents)}] "
                f"{document['file_name']}"
            )

            book_id = self.database.insert_book(
                document
            )

            document["book_id"] = book_id

            self.database.insert_document(
                document
            )

            inserted += 1

        print()
        print("=" * 70)
        print("STEP 3 : EXTRACTING TEXT")
        print("=" * 70)

        extracted_documents = self.text_extractor.process(

            input_folder,

            output_folder

        )

        print()

        print("=" * 70)
        print("STEP 4 : ASSEMBLING DOCUMENTS")
        print("=" * 70)

        assembled_documents = self.document_assembler.process_all()

        # DEBUG MODE
        assembled_documents = assembled_documents[:1]

        total_chunks = 0

        for assembled_document in assembled_documents:

            book = self.database.fetchone(

                """
                SELECT id
                FROM books
                WHERE file_name = ?
                """,

                (

                    assembled_document["file_name"].replace(

                        ".json",

                        ".pdf"

                    ),

                )

            )

            if not book:

                continue

            book_id = book["id"]

            for chunk in assembled_document["chunks"]:

                chunk["book_id"] = book_id

                self.database.insert_chunk(

                    chunk

                )

                total_chunks += 1
        
        print()

        print("=" * 70)
        print("STEP 5 : AI KNOWLEDGE EXTRACTION")
        print("=" * 70)

        knowledge_objects = self.knowledge_parser.process(

            assembled_documents

        )

        print()
        print("=" * 70)
        print("KNOWLEDGE BASE SUMMARY")
        print("=" * 70)

        print(f"Books Scanned : {len(documents)}")
        print(f"Books Stored  : {inserted}")

        print(
            f"Documents Registered : {self.database.document_count()}"
        )
        print(
            f"Database Rows : {self.database.book_count()}"
        )
        print(
            f"PDFs Cached : {extracted_documents['pdfs']}"
        )

        print(
            f"Pages Cached : {extracted_documents['pages']}"
        )

        print(
            f"Chunks Processed : {total_chunks}"
        )

        print(
            f"Knowledge Chunks : {self.database.chunk_count()}"
        )

        print(
            f"Knowledge Objects : {len(knowledge_objects)}"
        )

        print("=" * 70)

        self.logger.info(
            "Knowledge Base Build Completed."
        )

    # ==================================================

    def test_ai_parser(self):

        print()
        print("=" * 70)
        print("AI PARSER TEST")
        print("=" * 70)

        json_file = Path(
            "cache/extracted/neet_2021.json"
        )

        if not json_file.exists():

            print("OCR JSON not found.")
            return

        with open(

            json_file,

            "r",

            encoding="utf-8"

        ) as file:

            document = json.load(file)

        questions = self.ai_parser.parse_document(

            document["pages"]

        )

        questions = self.ai_validator.validate_all(

            questions

        )

        print()

        print("=" * 70)
        print("FIRST 3 QUESTIONS")
        print("=" * 70)

        for question in questions[:3]:

            print(question)

            print("-" * 70)

        print()

        print(f"Total AI Questions : {len(questions)}")

    def test_document_assembler(self):

        print()

        print("=" * 70)
        print("DOCUMENT ASSEMBLER TEST")
        print("=" * 70)

        documents = self.document_assembler.process_all()

        if not documents:

            print("No OCR documents found.")

            return

        first = documents[0]

        print()

        print("=" * 70)
        print(first["file_name"])
        print("=" * 70)

        print()

        print("Biology Chunks :", len(first["biology"]))
        print("Chemistry Chunks :", len(first["chemistry"]))
        print("Physics Chunks :", len(first["physics"]))

        print()

        if first["biology"]:

            print("=" * 70)
            print("FIRST BIOLOGY CHUNK")
            print("=" * 70)

            print(first["biology"][0][:1200])

    def analyze_previous_papers(self):

        self.logger.info(
            "Previous Paper Analysis Started."
        )

        from questions.extractor import QuestionExtractor

        extractor = QuestionExtractor()

        questions = extractor.process()

        inserted = self.question_repository.insert_many(
            questions
        )

        print()

        print("=" * 70)
        print("QUESTION BANK SUMMARY")
        print("=" * 70)

        print(f"Questions Extracted : {len(questions)}")

        print(f"Inserted Into SQLite : {inserted}")

        print(
            f"Total Database Questions : "
            f"{self.question_repository.count()}"
        )

        print("=" * 70)

        self.logger.info(
            "Previous Paper Analysis Completed."
        )

    # ==================================================

    def generate_mock_test(self):

        self.logger.info(
            "Mock Test Generation Requested."
        )

        print()

        print("=" * 70)
        print("MOCK TEST GENERATOR")
        print("=" * 70)

        print("Question Bank not built yet.")

        print("=" * 70)
    
        # ==================================================

    def search_questions(self):

        self.logger.info(
            "Question Search Requested."
        )

        print()

        print("=" * 70)
        print("QUESTION SEARCH")
        print("=" * 70)

        keyword = input(
            "Enter keyword (leave blank to return): "
        ).strip()

        if not keyword:

            print("Returning to main menu...")

            return

        rows = self.database.fetchall(

            """
            SELECT
                id,
                subject,
                chapter,
                exam_year,
                question_text
            FROM questions
            WHERE question_text LIKE ?
            ORDER BY exam_year
            """,

            (f"%{keyword}%",)

        )

        print()

        if not rows:

            print("No matching questions found.")

            return

        print(f"Found {len(rows)} question(s)\n")

        for row in rows:

            print("-" * 70)

            print(
                f"[{row['id']}] "
                f"{row['subject']} "
                f"{row['exam_year']}"
            )

            print(
                f"Chapter : {row['chapter']}"
            )

            print()

            print(row["question_text"][:300])

        print("-" * 70)

    # ==================================================

    def student_history(self):

        self.logger.info(
            "Student History Requested."
        )

        print()

        print("=" * 70)
        print("STUDENT HISTORY")
        print("=" * 70)

        rows = self.database.fetchall(

            """
            SELECT
                student_name,
                obtained_marks,
                percentage,
                submitted_at
            FROM student_results
            ORDER BY submitted_at DESC
            LIMIT 20
            """

        )

        if not rows:

            print("No history available.")

            return

        for row in rows:

            print(
                f"{row['submitted_at']} | "
                f"{row['student_name']} | "
                f"{row['obtained_marks']} Marks | "
                f"{row['percentage']}%"
            )

    # ==================================================

    def shutdown(self):

        self.logger.info(
            "Shutting Down AI_NEET..."
        )

        try:

            self.database.close()

        except Exception as ex:

            self.logger.error(str(ex))

        print()

        print("=" * 70)
        print("Thank you for using AI_NEET")
        print("=" * 70)

        self.logger.info(
            "Application Closed Successfully."
        )