from app.models import NewsArticle
from app.preferences import UserPreferences


PRIORITY_MULTIPLIERS = {
    "Low": 0.8,
    "Medium": 1.0,
    "High": 1.2,
}


class NewsRanker:
    def __init__(self, preferences: UserPreferences):
        self.preferences = preferences

    def rank(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        scored_articles = []

        for article in articles:
            priority = self.preferences.get_priority(article.category)
            multiplier = PRIORITY_MULTIPLIERS[priority]

            final_score = article.importance * multiplier

            scored_articles.append((final_score, article))

        scored_articles.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [article for _, article in scored_articles]