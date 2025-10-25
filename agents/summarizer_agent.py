import os

from transformers import logging

try:
    # Optional imports - may fail in minimal/test environments
    import torch
    from transformers import pipeline
except Exception:
    pipeline = None
    torch = None


class SummarizerAgent:
    """SummarizerAgent with lazy model initialization and a safe offline fallback.

    - If a `summarizer` callable is provided, it will be used.
    - If transformers is available, the pipeline is created lazily on first use.
    - If the pipeline cannot be created, a simple offline fallback returns the
      first N tokens/sentences to keep the system usable in tests/demos.
    """

    def __init__(
        self, model_name="facebook/bart-large-cnn", summarizer=None, test_mode=False
    ):
        # Disable unwanted HF warnings globally when available
        try:
            logging.set_verbosity_error()
        except Exception:
            pass

        self.model_name = model_name
        self._summarizer = summarizer
        self._pipeline = None
        self.test_mode = test_mode

    def _init_pipeline(self):
        if self._summarizer is not None:
            return

        if pipeline is None:
            return

        try:
            device = 0 if torch is not None and torch.cuda.is_available() else -1
            self._pipeline = pipeline(
                "summarization",
                model=self.model_name,
                device=device,
            )
            print(f"🧠 Summarizer model ready: {self.model_name}")
        except Exception as e:
            print("⚠️ Failed to initialize summarizer pipeline:", e)
            self._pipeline = None

    def summarize_text(self, text):
        """Summarize text with adaptive max_length and graceful fallback."""
        text = (text or "").strip()
        if not text:
            return "⚠️ No text provided for summarization."

        # If an injected summarizer is provided, use it (useful for tests)
        if self._summarizer:
            try:
                return self._summarizer(text)
            except Exception as e:
                print("❌ Injected summarizer failed:", e)

        # Lazy initialization of transformers pipeline
        if self._pipeline is None and not self.test_mode:
            self._init_pipeline()

        input_len = len(text.split())
        max_length = min(130, max(40, int(input_len * 0.8)))
        min_length = max(20, int(max_length * 0.4))

        # Use HF pipeline when available
        if self._pipeline is not None:
            try:
                result = self._pipeline(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False,
                )
                summary = result[0].get("summary_text", "").strip()
                return summary if summary else "⚠️ Empty summary returned."
            except Exception as e:
                print(f"❌ Summarization failed: {e}")

        # Offline fallback: return a short extractive summary (first 2 sentences)
        sentences = text.split(".")
        if len(sentences) >= 2:
            fallback = ".".join(sentences[:2]).strip()
            if not fallback.endswith("."):
                fallback += "."
            return fallback
        # As a last resort, truncate to 60 words
        words = text.split()
        return " ".join(words[:60]) + ("..." if len(words) > 60 else "")
