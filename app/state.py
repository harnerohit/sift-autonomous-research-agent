from typing import TypedDict

from app.schemas import ResearchReport


class ResearchState(TypedDict):
    topic: str
    queries: list[str]
    search_results: list[dict]
    facts: list[str]
    report: ResearchReport | None
    retry_count: int