from helpers.data_processor import DocumentProcessor
from helpers.dp_connector import DBConector
from dbs import DBS
import time
from tqdm import tqdm

# --------------------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------------------

NS2MS = 1e-6

# --------------------------------------------------------------------------------------
# helper funcs
# --------------------------------------------------------------------------------------


def benchmark_insert(dp: DocumentProcessor, db: DBConector, n_documents: int) -> int:
    dp.reset_parser()
    dp.fill_queue()
    t = time.time_ns()
    for i, doc in tqdm(enumerate(dp), leave=False):
        if i >= n_documents:
            break
        db.insert_document(doc)
    return time.time_ns() - t


def benchmark_query(
    dp: DocumentProcessor, db: DBConector, n_documents: int, n_results: int
):
    dp.fill_queue()
    t = time.time_ns()
    for i, doc in tqdm(enumerate(dp), leave=False):
        if i >= n_documents:
            break
        db.query_db(doc, n_results)
    return time.time_ns() - t


def benchmark_remove(dp: DocumentProcessor, db: DBConector, n_documents: int):
    dp.reset_parser()
    dp.fill_queue()
    t = time.time_ns()
    for i, doc in tqdm(enumerate(dp), leave=False):
        if i >= n_documents:
            break
        db.remove_document(doc.id)
    return time.time_ns() - t


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------


def main(dp: DocumentProcessor, n_docs: int, n_query_results: int):
    for m in (pbar := tqdm(DBS, leave=False)):
        pbar.desc = m.name

        db = m.value()
        tqdm.write(f"{m.name}:")

        # document insert
        ins = benchmark_insert(dp, db, n_docs)
        tqdm.write(f"insert: {ins * NS2MS / n_docs} ms/insert")

        # document query
        qry = benchmark_query(dp, db, n_docs, n_query_results)
        tqdm.write(f"query:  {qry * NS2MS / n_docs} ms/query")

        # document insert
        rem = benchmark_remove(dp, db, n_docs)
        tqdm.write(f"remove: {rem * NS2MS / n_docs} ms/removal")

    dp.stop_parser()


if __name__ == "__main__":
    file_path = "data/Books.json"
    multiprocess = True
    n_docs = 1_000
    n_query_results = 3

    dp = DocumentProcessor(file_path=file_path, multiprocess=multiprocess, qsize=n_docs)
    dp.start_parser()

    main(dp, n_docs, n_query_results)
