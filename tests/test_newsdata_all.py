from datetime import datetime

from app.news_api import NewsDataClient


client = NewsDataClient()

today = datetime.now().date()

articles = client.get_news_for_date(today)

print("Today's articles:", len(articles))

for article in articles[:20]:

    print(
        article.published_at,
        "|",
        article.source,
        "|",
        article.title,
    )