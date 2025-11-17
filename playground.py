# import openai
# from dotenv import load_dotenv
# load_dotenv()

# from fastapi.middleware.cors import CORSMiddleware

# from phi.agent import Agent
# from phi.model.groq import Groq
# from phi.playground import Playground, serve_playground_app
# from phi.tools import Tool

# import yfinance as yf
# from duckduckgo_search import DDGS


# # -------------------------
# # Custom Tools (Playground Safe)
# # -------------------------

# def simple_web_search(query: str):
#     with DDGS() as ddgs:
#         results = ddgs.text(query, max_results=5)
#     return {"results": results}

# WebSearchTool = Tool(
#     name="web_search",
#     description="Search the web using DuckDuckGo",
#     type="function",
#     func=simple_web_search
# )


# def simple_finance(symbol: str):
#     stock = yf.Ticker(symbol)
#     price = stock.history(period="1d")["Close"].iloc[-1]
#     news = stock.news[:5] if stock.news else []
#     return {
#         "symbol": symbol,
#         "price": float(price),
#         "news": news
#     }

# FinanceTool = Tool(
#     name="finance_data",
#     description="Get stock info and recent news",
#     type="function",
#     func=simple_finance
# )


# # -------------------------
# # Agents
# # -------------------------

# web_search_agent = Agent(
#     name="Web Search Agent",
#     role="Search the web for information",
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[WebSearchTool],
#     instructions=["Always include sources."],
#     show_tool_calls=True,
#     markdown=True,
# )

# finance_agent = Agent(
#     name="Finance AI Agent",
#     role="Analyze stock price and market news",
#     model=Groq(id="llama-3.3-70b-versatile"),
#     tools=[FinanceTool],
#     instructions=["Use tables to display financial data."],
#     show_tool_calls=True,
#     markdown=True,
# )

# print("Loaded agents:", [a.name for a in [finance_agent, web_search_agent]])


# # -------------------------
# # Playground App
# # -------------------------

# app = Playground(agents=[finance_agent, web_search_agent]).get_app()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # -------------------------
# # Run Server
# # -------------------------

# if __name__ == "__main__":
#     serve_playground_app("playground:app", host="127.0.0.1", port=7777, reload=True)
