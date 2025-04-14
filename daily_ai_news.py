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
            headlines.append((entry.title, entry.link))

# Create plaintext file (still useful)
with open("output.txt", "w", encoding="utf-8") as f:
    if headlines:
        for title, link in headlines:
            f.write(f"{title}\n{link}\n\n")
    else:
        f.write("No new AI headlines today.")

# Create HTML-formatted email body
html_content = "<h2>🧠 Your Daily AI News Digest</h2><ul>"
for title, link in headlines:
    html_content += f'<li><a href="{link}">{title}</a></li>'
html_content += "</ul>"

if not headlines:
    html_content = "<p>No new AI news today.</p>"

with open("email_body.html", "w", encoding="utf-8") as f:
    f.write(html_content)
