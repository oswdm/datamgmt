from enum import Enum

from .chromadb import Chroma
from .pgvector import PGVector
from .qdrant import Qdrant

class DBS(Enum):
    chromadb = Chroma
    pgvector = PGVector
    qdrant = Qdrant
