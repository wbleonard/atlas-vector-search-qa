# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
from sentence_transformers import SentenceTransformer, util
import params
from pymongo import MongoClient
import argparse

# print("\n*** Atlas Vector Search Demo ***\n")

# Process arguments
parser = argparse.ArgumentParser(description='Atlas Vector Search Demo')
parser.add_argument('-q', '--question', help="The question to ask")
args = parser.parse_args()

if args.question is None:
    # Some questions to try...
    query = "Who did Discovery acquire?"
    query = "When was Warner Bros. founded?"
    query = "Who founded TBS?"
    query = "Who did Warner purchase in 1982?"
    query = "What happened to TBS?"
else:
    query = args.question

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Show the default question if one wasn't provided:
if args.question is None:
    print("\nYour question:")
    print("--------------")
    print(query)

# Encode our question
query_vector = model.encode(query).tolist()

# Establish connections to MongoDB
mongo_client = MongoClient(params.mongodb_conn_string)
result_collection = mongo_client[params.database][params.collection]

pipeline = [
    {
        "$search": {
            "knnBeta": {
                "vector": query_vector,
                "path": "docVector",
                "k": 150
            }
        }
    },
    {
        "$limit": 1
    }
]

results = result_collection.aggregate(pipeline)

for result in results:
    print("\nAtlas Search's Answer:")
    print("----------------------")
    print(result['sentence'], "\n")

