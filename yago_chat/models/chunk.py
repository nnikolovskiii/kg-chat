from yago_chat.databases.mongo_db import MongoEntry


class WikipediaChunk(MongoEntry):
    content: str
    url: str
    order: int