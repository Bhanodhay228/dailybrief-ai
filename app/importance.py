from app.llm import MistralClient
from app.models import NewsArticle


class ImportanceScorer:

    def __init__(self):
        self.llm = MistralClient()

    def score_many(
        self,
        articles: list[NewsArticle],
    ) -> list[NewsArticle]:

        if not articles:
            return []

        articles_text = ""

        for index, article in enumerate(articles):
            articles_text += f"""
ARTICLE {index}

Title:
{article.title}

Description:
{article.description}

"""

        prompt = f"""
Rate the importance of each Indian news article
on a scale from 0 to 10.

Consider:

- Number of people potentially affected
- National significance
- Economic impact
- Political or legal significance
- Scientific or technological importance
- Long-term consequences
- Urgency

{articles_text}

Return ONLY the scores.

Use exactly this format:

0: 8.5
1: 6.0
2: 9.0

Do not add explanations.
"""

        response = self.llm.generate(prompt)

        score_map = {}

        for line in response.splitlines():

            line = line.strip()

            if ":" not in line:
                continue

            index_text, score_text = line.split(
                ":",
                1,
            )

            try:
                index = int(index_text.strip())
                score = float(score_text.strip())

                score = max(
                    0.0,
                    min(10.0, score),
                )

                score_map[index] = score

            except ValueError:
                continue

        for index, article in enumerate(articles):

            article.importance = score_map.get(
                index,
                0.0,
            )

        return articles

    def score(
        self,
        article: NewsArticle,
    ) -> NewsArticle:

        return self.score_many([article])[0]