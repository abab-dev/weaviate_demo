from dotenv import load_dotenv
import google.generativeai as genai
import weaviate
import os
from utils import *
import weaviate
from weaviate.classes.init import Auth
import weaviate.classes as wc
from utils import *
auth_config = Auth.api_key(api_key=wcd_api_key)

# Load environment variables
load_dotenv()
studio_key = os.getenv("GEMINI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=studio_key)

# Initialize Weaviate client
weaviate_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),  # Replace with your Weaviate Cloud key
)


# Add schema to Weaviate (run this only once)
# if not weaviate_client.collections.exists(schema):
#     weaviate_client.collections.exists(schema)

# Example documents
documents = [
    {"id": "1", "title": "AI Basics", "content": "This is a sample document about AI."},
    {"id": "2", "title": "Machine Learning", "content": "This document is about machine learning."},
]

if (weaviate_client.collections.exists("Document")):
    weaviate_client.collections.delete("Document")
weaviate_client.collections.create(
    name="Document",
     vectorizer_config=wc.config.Configure.Vectorizer.none(),
)
objs = list()
for i,d  in enumerate(documents):
    vec = genai.embed_content( model="models/text-embedding-004", content=d["content"])
    objs.append(wc.data.DataObject(
        properties={
            "title":d["title"]
        },
        vector = vec["embedding"]
    ))
print("Documents successfully inserted into Weaviate!")

questions = weaviate_client.collections.get("Document")
questions.data.insert_many(objs)

query = genai.embed_content( model="models/text-embedding-004", content="News reporters have forcasted the looming weather")
import time
time.sleep(1)  # Sleep so we don't query before async indexing finishes

response = questions.query.near_vector(
    near_vector=query["embedding"],
    limit=2,
    return_metadata=wc.query.MetadataQuery(certainty=True)
)

def pretty_print_query_return(query_return):
    for obj in query_return.objects:
        print(f"Title: {obj.properties.get('title', 'N/A')}")
        print(f"UUID: {obj.uuid}")
        print(f"Certainty: {obj.metadata.certainty}")
        print("-" * 40)

# Example usage:
# pretty_print_query_return(your_query_return_object)

pretty_print_query_return(response)



