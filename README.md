# LangGraph Chatbot

An intelligent, stateful chatbot built with **LangGraph**, **Google Gemini**, and **Streamlit**. This repository demonstrates building conversational AI from basic memory graphs to multi-session streaming chatbots backed by persistent SQLite storage.

---

## 🌟 Key Features

- **LangGraph StateGraph Architecture**: Clean, cyclical and extensible graph-based conversational flow.
- **Persistent Memory Checkpointing**: Uses `SqliteSaver` to store conversations across app restarts.
- **Multi-Turn & Multi-Session Support**: Create, manage, and switch between multiple distinct chat threads via a sidebar UI.
- **Real-Time Token Streaming**: Streams generated tokens from the LLM in real-time using Streamlit's `write_stream`.
- **Google Gemini Integration**: Powered by `ChatGoogleGenerativeAI` (`gemini-1.5-flash` / `gemini-2.5-flash` models).

---

## 📁 Project Structure

| File | Description |
|---|---|
| `langgraph_backend.py` | Core LangGraph graph with in-memory checkpointer (`InMemorySaver`). |
| `langgraph_database_backend.py` | Production-ready LangGraph backend with SQLite checkpointer (`SqliteSaver`) and thread listing utilities. |
| `streamlit_frontend.py` | Basic Streamlit UI for single-thread conversations. |
| `streamlit_frontend_streaming.py` | Streamlit UI demonstrating real-time token streaming. |
| `streamlit_frontend_threading.py` | Streamlit UI supporting multiple active chat sessions (thread management). |
| `streamlit_frontend_database.py` | Complete Streamlit app with persistent SQLite thread storage, history restoration, and new chat creation. |
| `requirements.txt` | Python dependencies required to run the project. |
| `.env.example` | Template for environment variables (Google Gemini API key). |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Sid-LD/LangGraph-Chatbot.git
cd LangGraph-Chatbot
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv myenv
.\myenv\Scripts\activate

# macOS / Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and insert your Gemini API Key:
```bash
cp .env.example .env
```
In `.env`:
```env
GEMINI_API_KEY="your-google-gemini-api-key"
```

---

## 💻 Running the Applications

You can run any of the frontend variants depending on what you want to explore:

### Persistent SQLite Multi-Thread Chatbot (Recommended)
```bash
streamlit run streamlit_frontend_database.py
```

### Streaming Chatbot
```bash
streamlit run streamlit_frontend_streaming.py
```

### Basic Chatbot
```bash
streamlit run streamlit_frontend.py
```

---

## 🛠️ Tech Stack

- **Framework**: [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain Core](https://github.com/langchain-ai/langchain)
- **Model**: Google Gemini (`langchain-google-genai`)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Database / Checkpointing**: SQLite (`langgraph-checkpoint-sqlite`)
- **Environment**: Python 3.10+

---

## 📝 License
This project is open-source and available under the [MIT License](LICENSE).
