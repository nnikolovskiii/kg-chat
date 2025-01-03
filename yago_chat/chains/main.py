import asyncio

from yago_chat.chains.guess_wikidata import guess_wikidata
from yago_chat.llms.generic_chat import generic_chat
from yago_chat.wikidata_api.sparkql import get_wikidata_url


async def main_flow(
        question:str
)->str:
    raw_response = await generic_chat(message=question, system_message="You are an helpful AI assistant.")
    print(raw_response)
    wikidata_nodes = await guess_wikidata(
        question=question,
        raw_response=raw_response
    )

    links = []
    for wikidata_node in wikidata_nodes:
        print(wikidata_node)
        link = get_wikidata_url(wikidata_label=wikidata_node.id)
        links.append(link)

    print(links)

    return ""

asyncio.run(main_flow("What did Einstein contribute in the field of physics?"))
