## 🌐 Live Demo

👉 **[Try Zeno AI Live](https://zeno-ai-vacvfnhdcghicxxxpp9wrj.streamlit.app/)**
A conversational AI chatbot built with **Streamlit**, **LangChain**, and **LangGraph**,
powered by **Groq's ultra-fast LLM inference**.

---

## 🚀 Features

- 💬 Multi-turn conversation with memory (per session)
- ⚡ Powered by Groq — blazing fast responses
- 🤖 Multiple model options (LLaMA, Mixtral)
- ✍️ Typewriter effect for bot replies
- 🆕 New Chat / Clear Chat support
- 🎨 Clean UI with custom chat bubbles

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Frontend     | Streamlit                         |
| LLM Backend  | Groq API (LLaMA 3, Mixtral)       |
| Agent Graph  | LangGraph + LangChain             |
| Memory       | LangGraph InMemorySaver           |
| Deployment   | Streamlit Cloud                   |

---

## 📁 Project Structure
zeno-ai/
│
├── .streamlit/
│   └── secrets.toml        # LOCAL ONLY — never push to GitHub
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── .gitignore              # Excludes secrets & cache
└── README.md               # You are here

---

## ⚙️ Setup — Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/zeno-ai.git
cd zeno-ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create the file `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxx"
```

> ⚠️ Never commit this file. It's already in `.gitignore`.

### 4. Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push your repo to GitHub (without `secrets.toml`)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) → **New app**
3. Select your repo and set `app.py` as the main file
4. Go to **Settings → Secrets** and add:

```toml
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxxxxxx"
```

5. Click **Deploy** ✅

---

## 📦 Requirements
streamlit
langchain-groq
langgraph
langchain-core
python-dotenv

---

## 🤖 Available Models

| Model                      | Best For                        |
|----------------------------|---------------------------------|
| `llama-3.1-8b-instant`     | Fast, lightweight responses     |
| `llama-3.3-70b-versatile`  | High quality, complex reasoning |
| `mixtral-8x7b-32768`       | Long context, multilingual      |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

> Made with ❤️ using Streamlit + Groq
