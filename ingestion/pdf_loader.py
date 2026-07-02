"""
=========================================================
AI_NEET

PDF Loader

Author : Praveen Mark

Description
-----------
Scans every PDF inside the data directory,
collects metadata and returns structured
Document objects.

=========================================================
"""

from pathlib import Path
import fitz


class PDFLoader:
    """
    PDF Loader

    Responsibilities
    ----------------
    - Scan PDF files
    - Read metadata
    - Count pages
    - Classify document
    """

    def __init__(self, root_folder: str = "data"):

        self.root = Path(root_folder)

        self.documents = []

    # --------------------------------------------------

    def scan(self):

        self.documents.clear()

        pdf_files = sorted(self.root.rglob("*.pdf"))

        for pdf in pdf_files:

            document = self._load_document(pdf)

            self.documents.append(document)

        return self.documents

    # --------------------------------------------------

    def _load_document(self, pdf_path: Path):

        pdf = fitz.open(pdf_path)

        metadata = pdf.metadata

        info = {

            "title": metadata.get("title") or pdf_path.stem,

            "author": metadata.get("author", ""),

            "subject": self._detect_subject(pdf_path),

            "class_level": self._detect_class(pdf_path),

            "source_type": self._detect_source(pdf_path),

            "file_name": pdf_path.name,

            "file_path": str(pdf_path.resolve()),

            "page_count": pdf.page_count,

            "processed": False

        }

        pdf.close()

        return info

    # --------------------------------------------------

    def _detect_subject(self, path: Path):

        text = str(path).lower()

        if "biology" in text:
            return "Biology"

        if "physics" in text:
            return "Physics"

        if "chemistry" in text:
            return "Chemistry"

        return "Unknown"

    # --------------------------------------------------

    def _detect_class(self, path: Path):

        text = str(path).lower()

        if "class11" in text:
            return "11"

        if "class12" in text:
            return "12"

        return ""

    # --------------------------------------------------

    def _detect_source(self, path: Path):

        text = str(path).lower()

        if "previous_papers" in text:
            return "Previous Paper"

        return "NCERT"
    
        # --------------------------------------------------

    def summary(self):

        summary = {
            "Biology": {"11": 0, "12": 0},
            "Physics": {"11": 0, "12": 0},
            "Chemistry": {"11": 0, "12": 0},
            "Previous Paper": 0,
            "Total PDFs": 0,
            "Total Pages": 0
        }

        for document in self.documents:

            summary["Total PDFs"] += 1
            summary["Total Pages"] += document["page_count"]

            if document["source_type"] == "Previous Paper":

                summary["Previous Paper"] += 1
                continue

            subject = document["subject"]
            class_level = document["class_level"]

            if (
                subject in summary
                and class_level in summary[subject]
            ):
                summary[subject][class_level] += 1

        print()

        print("=" * 70)
        print("DOCUMENT SCAN SUMMARY")
        print("=" * 70)

        for subject in ["Biology", "Physics", "Chemistry"]:

            total = (
                summary[subject]["11"]
                + summary[subject]["12"]
            )

            print(subject)

            print(
                f"   Class 11 : {summary[subject]['11']}"
            )

            print(
                f"   Class 12 : {summary[subject]['12']}"
            )

            print(
                f"   Total    : {total}"
            )

            print()

        print(
            f"Previous Papers : {summary['Previous Paper']}"
        )

        print("-" * 70)

        print(
            f"Total PDFs  : {summary['Total PDFs']}"
        )

        print(
            f"Total Pages : {summary['Total Pages']}"
        )

        print("=" * 70)

        return summary

    # --------------------------------------------------

    def get_documents(self):

        return self.documents

    # --------------------------------------------------

    def print_documents(self):

        print()

        print("=" * 70)
        print("DOCUMENT LIST")
        print("=" * 70)

        for index, document in enumerate(
            self.documents,
            start=1
        ):

            print(
                f"{index:03d}. "
                f"{document['subject']:10} "
                f"Class {document['class_level']:2} "
                f"{document['page_count']:4} Pages "
                f"{document['file_name']}"
            )

        print("=" * 70)

    # --------------------------------------------------

    def __len__(self):

        return len(self.documents)