# Atlas Vector Search Question and Answer Demo

This demo showcases how Atlas Search's Vector capability can be used to query a body of text. The demo leverages the Hugging Face [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model to map sentences and the questions presented to a 384 dimension dense vector space. 

## Setup

### Text to Query
Save your body of text to the [corpus.txt](corpus.txt) file, or feel free to use the sample provided, which is the background information from the [Warner Bros. Discovery Wikipedia page](https://en.wikipedia.org/wiki/Warner_Bros._Discovery).

### Atlas

Open [params.py](params.py) and configure your connection to Atlas, along with the name of the database and collection you'd like to store your text. 
### Encode your text
Install the Sentence Transformers model:
```zsh
pip install -U sentence-transformers
```

Run the [encoder](encode.py), which will store the sentences along with their dense vectors to MongoDB. 
```python
python3 encode.py
```

### Create Search Index
Create a default search index on the collection:
```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "docVector": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "euclidean"
      }
    }
  }
}
```

## Demo
You are now ready to ask questions about your body of text! The [search.py](search.py) will use the same sentence transformers  library to encode your question and submit it to Atlas Search for the answer.

For example:

```zsh
python3 search -q "Who founded TBS?"

Atlas Search's Answer:
----------------------
In 1965, Turner Broadcasting System was founded by Ted Turner and based in Atlanta, Georgia. 
```
Try other questions, such as:

    "Who did Discovery acquire?"
    "When was Warner Bros. founded?"
    "Who founded TBS?"
    "Who did Warner purchase in 1982?"

# The Search Query
This is the simple query passed to MongoDB:

```json
[
    {
        "$search": {
            "knnBeta": {
                "vector": <geneated query vector>,
                "path": "docVector",
                "k": 150  // Number of neareast neighbors (nn) to return 
            }
        }
    },
    {
        "$limit": 1      // Let's assume the first result is correct :-).
    }
]
```

The knnBeta operator uses the [Hierarchical Navigable Small Worlds](https://arxiv.org/abs/1603.09320) algorithm to perform semantic search. You can use Atlas Search support for kNN query to search similar to a selected product, search for images, etc.