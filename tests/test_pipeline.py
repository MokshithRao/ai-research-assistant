import pytest
from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.insight_agent import InsightAgent

def test_full_pipeline():
    query = "artificial intelligence ethics"

    search_agent = SearchAgent(max_results=1)
    summarizer_agent = SummarizerAgent()
    insight_agent = InsightAgent()

    results = search_agent.search_papers(query)
    assert results, "Search returned no results"

    summaries = [summarizer_agent.summarize_text(r["summary"]) for r in results]
    insights = insight_agent.analyze(summaries)

    assert isinstance(insights, str)
    assert len(insights) > 10
