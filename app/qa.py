from app.llm import MistralClient
from app.web_search import WebSearchClient


class NewsQA:

    def __init__(self):

        self.llm = MistralClient()
        self.search = WebSearchClient()


    def answer(
        self,
        question: str,
        event,
        conversation_history=None,
    ):

        # ------------------------------------------
        # SEARCH FRESH INFORMATION
        # ------------------------------------------

        search_query = (
            f"{event.title} {question}"
        )

        search_results = self.search.search_news(
            search_query,
            max_results=5,
        )


        # ------------------------------------------
        # FRESH SEARCH RESULTS
        # ------------------------------------------

        sources_text = ""

        for index, article in enumerate(
            search_results,
            start=1,
        ):

            sources_text += f"""
SOURCE {index}

Title:
{article.title}

Source:
{article.source}

Content:
{article.description}

URL:
{article.url}

"""


        # ------------------------------------------
        # ORIGINAL EVENT SOURCES
        # ------------------------------------------

        event_sources = ""

        for article in event.articles:

            event_sources += f"""
Source:
{article.source}

Title:
{article.title}

URL:
{article.url}

"""


        # ------------------------------------------
        # CONVERSATION HISTORY
        # ------------------------------------------

        history_text = ""

        if conversation_history:

            for message in conversation_history:

                history_text += f"""
{message["role"].upper()}:
{message["content"]}

"""


        # ------------------------------------------
        # PROMPT
        # ------------------------------------------

        prompt = f"""
You are an AI news assistant.

You are helping the user understand an Indian news event.

CURRENT NEWS EVENT:

Title:
{event.title}

Category:
{event.category}

Summary:
{event.summary}

Key Facts:
{event.key_facts}

Why It Matters:
{event.why_it_matters}

Original Sources:
{event_sources}


PREVIOUS CONVERSATION:

{history_text}


USER'S NEW QUESTION:

{question}


FRESH SEARCH INFORMATION:

{sources_text}


INSTRUCTIONS:

- Answer the user's question clearly.
- Use the current news event as context.
- Use fresh search information when relevant.
- Use previous conversation context when relevant.
- Do not invent facts.
- If information is insufficient, clearly say so.
- Prefer recent information when answering.
- Keep the answer easy to understand.
- Do not repeat the entire previous conversation.

At the end provide:

SOURCES:
- source name: URL
"""

        return self.llm.generate(prompt)