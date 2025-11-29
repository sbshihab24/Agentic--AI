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
```bash
Agentic--AI/
│
├── app.py                  # Streamlit chat UI
├── financial_agent.py      # Multi-agent supervisor + finance tools
├── google_news_tool.py     # Google News scraping tool
├── playground.py           # Optional test script
├── requirements.txt        # Python dependencies
├── .gitignore
│
├── .devcontainer/          # Dev environment config
│   └── (container files)
│
└── __pycache__/            # Auto-generated
```


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
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Your API Key
```bash
Create a .env file:
OPENAI_API_KEY=your_api_key_here
```
### ▶️ Run the App
```bash
streamlit run app.py
```

## 🧠 System Architecture

### 1. User Sends a Message
Passed from Streamlit UI (`app.py`).

### 2. Supervisor Agent Routes Tasks
- Finance questions → **Finance Agent**  
- News questions → **Web Search Agent**

### 3. Tools Fetch Real Data
Custom tools include:
- `one_year_tool`
- `compare_stocks_tool`
- `ten_year_analysis_tool`
- `compare_multi_stocks_tool`

### 4. Google News Tool
Fetches fresh news with clickable markdown links.

### 5. Response Streams Back
Character-by-character typing effect in the UI.

---

## 📈 Supported Queries

```yaml
supported_queries:
  - title: "Stock Price"
    example: "What is the current price of NVDA?"
  - title: "1-Year Performance"
    example: "Show me 1-year performance of AAPL."
  - title: "Compare Stocks"
    example: "Compare TSLA vs AMZN over 1 year."
  - title: "10-Year Analysis"
    example: "Give me a 10-year analysis of MSFT."
  - title: "Latest News"
    example: "What is the latest Google News about Bitcoin?"
  - title: "Multi Stock Ranking"
    example: "Compare: AAPL, MSFT, GOOG, NVDA over 10 years."

tech_stack:
  - layer: "Frontend"
    technology: "Streamlit"
  - layer: "AI Model"
    technology: "GPT-4o via OpenAI API"
  - layer: "Agent Framework"
    technology: "Phi Agents"
  - layer: "Financial Data"
    technology: "yFinance API"
  - layer: "News Search"
    technology: "GoogleNews, DuckDuckGo"
  - layer: "UI Rendering"
    technology: "markdown2, custom CSS"
  - layer: "Deployment Ready"
    technology: "Local / Cloud"

development_scripts:
  run_agent:
    command: "python playground.py"
    description: "Run the agent without UI."

contribution:
  guidelines: |
    Pull requests are welcome!
    Make sure code is clean and well-formatted.

license:
  type: "MIT License"
  permissions: "Free to use and modify."

author:
  name: "Mehedi Hasan Shihab"
  role: "AI Developer & Researcher"
  github: "https://github.com/sbshihab24"
```
