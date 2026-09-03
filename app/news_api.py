import os
from datetime import datetime

import requests
from dotenv import load_dotenv

from app.models import NewsArticle


load_dotenv()


class NewsDataClient:

    def __init__(self):
        self.api_key = os.getenv("NEWSDATA_API_KEY")
        self.base_url = "https://newsdata.io/api/1/latest"

    def get_latest_news(self, limit=10):

        params = {
            "apikey": self.api_key,
            "country": "in",
            "language": "en",
            "removeduplicate": 1,
        }

        response = requests.get(
            self.base_url,
            params=params,
            timeout=30,
        )

        if response.status_code == 429:
            raise RuntimeError(
                "NewsData rate limit reached. "
                "Please try again after the API limit resets."
            )

        response.raise_for_status()

        data = response.json()

        articles = []

        for item in data.get("results", []):

            article = self._convert_to_article(item)

            if article.url:
                articles.append(article)

        return articles[:limit]

    def _convert_to_article(self, item):

        published_at = None

        pub_date = item.get("pubDate")

        if pub_date:

            try:
                published_at = datetime.fromisoformat(
                    pub_date.replace("Z", "+00:00")
                )

            except ValueError:

                try:
                    published_at = datetime.strptime(
                        pub_date,
                        "%Y-%m-%d %H:%M:%S",
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