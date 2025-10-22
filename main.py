from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.insight_agent import InsightAgent

if __name__ == "__main__":
    # Initialize agents
    search_agent = SearchAgent(max_results=3)
    summarizer_agent = SummarizerAgent()
    insight_agent = InsightAgent()

    # Step 1: Search for papers
    # query = "natural language processing"
    query = input("Enter your research topic:")
    papers = search_agent.search_papers(query)

    # Step 2: Print search results
    print("\n🔍 Search Results:\n")
    for i, paper in enumerate(papers, 1):
        print(f"{i}. {paper['title']}")
        print(f"   🔗 {paper['link']}")
        print(f"   🧾 Abstract: {paper['summary'][:250]}...\n")

    # Step 3: Summarize each paper
    print("\n📝 Summarized Papers:\n")
    summaries = []
    for i, paper in enumerate(papers, 1):
        if paper.get('summary'):
            summary = summarizer_agent.summarize_text(paper['summary'])
            summaries.append(summary)
            print(f"{i}. {paper['title']}")
            print(f"   🧾 Summary: {summary}\n")

    # Step 4: Generate overall insights
    print("\n💡 Overall Insights Across Papers:\n")
    insights = insight_agent.analyze(summaries)
    print(insights)
