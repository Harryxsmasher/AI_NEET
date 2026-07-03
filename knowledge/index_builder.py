"""
=========================================================
AI_NEET

Knowledge Index Builder

Author : Praveen Mark

Description
-----------
Builds the FAISS vector database from
all stored knowledge objects.

=========================================================
"""

from knowledge.knowledge_repository import KnowledgeRepository

from knowledge.embeddings import KnowledgeEmbeddingEngine

from vectordb.faiss_store import FAISSStore

class KnowledgeIndexBuilder:

    def __init__(self):

        self.repository = KnowledgeRepository()

        self.embedding_engine = KnowledgeEmbeddingEngine()

        self.vector_store = FAISSStore()

        self.vector_store.create_index()

        # --------------------------------------------------

    def build(self):

        print()

        print("=" * 70)
        print("KNOWLEDGE INDEX BUILDER")
        print("=" * 70)

        knowledge_objects = self.repository.get_all()

        print(

            f"Knowledge Objects : {len(knowledge_objects)}"

        )

        embedded = self.embedding_engine.embed_many(

            knowledge_objects

        )

        self.vector_store.add_many(

            embedded

        )

        self.vector_store.save()

        print()

        print("=" * 70)
        print("INDEX BUILD COMPLETE")
        print("=" * 70)

        print(

            f"Vectors : {len(embedded)}"

        )

        print("=" * 70)
    
    


