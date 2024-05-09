import time

import yaml
from dbs import DBS
from dvclive import Live
from helpers.data_processor import DocumentProcessor
from helpers.dp_connector import DBConector
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


def main():
    # params
    cfg = yaml.safe_load(open("params.yaml"))
    data_path = cfg["data_path"]
    multiprocess = cfg["multiprocess"]
    n_docs = cfg["n_docs"]
    n_query_results = cfg["n_query_results"]

    # document processor
    dp = DocumentProcessor(file_path=data_path, multiprocess=multiprocess, qsize=n_docs)
    dp.start_parser()

    # benchmarks
    with Live() as live:
        for m in (pbar := tqdm(DBS, leave=False)):
            pbar.desc = m.name

            db = m.value()
            tqdm.write(f"{m.name}:")

            # document insert
            ins = benchmark_insert(dp, db, n_docs) * NS2MS / n_docs
            live.log_metric(f"{m.name}/insert", ins)
            tqdm.write(f"insert: {ins} ms/insert")

            # document query
            qry = benchmark_query(dp, db, n_docs, n_query_results) * NS2MS / n_docs
            live.log_metric(f"{m.name}/query", qry)
            tqdm.write(f"query:  {qry} ms/query")

            # document insert
            rem = benchmark_remove(dp, db, n_docs) * NS2MS / n_docs
            live.log_metric(f"{m.name}/remove", rem)
            tqdm.write(f"remove: {rem} ms/removal")

        dp.stop_parser()


if __name__ == "__main__":
    main()
