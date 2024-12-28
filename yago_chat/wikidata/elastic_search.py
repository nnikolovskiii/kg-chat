import asyncio

import requests

from yago_chat.text_splitter.entity_recognition import entity_recognition, guess_wikidata


def entity_elastic_search(
        entity: str
):
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
        for elem in response_json["search"]:
            print(elem)
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

    for entity_dict in wikidata_dict:
        entity = list(entity_dict.keys())[0]
        wikidata_entity = entity_dict[entity]["wikidata_label"]

        print("==============")
        print(entity, wikidata_entity)
        print("==============")
        entity_elastic_search(entity=wikidata_entity)
        print()

asyncio.run(elastic_search_workflow(question="""How does the pathophysiology of Osteo porosis, characterized by reduced bone density and quality, contribute to its clinical manifestations, such as increased bone fragility and fracture risk, particularly in elderly individuals, and what are the implications for public health strategies aimed at prevention and management?"""))