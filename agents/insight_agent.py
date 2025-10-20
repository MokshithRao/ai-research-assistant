import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class InsightAgent:
    """Analyzes multiple paper summaries and produces overall insights."""

    def __init__(self):
        self.name = "InsightAgent"

    def analyze(self, summaries):
        """Generate insights and key takeaways from a list of paper summaries."""
        if not summaries:
            return "No summaries available for analysis."

        combined_text = "\n\n".join(
            [f"{i+1}. {s}" for i, s in enumerate(summaries)]
        )

        prompt = f"""
        You are an AI research assistant that synthesizes insights across papers.

        Below are summaries of several recent NLP papers:
        {combined_text}

        Please provide:
        1. Common research themes or trends
        2. Key technical approaches
        3. Any noteworthy differences or future directions

        Respond clearly and concisely in bullet points.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # <--- change here
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )


        return response.choices[0].message.content.strip()
