# DB Benchmark

## Setup

### Step I: downloading data

TODO: explain requirements.txt

Be sure to have `dvc` installed. Then run the following command in the git root directory
```shell
dvc update -R data/
```

unzip data with gunzip

### DocumentProcessor

usage

```python
    from helpers.data_processor import DocumentProcessor

    file_path = "data/Books.json"
    multiprocess = True

    dp = DocumentProcessor(file_path=file_path, multiprocess=multiprocess)

    dp.start_parser()

    for doc in dp:
        # do something
        print(doc)

    dp.stop_parser()
```
