from app.web_search import WebSearchClient


client = WebSearchClient()

articles = client.search_news(
    query="latest major news in India today",
    max_results=5,
)

print("Tavily search working!")
print("Number of articles:", len(articles))

for article in articles:
    print("\nTitle:", article.title)
    print("Source:", article.source)
    print("URL:", article.url)