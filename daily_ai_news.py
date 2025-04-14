from urllib.parse import urlparse
import feedparser
from datetime import datetime

# ✅ List of trusted domains
trusted_domains = [
    "openai.com", "anthropic.com", "deepmind.com", "ai.google", "blog.google", "google.com",
    "microsoft.com", "huggingface.co", "x.ai", "mistral.ai", "cohere.com", "stability.ai",
    "nvidia.com", "developer.nvidia.com", "aws.amazon.com", "apple.com",
    "research.ibm.com", "ibm.com", "salesforce.com", "blog.adobe.com",
    "intel.com", "oracle.com", "palantir.com", "databricks.com", "zoom.us",
    "damo.alibaba.com", "ai.baidu.com", "ai.tencent.com", "huawei.com",
    "research.samsung.com", "lgai.lge.com", "cerebras.net", "anduril.com",
    "safesuperintelligence.com", "csail.mit.edu", "bair.berkeley.edu", "ai.cs.cmu.edu", "allenai.org"
]

# ✅ Function to check if a URL is from a preferred source
def is_preferred_source(url: str) -> bool:
    try:
        domain = urlparse(url).netloc.replace("www.", "").lower()
        if domain.endswith(".gov") or domain.endswith(".edu"):
            return True
        return any(domain.endswith(trusted) for trusted in trusted_domains)
    except Exception:
        return False

# RSS feeds to pull from
feeds = [
    "https://news.google.com/rss/search?q=artificial+intelligence",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/artificial-intelligence/rss/index.xml"
]

# Today's date
today = datetime.today().date()
headlines = []

# Parse feeds and filter by date and trusted sources
for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        pub_date = entry.published_parsed
        entry_date = datetime(*pub_date[:6]).date()
        if entry_date == today and is_preferred_source(entry.link):
            headlines.append((entry.title, entry.link))

# Save to output.txt
with open("output.txt", "w", encoding="utf-8") as f:
    if headlines:
        for title, link in headlines:
            f.write(f"{title}\n{link}\n\n")
    else:
        f.write("No new AI headlines today from preferred sources.")

# Save to email_body.html
if headlines:
    html_content = "<h2>🧠 Your Daily AI News Digest</h2><ul>"
    for title, link in headlines:
        html_content += f'<li><a href="{link}">{title}</a></li>'
    html_content += "</ul>"
else:
    html_content = "<p>No new AI news today from preferred sources.</p>"

with open("email_body.html", "w", encoding="utf-8") as f:
    f.write(html_content)
