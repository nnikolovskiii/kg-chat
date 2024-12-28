from yago_chat.databases.mongo_db import MongoEntry


class WikidataNode(MongoEntry):
    id: str
    concept_uri:str
    label: str
    description: str