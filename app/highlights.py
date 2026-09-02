from app.models import NewsEvent


CRITICAL_IMPORTANCE_THRESHOLD = 9.0


class ImportantNewsSelector:

    def select(
        self,
        events: list[NewsEvent]
    ) -> list[NewsEvent]:

        return [
            event
            for event in events
            if event.importance >= CRITICAL_IMPORTANCE_THRESHOLD
        ]