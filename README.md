# 🇮🇳 Government Scheme Finder

An AI-powered web application that helps Indian citizens find government schemes they are eligible for — instantly.

## 🚀 Features
- 🔍 AI scheme matching with confidence scores
- 💬 Chat mode — describe yourself naturally
- 📊 Side-by-side scheme comparison
- 👨‍👩‍👧 Family profile comparison
- 📁 Application tracker (Applied/Pending/Approved/Rejected)
- 📅 Scheme deadline alerts
- 📈 Personal dashboard with AI insights
- 🌐 3-language support — English, Telugu, Hindi
- 📄 PDF report download

## 🛠️ Tech Stack
- Python + Streamlit
- Groq API (LLaMA 3.3 70B)
- FPDF2 + Pandas

## ⚙️ Installation

1. Clone the repo:
```bash
   git clone https://github.com/YOURUSERNAME/government-scheme-finder.git
   cd government-scheme-finder
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Add your Groq API key in `app.py`:
```python
   client = Groq(api_key="YOUR_GROQ_API_KEY")
```

4. Run the app:
```bash
   streamlit run app.py
```

## 🌐 Live Demo
[Click here to try the app](https://your-app-link.streamlit.app)

## 📸 Built With
- [Streamlit](https://streamlit.io)
- [Groq](https://groq.com)
- [LLaMA 3.3](https://ai.meta.com/llama/)