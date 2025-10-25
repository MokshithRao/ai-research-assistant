# 🧠 AI Research Assistant

An intelligent research assistant that automatically searches, summarizes, and extracts insights from recent research papers on any topic.  
Built using **Python**, Hugging Face Inference API, and arXiv.

---

## 🚀 Features

- **🔍 Search** — Automatically fetches recent papers from [arXiv.org](https://arxiv.org) based on a given query.
- **🧾 Summarize** — Generates short, clear summaries of abstracts using transformer models.
- **💡 Insights** — Analyzes multiple papers together and extracts common trends, key findings, and observations.
- **⚙️ Modular Design** — Clean separation between agents (search, summarize, insight).
- **💬 User Input** — Allows any user to enter a research topic dynamically.

---

## 🗂️ Project Structure

```
ai-research-assistant/
├─ agents/                   # agent implementations (search, summarize, insight)
│  ├─ search_agent.py
│  ├─ summarizer_agent.py
│  └─ insight_agent.py
├─ app.py                    # Streamlit UI
├─ main.py                   # CLI runner / pipeline orchestrator
├─ tests/                    # Unit and integration tests
├─ utils/                    # small helpers (sanitization, moderation)
├─ logs/                     # runtime logs (should be gitignored)
├─ requirements.txt          # minimal runtime dependencies (Streamlit + core libs)
├─ requirements-dev.txt      # dev dependencies (pytest, linters)
├─ .env.example              # sample env vars (copy to .env locally)
├─ README.md
```

---

## 🧩 Installation & Setup

**1️⃣ Clone the Repository**
```bash
git https://github.com/MokshithRao/ai-research-assistant.git
cd ai-research-assistant
```

**2️⃣ Create Virtual Environment**
```bash
python -m venv venv
venv\Scripts/activate      # On Windows
source venv/bin/activate   # On macOS/Linux
```

**3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

**4️⃣ Add API Key**
Create a `.env` file in the project root with:
```
HUGGINGFACE_API_KEY=hf_your_actual_key_here
```
Get your API key from 👉 [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

Tip: A sample env file is provided as `.env.sample` — copy it to `.env` and fill in your keys.


For development (tests, linters, and formatters), install the dev dependencies:

```powershell
pip install -r requirements-dev.txt
```

---

## 📈 How It Works (Workflow)

```text
           ┌──────────────────────────┐
           │      User Input          │
           │  (Enter research topic)  │
           └────────────┬─────────────┘
                        │
                        ▼
           ┌──────────────────────────┐
           │   SearchAgent (arXiv)    │
           │ Fetch top relevant papers│
           └────────────┬─────────────┘
                        │
                        ▼
           ┌──────────────────────────┐
           │ SummarizerAgent (HF LLM) │
           │ Summarize each abstract  │
           └────────────┬─────────────┘
                        │
                        ▼
           ┌──────────────────────────┐
           │ InsightAgent (HF LLM)    │
           │ Extract overall insights │
           └────────────┬─────────────┘
                        │
                        ▼
           ┌──────────────────────────┐
           │ Display summarized output│
           │   & high-level insights  │
           └──────────────────────────┘
```

---

## ▶️ Run the Assistant

```bash
python main.py
```

You’ll be prompted to enter any research topic:
```
🤖 Welcome to AI Research Assistant!
🔍 Enter a research topic: quantum computing in medicine
```

---

## 📊 Example Output

> 🔍 Searching for papers on: quantum computing in medicine  
>
> 1. **Quantum Computing for Drug Discovery**  
>    🧾 Summary: This paper explores the application of quantum algorithms...
>
> 2. **Hybrid Quantum-Classical Systems for Biomedical Data**  
>    🧾 Summary: The study investigates quantum machine learning models...
>
> 💡 **Overall Insights Across Papers:**  
> Quantum computing shows growing potential in medical research...

---

## 🧠 Tech Stack

- **Language:** Python 3.10+
- **APIs:** Hugging Face Inference API, arXiv API
- **Libraries:**
  - requests
  - transformers
  - huggingface_hub
  - python-dotenv
  - beautifulsoup4

---

## ⚠️ Notes

If you encounter model not supported for text-generation, try a different model like:

- meta-llama/Llama-3.1-8B-Instruct
- mistralai/Mixtral-8x7B-Instruct-v0.1

Ensure your Hugging Face token has Inference API permissions.

---

## 📚 Future Enhancements

- 🧩 Add fact-checking agent for claim validation.
- 🔍 Use semantic search (RAG) for contextual retrieval.
- 💻 Implement web UI using Streamlit or Gradio.
- 🐳 Add Docker support for deployment.

## ▶️ Running the Streamlit UI

This project is primarily designed to be used via the included Streamlit app (`app.py`). To run it locally:

```powershell
pip install -r requirements.txt
# (optional) set HF key for full features
$env:HUGGINGFACE_API_KEY = "hf_your_key_here"
streamlit run app.py
```

Open your browser at http://127.0.0.1:8501 to access the UI.



