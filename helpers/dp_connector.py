from typing import Any
from helpers.data_processor import Document
from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------
# connector class
# --------------------------------------------------------------------------------------


class DBConector(ABC):
    @abstractmethod
    def insert_document(self, doc: Document) -> None:
        pass

    @abstractmethod
    def remove_document(self, id: str) -> None:
        pass

    @abstractmethod
    def query_db(self, doc: Document, n_results: int) -> Any:
        pass
