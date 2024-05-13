import os

import yaml
import tempfile

from helpers.dp_connector import DBConector
from helpers.data_processor import DocumentProcessor, Document

from vespa.package import ApplicationPackage
from vespa.package import Field, FieldSet, RankProfile
from vespa.application import Vespa
from vespa.io import VespaQueryResponse
from vespa.exceptions import VespaError
from vespa.deployment import VespaDocker



class VespaDB(DBConector):
    def __init__(self) -> None:
        super().__init__()
        self.init()
        self.app = Vespa(url="http://localhost:8080")

    def init(self):
        app_name = "bench"
        app_package = ApplicationPackage(name=app_name, create_query_profile_by_default=False)

        temp_dir = tempfile.TemporaryDirectory()
        app_package.to_files(temp_dir.name)

        os.environ["TMP_APP_DIR"] = temp_dir.name
        os.environ["APP_NAME"] = app_name

        app_package.schema.add_fields(
            Field(name="id", type="string", indexing=["index"]),
            Field(
                name="text", type="string", indexing=["index", "summary"]
            ),
            Field(
                name="embedding", type="tensor<float>(d0[384])", indexing=["index", "summary"]
            ),
        )
        app_package.schema.add_field_set(FieldSet(name="default", fields=["id", "text", "embedding"]))
        app_package.schema.add_rank_profile(
            RankProfile(name="cosine", first_phase="cos(distance(field, embedding))", inputs=[('query(q_embedding)', 'tensor(d0[384])')])
        )

        app_package.to_files(temp_dir.name)

        self.vespa_container = VespaDocker()
        self.vespa_connection = self.vespa_container.deploy(application_package=app_package)

    def cleanup(self):
        self.temp_dir.cleanup()
        self.vespa_container.container.stop()
        self.vespa_container.container.remove()

    def insert_document(self, doc: Document):
        self.app.feed_data_point(schema="bench", data_id=doc.id, fields={
            'id': doc.id,
            'text': doc.text,
            'embedding': doc.emb
        })

    def remove_document(self, id: str):
        self.app.delete_data(schema="bench", data_id=id)

    def query_db(self, doc: Document, n_results: int):

        with self.app.syncio() as session:
            response: VespaQueryResponse = session.query(
                yql="select * from bench where ({targetHits:100}nearestNeighbor(embedding,q_embedding)) limit " + str(n_results),
                ranking="cosine",
                body={"input.query(q_embedding)": doc.emb},
            )

            results = map(lambda x: {'id': x['fields']['id'], 'id': x['fields']['id'], 'relevance': x['relevance']},response.json['root']['children'])

        return results
