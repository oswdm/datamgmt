from helpers.dp_connector import DBConector
from helpers.data_processor import Document

import psycopg2
from pgvector.psycopg2 import register_vector


SQL_COMMANDS = [
    """
        CREATE EXTENSION IF NOT EXISTS vector;
    """,
    """
    CREATE TABLE documents (
        id VARCHAR(64) PRIMARY KEY,
        content TEXT NOT NULL,
        embedding vector(384) NOT NULL
    );
    """,
]


class PGVector(DBConector):
    def __init__(self) -> None:
        super().__init__()
        self.conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
        )

        with self.conn.cursor() as cur:
            # extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.conn.commit()
            register_vector(self.conn)
            # table
            cur.execute("""
                CREATE TABLE documents (
                    id VARCHAR(64) PRIMARY KEY,
                    content TEXT NOT NULL,
                    embedding vector(384) NOT NULL
                );
                """)

    def insert_document(self, doc: Document):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO documents (id, content, embedding) VALUES (%s, %s, %s);",
                (doc.id, doc.text, doc.emb),
            )
            self.conn.commit()

    def remove_document(self, id: str):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE id = %s;", (id,))
            self.conn.commit()

    def query_db(self, doc: Document, n_results: int):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM documents ORDER BY embedding <=> %s::vector LIMIT %s",
                (doc.emb, n_results),
            )
            res = cur.fetchall()
            return res
