import asyncio
import os
from langchain_text_splitters.character import RecursiveCharacterTextSplitter

from yago_chat.databases.mongo_db import MongoDBDatabase


def _read_file(file_path) -> str | None:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


async def chunk_file(file_path: str, mdb: MongoDBDatabase):
    content = _read_file(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " "]
    )

    chunks = text_splitter.split_text(content)
    print(chunks)
    print(len(chunks))
    return chunks


asyncio.run(chunk_file(file_path="/home/nnikolovskii/test.txt", mdb=MongoDBDatabase()))