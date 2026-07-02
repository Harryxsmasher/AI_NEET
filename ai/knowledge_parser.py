"""
=========================================================
AI_NEET

Knowledge Parser

Author : Praveen Mark

Description
-----------
Uses the Local AI model to convert
NCERT knowledge chunks into structured
educational knowledge.

=========================================================
"""

import json


class KnowledgeParser:

    def __init__(

        self,

        llm

    ):

        self.llm = llm

    # --------------------------------------------------

        # --------------------------------------------------

    def build_prompt(

        self,

        chunk

    ):

        return f"""
You are a JSON API.

Your job is to convert NCERT textbook text into JSON.

You MUST reply with ONLY valid JSON.

Do NOT write explanations.

Do NOT write markdown.

Do NOT write notes.

Do NOT write "Here is the JSON".

If you cannot determine a field,
use an empty string or empty list.

Required JSON Schema

{{
  "subject":"",
  "chapter":"",
  "topics":[],
  "keywords":[],
  "summary":""
}}

NCERT TEXT

{chunk}

Return ONLY JSON.


-----------------------


"""

    # --------------------------------------------------

    def extract_json(

        self,

        response

    ):

        start = response.find("{")

        end = response.rfind("}")

        if start == -1 or end == -1:

            return None

        try:

            return json.loads(

                response[start:end + 1]

            )

        except Exception:

            return None
        
        # --------------------------------------------------

    def validate(

        self,

        knowledge

    ):

        if knowledge is None:

            return False

        required = [

            "subject",

            "chapter",

            "topics",

            "keywords",

            "summary"

        ]

        for field in required:

            if field not in knowledge:

                return False

        return True

    # --------------------------------------------------

    def parse_chunk(

        self,

        chunk,

        retries=3

    ):

        prompt = self.build_prompt(

            chunk

        )

        for attempt in range(

            retries

        ):

            response = self.llm.generate(
                prompt
            )

            print()
            print("=" * 70)
            print("RAW LLM RESPONSE")
            print("=" * 70)
            print(response)
            print("=" * 70)

            knowledge = self.extract_json(

                response

            )

            print()

            if knowledge is None:

                print("JSON EXTRACTION FAILED")

            else:

                print("JSON EXTRACTED SUCCESSFULLY")

            if self.validate(

                knowledge

            ):

                return knowledge

        return None

    # --------------------------------------------------

    def parse_chunks(

        self,

        chunks

    ):

        parsed = []

        print()

        print("=" * 70)
        print("KNOWLEDGE EXTRACTION")
        print("=" * 70)

        total = len(chunks)

        for index, chunk in enumerate(

            chunks,

            start=1

        ):

            print(

                f"[{index}/{total}]"

            )

            knowledge = self.parse_chunk(

                chunk["chunk_text"]

            )

            if knowledge:

                chunk["knowledge"] = knowledge

                parsed.append(

                    chunk

                )

        print()

        print("=" * 70)
        print("KNOWLEDGE SUMMARY")
        print("=" * 70)
        print(f"Chunks Parsed : {len(parsed)}")
        print("=" * 70)

        return parsed
    
        # --------------------------------------------------

    def parse_document(

        self,

        document

    ):

        if "chunks" not in document:

            return []

        return self.parse_chunks(

            document["chunks"]

        )

    # --------------------------------------------------

    def parse_documents(

        self,

        documents

    ):

        knowledge_base = []

        print()

        print("=" * 70)
        print("KNOWLEDGE PARSER")
        print("=" * 70)

        total = len(documents)

        for index, document in enumerate(

            documents,

            start=1

        ):

            print(

                f"[{index}/{total}] "

                f"{document['file_name']}"

            )

            parsed = self.parse_document(

                document

            )

            knowledge_base.extend(

                parsed

            )

        print()

        print("=" * 70)
        print("KNOWLEDGE PARSER SUMMARY")
        print("=" * 70)
        print(
            f"Documents Parsed : {total}"
        )
        print(
            f"Knowledge Objects : {len(knowledge_base)}"
        )
        print("=" * 70)

        return knowledge_base

    # --------------------------------------------------

    def statistics(

        self,

        knowledge_objects

    ):

        statistics = {

            "chunks": len(

                knowledge_objects

            ),

            "biology": 0,

            "chemistry": 0,

            "physics": 0

        }

        for chunk in knowledge_objects:

            subject = chunk["knowledge"][

                "subject"

            ].lower()

            if subject in statistics:

                statistics[

                    subject

                ] += 1

        return statistics
    
        # --------------------------------------------------

    def print_summary(

        self,

        knowledge_objects

    ):

        summary = self.statistics(

            knowledge_objects

        )

        print()

        print("=" * 70)
        print("KNOWLEDGE EXTRACTION SUMMARY")
        print("=" * 70)

        print(
            f"Knowledge Objects : {summary['chunks']}"
        )

        print(
            f"Biology           : {summary['biology']}"
        )

        print(
            f"Chemistry         : {summary['chemistry']}"
        )

        print(
            f"Physics           : {summary['physics']}"
        )

        print("=" * 70)

    # --------------------------------------------------

    def process(

        self,

        documents

    ):

        if not documents:

            print()

            print("=" * 70)
            print("KNOWLEDGE PARSER")
            print("=" * 70)
            print("No documents available.")
            print("=" * 70)

            return []

        knowledge_objects = self.parse_documents(

            documents

        )

        self.print_summary(

            knowledge_objects

        )

        return knowledge_objects


# =========================================================
# End of File
# =========================================================