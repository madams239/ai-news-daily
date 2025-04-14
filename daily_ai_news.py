import feedparser
from datetime import datetime

feeds = [
    "https://news.google.com/rss/search?q=artificial+intelligence",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/artificial-intelligence/rss/index.xml"
]

today = datetime.today().date()
headlines = []

for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        pub_date = entry.published_parsed
        entry_date = datetime(*pub_date[:6]).date()
        if entry_date == today:
            headlines.append(f"{entry.title}\n{entry.link}\n")

if headlines:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(headlines))
else:
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write("No new AI headlines today.")
