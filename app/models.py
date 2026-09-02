from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsArticle:
    title: str
    description: str
    source: str
    url: str
    published_at: datetime | None
    category: str = "Other"
    importance: float = 0.0
    user_priority: str = "Medium"
    summary: str = ""
    why_it_matters: str = ""