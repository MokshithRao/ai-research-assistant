import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load .env variables
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

print("🔑 Loaded Hugging Face API key:", HF_API_KEY[:10] + "..." if HF_API_KEY else "❌ Not found")


class InsightAgent:
    def __init__(self, model_name="mistralai/Mixtral-8x7B-Instruct-v0.1"):
        if not HF_API_KEY:
            raise ValueError("Hugging Face API key not found. Please set HUGGINGFACE_API_KEY in your .env file")

        self.client = InferenceClient(model=model_name, token=HF_API_KEY)
        print(f"🧠 Insight model ready: {model_name}")

    def analyze(self, summaries):
        """Generate overall insights from summarized research papers."""
        if not summaries:
            return "No summaries provided for analysis."

        combined = "\n\n".join(summaries)

        prompt = f"""You are an AI research assistant.
Given the following research paper summaries, identify:
- The common themes or trends
- Differences in methodology or findings
- Overall insights or conclusions

Summaries:
{combined}

Provide your insights in a concise, academic paragraph format."""

        print("\n🧠 Generating insights... (this may take a few seconds)\n")

        try:
            # ✅ Use chat.completions for Mixtral
            response = self.client.chat.completions.create(
                model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "You are an expert AI research assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7,
            )

            return response.choices[0].message["content"].strip()

        except Exception as e:
            print("❌ Error generating insights:", e)
            return "Insight generation failed due to an API error."