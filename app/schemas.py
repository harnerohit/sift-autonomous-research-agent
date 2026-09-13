from pydantic import BaseModel, Field


class ResearchSection(BaseModel):
    heading: str = Field(
        description="Heading of the research section"
    )
    content: str = Field(
        description="Content of the research section"
    )

class QueryPlan(BaseModel):
    queries: list[str] = Field(
        min_length=3,
        max_length=5,
        description="3 to 5 focused search queries for the research topic"
    )

class FactList(BaseModel):
    facts: list[str] = Field(
        min_length=1,
        description="Clean, factual statements extracted from the research results"
    )

class ResearchReport(BaseModel):
    title: str = Field(
        description="Title of the research report"
    )
    summary: str = Field(
        description="Concise summary of the research"
    )
    sections: list[ResearchSection] = Field(
        min_length=1,
        description="Main sections of the research report"
    )
    sources: list[str] = Field(
        min_length=1,
        description="Sources used to produce the research report"
    )