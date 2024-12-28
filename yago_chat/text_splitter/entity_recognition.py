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
    return f"""Given the question and entities below your job is to generate for each entity the relevant node in wikidata. Keep in mind the context of the question when generating.

Question:
{question}

Entities:
{",".join(entities)}

Return in json format: 
{{"nodes":[
    {{
        "entity_name": {{
            "wikidata_id": "",
            "wikidata_label": ""
        }}
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
) -> List[Dict[str, Dict[str, str]]]:
    template = guess_wikidata_template(
        question=question,
        entities=entities
    )
    response = await get_json_response(
        template,
        system_message="You are an helpful AI assistant."
    )
    print(response["nodes"])
    return response["nodes"]

async def _test():
    content = """How does the pathophysiology of Osteo porosis, characterized by reduced bone density and quality, contribute to its clinical manifestations, such as increased bone fragility and fracture risk, particularly in elderly individuals, and what are the implications for public health strategies aimed at prevention and management?"""
    entities = await entity_recognition(content=content)
    await guess_wikidata(
        question=content,
        entities=entities
    )

# asyncio.run(_test())