import asyncio
from typing import List, Dict

from yago_chat.llms.json_response import get_json_response


def entity_recognition_template(
        content: str,
):
    return f"""Given the question below your job is to perform entity name recognition. Extract as many different entities as possible.

Question:
{content}

Return in json format: {{"entities"=["list all entities"]}}
"""


def guess_wikidata_template(
        question: str,
        entities: List[str]
):
    return f"""Given the question and entities below your job is to search wikidata and return all relevant nodes.

Question:
{question}

Entities:
{",".join(entities)}

Important: The search must be relevant to the question.

Return in json format: 
{{"nodes":[
    {{
        "wikidata_id": "",
        "wikidata_label": ""
    }}
]}}
"""


async def entity_recognition(
        content: str
) -> List[str]:
    template = entity_recognition_template(content=content)
    response = await get_json_response(
        template,
        system_message="You are an helpful AI assistant."
    )
    return response["entities"]


async def guess_wikidata(
        question: str,
        entities: List[str]
) -> List[Dict[str, str]]:
    template = guess_wikidata_template(
        question=question,
        entities=entities
    )
    response = await get_json_response(
        template,
        system_message="You are an helpful AI assistant, expert in Wikidata."
    )
    print(response["nodes"])
    return response["nodes"]

