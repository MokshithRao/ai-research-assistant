from transformers import pipeline

class SummarizerAgent:
    """
    Summarizes text using a transformer model.
    """

    def __init__(self, model_name="facebook/bart-large-cnn"):
        print("🔧 Loading summarization model... (first time may take 1–2 min)")
        self.summarizer = pipeline("summarization", model=model_name)

    def summarize_text(self, text, max_length=130, min_length=30):
        """
        Generate a concise summary for a given text.
        """
        if len(text.split()) < 50:
            # Skip summarizing very short texts
            return text

        summary = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]['summary_text']

        return summary
