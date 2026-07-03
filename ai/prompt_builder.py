"""
=========================================================
AI_NEET

Prompt Builder

Author : Praveen Mark

Description
-----------
Builds optimized prompts for the
local AI Tutor.

=========================================================
"""


class PromptBuilder:

    def __init__(self):

        pass

    # --------------------------------------------------

    def build(

        self,

        question,

        knowledge_objects,

        graph_data=None,

        pyq_data=None

    ):

        knowledge_text = ""

        for index, item in enumerate(

            knowledge_objects,

            start=1

        ):

            knowledge_text += (

                f"\nKnowledge {index}\n"

                f"Subject : {item['subject']}\n"

                f"Chapter : {item['chapter']}\n"

                f"Summary : {item['summary']}\n"

            )

        graph_text = ""

        if graph_data:

            graph_text = str(

                graph_data

            )

        pyq_text = ""

        if pyq_data:

            pyq_text = str(

                pyq_data

            )

        prompt = f"""
You are AI_NEET.

You are an expert NEET tutor.

Answer ONLY using the supplied NCERT knowledge.

If the answer cannot be found,
say

"I couldn't find enough information
inside the current knowledge base."

--------------------------------------------

Student Question

{question}

--------------------------------------------

Knowledge Base

{knowledge_text}

--------------------------------------------

Related Concepts

{graph_text}

--------------------------------------------

Previous Year Analysis

{pyq_text}

--------------------------------------------

Instructions

1. Explain in simple English.

2. Do not invent facts.

3. Mention important keywords.

4. Keep the answer educational.

5. Mention related concepts if available.

6. Mention PYQ importance if available.

"""

        return prompt