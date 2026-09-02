from app.importance import ImportanceScorer
from app.models import NewsArticle


article = NewsArticle(
    title="India announces a major national economic reform",
    description="The government announced a major policy change expected to affect businesses and citizens across the country.",
    source="Test Source",
    url="https://example.com",
    published_at=None,
)

scorer = ImportanceScorer()

result = scorer.score(article)

print("Importance:", result.importance)