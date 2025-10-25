import requests
import feedparser
import time
import logging
from typing import List, Dict

# Setup logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SearchAgent:
    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0, timeout: int = 10):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout

    def search_papers(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search for research papers on arXiv based on the query with retry and error handling."""
        if not query or len(query.strip()) < 2:
            logging.warning("Empty or invalid search query.")
            return [{"title": "Invalid Search Query", "summary": "Please enter a valid topic.", "url": "#"}]

        params = {"search_query": query, "start": 0, "max_results": max_results}

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
                response.raise_for_status()

                feed = feedparser.parse(response.text)
                entries = feed.entries

                if not entries:
                    logging.info(f"No results found for topic: {query}")
                    return [{"title": "No Results Found", "summary": f"No papers found for topic: {query}. Try refining your search.", "url": "#"}]

                papers = [
                    {
                        "title": entry.title,
                        "summary": entry.summary[:500] + "...",
                        "url": entry.link
                    }
                    for entry in entries
                ]

                logging.info(f"Found {len(papers)} papers for topic: {query}")
                return papers

            except requests.exceptions.RequestException as e:
                logging.error(f"Attempt {attempt}: Failed to fetch from arXiv API - {e}")
                if attempt < self.max_retries:
                    sleep_time = self.backoff_factor ** attempt
                    logging.info(f"Retrying in {sleep_time:.1f}s...")
                    time.sleep(sleep_time)
                else:
                    logging.critical(f"All retries failed for topic: {query}")
                    return [{"title": "Connection Error", "summary": f"Failed to connect to arXiv after {self.max_retries} attempts. Please try again later.", "url": "#"}]
