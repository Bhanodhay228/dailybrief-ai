from dataclasses import dataclass
from datetime import datetime


@dataclass
class NewsArticle:
    title: str
    description: str
    source: str
    url: str
    published_at: datetime
    category: str
    importance: float = 0.0
    user_priority: str = "Medium"