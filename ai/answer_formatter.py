"""
=========================================================
AI_NEET

Answer Formatter

Author : Praveen Mark

Description
-----------
Formats AI responses for display.

=========================================================
"""


class AnswerFormatter:

    def __init__(self):

        pass

    # --------------------------------------------------

    def format(

        self,

        question,

        answer,

        graph_data=None,

        pyq_data=None

    ):

        output = []

        output.append("=" * 70)
        output.append("AI_NEET TUTOR")
        output.append("=" * 70)

        output.append("")
        output.append("QUESTION")
        output.append("-" * 70)
        output.append(question)

        output.append("")
        output.append("ANSWER")
        output.append("-" * 70)
        output.append(answer)

        if graph_data:

            output.append("")
            output.append("RELATED CONCEPTS")
            output.append("-" * 70)

            output.append(

                str(graph_data)

            )

        if pyq_data:

            output.append("")
            output.append("PYQ ANALYSIS")
            output.append("-" * 70)

            output.append(

                str(pyq_data)

            )

        output.append("")
        output.append("=" * 70)

        return "\n".join(output)