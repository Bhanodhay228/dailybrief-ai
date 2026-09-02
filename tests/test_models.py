from app.models import NewsArticle, NewsEvent


article1 = NewsArticle(
    title="India announces new space mission",
    description="India announced a new space mission.",
    source="Source A",
    url="https://example.com/1",
    published_at=None,
)

article2 = NewsArticle(
    title="New Indian space mission announced",
    description="A second report discusses the same space mission.",
    source="Source B",
    url="https://example.com/2",
    published_at=None,
)

event = NewsEvent(
    title="India announces new space mission",
    category="Science & Space",
    articles=[article1, article2],
    importance=9.0,
    summary="India has announced a new space mission.",
    key_facts=[
        "The mission was announced by India.",
        "The mission focuses on space exploration.",
    ],
    why_it_matters="The mission could strengthen India's space capabilities.",
)

print("Event:", event.title)
print("Category:", event.category)
print("Number of sources:", len(event.articles))
print("Importance:", event.importance)
print("Summary:", event.summary)

print("\nSources:")
for article in event.articles:
    print("-", article.source, article.url)