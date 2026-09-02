from app.deduplicator import NewsDeduplicator
from app.models import NewsArticle


articles = [
    NewsArticle(
        title="India launches new space mission",
        description="Space mission launched successfully.",
        source="Source A",
        url="https://example.com/1",
        published_at=None,
    ),
    NewsArticle(
        title="India launches new space mission",
        description="Another report about the mission.",
        source="Source B",
        url="https://example.com/2",
        published_at=None,
    ),
    NewsArticle(
        title="Government announces new education policy",
        description="New education policy announced.",
        source="Source C",
        url="https://example.com/3",
        published_at=None,
    ),
]

deduplicator = NewsDeduplicator()

unique_articles = deduplicator.remove_duplicates(articles)

print("Original articles:", len(articles))
print("Unique articles:", len(unique_articles))

for article in unique_articles:
    print("-", article.title)