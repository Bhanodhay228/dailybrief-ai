import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NewsDataClient:
    def __init__(self):
        self.api_key = os.getenv("NEWSDATA_API_KEY")
        self.base_url = "https://newsdata.io/api/1/latest"

    def get_latest_news(self):
        params = {
            "apikey": self.api_key,
            "country": "in",
            "language": "en",
            "removeduplicate": 1,
        }

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()

        return response.json()