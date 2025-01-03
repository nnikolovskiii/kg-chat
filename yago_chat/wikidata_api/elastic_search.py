from typing import List

import requests

from yago_chat.models.wikidata_node import WikidataNode



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
        "limit": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        response_json = response.json()
        wikidata_nodes = []

        for elem in response_json["search"]:
            if "id" in elem and "label" in elem and "description" in elem and "concepturi" in elem:
                print(elem)
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
