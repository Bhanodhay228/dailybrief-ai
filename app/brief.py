from app.models import NewsEvent
from app.preferences import UserPreferences


class DailyBriefBuilder:
    def __init__(self, preferences: UserPreferences):
        self.preferences = preferences

    def build(
        self,
        events: list[NewsEvent],
        important_events: list[NewsEvent],
    ):
        important_ids = {
            id(event)
            for event in important_events
        }

        normal_events = [
            event
            for event in events
            if id(event) not in important_ids
        ]

        high = []
        medium = []
        low = []

        for event in normal_events:
            priority = self.preferences.get_priority(
                event.category
            )

            if priority == "High":
                high.append(event)

            elif priority == "Medium":
                medium.append(event)

            else:
                low.append(event)

        return {
            "important": important_events,
            "high": high,
            "medium": medium,
            "low": low,
        }