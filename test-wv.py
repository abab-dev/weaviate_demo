import weaviate
from weaviate.classes.init import Auth 
from dotenv import load_dotenv
from weaviate.classes.config import Configure,Property,DataType
import os
import pandas as  pd
load_dotenv()

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WEAVIATE_URL"]
wcd_api_key = os.environ["WEAVIATE_API_KEY"]
studio_key = os.environ["GEMINI_API_KEY"]
headers = {
 "X-Goog-Studio-Api-Key"   : studio_key
}

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),  # Replace with your Weaviate Cloud key
    headers=headers
)

print(client.is_ready())


pd.set_option('max_colwidth', None)

df = pd.read_csv('pastry_data.csv', delimiter=';')
# df
if client.collections.exists("Pastries"):
    client.collections.delete("Pastries")

 
pastries = client.collections.create(
    name="Pastries",
    vectorizer_config=Configure.Vectorizer.text2vec_google(project_id=""),
    # vectorizer_config=Configure.Vectorizer.text2vec_weaviate(),
    properties=[
        Property(name="pastry_name", data_type=DataType.TEXT),
        Property(name="pastry_description", data_type=DataType.TEXT),
    ]
)
pastry_objects = list()
for _, row in df.iterrows():
    properties = {
        "pastry_name": row.pastry_name,
        "pastry_description": row.pastry_description
    }
    pastry_objects.append(properties)

pastries.data.insert_many(pastry_objects)

client.close()