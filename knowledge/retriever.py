"""
=========================================================
AI_NEET

Knowledge Retriever

Author : Praveen Mark

Description
-----------
Performs semantic retrieval from the
FAISS vector database.

=========================================================
"""

import numpy as np

from knowledge.embeddings import KnowledgeEmbeddingEngine
from vectordb.faiss_store import FAISSStore

class KnowledgeRetriever:

    def __init__(self):

        self.embedding_engine = KnowledgeEmbeddingEngine()

        self.vector_store = FAISSStore()

        self.vector_store.load()

        # --------------------------------------------------

    def build_query_vector(

        self,

        question

    ):

        return self.embedding_engine.embed(

            question

        )
    
        # --------------------------------------------------

    def retrieve(

        self,

        question,

        top_k=5

    ):

        vector = self.build_query_vector(

            question

        )

        return self.vector_store.search(

            vector,

            top_k

        )
    
    

