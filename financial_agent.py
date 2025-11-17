
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from google_news_tool import google_news_tool

from phi.tools import tool
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import math
import traceback
from GoogleNews import GoogleNews
from phi.tools import tool

load_dotenv()


# ---------------------------
# Internal helpers
# ---------------------------

def _safe_history(symbol: str, period: str = "1y"):
    """Fetch historical dataframe safely; raises ValueError on failure."""
    symbol = (symbol or "").upper().strip()
    if not symbol:
        raise ValueError("Empty symbol provided")

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
    except Exception as e:
        raise ValueError(f"yfinance error for {symbol}: {e}")

    if df is None or df.empty or "Close" not in df.columns:
        raise ValueError(f"No historical data available for {symbol} (period={period})")

    return df

def _cagr(start_price: float, end_price: float, years: float):
    if start_price <= 0 or years <= 0:
        return float("nan")
    return ((end_price / start_price) ** (1.0 / years) - 1.0) * 100.0

def _max_drawdown(series: pd.Series):
    # series expected to be price series
    roll_max = series.cummax()
    drawdown = (series - roll_max) / roll_max
    return drawdown.min() * 100.0  # as percentage (negative value)


# ---------------------------
# TOOL: 1-year performance
# ---------------------------

@tool
def one_year_tool(symbol: str):
    """
    Returns 1-year performance for a given stock symbol.
    Input: symbol: str (e.g., 'AAPL')
    Output: plain text (markdown friendly)
    """
    symbol = (symbol or "").upper().strip()
    try:
        df = _safe_history(symbol, period="1y")
        start = float(df["Close"].iloc[0])
        end = float(df["Close"].iloc[-1])
        pct = ((end - start) / start) * 100.0 if start != 0 else float("nan")
        txt = (
            f"# 1-Year Performance — {symbol}\n\n"
            f"- Start price: ${start:.2f}\n"
            f"- End price:   ${end:.2f}\n"
            f"- Change:      {pct:.2f}%\n\n"
            f"Reference: https://finance.yahoo.com/quote/{symbol}\n"
        )
        return txt
    except Exception as e:
        return f"Error fetching 1-year performance for {symbol}: {e}"


# ---------------------------
# TOOL: compare two stocks (1-year)
# ---------------------------

@tool
def compare_stocks_tool(symbol1: str, symbol2: str):
    """
    Compare two stocks over 1 year. Inputs: symbol1, symbol2.
    Returns a markdown summary with winner.
    """
    s1 = (symbol1 or "").upper().strip()
    s2 = (symbol2 or "").upper().strip()
    if not s1 or not s2:
        return "Please provide two symbols, e.g., symbol1=GOOG, symbol2=AMZN"

    try:
        df1 = _safe_history(s1, period="1y")
        df2 = _safe_history(s2, period="1y")

        s1_start, s1_end = float(df1["Close"].iloc[0]), float(df1["Close"].iloc[-1])
        s2_start, s2_end = float(df2["Close"].iloc[0]), float(df2["Close"].iloc[-1])

        s1_pct = ((s1_end - s1_start) / s1_start) * 100.0 if s1_start != 0 else float("nan")
        s2_pct = ((s2_end - s2_start) / s2_start) * 100.0 if s2_start != 0 else float("nan")

        winner = s1 if s1_pct > s2_pct else s2

        txt = (
            f"# 1-Year Comparison: {s1} vs {s2}\n\n"
            f"- {s1}: ${s1_start:.2f} → ${s1_end:.2f} ({s1_pct:.2f}%)\n"
            f"- {s2}: ${s2_start:.2f} → ${s2_end:.2f} ({s2_pct:.2f}%)\n\n"
            f"**Better performer:** {winner}\n\n"
            f"References:\n- https://finance.yahoo.com/quote/{s1}\n- https://finance.yahoo.com/quote/{s2}\n"
        )
        return txt
    except Exception as e:
        return f"Error comparing {s1} and {s2}: {e}"


# ---------------------------
# TOOL: 10-year analysis (detailed)
# ---------------------------

@tool
def ten_year_analysis_tool(symbol: str):
    """
    10-year analysis for a given stock symbol:
    - 10-year total return
    - CAGR
    - Volatility (annualized)
    - Max drawdown
    - Yearly returns (by calendar year)
    - Reference link
    """
    symbol = (symbol or "").upper().strip()
    try:
        df = _safe_history(symbol, period="10y")
        df = df.sort_index()

        # daily returns
        df["Pct"] = df["Close"].pct_change()
        daily_ret = df["Pct"].dropna()

        # yearly returns (calendar year)
        yearly_last = df["Close"].resample("Y").last()
        yearly_returns = yearly_last.pct_change().dropna() * 100.0

        start_price = float(df["Close"].iloc[0])
        end_price = float(df["Close"].iloc[-1])
        total_return = (end_price / start_price - 1) * 100.0
        years = (df.index[-1] - df.index[0]).days / 365.25
        cagr = _cagr(start_price, end_price, years if years > 0 else 10)
        volatility = daily_ret.std() * (252 ** 0.5) * 100.0 if not daily_ret.empty else float("nan")
        max_dd = _max_drawdown(df["Close"])

        # key highs/lows
        max_price = float(df["Close"].max())
        min_price = float(df["Close"].min())

        # yearly string
        yearly_md = "\n".join([f"- {idx.year}: {ret:.2f}%" for idx, ret in yearly_returns.items()])

        txt = (
            f"# 10-Year Analysis — {symbol}\n\n"
            f"**Start (10y ago):** ${start_price:.2f}\n"
            f"**Current:** ${end_price:.2f}\n"
            f"**Total Return (10y):** {total_return:.2f}%\n\n"
            f"**CAGR:** {cagr:.2f}% per year\n"
            f"**Annualized Volatility:** {volatility:.2f}%\n"
            f"**Max Drawdown:** {max_dd:.2f}%\n"
            f"**High (10y):** ${max_price:.2f}\n"
            f"**Low (10y):**  ${min_price:.2f}\n\n"
            f"---\n\n"
            f"### Yearly Returns\n{yearly_md}\n\n"
            f"---\n\n"
            f"**Reference:** https://finance.yahoo.com/quote/{symbol}\n"
        )
        return txt
    except Exception as e:
        
        return f"Error fetching 10-year analysis for {symbol}: {e}"


# ---------------------------
# TOOL: Compare multiple stocks (10-year by default)
# ---------------------------

@tool
def compare_multi_stocks_tool(symbols):
    """
    Compare multiple symbols over 10 years.
    Input: symbols can be a comma-separated string or a list of strings.
    Returns a sorted ranking with links.
    """
    # normalize input
    if isinstance(symbols, str):
        # accept comma separated or space separated
        raw = [s.strip() for s in symbols.replace(";", ",").split(",") if s.strip()]
    elif isinstance(symbols, (list, tuple)):
        raw = [str(s).strip() for s in symbols if str(s).strip()]
    else:
        return "Please provide a list of symbols or a comma-separated string."

    if len(raw) < 2:
        return "Please provide at least two symbols to compare."

    results = []
    errors = []

    for sym in raw:
        symu = sym.upper()
        try:
            df = _safe_history(symu, period="10y")
            start = float(df["Close"].iloc[0])
            end = float(df["Close"].iloc[-1])
            total_return = (end / start - 1) * 100.0
            cagr = _cagr(start, end, 10.0)
            results.append({"symbol": symu, "total_return": total_return, "cagr": cagr})
        except Exception as e:
            errors.append(f"{symu}: {e}")

    # sort by total_return descending
    results_sorted = sorted(results, key=lambda r: (r["total_return"] is not None, r["total_return"]), reverse=True)

    txt = "# 10-Year Multi-Stock Comparison\n\n"
    for r in results_sorted:
        txt += f"- **{r['symbol']}**: Total Return {r['total_return']:.2f}% — CAGR {r['cagr']:.2f}%\n"

    if errors:
        txt += "\n---\n\n**Warnings / Errors:**\n"
        for er in errors:
            txt += f"- {er}\n"

    txt += "\n\n**References:**\n"
    for r in results_sorted:
        txt += f"- {r['symbol']}: https://finance.yahoo.com/quote/{r['symbol']}\n"

    return txt


# ---------------------------
# AGENT FACTORY (returns master Supervisor agent)
# ---------------------------

def get_financial_agent():
    """
    Build and return the multi-agent Supervisor (team) that routes tasks:
     - Web Search Agent: DuckDuckGo for news/trends
     - Finance Agent: yfinance tools + custom historical tools
     - Supervisor Agent: team routing and final answer aggregation
    """

    # Web Search Agent
    web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web and fetch news/trends",
        model=OpenAIChat(model="gpt-4o"),
        tools=[DuckDuckGo()],
        markdown=True,
        show_tool_calls=False,
        instructions=[
            "Use DuckDuckGo for news, trends, or general web research.",
            "Return short summaries and include source links.",
        ],
    )

def get_financial_agent():
    """
    Build and return the multi-agent Supervisor (team) that routes tasks:
     - Web Search Agent: DuckDuckGo for news/trends
     - Finance Agent: yfinance tools + custom historical tools
     - Supervisor Agent: team routing and final answer aggregation
    """

    # ---------------------------------------------------------
    # 1) WEB SEARCH AGENT
    # ---------------------------------------------------------
    web_search_agent = Agent(
        name="Web Search Agent",
        role="Search the web and fetch news/trends",
        model=OpenAIChat(model="gpt-4o"),
        tools=[DuckDuckGo()],
        markdown=True,
        show_tool_calls=False,
        instructions=[
            "Use DuckDuckGo for news, trends, or general web research.",
            "Always provide short summaries and include source links.",
        ],
    )

    # ---------------------------------------------------------
    # 2) FINANCE AGENT
    # ---------------------------------------------------------

    
    yfinance_tools = YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        stock_fundamentals=True,
        company_news=True,
    )

    # Finance agent with all custom tools correctly added
    finance_agent = Agent(
        name="Finance Agent",
        role="Handles all stock & financial queries",
        model=OpenAIChat(model="gpt-4o"),
        tools=[
            yfinance_tools,         
            one_year_tool,           
            compare_stocks_tool,            
            google_news_tool, 
            DuckDuckGo()        
        ],
        markdown=True,
        show_tool_calls=False,
        instructions=[
            "Use yfinance tools for real-time data (price, fundamentals, earnings, news).",
            "Use one_year_tool for 1-year performance.",
            "Use compare_stocks_tool for comparing multiple stocks.",
            "Use google_news_tool for the latest news (prefer it over DuckDuckGo for finance).",
            "If 5+ stocks are given, produce a comparison table.",
            "Always include reference links and a professional summary.",
            "Do NOT output LaTeX formulas. Write formulas in plain English only.",
        ],
    )

    # ---------------------------------------------------------
    # 3) SUPERVISOR AGENT (TEAM ROUTER)
    # ---------------------------------------------------------
    master_agent = Agent(
        name="Supervisor Agent",
        role="Routes user questions to correct sub-agent",
        model=OpenAIChat(model="gpt-4o"),
        team=[web_search_agent, finance_agent],
        markdown=True,
        show_tool_calls=False,
        instructions=[
            "If user asks for *news / trends / latest events*, ALWAYS use DuckDuckGo or google_news_tool.",
            "Yahoo Finance news should be used ONLY when specifically asked.",
            "For stock-specific real-time data → Finance Agent.",
            "For multi-stock comparisons → Finance Agent (use compare_stocks_tool).",
            "For long-term (5-10 years) history → use Finance Agent + one_year_tool repeatedly.",
            "Produce a friendly, conversational tone. Always return final structured summary.",
            "Always include reference links, a TL;DR section, and properly formatted tables.",
            "Always include reference links, a TL;DR section, and properly formatted tables.",
        ],
    )

    return master_agent


# ---------------------------------------------------------
# STREAMING WRAPPER FOR UI
# ---------------------------------------------------------

def run_agent_stream(message: str):
    """
    Streaming generator for Streamlit UI.
    """
    import traceback
    try:
        agent = get_financial_agent()
        for chunk in agent.run(message=message, stream=True):
            yield chunk
    except Exception as e:
        yield f"Error running agent: {e}\n{traceback.format_exc()}"




