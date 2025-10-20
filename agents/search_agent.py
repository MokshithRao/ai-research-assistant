import requests

class SearchAgent:
    """
    Searches research papers from the arXiv API.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, max_results=5):
        self.max_results = max_results

    def search_papers(self, query):
        """
        Search for papers related to a query string.
        """
        params = {
            "search_query": query,
            "start": 0,
            "max_results": self.max_results
        }
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}")

        data = response.text
        return self._parse_results(data)

    def _parse_results(self, raw_xml):
        """
        Extracts title, summary, and link from raw XML results.
        """
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw_xml)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        results = []

        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip()
            link = entry.find('atom:id', ns).text.strip()
            results.append({
                "title": title,
                "summary": summary,
                "link": link
            })

        return results
