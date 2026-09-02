from app.llm import MistralClient
from app.models import NewsArticle
from app.categories import CATEGORIES


class NewsCategorizer:
    def __init__(self):
        self.llm = MistralClient()

    def categorize(self, article: NewsArticle) -> NewsArticle:
        categories = ", ".join(CATEGORIES)

        prompt = f"""
Classify the following news article into exactly one category.

Allowed categories:
{categories}

Title:
{article.title}

Description:
{article.description}

Return only the category name.
"""

        category = self.llm.generate(prompt).strip()

        if category not in CATEGORIES:
            category = "Other"

        article.category = category

        return article