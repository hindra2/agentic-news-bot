import trafilatura
import feedparser
import httpx

ollama_url = "http://localhost:11434/api/generate"
model = "ministral-3:8b"

feeds = [
    "https://feeds.npr.org/1001/rss.xml",
]

def get_article_text(url: str) -> str:
    downloaded = trafilatura.fetch_url(url)
    return trafilatura.extract(downloaded)

def fetch_articles() -> list[dict]:
    articles = []
    for feedurl in feeds:
        feed = feedparser.parse(feedurl)
        for entry in feed.entries[:3]:
            text = get_article_text(entry.link)
            if text:
                articles.append(
                    {
                        "title": entry.title,
                        "url": entry.link,
                        "text": text
                    }
                )
    return articles

def summarize(text: str) -> str:
    response = httpx.post(ollama_url, json={
        "model": model,
        "prompt": f"Summarize this news article in 2-3 sentences:\n\n{text}",
        "stream": False
    }, timeout=60)

    return response.json()["response"]
