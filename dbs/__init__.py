from enum import Enum

from .chromadb import Chroma
from .pgvector import PGVector
from .vespadb import VespaDB
from .qdrant import Qdrant

class DBS(Enum):
    chromadb = Chroma
    pgvector = PGVector
    vespa = VespaDB
    qdrant = Qdrant
