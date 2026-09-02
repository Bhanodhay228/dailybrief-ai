from app.categories import CATEGORIES


PRIORITY_VALUES = ["Low", "Medium", "High"]


class UserPreferences:
    def __init__(self):
        self.priorities = {
            category: "Medium"
            for category in CATEGORIES
        }

    def set_priority(self, category: str, priority: str):
        if category not in CATEGORIES:
            raise ValueError(f"Unknown category: {category}")

        if priority not in PRIORITY_VALUES:
            raise ValueError(
                f"Priority must be one of: {PRIORITY_VALUES}"
            )

        self.priorities[category] = priority

    def get_priority(self, category: str) -> str:
        return self.priorities.get(category, "Medium")