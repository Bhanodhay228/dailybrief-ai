from app.highlights import ImportantNewsSelector
from app.models import NewsArticle


articles = [
    NewsArticle(
        title="Major national event",
        description="A major event affecting the country.",
        source="Source A",
        url="https://example.com/1",
        published_at=None,
        category="India / National",
        importance=9.5,
    ),
    NewsArticle(
        title="Minor technology update",
        description="A small technology development.",
        source="Source B",
        url="https://example.com/2",
        published_at=None,
        category="Technology & AI",
        importance=6.0,
    ),
]

selector = ImportantNewsSelector()

highlights = selector.select(articles)

print("You Should Know:", len(highlights))

for article in highlights:
    print("-", article.title)