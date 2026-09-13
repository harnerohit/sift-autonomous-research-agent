# SIFT — Autonomous Research Agent

SIFT is an autonomous research agent built with LangGraph.

Give it a research topic, and SIFT plans focused search queries, searches the web, extracts key facts, and generates a structured research report with sources.

## Features

- Autonomous research planning
- Multi-query web search using Tavily
- Structured fact extraction
- Pydantic-validated research reports
- Retry logic for invalid report generation
- Report saved as Markdown
- LangGraph workflow orchestration
- LangSmith tracing
- Streamlit interface

## Architecture

```text
User Topic
    ↓
Planner
    ↓
Searcher
    ↓
Analyzer
    ↓
Writer
    ↓
Validation
    ↓
Saver
    ↓
report.md