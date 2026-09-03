from app.llm import MistralClient
from app.models import NewsArticle
from app.categories import CATEGORIES


class NewsCategorizer:

    def __init__(self):
        self.llm = MistralClient()

    def categorize_many(
        self,
        articles: list[NewsArticle],
    ) -> list[NewsArticle]:

        if not articles:
            return []

        categories = ", ".join(CATEGORIES)

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
Classify each Indian news article into exactly one category.

Allowed categories:
{categories}

{articles_text}

Return ONLY the category for each article.

Use exactly this format:

0: category
1: category
2: category

Do not add explanations.
"""

        response = self.llm.generate(prompt)

        category_map = {}

        for line in response.splitlines():

            line = line.strip()

            if ":" not in line:
                continue

            index_text, category = line.split(
                ":",
                1,
            )

            try:
                index = int(index_text.strip())
            except ValueError:
                continue

            category = category.strip()

            if category in CATEGORIES:
                category_map[index] = category

        for index, article in enumerate(articles):

            article.category = category_map.get(
                index,
                "Other",
            )

        return articles

    def categorize(
        self,
        article: NewsArticle,
    ) -> NewsArticle:

        return self.categorize_many([article])[0]