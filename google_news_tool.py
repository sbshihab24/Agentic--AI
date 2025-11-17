from phi.tools import tool
from GoogleNews import GoogleNews

@tool
def google_news_tool(query: str, limit: int = 5):
    """
    Google News search tool.
    Returns clickable markdown links.
    """
    try:
        google = GoogleNews(lang='en')
        google.search(query)
        results = google.results()

        if not results:
            return f"No recent Google News found for **{query}**."

        text = f"# 📰 Latest Google News for **{query}**\n\n"

        for item in results[:limit]:
            title = item.get("title", "No title")
            date = item.get("date", "Unknown date")
            link = item.get("link", "")

            # Fix invalid GoogleNews links
            if link.startswith("./"):
                link = "https://news.google.com" + link[1:]

            text += (
                f"### {title}\n"
                f"- 📅 {date}\n"
                f"- 🔗 [Read full article]({link})\n\n"
            )

        return text

    except Exception as e:
        return f"Error using Google News: {e}"
