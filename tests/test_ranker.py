from app.models import NewsArticle
from app.preferences import UserPreferences
from app.ranker import NewsRanker


preferences = UserPreferences()

preferences.set_priority("Technology & AI", "High")
preferences.set_priority("Sports", "Low")

articles = [
    NewsArticle(
        title="Major technology development",
        description="Important technology news.",
        source="Source A",
        url="https://example.com/tech",
        published_at=None,
        category="Technology & AI",
        importance=8.0,
    ),
    NewsArticle(
        title="Major sports development",
        description="Important sports news.",
        source="Source B",
        url="https://example.com/sports",
        published_at=None,
        category="Sports",
        importance=8.0,
    ),
]

ranker = NewsRanker(preferences)

ranked = ranker.rank(articles)

for article in ranked:
    print(
        article.category,
        "Importance:", article.importance,
    )