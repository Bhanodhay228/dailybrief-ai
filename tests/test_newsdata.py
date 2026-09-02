from app.news_api import NewsDataClient


client = NewsDataClient()

articles = client.get_latest_news()

print("News API working!")
print("Number of articles:", len(articles))

for article in articles[:3]:
    print("\nTitle:", article.title)
    print("Source:", article.source)
    print("URL:", article.url)
    print("Category:", article.category)