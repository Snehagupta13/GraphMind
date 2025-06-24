from langchain.tools import tool
import arxiv

def _search_arxiv(query: str, max_results: int = 5) -> str:
    """Raw function to fetch arXiv papers."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        results = list(search.results())
        if not results:
            return "No results found on arXiv for that query."

        output = []
        for i, r in enumerate(results):
            output.append(
                f"{i+1}. {r.title.strip()}\n"
                f"Authors: {', '.join(a.name for a in r.authors)}\n"
                f"Summary: {r.summary[:300].strip()}...\n"
                f"URL: {r.entry_id}"
            )
        return "\n\n".join(output)

    except Exception as e:
        return f"arXiv search failed: {e}"

@tool
def search_arxiv(query: str) -> str:
    """Searches arXiv for recent papers given a query."""
    return _search_arxiv(query, max_results=10)
