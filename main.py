from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent

if __name__ == "__main__":
    search_agent = SearchAgent(max_results=2)
    summarizer_agent = SummarizerAgent()

    query = "transformers in NLP"
    results = search_agent.search_papers(query)

    print("\n🔍 Search Results with Summaries:\n")
    for i, paper in enumerate(results, 1):
        print(f"{i}. {paper['title']}")
        print(f"   🔗 {paper['link']}")
        summary = summarizer_agent.summarize_text(paper['summary'])
        print(f"   🧾 Summary: {summary}\n")
