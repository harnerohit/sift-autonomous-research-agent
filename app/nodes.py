from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY
from app.schemas import QueryPlan


from tavily import TavilyClient

from app.config import TAVILY_API_KEY
from app.tools import search_tavily

from app.schemas import FactList

from app.schemas import FactList, QueryPlan, ResearchReport

from pydantic import ValidationError
from langchain_core.exceptions import OutputParserException

def planner(state: dict) -> dict:
    """Generate 3–5 focused search queries from the research topic."""

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(QueryPlan)

    prompt = f"""
You are a research planning assistant.

Given the research topic below, generate 3 to 5 focused search queries
that will help gather reliable and diverse information about the topic.

Research topic:
{state["topic"]}
"""

    result = structured_llm.invoke(prompt)

    return {
        "queries": result.queries
    }
    
def searcher(state: dict) -> dict:
    """Run one Tavily search for each planner-generated query."""

    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

    search_results = []

    for query in state["queries"]:
        result = search_tavily(query, tavily_client)
        search_results.append(result)

    return {
        "search_results": search_results
    }
    
def analyzer(state: dict) -> dict:
    """Extract clean factual statements from Tavily search results."""

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(
    FactList,
    method="json_schema",
    strict=True,
)

    prompt = f"""
You are a research analyst.

Extract the important, factual statements from the research search results below.

Rules:
- Return only useful factual statements.
- Remove duplicates and irrelevant information.
- Do not invent information.
- Base every fact only on the provided search results.

Search results:
{state["search_results"]}
"""

    result = structured_llm.invoke(prompt)

    return {
        "facts": result.facts
    }
    
def writer(state: dict) -> dict:
    """Write the final research report from the extracted facts."""

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0,
    )

    structured_llm = llm.with_structured_output(
        ResearchReport,
        method="json_schema",
        strict=True,
    )

    prompt = f"""
You are a research report writer.

Write a clear, factual research report using only the facts provided below.

Requirements:
- Create a concise title.
- Write a concise summary.
- Organize the information into meaningful sections.
- Include the source URLs from the research results.
- Do not invent facts or sources.
- Every section must contain useful content.

Facts:
{state["facts"]}

Sources:
{[result["url"] for search in state["search_results"] for result in search["results"]]}
"""

    try:
        result = structured_llm.invoke(prompt)

        return {
            "report": result
        }

    except (ValidationError, OutputParserException) as error:
        print(f"Writer validation failed: {error}")

        return {
            "report": None,
            "retry_count": state["retry_count"] + 1,
        }
    
def saver(state: dict) -> dict:
    """Save the validated research report to report.md."""

    report = state["report"]

    if report is None:
        raise ValueError("Cannot save report: report is missing.")

    with open("report.md", "w", encoding="utf-8") as file:
        file.write(f"# {report.title}\n\n")
        file.write(f"## Summary\n\n{report.summary}\n\n")

        for section in report.sections:
            file.write(f"## {section.heading}\n\n")
            file.write(f"{section.content}\n\n")

        file.write("## Sources\n\n")

        for source in report.sources:
            file.write(f"- {source}\n")

    return {}