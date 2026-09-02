import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=api_key)

response = client.search(
    query="latest major news in India today",
    max_results=5
)

print("Search successful!")
print(response)