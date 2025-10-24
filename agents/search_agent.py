import requests
import feedparser
import time

class SearchAgent:
    BASE_URL = "https://export.arxiv.org/api/query"

    def __init__(self, max_results=3):
        self.max_results = max_results

    def search_papers(self, query):
        params = {
            "search_query": query,
            "start": 0,
            "max_results": self.max_results
        }

        # 🧱 Retry with exponential backoff for resilience
        for attempt in range(3):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=10)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                print(f"⚠️ Attempt {attempt+1}/3 failed: {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)  # wait 1s, then 2s
                else:
                    # ❌ Return graceful fallback
                    return [{
                        "title": "Connection Error",
                        "summary": "Could not connect to arXiv. Please check your network or try a different topic.",
                        "link": ""
                    }]

        # 🧠 Parse XML safely
        feed = feedparser.parse(response.text)
        if not feed.entries:
            return [{
                "title": "No Results Found",
                "summary": f"No papers found for topic: {query}. Try refining your search.",
                "link": ""
            }]

        # ✅ Extract top N results
        results = []
        for entry in feed.entries:
            results.append({
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link
            })
        return results
