from app.models import NewsArticle, NewsEvent
from app.pipeline import DailyBriefPipeline


articles = [
    NewsArticle(
        title="Supreme Court announces important decision",
        description=(
            "The Supreme Court announced a decision "
            "that could affect several stakeholders."
        ),
        source="Example Source",
        url="https://example.com/story",
        published_at=None,
        category="Law & Judiciary",
        importance=9.0,
    )
]


event = NewsEvent(
    title="Supreme Court announces important decision",
    category="Law & Judiciary",
    articles=articles,
    importance=9.0,
    summary=(
        "The Supreme Court announced an important decision."
    ),
    key_facts=[
        "The Supreme Court announced a decision."
    ],
    why_it_matters=(
        "The decision could affect several stakeholders."
    ),
)


pipeline = DailyBriefPipeline()

answer = pipeline.answer_question(
    "Tell me more about this story.",
    event,
)

print("\nANSWER:")
print(answer)