import os

from dotenv import load_dotenv

# Optional import - only required when an actual HF client is used at runtime
try:
    from huggingface_hub import InferenceClient
except Exception:
    InferenceClient = None

# Load .env variables (if present)
load_dotenv()


class InsightAgent:
    """InsightAgent generates overall insights from summaries.

    Behavior:
    - If a preconfigured client is provided, it will be used.
    - Otherwise, the agent will try to create an InferenceClient using
      HUGGINGFACE_API_KEY from environment variables when analyze() is called.
    - If no HF key / client is available, a lightweight offline fallback
      is used so the system remains usable in test or demo environments.
    """

    def __init__(self, model_name="mistralai/Mixtral-8x7B-Instruct-v0.1", client=None):
        self.model_name = model_name
        self._provided_client = client
        self.client = client  # may be None; lazy-initialized in analyze()

    def _create_client(self):
        """Attempt to create a huggingface InferenceClient using env var.
        Returns None if the client cannot be created (no key or package).
        """
        if self._provided_client:
            return self._provided_client

        if InferenceClient is None:
            print(
                "⚠️ huggingface_hub not installed; running offline fallback for insights."
            )
            return None

        hf_key = os.getenv("HUGGINGFACE_API_KEY")
        if not hf_key:
            print(
                "⚠️ HUGGINGFACE_API_KEY not set; running offline fallback for insights."
            )
            return None

        try:
            client = InferenceClient(model=self.model_name, token=hf_key)
            print(f"🧠 Insight model ready: {self.model_name}")
            return client
        except Exception as e:
            print("❌ Failed to initialize InferenceClient:", e)
            return None

    def analyze(self, summaries):
        """Generate overall insights from summarized research papers.

        If no external LLM client is available, this method falls back to a
        simple offline summary that concatenates input summaries. This keeps
        the pipeline resilient for tests and demos while still allowing the
        full HF client to be used in production when configured.
        """
        if not summaries:
            return "No summaries provided for analysis."

        combined = "\n\n".join(summaries)

        # Ensure client is available (lazy init)
        if self.client is None:
            self.client = self._create_client()

        # If we have a real client, call it
        if self.client is not None:
            prompt = f"""You are an AI research assistant.
Given the following research paper summaries, identify:
- The common themes or trends
- Differences in methodology or findings
- Overall insights or conclusions

Summaries:
{combined}

Provide your insights in a concise, academic paragraph format."""

            print("\n🧠 Generating insights via HF InferenceClient...\n")
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert AI research assistant.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=300,
                    temperature=0.7,
                )

                return response.choices[0].message["content"].strip()

            except Exception as e:
                print("❌ Error generating insights via HF client:", e)
                return "Insight generation failed due to an API error."

        # Offline fallback: return a short combined insight so the pipeline is usable
        print("ℹ️ No HF client available — returning offline fallback insights.")
        snippet = combined[:800].strip()
        return f"Offline insights (fallback): {snippet if snippet else 'No content.'}"
