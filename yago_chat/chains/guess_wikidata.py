import asyncio
from typing import List, Dict, Tuple

from yago_chat.llms.generic_chat import generic_chat
from yago_chat.llms.json_response import get_json_response
from yago_chat.models.wikidata_node import WikidataNode
from yago_chat.wikidata_api.elastic_search import entity_elastic_search


def guess_wikidata_template(
        context: str,
):
    return f"""Given the user context below your job is to search wikidata_api and return all relevant nodes which are connected to the context.

User context:
{context}

Important: The search must be relevant to the question.

Return in json format: 
{{"nodes":[
    {{
        "wikidata_id": "",
        "wikidata_label": ""
    }}
]}}
"""

async def elastic_search_workflow(
        question: str,
        wikidata_dict: List[Dict[str, str]]
)->List[WikidataNode]:
    wikidata_nodes_li:List[WikidataNode] = []

    for entity_dict in wikidata_dict:
        wikidata_entity = entity_dict["wikidata_label"]
        wikidata_nodes = entity_elastic_search(entity=wikidata_entity)
        wikidata_nodes_li.extend(wikidata_nodes)

    return wikidata_nodes_li


async def guess_wikidata(
        raw_response: str,
        question: str,
)->List[WikidataNode]:
    template = guess_wikidata_template(
        context=raw_response,
    )
    wikidata_response = await get_json_response(
        template,
        system_message="You are an helpful AI assistant, expert in Wikidata."
    )

    wikidata_nodes = await elastic_search_workflow(question=question, wikidata_dict=wikidata_response["nodes"])
    return wikidata_nodes
