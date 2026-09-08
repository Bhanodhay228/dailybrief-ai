import re
from datetime import datetime

from app.web_search import WebSearchClient
from app.llm import MistralClient


class GovernmentExamNews:

    EXAM_QUERIES = [
        "India government schemes initiatives current affairs",
        "India government appointments resignations current affairs",
        "India awards honours current affairs",
        "India defence military exercises current affairs",
        "India economy banking RBI current affairs",
        "India reports indexes rankings current affairs",
        "India science technology ISRO space current affairs",
        "India international relations summits agreements current affairs",
        "India important days themes current affairs",
        "India sports achievements records current affairs",
        "India books authors obituaries current affairs",
        "India government policies bills acts judiciary current affairs",
    ]

    def __init__(self):
        self.search = WebSearchClient()
        self.llm = MistralClient()

    def fetch_articles(self):
        """
        Fetch exam-oriented current affairs from
        multiple targeted Tavily searches.
        """

        all_articles = []
        seen_urls = set()
        seen_titles = set()

        for query in self.EXAM_QUERIES:

            try:
                articles = self.search.search_news(
                    query,
                    max_results=3,
                )

                for article in articles:

                    title = (
                        article.title or ""
                    ).strip()

                    url = (
                        article.url or ""
                    ).strip()

                    if not title:
                        continue

                    title_key = title.lower()

                    if (
                        url in seen_urls
                        or title_key in seen_titles
                    ):
                        continue

                    seen_urls.add(url)
                    seen_titles.add(title_key)

                    all_articles.append(article)

            except Exception as exc:
                print(
                    f"Exam search failed for "
                    f"'{query}': {exc}"
                )

        print(
            "Exam articles retrieved:",
            len(all_articles),
        )

        return all_articles

    def generate_brief(self):
        """
        Search the web and convert the results into
        an exam-focused current affairs briefing.
        """

        articles = self.fetch_articles()

        if not articles:
            raise RuntimeError(
                "No exam current-affairs articles "
                "could be retrieved."
            )

        article_text = []

        for index, article in enumerate(
            articles[:30],
            start=1,
        ):

            article_text.append(
                f"""
ARTICLE {index}

Title:
{article.title}

Source:
{article.source}

Content:
{article.description}

URL:
{article.url}
"""
            )

        combined_articles = "\n".join(
            article_text
        )

        prompt = f"""
You are an expert Indian government-exam
current-affairs editor.

Your job is to convert the retrieved news below
into a highly useful current-affairs briefing for
SSC CGL, Banking, Railway, UPSC and State PSC
aspirants.

IMPORTANT:

1. Use ONLY information supported by the retrieved
   articles.

2. Do NOT invent facts, dates, numbers, names or
   government schemes.

3. Remove entertainment, celebrity gossip,
   advertisements and irrelevant news.

4. Prefer developments that are useful for
   competitive exams.

5. Focus especially on:
   - Government schemes
   - Government initiatives
   - Important appointments
   - Awards and honours
   - Defence exercises
   - Economy and banking
   - RBI
   - Reports and indexes
   - Science and technology
   - ISRO and space
   - International relations
   - Summits
   - Agreements
   - Important government decisions
   - Bills, Acts and judiciary
   - Important days and themes
   - Sports achievements
   - Books and authors
   - Important personalities
   - Obituaries

6. Combine duplicate reports about the same event.

7. Prefer important factual information over
   long explanations.

For every selected current-affairs item, produce:

TITLE

CATEGORY

WHY IMPORTANT

SUMMARY

EXAM FACTS

ONE-LINE REVISION

SOURCE

Return ONLY valid JSON in this exact structure:

{{
    "items": [
        {{
            "title": "string",
            "category": "string",
            "why_important": "string",
            "summary": "string",
            "exam_facts": [
                "fact 1",
                "fact 2",
                "fact 3"
            ],
            "one_line_revision": "string",
            "source": "string",
            "url": "string"
        }}
    ]
}}

Keep the final output to approximately
15 important current-affairs items.

Retrieved articles:

{combined_articles}
"""

        response = self.llm.generate(
            prompt
        )

        return self._parse_response(response)

    def _parse_response(self, response):

        response = response.strip()

        # Remove markdown JSON fences if the model
        # returns them.
        response = re.sub(
            r"^```json\s*",
            "",
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"^```\s*",
            "",
            response,
        )

        response = re.sub(
            r"\s*```$",
            "",
            response,
        )

        try:
            import json

            data = json.loads(response)

            if not isinstance(data, dict):
                raise ValueError(
                    "Invalid exam brief format."
                )

            items = data.get(
                "items",
                [],
            )

            if not isinstance(items, list):
                items = []

            return {
                "items": items,
                "date": datetime.now().strftime(
                    "%A, %d %B %Y"
                ),
            }

        except Exception as exc:

            print(
                "Exam JSON parsing failed:",
                exc,
            )

            raise RuntimeError(
                "The AI returned an invalid "
                "exam-current-affairs response."
            )