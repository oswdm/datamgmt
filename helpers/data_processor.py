import json
import multiprocessing
import uuid
from typing import List
from time import sleep

from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# --------------------------------------------------------------------------------------
# pydantic schema
# --------------------------------------------------------------------------------------


class Document(BaseModel):
    id: str
    text: str
    emb: List[float]


# --------------------------------------------------------------------------------------
# parser func
# --------------------------------------------------------------------------------------


def parse_line(model, line: str):
    obj = json.loads(line)
    uid = str(uuid.uuid4())
    emb = model.encode(obj["reviewText"]).tolist()
    doc = Document(id=uid, text=obj["reviewText"], emb=emb)
    return doc


# --------------------------------------------------------------------------------------
# processor
# --------------------------------------------------------------------------------------


class DocumentProcessor:
    def __init__(
        self,
        file_path: str,
        model="sentence-transformers/all-MiniLM-L6-v2",
        multiprocess=False,
    ) -> None:
        self.file_path = file_path
        self.multiprocess = multiprocess
        self.model = model

        # setup
        self._setup()

    def _parse_mp(self):
        model = SentenceTransformer(self.model)
        with open(self.file_path, "r") as f:
            while line := f.readline():
                # check stop event
                if self.stop_event.is_set():
                    self.queue.close()
                    return
                # deserialize and queue
                doc = parse_line(model, line)
                self.queue.put(doc)
        # none as end marker
        self.queue.put(None)

    def _parse_sp(self):
        model = SentenceTransformer(self.model)
        with open(self.file_path, "r") as f:
            while line := f.readline():
                # deserialize and yield
                doc = parse_line(model, line)
                yield doc

    def _setup(self):
        if self.multiprocess:
            self.queue = multiprocessing.Queue(maxsize=1_000)
            self.pars_proc = None
            self.stop_event = multiprocessing.Event()
        else:
            self.pars_gen = self._parse_sp()

    def start_parser(self):
        if self.multiprocess and not self.pars_proc:
            self.pars_proc = multiprocessing.Process(target=self._parse_mp)
            self.pars_proc.daemon = True
            self.pars_proc.start()

    def fill_queue(self):
        if self.multiprocess and self.pars_proc and self.pars_proc.is_alive():
            while not self.queue.full():
                sleep(1)

    def stop_parser(self):
        if self.multiprocess and self.pars_proc and self.pars_proc.is_alive():
            self.stop_event.set()
            if self.queue.full():
                self.queue.get_nowait()
            self.pars_proc.join(3)

    def reset_parser(self):
        self.queue.close()
        self.stop_parser()
        self._setup()
        self.start_parser()

    def __iter__(self):
        return self

    def __next__(self) -> Document:
        # get item
        if self.multiprocess:
            item = self.queue.get()
        else:
            item = next(self.pars_gen)
        # return
        if item is None:
            raise StopIteration
        else:
            return item
