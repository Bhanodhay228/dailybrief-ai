from app.news_api import NewsDataClient
from app.categorizer import NewsCategorizer
from app.importance import ImportanceScorer
from app.deduplicator import NewsDeduplicator
from app.event_clustering import EventClusterer
from app.summarizer import EventSummarizer
from app.preferences import UserPreferences
from app.ranker import NewsRanker
from app.highlights import ImportantNewsSelector
from app.brief import DailyBriefBuilder


class DailyBriefPipeline:
    def __init__(self):
        self.news_client = NewsDataClient()
        self.categorizer = NewsCategorizer()
        self.importance_scorer = ImportanceScorer()
        self.deduplicator = NewsDeduplicator()
        self.clusterer = EventClusterer()
        self.summarizer = EventSummarizer()

        self.preferences = UserPreferences()
        self.ranker = NewsRanker(self.preferences)
        self.highlights = ImportantNewsSelector()
        self.brief_builder = DailyBriefBuilder(self.preferences)

    def run(self):
        articles = self.news_client.get_latest_news()

        print("Articles retrieved:", len(articles))

        articles = self.deduplicator.remove_duplicates(articles)

        print("After deduplication:", len(articles))

        categorized_articles = []

        for article in articles:
            article = self.categorizer.categorize(article)
            categorized_articles.append(article)

        scored_articles = []

        for article in categorized_articles:
            article = self.importance_scorer.score(article)
            scored_articles.append(article)

        events = self.clusterer.cluster(scored_articles)

        print("Events created:", len(events))

        summarized_events = []

        for event in events:
            event = self.summarizer.summarize(event)
            summarized_events.append(event)

        ranked_events = self.ranker.rank(summarized_events)

        important_events = self.highlights.select(
            ranked_events
        )

        brief = self.brief_builder.build(
            ranked_events,
            important_events,
        )

        return brief