"""
=========================================================
AI_NEET

Knowledge Embedding Engine

Author : Praveen Mark

Description
-----------
Converts structured knowledge into
vector embeddings.

Supports

✓ Sentence Transformers
✓ Local Embeddings
✓ Offline Processing

=========================================================
"""

from sentence_transformers import SentenceTransformer

from core.config import ConfigManager

class KnowledgeEmbeddingEngine:

    def __init__(self):

        self.config = ConfigManager()

        self.model_name = self.config.get(
            "embedding.model"
        )

        print()

        print("=" * 70)
        print("KNOWLEDGE EMBEDDING ENGINE")
        print("=" * 70)
        print(f"Model : {self.model_name}")
        print("=" * 70)

        self.model = SentenceTransformer(
            self.model_name
        )

        # --------------------------------------------------

    def build_text(

        self,

        knowledge

    ):

        topics = ", ".join(

            knowledge.get(

                "topics",

                []

            )

        )

        keywords = ", ".join(

            knowledge.get(

                "keywords",

                []

            )

        )

        text = f"""

Subject:
{knowledge.get("subject", "")}

Chapter:
{knowledge.get("chapter", "")}

Topics:
{topics}

Keywords:
{keywords}

Summary:
{knowledge.get("summary", "")}

"""

        return text.strip()
    

        # --------------------------------------------------

    def embed(

        self,

        text

    ):

        vector = self.model.encode(

            text,

            convert_to_numpy=True,

            normalize_embeddings=True

        )

        return vector
    
        # --------------------------------------------------

    def embed_knowledge(

        self,

        knowledge

    ):

        text = self.build_text(

            knowledge

        )

        vector = self.embed(

            text

        )

        return {

            "knowledge": knowledge,

            "text": text,

            "vector": vector

        }
    
        # --------------------------------------------------

    def embed_many(

        self,

        knowledge_objects

    ):

        embedded = []

        print()

        print("=" * 70)
        print("GENERATING EMBEDDINGS")
        print("=" * 70)

        total = len(

            knowledge_objects

        )

        for index, knowledge in enumerate(

            knowledge_objects,

            start=1

        ):

            print(

                f"[{index}/{total}]"

            )

            embedded.append(

                self.embed_knowledge(

                    knowledge

                )

            )

        print()

        print("=" * 70)
        print("EMBEDDING SUMMARY")
        print("=" * 70)

        print(

            f"Vectors Generated : {len(embedded)}"

        )

        print("=" * 70)

        return embedded
    
    