"""
=========================================================
AI_NEET
SQLite Database Schema

Author : Praveen Mark
=========================================================
"""

SCHEMA = [

    """
    CREATE TABLE IF NOT EXISTS books (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        subject TEXT NOT NULL,

        class_level TEXT,

        source_type TEXT NOT NULL,

        file_name TEXT NOT NULL,

        file_path TEXT NOT NULL,

        total_pages INTEGER DEFAULT 0,

        processed INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );
    """,

    """
    CREATE TABLE IF NOT EXISTS knowledge_chunks (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        book_id INTEGER,

        page_number INTEGER,

        chunk_index INTEGER,

        chunk_text TEXT,

        embedding_id TEXT,

        FOREIGN KEY(book_id) REFERENCES books(id)

    );
    """,

    """
    CREATE TABLE IF NOT EXISTS questions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    question_number INTEGER,

    question_text TEXT NOT NULL,

    option_a TEXT,

    option_b TEXT,

    option_c TEXT,

    option_d TEXT,

    correct_answer TEXT,

    explanation TEXT,

    subject TEXT,

    chapter TEXT,

    topic TEXT,

    difficulty TEXT,

    source_file TEXT,

    exam_year INTEGER,

    page_number INTEGER,

    repeat_count INTEGER DEFAULT 0,

    image_path TEXT,

    formula_path TEXT,

    embedding_id TEXT,

    verified INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(question_text, exam_year)

);
    """,

    """
    CREATE TABLE IF NOT EXISTS mock_test_questions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        mock_test_id INTEGER,

        question_id INTEGER,

        question_order INTEGER,

        FOREIGN KEY(mock_test_id) REFERENCES mock_tests(id),

        FOREIGN KEY(question_id) REFERENCES questions(id)

    );
    """,

    """
    CREATE TABLE IF NOT EXISTS student_results (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        mock_test_id INTEGER,

        student_name TEXT,

        correct_answers INTEGER,

        wrong_answers INTEGER,

        skipped_answers INTEGER,

        obtained_marks INTEGER,

        percentage REAL,

        submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(mock_test_id) REFERENCES mock_tests(id)

    );
    """,

    """
CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    book_id INTEGER,

    source_file TEXT NOT NULL,

    source_type TEXT NOT NULL,

    exam_year INTEGER,

    total_pages INTEGER DEFAULT 0,

    processing_status TEXT DEFAULT 'REGISTERED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(book_id) REFERENCES books(id)

);
""",
"""
CREATE INDEX IF NOT EXISTS idx_documents_source
ON documents(source_type);
""",

"""
CREATE INDEX IF NOT EXISTS idx_documents_year
ON documents(exam_year);
""",

    """
    CREATE INDEX IF NOT EXISTS idx_question_subject
    ON questions(subject);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_question_chapter
    ON questions(chapter);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_question_year
    ON questions(exam_year);
    """,

    """
    CREATE INDEX IF NOT EXISTS idx_chunk_book
    ON knowledge_chunks(book_id);
    """

]