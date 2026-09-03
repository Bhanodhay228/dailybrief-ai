import os

from dotenv import load_dotenv
from tavily import TavilyClient

from app.models import NewsArticle


load_dotenv()


class WebSearchClient:

    def __init__(self):

        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )

        if not self.api_key:

            try:
                import streamlit as st

                self.api_key = st.secrets[
                    "TAVILY_API_KEY"
                ]

            except Exception:
                self.api_key = None


        if not self.api_key:

            raise RuntimeError(
                "TAVILY_API_KEY is not configured."
            )


        self.client = TavilyClient(
            api_key=self.api_key
        )


    def search_news(
        self,
        query: str,
        max_results: int = 5,
    ):

        response = self.client.search(
            query=query,
            max_results=max_results,
        )


        return [
            self._convert_to_article(
                result
            )
            for result in response.get(
                "results",
                [],
            )
        ]


    def _convert_to_article(
        self,
        result,
    ):

        url = result.get(
            "url",
            "",
        )


        source = ""

        if url:

            try:

                source = url.split(
                    "/"
                )[2]

            except IndexError:

                source = ""


        return NewsArticle(
            title=result.get(
                "title",
                "",
            ),
            description=result.get(
                "content",
                "",
            ),
            source=source,
            url=url,
            published_at=None,
        )