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
        # Fresh search
        # ------------------------------------------

        search_query = (
            f"{event.title} {question}"
        )

        search_results = self.search.search_news(
            search_query,
            max_results=5,
        )


        # ------------------------------------------
        # Search information
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
        # Original event sources
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
        # Conversation
        # ------------------------------------------

        history_text = ""

        if conversation_history:

            for message in conversation_history:

                history_text += f"""
{message["role"].upper()}:
{message["content"]}
"""


        # ------------------------------------------
        # Prompt
        # ------------------------------------------

        prompt = f"""
You are DailyBrief AI, an Indian news assistant.

Answer the user's question about the news event below.

CURRENT NEWS EVENT

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

ORIGINAL SOURCES:
{event_sources}

PREVIOUS CONVERSATION:
{history_text}

USER QUESTION:
{question}

FRESH SEARCH INFORMATION:
{sources_text}


IMPORTANT ANSWER RULES:

1. Keep the answer SHORT and easy to scan.
2. Use simple bullet points.
3. Give a maximum of 5 bullet points.
4. Each bullet should normally be 1-2 sentences.
5. Start with one short sentence directly answering the question.
6. Do not write a long essay.
7. Do not repeat the entire news story.
8. Do not use Markdown headings such as ###.
9. Do not use bold Markdown such as **text**.
10. Do not use tables.
11. Do not add unnecessary background information.
12. Use only information provided by the event and fresh search results.
13. Do not invent facts.
14. If the information is insufficient, clearly say so.
15. Prefer the newest relevant information.


Use this exact structure:

Direct answer: <one short sentence>

• <important point>
• <important point>
• <important point>

Sources:
<source name> - <URL>
<source name> - <URL>

Do not add anything after the sources.
"""

        return self.llm.generate(
            prompt
        )