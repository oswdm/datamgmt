from helpers.dp_connector import DBConector
from helpers.data_processor import DocumentProcessor, Document

import chromadb


class Chroma(DBConector):
    def __init__(self) -> None:
        super().__init__()
        self.client = chromadb.HttpClient(host="localhost", port=8000)
        self.collection = self.client.get_or_create_collection(name="bench")

    def insert_document(self, doc: Document):
        self.collection.add(ids=doc.id, embeddings=doc.emb, documents=doc.text)

    def remove_document(self, id: str):
        self.collection.delete(ids=id)

    def query_db(self, doc: Document, n_results: int):
        return self.collection.query(query_embeddings=doc.emb, n_results=n_results)
