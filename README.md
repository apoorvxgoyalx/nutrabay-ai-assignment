# 🎓 AI SOP Training Generator

Transform any Standard Operating Procedure (SOP) document into a complete employee training module — automatically.

**Powered by:** Groq API (free) · LLaMA 3 70B · Streamlit · Python

---

## 🚀 Quick Start

### 1. Clone / download the project

```bash
git clone <your-repo> sop_trainer
cd sop_trainer
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → Create a new key (starts with `gsk_`)

### 5. Set your API key (choose one method)

**Option A — Environment variable (recommended):**
```bash
# macOS/Linux
export GROQ_API_KEY="gsk_your_key_here"

# Windows Command Prompt
set GROQ_API_KEY=gsk_your_key_here

# Windows PowerShell
$env:GROQ_API_KEY="gsk_your_key_here"
```

**Option B — Enter directly in the app sidebar** (no setup needed)

### 6. Run the app

```bash
streamlit run ui.py
```

The app opens automatically at `http://localhost:8501`

---

## 📁 Project Structure

```
sop_trainer/
├── ui.py              # Main Streamlit application (entry point)
├── pdf_parser.py      # PDF extraction & text preprocessing
├── llm_handler.py     # Groq API integration & prompt engineering
├── export_utils.py    # PDF & PPTX export functionality
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 🔧 Features

| Feature | Details |
|---|---|
| **PDF Upload** | Extract text from any text-based PDF |
| **Text Input** | Paste SOP text directly |
| **AI Summary** | Overview, key objectives, important rules |
| **Training Module** | 4–8 step-by-step training steps with examples |
| **Quiz** | 5 questions (MCQ + scenario-based) with answers |
| **PDF Export** | Download formatted PDF training document |
| **PPTX Export** | Download PowerPoint presentation |
| **JSON Export** | Raw structured data for further processing |

---

## 🤖 Supported Models (all free via Groq)

| Model | Speed | Quality |
|---|---|---|
| LLaMA 3 70B | Medium | ⭐⭐⭐⭐⭐ Best |
| LLaMA 3 8B | Fast | ⭐⭐⭐⭐ |
| Mixtral 8x7B | Fast | ⭐⭐⭐⭐ |
| Gemma 7B | Fastest | ⭐⭐⭐ |

---

## ⚠️ Troubleshooting

**"No text could be extracted from the PDF"**  
→ Your PDF may be scanned/image-based. Copy-paste the text instead.

**"Invalid Groq API key"**  
→ Double-check your key starts with `gsk_` and has no spaces.

**"Rate limit hit"**  
→ Groq free tier has rate limits. Wait 30 seconds and try again.

**Export buttons not working**  
→ Run `pip install reportlab python-pptx` to enable export features.

---

## 📝 Notes

- This app uses **no paid APIs** — Groq is completely free for development use
- Your SOP text is sent to Groq's servers for processing but is **not stored**
- Very long SOPs (>12,000 characters) are automatically truncated to fit the model's context window
