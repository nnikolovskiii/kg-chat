import asyncio
from typing import List

import requests

from yago_chat.chains.sparql_generate import sparql_generate
from yago_chat.models.wikidata_node import WikidataNode
from yago_chat.chains.entity_recognition import entity_recognition, guess_wikidata


def entity_elastic_search(
        entity: str
)-> List[WikidataNode]:
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": entity,
        "language": "en",
        "type": "item",
        "format": "json",
        "limit": 5
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response_json = response.json()
        wikidata_nodes = []

        for elem in response_json["search"]:
            if "id" in elem and "label" in elem and "description" in elem and "concepturi" in elem:
                wikidata_node_arg = {
                    "id": elem["id"],
                    "label": elem["label"],
                    "description": elem["description"],
                    "concept_uri": elem["concepturi"]
                }
                wikidata_nodes.append(WikidataNode(**wikidata_node_arg))
        return wikidata_nodes
    else:
        print(f"Request failed with status code: {response.status_code}")


async def elastic_search_workflow(
        question: str,
):
    entities = await entity_recognition(content=question)
    wikidata_dict = await guess_wikidata(
        question=question,
        entities=entities
    )

    wikidata_nodes_li = []

    for entity_dict in wikidata_dict:
        wikidata_entity = entity_dict["wikidata_label"]
        wikidata_nodes = entity_elastic_search(entity=wikidata_entity)
        wikidata_nodes_li.extend(wikidata_nodes)

    await sparql_generate(question=question, wikidata_nodes=[str(elem) for elem in wikidata_nodes_li])

asyncio.run(elastic_search_workflow(question="""How does the pathophysiology of Osteo porosis, characterized by reduced bone density and quality, contribute to its clinical manifestations, such as increased bone fragility and fracture risk, particularly in elderly individuals, and what are the implications for public health strategies aimed at prevention and management?"""))