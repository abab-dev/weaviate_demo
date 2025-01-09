import weaviate
from weaviate import WeaviateClient
from weaviate.classes.init import Auth
from dotenv import load_dotenv
from weaviate.classes.config import Configure,Property,DataType
load_dotenv()
import os
gemini_key= os.environ["GEMINI_API_KEY"]
wcd_url = os.environ["WEAVIATE_URL"]
wcd_api_key = os.environ["WEAVIATE_API_KEY"]
def connect_to_weaviate(gemini_key) -> WeaviateClient:
    # Connect to your local Weaviate instance deployed with Docker
    client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),  # Replace with your Weaviate Cloud key
        headers={
       "X-Goog-Studio-Api-Key":gemini_key
        }
    )


    print(client.is_ready())

    return client
# Note: in practice, you shouldn't rerun this cell, as it deletes your data
# in "JeopardyQuestion", and then you need to re-import it again.
import weaviate.classes.config as wc
client = connect_to_weaviate(gemini_key)

# Delete the collection if it already exists
if (client.collections.exists("JeopardyQuestion")):
    client.collections.delete("JeopardyQuestion")

client.collections.create(
    name="JeopardyQuestion",

    vectorizer_config=wc.Configure.Vectorizer.text2vec_palm( # specify the vectorizer and model type you're using
        project_id="", # required. replace with your value: (e.g. "cloud-large-language-models")
        # api_endpoint="generativelanguage.googleapis.com", # This is the endpoint for Google MakerSuite
    ),

    properties=[ # defining properties (data schema) is optional
        wc.Property(name="Question", data_type=wc.DataType.TEXT), 
        wc.Property(name="Answer", data_type=wc.DataType.TEXT),
        wc.Property(name="Category", data_type=wc.DataType.TEXT, skip_vectorization=True), 
    ]
)

print("Successfully created collection: JeopardyQuestion.")

import requests, json
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Get a collection object for "JeopardyQuestion"
jeopardy = client.collections.get("JeopardyQuestion")

# Insert data objects
response = jeopardy.data.insert_many(data)

# Note, the `data` array contains 10 objects, which is great to call insert_many with.
# However, if you have a milion objects to insert, then you should spit them into smaller batches (i.e. 100-1000 per insert)

if (response.has_errors):
    print(response.errors)
else:
    print("Insert complete.")

# note, you can reuse the collection object from the previous cell.
# Get a collection object for "JeopardyQuestion"
jeopardy = client.collections.get("JeopardyQuestion")

response = jeopardy.query.hybrid(
    query="northern beast",
    alpha=0.8,
    limit=3
)

for item in response.objects:
    print("ID:", item.uuid)
    print("Data:", json.dumps(item.properties, indent=2), "\n")
response = jeopardy.query.hybrid(
    query="northern beast",
    query_properties=["question"],
    alpha=0.8,
    limit=3
)

for item in response.objects:
    print("ID:", item.uuid)
    print("Data:", json.dumps(item.properties, indent=2), "\n")
     