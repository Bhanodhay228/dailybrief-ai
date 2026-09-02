import os
from datetime import datetime

from dotenv import load_dotenv
from tavily import TavilyClient

from app.models import NewsArticle

load_dotenv()


class WebSearchClient:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=self.api_key)

    def search_news(self, query: str, max_results: int = 5):
        response = self.client.search(
            query=query,
            max_results=max_results,
        )

        return [
            self._convert_to_article(result)
            for result in response.get("results", [])
        ]

    def _convert_to_article(self, result):
        return NewsArticle(
            title=result.get("title", ""),
            description=result.get("content", ""),
            source=result.get("url", "").split("/")[2],
            url=result.get("url", ""),
            published_at=None,
        )