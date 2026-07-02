"""
=========================================================
AI_NEET

Document Registry

Author : Praveen Mark

Description
-----------
Registers every document inside AI_NEET.

Every document receives a permanent ID and
stores metadata required by all AI pipelines.

=========================================================
"""


from pathlib import Path


class DocumentRegistry:

    def __init__(self):

        self.documents = {}

    # --------------------------------------------------

    def create_document(

        self,

        file_name,

        page_count=0

    ):

        metadata = self.extract_metadata(

            file_name

        )

        document = {

            "document_id":

                self.generate_document_id(),

            "file_name":

                file_name,

            "file_stem":

                Path(file_name).stem,

            "source_type":

                metadata["source_type"],

            "subject":

                metadata["subject"],

            "class":

                metadata["class"],

            "chapter":

                metadata["chapter"],

            "exam_year":

                metadata["exam_year"],

            "page_count":

                page_count,

            "chunk_count":

                0,

            "question_count":

                0,

            "embedding_count":

                0,

            "ocr_completed":

                False,

            "ai_completed":

                False,

            "embedding_completed":

                False,

            "status":

                "REGISTERED"

        }

        self.documents[

            document["document_id"]

        ] = document

        return document

    # --------------------------------------------------

    def generate_document_id(self):

        return f"DOC-{len(self.documents)+1:06d}"

    # --------------------------------------------------

    def extract_metadata(

        self,

        file_name

    ):

        name = Path(

            file_name

        ).stem.lower()

        metadata = {

            "source_type": "UNKNOWN",

            "subject": "Unknown",

            "class": None,

            "chapter": None,

            "exam_year": None

        }

        # -----------------------------
        # Previous Papers
        # -----------------------------

        if name.startswith("neet_"):

            metadata["source_type"] = "NEET"

            try:

                metadata["exam_year"] = int(

                    name.split("_")[1]

                )

            except Exception:

                pass

            return metadata
        
                # -----------------------------
        # NCERT BIOLOGY
        # -----------------------------

        if name.startswith("kebo"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Biology"
            metadata["class"] = 11
            return metadata

        if name.startswith("lebo"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Biology"
            metadata["class"] = 12
            return metadata

        # -----------------------------
        # NCERT CHEMISTRY
        # -----------------------------

        if name.startswith("kech"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Chemistry"
            metadata["class"] = 11
            return metadata

        if name.startswith("lech"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Chemistry"
            metadata["class"] = 12
            return metadata

        # -----------------------------
        # NCERT PHYSICS
        # -----------------------------

        if name.startswith("keph"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Physics"
            metadata["class"] = 11
            return metadata

        if name.startswith("leph"):

            metadata["source_type"] = "NCERT"
            metadata["subject"] = "Physics"
            metadata["class"] = 12
            return metadata

        return metadata

    # --------------------------------------------------

    def register_documents(

        self,

        documents

    ):

        registered = []

        print()
        print("=" * 70)
        print("DOCUMENT REGISTRY")
        print("=" * 70)

        for index, document in enumerate(

            documents,

            start=1

        ):

            entry = self.create_document(

                file_name=document["file_name"],

                page_count=document.get(

                    "page_count",

                    0

                )

            )

            registered.append(

                entry

            )

            print(

                f"[{index:03d}] "

                f"{entry['document_id']} "

                f"{entry['file_name']}"

            )

        print()
        print("=" * 70)
        print(f"Registered : {len(registered)}")
        print("=" * 70)

        return registered
    
        # --------------------------------------------------

    def update_status(

        self,

        document_id,

        status

    ):

        if document_id in self.documents:

            self.documents[

                document_id

            ]["status"] = status

    # --------------------------------------------------

    def update_counts(

        self,

        document_id,

        chunks=0,

        questions=0,

        embeddings=0

    ):

        if document_id not in self.documents:

            return

        document = self.documents[

            document_id

        ]

        document["chunk_count"] = chunks

        document["question_count"] = questions

        document["embedding_count"] = embeddings

    # --------------------------------------------------

    def get_document(

        self,

        document_id

    ):

        return self.documents.get(

            document_id

        )

    # --------------------------------------------------

    def get_all_documents(

        self

    ):

        return list(

            self.documents.values()

        )

    # --------------------------------------------------

    def filter_by_source(

        self,

        source_type

    ):

        return [

            document

            for document in self.documents.values()

            if document["source_type"] == source_type

        ]

    # --------------------------------------------------

    def filter_by_subject(

        self,

        subject

    ):

        return [

            document

            for document in self.documents.values()

            if document["subject"] == subject

        ]

    # --------------------------------------------------

    def filter_by_year(

        self,

        year

    ):

        return [

            document

            for document in self.documents.values()

            if document["exam_year"] == year

        ]

    # --------------------------------------------------

    def statistics(

        self

    ):

        statistics = {

            "documents": len(

                self.documents

            ),

            "ncert": 0,

            "neet": 0,

            "biology": 0,

            "chemistry": 0,

            "physics": 0

        }

        for document in self.documents.values():

            if document["source_type"] == "NCERT":

                statistics["ncert"] += 1

            elif document["source_type"] == "NEET":

                statistics["neet"] += 1

            subject = document["subject"].lower()

            if subject in statistics:

                statistics[subject] += 1

        return statistics

    # --------------------------------------------------

    def print_summary(

        self

    ):

        summary = self.statistics()

        print()

        print("=" * 70)
        print("DOCUMENT REGISTRY SUMMARY")
        print("=" * 70)

        print(f"Documents  : {summary['documents']}")
        print(f"NCERT      : {summary['ncert']}")
        print(f"NEET       : {summary['neet']}")
        print(f"Biology    : {summary['biology']}")
        print(f"Chemistry  : {summary['chemistry']}")
        print(f"Physics    : {summary['physics']}")

        print("=" * 70)


# =========================================================
# End of File
# =========================================================
    