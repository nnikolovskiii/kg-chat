import asyncio

from yago_chat.chains.guess_wikidata import guess_wikidata
from yago_chat.databases.singletons import get_qdrant_db
from yago_chat.llms.generic_chat import generic_chat
from yago_chat.models.chunk import WikipediaChunk
from yago_chat.models.markdown_splitter import MarkdownTextSplitter
from yago_chat.wikidata_api.sparkql import get_wikidata_url
from yago_chat.wikidata_api.wikipedia import get_wikipedia_page_markdown


async def main_flow(
        question:str
)->str:
    qdb = await get_qdrant_db()

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

    text_splitter = MarkdownTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )

    for link in links:
        wikipedia_content = await get_wikipedia_page_markdown(url=link)
        chunks = text_splitter.split_text(text=wikipedia_content)

        for i,chunk in enumerate(chunks):
            chunk_obj = WikipediaChunk(
                content=chunk,
                url=link,
                order=i
            )
            await qdb.embedd_and_upsert_record(
                value=chunk_obj.content,
                entity=chunk_obj,
            )

    print(links)
    return ""

asyncio.run(main_flow("What did Einstein contribute in the field of physics?"))
