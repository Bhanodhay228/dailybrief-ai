from app.pipeline import DailyBriefPipeline


pipeline = DailyBriefPipeline()

brief = pipeline.run()


print("\n" + "=" * 60)
print("🚨 YOU SHOULD KNOW")
print("=" * 60)

for event in brief["important"]:
    print("\n", event.title)
    print("Importance:", event.importance)
    print(event.summary)


print("\n" + "=" * 60)
print("🔥 HIGH PRIORITY")
print("=" * 60)

for event in brief["high"]:
    print("\n", event.title)
    print("Category:", event.category)
    print("Importance:", event.importance)


print("\n" + "=" * 60)
print("📰 MEDIUM PRIORITY")
print("=" * 60)

for event in brief["medium"]:
    print("\n", event.title)
    print("Category:", event.category)
    print("Importance:", event.importance)


print("\n" + "=" * 60)
print("📌 LOW PRIORITY")
print("=" * 60)

for event in brief["low"]:
    print("\n", event.title)
    print("Category:", event.category)
    print("Importance:", event.importance)