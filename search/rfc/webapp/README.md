# Elasticsearch meets NetBERT

## System architecture

![System architecture](./-/figures/architecture.png)

## Getting Started

### 1. Setup
The following section lists the requirements in order to start running the project.

This project is based on Docker containers, so ensure to have [Docker](https://docs.docker.com/v17.12/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your machine. In addition, your machine should dispose from a working version of Python 3.6 as well as the following packages:
- [bert-serving-client](https://pypi.org/project/bert-serving-client/)
- [elasticsearch](https://pypi.org/project/elasticsearch/)
- [pandas](https://pypi.org/project/pandas/)

These libraries can be installed automatically by running the following command in the *code/* repository:
```bash
pip install -r requirements.txt
```

### 2. Deployment
####  Launch the Docker containers
In order to run the containers, run the following command:
```bash
sudo make install
```

### Create index

You can use the create index API to add a new index to an Elasticsearch cluster. When creating an index, you can specify the following:

* Settings for the index
* Mappings for fields in the index
* Index aliases

For example, if you want to create `rfcsearch` index with `title`, `text` and `text_vector` fields, you can create the index by the following command:

```bash
$ bash create_index.sh

# index.json
{
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "dynamic": "true",
    "_source": {
      "enabled": "true"
    },
    "properties": {
      "title": {
        "type": "text"
      },
      "text": {
        "type": "text"
      },
      "text_vector": {
        "type": "dense_vector",
        "dims": 768
      }
    }
  }
}
```

*NB*: The `dims` value of `text_vector` must need to match the dims of a pretrained BERT model.


### Create documents

Once you created an index, you’re ready to index some document. The point here is to convert your document into a vector using BERT. The resulting vector is stored in the `text_vector` field. Let`s convert your data into a JSON document:

```bash
bash create_documents.sh

# example/example.csv
"Title","Text"
"rfc1 - Host Software","Somewhat independently, Gerard DeLoche of UCLA has been working on the HOST-IMP interface."
"rfc153 - SRI ARC-NIC status","The specifications of DEL are under discussion. The following diagrams show the sequence of actions."
"rfc354 - File Transfer Protocol","The links have the following primitive characteristics. They are always functioning and there are always 32 of them."
"rfcxxx - Lorem Ipsum","Lorem Ipsum"
...
```

After finishing the script, you get a JSON document as follows:

```python
# documents.json
{"_op_type": "index", "_index": "rfcsearch", "text": "lorem ipsum", "title": "lorem ipsum", "text_vector": [...]}
{"_op_type": "index", "_index": "rfcsearch", "text": "lorem ipsum", "title": "lorem ipsum", "text_vector": [...]}
{"_op_type": "index", "_index": "rfcsearch", "text": "lorem ipsum", "title": "lorem ipsum", "text_vector": [...]}
...
```