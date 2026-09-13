from tavily import TavilyClient


MAX_CONTENT_CHARS = 400


def search_tavily(query: str, tavily_client: TavilyClient) -> dict:
    """Run one Tavily search for a single query."""

    response = tavily_client.search(
        query=query,
        max_results=3,
    )

    results = []

    for result in response["results"]:
        results.append(
            {
                "url": result["url"],
                "title": result["title"],
                "content": result["content"][:MAX_CONTENT_CHARS],
            }
        )

    return {
        "query": response["query"],
        "results": results,
    }