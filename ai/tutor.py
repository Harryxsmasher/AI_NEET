"""
=========================================================
AI_NEET

AI Tutor

Author : Praveen Mark

Description
-----------
Main AI Tutor.

Coordinates

✓ Retriever
✓ Knowledge Graph
✓ PYQ Analyzer
✓ Prompt Builder
✓ Local LLM
✓ Answer Formatter

=========================================================
"""

from ai.prompt_builder import PromptBuilder
from ai.answer_formatter import AnswerFormatter

class Tutor:

    def __init__(

        self,

        retriever,

        knowledge_graph,

        pyq_analyzer,

        llm

    ):

        self.retriever = retriever

        self.knowledge_graph = knowledge_graph

        self.pyq_analyzer = pyq_analyzer

        self.llm = llm

        self.prompt_builder = PromptBuilder()

        self.answer_formatter = AnswerFormatter()
    

        # --------------------------------------------------

    def ask(

        self,

        question

    ):

        print()

        print("=" * 70)
        print("AI TUTOR")
        print("=" * 70)

        knowledge = self.retriever.retrieve(

            question

        )

        graph_data = None

        pyq_data = None

        prompt = self.prompt_builder.build(

            question,

            knowledge,

            graph_data,

            pyq_data

    )
        
        answer = self.llm.generate(

            prompt

    )
        

        result = self.answer_formatter.format(

            question,

            answer,

            graph_data,

            pyq_data

        )

        return result
        






    
