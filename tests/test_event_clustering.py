from app.models import NewsArticle
from app.event_clustering import EventClusterer


articles = [
    NewsArticle(
        title="Supreme Court approves new online gaming rules",
        description="The Supreme Court announced new rules for online gaming.",
        source="Source A",
        url="https://example.com/1",
        published_at=None,
        category="Law & Judiciary",
        importance=8.0,
    ),
    NewsArticle(
        title="Supreme Court backs new online gaming regulations",
        description="The court supported new regulations for online gaming.",
        source="Source B",
        url="https://example.com/2",
        published_at=None,
        category="Law & Judiciary",
        importance=7.5,
    ),
    NewsArticle(
        title="India announces new space mission",
        description="India announced a new mission for space research.",
        source="Source C",
        url="https://example.com/3",
        published_at=None,
        category="Science & Space",
        importance=8.5,
    ),
]


clusterer = EventClusterer()

events = clusterer.cluster(articles)

print("Number of events:", len(events))

for event in events:
    print("\nEVENT:", event.title)
    print("Category:", event.category)
    print("Articles:", len(event.articles))

    for article in event.articles:
        print(" -", article.source, "|", article.url)