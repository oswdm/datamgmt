from helpers.dp_connector import DBConector
from helpers.data_processor import DocumentProcessor, Document

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, PointIdsList


class Qdrant(DBConector):
    def __init__(self) -> None:
        super().__init__()
        self.client = QdrantClient(host="localhost", port=6333)
        self.client.recreate_collection(
            collection_name="my_collection",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE))

    def insert_document(self, doc: Document) -> None:
        self.client.upsert(
            collection_name="my_collection",
            points=[
                PointStruct(
                    id=doc.id,
                    vector=doc.emb,
                    payload={
                        "text": doc.text
                    })
            ]
        )

    def remove_document(self, id: str) -> None:
        self.client.delete(
            collection_name="my_collection",
            points_selector=PointIdsList(
                points=[id],
            ),
        )

    def query_db(self, doc: Document, n_results: int):
        return self.client.search(
            collection_name="my_collection",
            query_vector=doc.emb,
            limit=n_results
        )
