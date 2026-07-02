"""
=========================================================
AI_NEET

Document Assembler

Author : Praveen Mark

Description
-----------
Reads OCR JSON files and assembles them into
subject-wise text blocks for AI processing.

Output

Biology
Chemistry
Physics

=========================================================
"""

import json

from pathlib import Path


class DocumentAssembler:

    def __init__(

        self,

        extracted_folder="cache/extracted",

        max_chunk_size=25000

    ):

        self.extracted_folder = Path(

            extracted_folder

        )

        self.max_chunk_size = max_chunk_size

    # --------------------------------------------------

    def load_document(

        self,

        json_file

    ):

        with open(

            json_file,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)

    # --------------------------------------------------

    def clean_text(

        self,

        text

    ):

        if not text:

            return ""

        text = text.replace("\x0c", "")

        text = text.replace("\t", " ")

        text = text.replace("\r", " ")

        lines = []

        for line in text.splitlines():

            line = " ".join(

                line.split()

            )

            if not line:

                continue

            lower = line.lower()

            # Ignore obvious OCR junk

            if lower.startswith("page "):

                continue

            if "copyright" in lower:

                continue

            if "ncert" in lower:

                continue

            if len(line) <= 2:

                continue

            lines.append(line)

        return "\n".join(lines)

    # --------------------------------------------------

    def detect_subject(

        self,

        text,

        current_subject

    ):

        upper = text.upper()

        if "CHEMISTRY" in upper:

            return "chemistry"

        if "PHYSICS" in upper:

            return "physics"

        if "BIOLOGY" in upper:

            return "biology"

        # Preserve current subject when
        # a page contains no heading.

        return current_subject

    # --------------------------------------------------

    def is_answer_key(

        self,

        text

    ):

        lower = text.lower()

        keywords = [

            "answer key",

            "ans section",

            "answer",

            "solutions"

        ]

        for keyword in keywords:

            if keyword in lower:

                return True

        return False
    
        # --------------------------------------------------

    def assemble_document(

        self,

        json_file

    ):

        document = self.load_document(

            json_file

        )

        subjects = {

            "biology": [],

            "chemistry": [],

            "physics": []

        }

        current_subject = "biology"

        for page in document["pages"]:

            text = self.clean_text(

                page.get(

                    "text",

                    ""

                )

            )

            if not text:

                continue

            if self.is_answer_key(

                text

            ):

                continue

            current_subject = self.detect_subject(

                text,

                current_subject

            )

            subjects[current_subject].append(

                text

            )

        return {

            "biology": "\n\n".join(

                subjects["biology"]

            ),

            "chemistry": "\n\n".join(

                subjects["chemistry"]

            ),

            "physics": "\n\n".join(

                subjects["physics"]

            )

        }

    # --------------------------------------------------

    def chunk_text(

        self,

        text

    ):

        if not text.strip():

            return []

        paragraphs = text.split("\n\n")

        chunks = []

        current = ""

        for paragraph in paragraphs:

            if len(current) + len(paragraph) < self.max_chunk_size:

                current += paragraph + "\n\n"

            else:

                chunks.append(

                    current.strip()

                )

                current = paragraph + "\n\n"

        if current.strip():

            chunks.append(

                current.strip()

            )

        return chunks

    # --------------------------------------------------

        # --------------------------------------------------

    def prepare_document(

        self,

        json_file

    ):

        assembled = self.assemble_document(

            json_file

        )

        output = []

        chunk_index = 1

        for subject in [

            "biology",

            "chemistry",

            "physics"

        ]:

            chunks = self.chunk_text(

                assembled[subject]

            )

            for chunk in chunks:

                output.append(

                    {

                        "subject": subject.title(),

                        "page_number": 0,

                        "chunk_index": chunk_index,

                        "chunk_text": chunk,

                        "embedding_id": None

                    }

                )

                chunk_index += 1

        return output
    
        # --------------------------------------------------

    def process_all(self):

        json_files = sorted(

            self.extracted_folder.glob(

                "*.json"

            )

        )

        assembled_documents = []

        total_biology = 0
        total_chemistry = 0
        total_physics = 0

        print()
        print("=" * 70)
        print("DOCUMENT ASSEMBLER")
        print("=" * 70)

        for index, json_file in enumerate(

            json_files,

            start=1

        ):

            print(

                f"[{index}/{len(json_files)}] {json_file.name}"

            )

            document_chunks = self.prepare_document(
                json_file
            )

            biology_chunks = len(

                [

                    chunk

                    for chunk in document_chunks

                    if chunk["subject"] == "Biology"

                ]

            )

            chemistry_chunks = len(

                [

                    chunk

                    for chunk in document_chunks

                    if chunk["subject"] == "Chemistry"

                ]

            )

            physics_chunks = len(

                [

                    chunk

                    for chunk in document_chunks

                    if chunk["subject"] == "Physics"

                ]

            )

            total_biology += biology_chunks
            total_chemistry += chemistry_chunks
            total_physics += physics_chunks

            assembled_documents.append(

                {

                    "file_name": json_file.name,

                    "chunks": document_chunks

                }

            )

        print()
        print("=" * 70)
        print("ASSEMBLY SUMMARY")
        print("=" * 70)
        print(f"Documents          : {len(assembled_documents)}")
        print(f"Biology Chunks     : {total_biology}")
        print(f"Chemistry Chunks   : {total_chemistry}")
        print(f"Physics Chunks     : {total_physics}")
        print("=" * 70)

        return assembled_documents

    # --------------------------------------------------

    def statistics(self, assembled_documents):

        biology = 0
        chemistry = 0
        physics = 0

        for document in assembled_documents:

            biology += len(

                document["biology"]

            )

            chemistry += len(

                document["chemistry"]

            )

            physics += len(

                document["physics"]

            )

        return {

            "documents": len(assembled_documents),

            "biology_chunks": biology,

            "chemistry_chunks": chemistry,

            "physics_chunks": physics

        }


# =========================================================
# End of File
# =========================================================