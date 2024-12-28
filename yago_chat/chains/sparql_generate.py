from typing import List

from yago_chat.llms.generic_chat import generic_chat


def sparql_generate_template(
        question: str,
        wikidata_nodes: List[str]
):
    return f"""Question:
{question}

Wikidata Nodes:
{",".join(wikidata_nodes)}

Above is given a user question and nodes that were retrieved from Wikidata which are relevant to the question. 
Your job is to generate a SPARKQL query that is going to get information that will answer the user question.

Generated SPARQL query:
"""

async def sparql_generate(
        question: str,
        wikidata_nodes: List[str]
):
    template = sparql_generate_template(question=question, wikidata_nodes=wikidata_nodes)
    response = await generic_chat(
        template,
        system_message="You are an helpful AI assistant."
    )
    print(response)