from pydantic import BaseModel, Field
from typing import Annotated

class ResearchSection(BaseModel):

    heading: str = Field(
        max_length=100,
        description="Heading of the research section"
    )

    content: str = Field(
        max_length=1200,
        description="Concise content of the research section"
    )


class QueryPlan(BaseModel):
    queries: list[str] = Field(
        min_length=3,
        max_length=5,
        description="3 to 5 focused search queries for the research topic"
    )


class FactList(BaseModel):

    facts: list[Annotated[str, Field(max_length=400)]] = Field(
        min_length=5,
        max_length=8,
        description="5 to 8 concise factual statements extracted from the research results"
    )


class ResearchReport(BaseModel):

    title: str = Field(
        max_length=150,
        description="Concise title of the research report"
    )

    summary: str = Field(
        max_length=1000,
        description="Concise summary of the research"
    )

    sections: list[ResearchSection] = Field(
        min_length=1,
        max_length=5,
        description="1 to 5 concise sections containing the main research findings"
    )

    sources: list[Annotated[str, Field(max_length=500)]] = Field(
        min_length=1,
        max_length=8,
        description="Sources used to produce the research"
    )