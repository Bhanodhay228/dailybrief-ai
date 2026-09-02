from app.models import NewsArticle, NewsEvent
from app.summarizer import EventSummarizer


articles = [
    NewsArticle(
        title="Supreme Court approves new online gaming rules",
        description=(
            "The Supreme Court announced new rules for online gaming. "
            "The rules aim to regulate online gaming platforms."
        ),
        source="Source A",
        url="https://example.com/1",
        published_at=None,
        category="Law & Judiciary",
        importance=8.0,
    ),
    NewsArticle(
        title="Supreme Court backs new online gaming regulations",
        description=(
            "The court supported regulations for online gaming platforms. "
            "The decision could affect gaming companies and users."
        ),
        source="Source B",
        url="https://example.com/2",
        published_at=None,
        category="Law & Judiciary",
        importance=7.5,
    ),
]


event = NewsEvent(
    title="Supreme Court online gaming decision",
    category="Law & Judiciary",
    articles=articles,
    importance=8.0,
)


summarizer = EventSummarizer()

event = summarizer.summarize(event)

print("\nTITLE:")
print(event.title)

print("\nSUMMARY:")
print(event.summary)

print("\nKEY FACTS:")
for fact in event.key_facts:
    print("-", fact)

print("\nWHY IT MATTERS:")
print(event.why_it_matters)

print("\nSOURCES:")
for article in event.articles:
    print("-", article.source, article.url)