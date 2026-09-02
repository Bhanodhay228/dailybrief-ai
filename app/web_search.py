import os
from dotenv import load_dotenv
from tavily import TavilyClient

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

        return response