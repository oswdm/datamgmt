from enum import Enum

from .chromadb import Chroma


class DBS(Enum):
    chromadb = Chroma
