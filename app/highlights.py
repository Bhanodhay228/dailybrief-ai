from app.models import NewsArticle


CRITICAL_IMPORTANCE_THRESHOLD = 9.0


class ImportantNewsSelector:
    def select(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        return [
            article
            for article in articles
            if article.importance >= CRITICAL_IMPORTANCE_THRESHOLD
        ]