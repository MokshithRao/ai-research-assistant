from transformers import pipeline, logging
import torch

class SummarizerAgent:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        # Disable unwanted HF warnings globally
        logging.set_verbosity_error()

        device = 0 if torch.cuda.is_available() else -1
        print(f"Device set to use {'GPU' if device == 0 else 'CPU'}")

        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            device=device
        )
        print(f"🧠 Summarizer model ready: {model_name}")

    def summarize_text(self, text):
        """Summarize text with adaptive max_length and no warning spam."""
        text = text.strip()
        if not text:
            return "⚠️ No text provided for summarization."

        input_len = len(text.split())

        # Dynamic summarization length
        max_length = min(130, max(40, int(input_len * 0.8)))
        min_length = max(20, int(max_length * 0.4))

        try:
            result = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
            )

            # ✅ Extract the actual text (not the dict)
            summary = result[0].get("summary_text", "").strip()
            return summary if summary else "⚠️ Empty summary returned."

        except Exception as e:
            print(f"❌ Summarization failed: {e}")
            return "Summarization failed."

