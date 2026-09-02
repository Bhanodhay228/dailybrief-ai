import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("NEWSDATA_API_KEY")

url = "https://newsdata.io/api/1/latest"

params = {
    "apikey": api_key,
    "country": "in",
    "language": "en",
    "removeduplicate": 1,
}

response = requests.get(url, params=params)

print("Status:", response.status_code)
print("Response:", response.json())