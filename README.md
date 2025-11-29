# Agentic Financial AI Assistant

A fully interactive **AI-powered financial analysis assistant** built with **Streamlit**, **OpenAI GPT-4o**, **Phi Agents**, **yFinance**, **Google News**, and **DuckDuckGo Search**.

This project provides advanced financial insights such as:
- Stock price queries  
- 1-year & 10-year performance  
- Multi-stock comparisons  
- Real-time financial news  
- Analyst summaries  
- Interactive chat interface with typing animation  

---

## 🚀 Features

### 🔹 1. Chat-Based Financial Assistant UI
Modern Streamlit UI with chat bubbles, typing animation, and Markdown rendering.

### 🔹 2. Multi-Agent Architecture
Powered by Phi Agents:
- Supervisor Agent (router)
- Finance Agent
- Web Search Agent

### 🔹 3. Financial Tools
Includes:
- 1-year performance tool  
- Stock comparison tool  
- 10-year analysis tool  
- Multi-stock ranking tool  
- Google News tool  

### 🔹 4. Real-Time Streaming Responses
Typing animation effect for every generated answer.

### 🔹 5. Custom Modern UI
Built with custom CSS for a clean, premium feel.

---

## 📂 Project Structure

Agentic--AI/
│── app.py # Streamlit chat UI
│── financial_agent.py # Multi-agent supervisor + finance tools
│── google_news_tool.py # Google News scraping tool
│── playground.py # Optional test script
│── requirements.txt # Python dependencies
│── .gitignore
│── .devcontainer/ # Dev environment config
│── pycache/ # Auto-generated


---

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sbshihab24/Agentic--AI.git
cd Agentic--AI
```
### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```
