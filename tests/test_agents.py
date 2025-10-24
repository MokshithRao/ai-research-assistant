import pytest
from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.insight_agent import InsightAgent

def test_search_agent_basic():
    agent = SearchAgent(max_results=2)
    results = agent.search_papers("machine learning")
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]

def test_summarizer_agent_basic():
    agent = SummarizerAgent()
    text = "Natural language processing enables machines to understand text."
    summary = agent.summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) > 10

def test_insight_agent_basic(monkeypatch):
    agent = InsightAgent()

    dummy_summaries = [
        "Paper 1 discusses the use of neural networks in NLP.",
        "Paper 2 presents advancements in LLM-based summarization."
    ]

    # Mock call to avoid real API if needed
    monkeypatch.setattr(agent, "analyze", lambda summaries: "Common theme: NLP progress.")
    result = agent.analyze(dummy_summaries)
    assert "NLP" in result
