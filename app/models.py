from dataclasses import dataclass, field
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


@dataclass
class NewsEvent:
    title: str
    category: str
    articles: list[NewsArticle] = field(default_factory=list)
    importance: float = 0.0
    summary: str = ""
    key_facts: list[str] = field(default_factory=list)
    why_it_matters: str = ""