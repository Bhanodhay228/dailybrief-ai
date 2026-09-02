from app.categorizer import NewsCategorizer
from app.models import NewsArticle


article = NewsArticle(
    title="OpenAI announces a new artificial intelligence model",
    description="The company introduced a new AI model with improved capabilities.",
    source="Test Source",
    url="https://example.com",
    published_at=None,
)

categorizer = NewsCategorizer()

result = categorizer.categorize(article)

print("Category:", result.category)