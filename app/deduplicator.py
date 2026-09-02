from app.models import NewsArticle


class NewsDeduplicator:
    def remove_duplicates(
        self, articles: list[NewsArticle]
    ) -> list[NewsArticle]:

        seen_titles = set()
        unique_articles = []

        for article in articles:
            title_key = article.title.strip().lower()

            if title_key and title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_articles.append(article)

        return unique_articles