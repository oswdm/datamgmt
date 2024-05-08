from enum import Enum

from .chromadb import Chroma
from .pgvector import PGVector


class DBS(Enum):
    chromadb = Chroma
    pgvector = PGVector
