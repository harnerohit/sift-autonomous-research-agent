from langgraph.graph import END, START, StateGraph

from app.nodes import analyzer, planner, saver, searcher, writer
from app.state import ResearchState


MAX_RETRIES = 2


def route_after_writer(state: ResearchState) -> str:
    """Route based on report validity and retry limit."""

    if state["report"] is not None:
        return "save"

    if state["retry_count"] < MAX_RETRIES:
        return "retry"

    return "end"


def build_graph():
    """Build and compile the autonomous research graph."""

    graph_builder = StateGraph(ResearchState)

    graph_builder.add_node("planner", planner)
    graph_builder.add_node("searcher", searcher)
    graph_builder.add_node("analyzer", analyzer)
    graph_builder.add_node("writer", writer)
    graph_builder.add_node("saver", saver)

    graph_builder.add_edge(START, "planner")
    graph_builder.add_edge("planner", "searcher")
    graph_builder.add_edge("searcher", "analyzer")
    graph_builder.add_edge("analyzer", "writer")

    graph_builder.add_conditional_edges(
        "writer",
        route_after_writer,
        {
            "save": "saver",
            "retry": "planner",
            "end": END,
        },
    )

    graph_builder.add_edge("saver", END)

    return graph_builder.compile()