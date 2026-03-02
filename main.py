from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feeds

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    articles = feeds.fetch_articles()
    results = []
    for article in articles:
        summary = feeds.summarize(article["text"])
        results.append({
            "title": article['title'],
            "url": article['url'],
            "summary": summary
        })

    return results
