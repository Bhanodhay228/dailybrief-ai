from app.preferences import UserPreferences
from app.models import NewsEvent
from app.ranker import NewsRanker


preferences = UserPreferences()

preferences.set_priority(
    "Technology & AI",
    "High"
)

preferences.set_priority(
    "Sports",
    "Low"
)


events = [
    NewsEvent(
        title="New AI breakthrough announced",
        category="Technology & AI",
        importance=7.0,
    ),
    NewsEvent(
        title="Major cricket match announced",
        category="Sports",
        importance=7.0,
    ),
]


ranker = NewsRanker(preferences)

ranked_events = ranker.rank(events)


print("Ranking after user preferences:")

for event in ranked_events:
    print(
        event.category,
        "→",
        event.importance
    )