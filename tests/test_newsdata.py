from app.news_api import NewsDataClient


client = NewsDataClient()

news = client.get_latest_news()

print("News API working!")
print("Number of results:", len(news.get("results", [])))

for article in news.get("results", [])[:3]:
    print("\nTitle:", article.get("title"))
    print("Source:", article.get("source_name"))
    print("URL:", article.get("link"))