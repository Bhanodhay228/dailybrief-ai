from app.web_search import WebSearchClient


client = WebSearchClient()

results = client.search_news(
    query="latest major news in India today",
    max_results=5,
)

print("Tavily search working!")
print("Number of results:", len(results.get("results", [])))

for result in results.get("results", []):
    print("\nTitle:", result.get("title"))
    print("URL:", result.get("url"))