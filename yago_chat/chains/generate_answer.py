from typing import List

from yago_chat.llms.generic_chat import generic_chat


def generate_answer_template(
        context: str,
        question: str
):
    return f"""<Wikipedia Context>
{context}
</Wikipedia Context>

Question: {question}

Above is given a user question and relevant wikipedia context. Your job is to generate an answer to the question that is factually based on the given context.

Your answer:
"""

async def generate_answer(
        question: str,
        context:str
)->str:
    template = generate_answer_template(question=question, context=context)
    response = await generic_chat(
        template,
        system_message="You are an helpful AI assistant."
    )
    return response