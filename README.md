# DB Benchmark

## Setup

### Step I: downloading data

The first step is to create your conda environment for this python project. Run the following command in your terminal and install the recommended packages like pip:
```shell
conda create --name <env-name> python=3.8
```

The necessary modules for this python project can be installed with the given [requirements.txt](requirements.txt) file. Navigate in your terminal to your project folder and run the following command:
```shell
conda activate <env-name>
pip install -r requirements.txt
```

If you followed the steps before `dvc` must now be installed. Run the following command in the git root directory to download the data:
```shell
dvc update -R data/
```
The files are now still compressed. So navigate to the data and unzip them with tools like gunzip in linux.

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
