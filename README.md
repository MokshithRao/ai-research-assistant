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
├─ agents/
│  ├─ search_agent.py        # Handles paper search (arXiv API)
│  ├─ summarizer_agent.py    # Summarizes abstracts using Hugging Face model
│  ├─ insight_agent.py       # Generates overall insights across papers
├─ main.py                   # Orchestrates the entire pipeline
├─ .env                      # Stores Hugging Face API key
├─ requirements.txt
└─ README.md
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

