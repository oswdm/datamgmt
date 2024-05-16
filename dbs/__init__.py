from enum import Enum

from .chromadb import Chroma
from .pgvector import PGVector
from .vespadb import VespaDB
from .milvus import Milvus
from .qdrant import Qdrant

class DBS(Enum):
    chromadb = Chroma
    pgvector = PGVector
    vespa = VespaDB
    milvus = Milvus
    qdrant = Qdrant
