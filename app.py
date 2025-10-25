import streamlit as st
from agents.search_agent import SearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.insight_agent import InsightAgent

st.set_page_config(page_title="AI Research Assistant", page_icon="🧠", layout="wide")

st.title("🧠 AI Research Assistant")
st.write("Search, summarize, and gain insights from AI research papers.")

query = st.text_input("Enter your research topic (e.g., 'transformer models in NLP'):")

if st.button("Search and Analyze"):
    if not query.strip():
        st.error("Please enter a valid query.")
    else:
        with st.spinner("🔍 Searching papers..."):
            search = SearchAgent()
            papers = search.search_papers(query)

        st.success(f"Found {len(papers)} papers.")
        summaries = []
        summarizer = SummarizerAgent()

        for paper in papers:
            st.subheader(paper['title'])
            st.markdown(f"[View Paper]({paper['url']})")
            summary = summarizer.summarize_text(paper['summary'])
            summaries.append(summary)
            st.write(summary)
            st.divider()

        insight = InsightAgent()
        with st.spinner("💡 Generating insights..."):
            insights = insight.analyze(summaries)
        st.header("💡 Overall Insights")
        st.write(insights)
