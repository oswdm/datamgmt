# DB Benchmark

## project structure
```
db-benchmark
├── README.md
├── compose.yaml            <- compose file for docker containers
├── data                    <- data folder containing .dvc files
│   └── Books.json.gz.dvc
├── dbs                     <- dbs that implement helpers.db_connector class
│   ├── chromadb.py
│   └── pgvector.py
├── helpers                 <- helper classes for data loading and db interaction   
│   ├── data_processor.py
│   └── dp_connector.py
├── dvc.yaml                <- dvc pipeline
├── main.py                 <- main file
├── params.yaml             <- dvc experiment parameters
└── requirements.txt
```

## Prerequisites

- docker
- docker-compose

## Setup

### Step I: create environment

The first step is to create your environment.
```shell
conda create --name <env-name> python=3.11
```

### Step II: install dependencies
The necessary modules for this python project can be installed with the given
[requirements.txt](requirements.txt) file. 
```shell
conda activate <env-name>
pip install -r requirements.txt
```

### Step III: downloading data
If you followed the steps before the `dvc` command is now available. Run the following
command in the git root directory to download the data:
```shell
dvc update -R data/
```

## Running the Benchmark

The benchmarking process involves several steps managed by DVC:

1. **Running the DVC Pipeline**:
   - Execute the main DVC pipeline which orchestrates the data processing and
     benchmarking tasks with `dvc exp run`.
   
1. **Reviewing Results**:
   - Use the `dvc exp show` command to visualize and analyze the results of the
     experiments conducted as part of the benchmark.

## Results

We found the following results (times in miliseconds):
| Experiment | Created | chromadb.insert | chromadb.query | chromadb.remove | pgvector.insert | pgvector.query | pgvector.remove | vespa.insert | vespa.query | vespa.remove | milvus.insert | milvus.query | milvus.remove | qdrant.insert | qdrant.query | qdrant.remove
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| workspace | - | 7.3517 | 5.8963 | 6.2306 | 7.0311 | 2.7662 | 0.30817 | 8.7366 | 11.556 | 5.6302 | 3.8154 | 2.0659 | 2.9517 | 6.9746 | 2.1554 | 6.8914 |       
| 039a025 [eerie-jota] | 01:20 PM | 7.3517 | 5.8963 | 6.2306 | 7.0311 | 2.7662 | 0.30817 | 8.7366 | 11.556 | 5.6302 | 3.8154 | 2.0659 | 2.9517 | 6.9746 | 2.1554 | 6.8914 | 


