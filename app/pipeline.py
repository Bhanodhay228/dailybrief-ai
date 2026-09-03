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
from app.qa import NewsQA
from app.conversation import ConversationManager


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
        self.brief_builder = DailyBriefBuilder(
            self.preferences
        )

        self.qa = NewsQA()
        self.conversation = ConversationManager()

    def run(self):

        articles = self.news_client.get_latest_news(
            limit=10
        )

        print(
            "Articles retrieved:",
            len(articles)
        )

        articles = self.deduplicator.remove_duplicates(articles)

        print("After deduplication:", len(articles))

        # Batch categorization
        articles = self.categorizer.categorize_many(
            articles
        )

        # Batch importance scoring
        articles = self.importance_scorer.score_many(
            articles
        )

        # Cluster related articles into events
        events = self.clusterer.cluster(articles)

        print("Events created:", len(events))

        summarized_events = self.summarizer.summarize_many(
            events
        )

        # Rank events according to user preferences
        ranked_events = self.ranker.rank(
            summarized_events
        )

        # Find major events
        important_events = self.highlights.select(
            ranked_events
        )

        # Build personalized brief
        brief = self.brief_builder.build(
            ranked_events,
            important_events,
        )

        return brief
    def answer_question(
    self,
    question: str,
    event,
):

        history = self.conversation.get_history()

        answer = self.qa.answer(
            question,
            event,
            history,
        )

        self.conversation.add_user_message(
            question
        )

        self.conversation.add_assistant_message(
            answer
        )

        return answer