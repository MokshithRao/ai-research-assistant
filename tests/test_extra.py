import os
import types

import pytest
import requests

from agents import insight_agent as ia_mod
from agents import search_agent as search_mod
from agents import summarizer_agent as sa_mod


def test_insight_agent_offline_fallback(monkeypatch):
    # Force InferenceClient to be unavailable and ensure no HF key
    monkeypatch.setattr(ia_mod, "InferenceClient", None)
    monkeypatch.delenv("HUGGINGFACE_API_KEY", raising=False)

    agent = ia_mod.InsightAgent()
    out = agent.analyze(["Paper A summary.", "Paper B summary."])
    assert out.startswith("Offline insights") or "Paper A" in out


def test_insight_agent_with_mock_client():
    # Create a mock HF-like client with the nested call structure
    def create(**kwargs):
        return types.SimpleNamespace(
            choices=[types.SimpleNamespace(message={"content": "  mocked insight  "})]
        )

    mock_client = types.SimpleNamespace(
        chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create))
    )

    agent = ia_mod.InsightAgent(client=mock_client)
    out = agent.analyze(["One summary."])
    assert "mocked insight" in out


def test_summarizer_injected_callable():
    agent = sa_mod.SummarizerAgent(summarizer=lambda t: "INJECTED")
    assert agent.summarize_text("any text") == "INJECTED"


def test_summarizer_offline_fallback_sentences():
    text = "First sentence. Second sentence. Third sentence."
    agent = sa_mod.SummarizerAgent(test_mode=True)
    out = agent.summarize_text(text)
    assert out.strip().endswith("Second sentence.")


def test_search_agent_no_results(monkeypatch):
    # Make feedparser.parse return no entries
    monkeypatch.setattr(
        search_mod,
        "feedparser",
        types.SimpleNamespace(parse=lambda x: types.SimpleNamespace(entries=[])),
    )
    agent = search_mod.SearchAgent()
    res = agent.search_papers("some topic")
    assert isinstance(res, list)
    assert "No Results Found" in res[0]["title"]


def test_search_agent_retry_failure(monkeypatch):
    # Make requests.get raise to trigger retry logic
    def bad_get(*args, **kwargs):
        raise requests.exceptions.RequestException("boom")

    # Replace only the requests.get function so exception types remain available
    monkeypatch.setattr(search_mod.requests, "get", bad_get)
    agent = search_mod.SearchAgent(max_retries=2)
    res = agent.search_papers("topic")
    assert isinstance(res, list)
    assert "Connection Error" in res[0]["title"]
