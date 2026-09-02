from app.models import NewsArticle
from app.summarizer import NewsSummarizer


article = NewsArticle(
    title="India announces a major space mission",
    description=(
        "India announced a new space mission focused on scientific "
        "research and exploration."
    ),
    source="Test Source",
    url="https://example.com",
    published_at=None,
    category="Science & Space",
    importance=8.5,
)

summarizer = NewsSummarizer()

result = summarizer.summarize(article)

print("Summary:")
print(result.summary)

print("\nWhy it matters:")
print(result.why_it_matters)