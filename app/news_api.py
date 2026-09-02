import os
import requests
from datetime import datetime
from dotenv import load_dotenv

from app.models import NewsArticle

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

        data = response.json()

        return [
            self._convert_to_article(item)
            for item in data.get("results", [])
        ]

    def _convert_to_article(self, item):
        published_at = None

        if item.get("pubDate"):
            try:
                published_at = datetime.fromisoformat(
                    item["pubDate"].replace("Z", "+00:00")
                )
            except ValueError:
                pass

        return NewsArticle(
            title=item.get("title", ""),
            description=item.get("description") or "",
            source=item.get("source_name") or "",
            url=item.get("link") or "",
            published_at=published_at,
        )