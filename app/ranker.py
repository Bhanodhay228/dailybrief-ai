from app.models import NewsEvent
from app.preferences import UserPreferences


PRIORITY_MULTIPLIERS = {
    "Low": 0.8,
    "Medium": 1.0,
    "High": 1.2,
}


class NewsRanker:
    def __init__(self, preferences: UserPreferences):
        self.preferences = preferences

    def rank(self, events: list[NewsEvent]) -> list[NewsEvent]:
        scored_events = []

        for event in events:
            priority = self.preferences.get_priority(event.category)

            multiplier = PRIORITY_MULTIPLIERS[priority]

            final_score = event.importance * multiplier

            scored_events.append(
                (final_score, event)
            )

        scored_events.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            event
            for _, event in scored_events
        ]