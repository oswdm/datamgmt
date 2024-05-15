from helpers.dp_connector import DBConector
from helpers.data_processor import Document

from pymilvus import MilvusClient, FieldSchema, CollectionSchema, DataType

class Milvus(DBConector):
    collection_name = "perftest"

    def __init__(self) -> None:
        super().__init__()
        # Connect to Milvus database
        self.client = MilvusClient(db_name="default", host="localhost", port="19530")
        
        # Prepare database schema(collection) for performance test with amazon books dataset
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=256, is_primary=True, auto_id=False),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=384)
        ]
        schema = CollectionSchema(fields=fields, auto_id=False, enable_dynamic_field=False, description="Schema for DB-Benchmark | TSM_DataMgmt")
        
        # Prepare index for embeddings with cosine distance
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="embeddings",
            index_type="IVF_FLAT",
            metric_type="COSINE",
            params={"nlist": 128}
        )

        # create collection with index
        self.client.create_collection(collection_name=self.collection_name, schema=schema, index_params=index_params)
        self.client.load_collection(collection_name=self.collection_name)

    def insert_document(self, doc: Document):
        self.client.insert(
            collection_name=self.collection_name, 
            data=[{"id": doc.id, "content": doc.text, "embeddings": doc.emb}]
        )

    def remove_document(self, id: str):
        self.client.delete(
            collection_name=self.collection_name,
            ids=[id]
        )

    def query_db(self, doc: Document, n_results: int):
        return self.client.search(
            collection_name=self.collection_name,
            data=[doc.emb],
            limit=n_results,
            search_params={"metric_type": "COSINE", "params": {}}
        )
