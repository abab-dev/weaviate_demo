from dotenv import load_dotenv
import os
load_dotenv()
wcd_url = os.environ["WEAVIATE_URL"]
wcd_api_key = os.environ["WEAVIATE_API_KEY"]
studio_key = os.environ["GEMINI_API_KEY"]
