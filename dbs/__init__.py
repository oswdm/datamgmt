from enum import Enum

from .chromadb import Chroma
from .pgvector import PGVector
from .vespadb import VespaDB


class DBS(Enum):
    # chromadb = Chroma
    # pgvector = PGVector
    vespa = VespaDB
