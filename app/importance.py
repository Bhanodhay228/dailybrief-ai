from app.llm import MistralClient
from app.models import NewsArticle


class ImportanceScorer:
    def __init__(self):
        self.llm = MistralClient()

    def score(self, article: NewsArticle) -> NewsArticle:
        prompt = f"""
Rate the importance of this news article on a scale from 0 to 10.

Consider:
- Number of people potentially affected
- National or international significance
- Economic impact
- Political or legal significance
- Scientific or technological importance
- Long-term consequences
- Urgency

Title:
{article.title}

Description:
{article.description}

Return ONLY a number between 0 and 10.
"""

        response = self.llm.generate(prompt).strip()

        try:
            score = float(response)
            score = max(0.0, min(10.0, score))
        except ValueError:
            score = 0.0

        article.importance = score

        return article