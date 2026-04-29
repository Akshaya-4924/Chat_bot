# 🤖 Agentic AI System — Assignment Setup Guide

## What Changed from the Assignment?
The assignment used **Google Gemini API** (paid). This project uses **Groq** instead — it's **100% free**, faster, and works identically with LangChain.

---

## 🆓 Step 1: Get Your FREE API Keys

### Groq API Key (replaces Google Gemini)
1. Go to → https://console.groq.com
2. Sign up (free, no credit card needed)
3. Click **"API Keys"** → **"Create API Key"**
4. Copy the key

### Tavily API Key (same as assignment)
1. Go to → https://app.tavily.com
2. Sign up (free tier: 1000 searches/month)
3. Copy your API key from the dashboard

---

## 🔧 Step 2: Set Up Environment

```bash
# 1. Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# 2. Install all dependencies
pip install -r requirements.txt
```

---

## 🔑 Step 3: Add API Keys

Open the `.env` file and replace the placeholder values:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Step 4: Run the App

```bash
streamlit run app.py
```

Open your browser at → http://localhost:8501

---

## 📁 Project Structure

```
agentic_ai_agent/
├── app.py          ← Streamlit UI
├── agent.py        ← LangGraph agent (Planner, Search, Code Writer, Executor, Response Generator)
├── requirements.txt
├── .env            ← Your API keys (never commit this!)
└── README.md
```

---

## 🧠 How It Works

```
User Question
     │
     ▼
  PLANNER  ─── decides ──▶  "search" ──▶ Tavily Search ──────┐
     │                                                          │
     └─────────────────────▶  "code"  ──▶ Code Writer         │
                                              │                 │
                                              ▼                 │
                                        Code Executor          │
                                              │                 │
                                              ▼                 ▼
                                       Response Generator
                                              │
                                              ▼
                                       Final Answer + Sources/Output
```

---

## ✅ Example Queries to Test

| Query | Tool Used |
|-------|-----------|
| "What is Bitcoin's price today?" | 🔍 Web Search |
| "Calculate compound interest ₹5000 at 7% for 3 years" | 💻 Code |
| "Latest news about AI in 2025" | 🔍 Web Search |
| "Is 97 a prime number? Write code to check" | 💻 Code |
| "What is the capital of Australia?" | 🔍 Web Search |

---

## ⚠️ Troubleshooting

**ModuleNotFoundError**: Run `pip install -r requirements.txt` again inside your venv.

**Invalid API Key error**: Double-check your `.env` file has no spaces around `=`.

**Tavily returns no results**: Your free quota might be used up — check app.tavily.com dashboard.

**Code execution timeout**: The executor has a 15-second limit. Simplify the code request.
