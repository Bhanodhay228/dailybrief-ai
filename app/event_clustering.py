from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models import NewsArticle, NewsEvent


class EventClusterer:
    SIMILARITY_THRESHOLD = 0.20

    def cluster(self, articles: list[NewsArticle]) -> list[NewsEvent]:
        if not articles:
            return []

        events = []

        # Group articles by category first
        categories = {}

        for article in articles:
            categories.setdefault(article.category, []).append(article)

        for category, category_articles in categories.items():

            if len(category_articles) == 1:
                article = category_articles[0]

                events.append(
                    NewsEvent(
                        title=article.title,
                        category=category,
                        articles=[article],
                        importance=article.importance,
                    )
                )

                continue

            texts = [
                f"{article.title}. {article.description}"
                for article in category_articles
            ]

            vectorizer = TfidfVectorizer(
                stop_words="english"
            )

            vectors = vectorizer.fit_transform(texts)

            similarity_matrix = cosine_similarity(vectors)

            assigned = set()

            for i, article in enumerate(category_articles):

                if i in assigned:
                    continue

                event_articles = [article]
                assigned.add(i)

                for j in range(i + 1, len(category_articles)):

                    if j in assigned:
                        continue

                    similarity = similarity_matrix[i][j]

                    if similarity >= self.SIMILARITY_THRESHOLD:
                        event_articles.append(
                            category_articles[j]
                        )
                        assigned.add(j)

                events.append(
                    NewsEvent(
                        title=article.title,
                        category=category,
                        articles=event_articles,
                        importance=max(
                            a.importance
                            for a in event_articles
                        ),
                    )
                )

        return events