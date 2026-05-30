# search_tool.py
# Wraps Tavily web search API into a simple function.
# Agents call search_web("query") and get back clean text results.

from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()


def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web using Tavily.
    Returns a clean combined string of all results.

    Example:
        result = search_web("AI in healthcare 2024")
        # Returns text with titles, URLs, and content from 5 articles
    """
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        results = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced"
        )

        output = f'Search results for: "{query}"\n'
        output += "=" * 50 + "\n"

        for i, result in enumerate(results["results"], 1):
            output += f"\n[{i}] {result['title']}\n"
            output += f"Source: {result['url']}\n"
            output += f"{result['content']}\n"

        return output

    except Exception as e:
        return f"Search failed: {str(e)}"
