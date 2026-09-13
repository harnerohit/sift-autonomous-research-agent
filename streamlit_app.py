import streamlit as st
import html
from app.graph import build_graph


st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="◈",
    layout="wide",
)


@st.cache_resource
def get_graph():
    return build_graph()


st.markdown(
    """
    <style>
    
        /* ---------- Streamlit header ---------- */

        [data-testid="stHeader"] {
            background: #292722  !important;
            border-bottom: none !important;
        }
        
        [data-testid="stHeader"] button {
            color: #E2B4BD !important;
        }

        [data-testid="stHeader"] button:hover {
            background: rgba(18, 84, 79, 0.12) !important;
        }
        
        .stApp {
            background: #f3f0e8;
            color: #292722;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 3rem;
            padding-bottom: 5rem;
        }

        /* ---------- Hero ---------- */

        .hero {
            position: relative;
            overflow: hidden;
            padding: 3.4rem 3.4rem 3.2rem;
            border-radius: 24px;
            background: #292722;
            color: #f3f0e8;
            margin-bottom: 2.8rem;
        }

        .hero::before {
            content: "";
            position: absolute;
            left: 0;
            bottom: 0;
            width: 38%;
            height: 1px;
            background: #b8a78d;
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 280px;
            height: 280px;
            right: -90px;
            top: -120px;
            border: 1px solid rgba(243, 240, 232, 0.15);
            border-radius: 50%;
        }

        .hero-eyebrow {
            color: #b8a78d;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-bottom: 1.2rem;
        }

        .hero-title {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 3.7rem;
            line-height: 1.02;
            letter-spacing: -0.035em;
            color: #f3f0e8;
            margin: 0;
        }

        .hero-description {
            max-width: 700px;
            margin-top: 1.4rem;
            color: #c9c4ba;
            font-size: 1rem;
            line-height: 1.75;
        }

        /* ---------- Research section ---------- */

        .input-heading {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.55rem;
            font-weight: 600;
            color: #292722;
            margin-bottom: 0.25rem;
        }

        .input-description {
            color: #716b61;
            font-size: 0.92rem;
            margin-bottom: 0.8rem;
        }

        div[data-testid="stTextInput"] input {
            background: #faf8f3 !important;
            color: #292722 !important;
            caret-color: #292722 !important;
            border: 1px solid #cfc7ba !important;
            border-radius: 12px !important;
            padding: 0.9rem 1rem !important;
            font-size: 1rem !important;
        }

        div[data-testid="stTextInput"] input::placeholder {
            color: #999186 !important;
            opacity: 1 !important;
        }

        div[data-testid="stTextInput"] input:focus {
            border-color: #292722 !important;
            box-shadow: 0 0 0 1px #292722 !important;
        }

        /* ---------- Button ---------- */

        div.stButton > button {
            margin-top: 0.7rem;
            background: #292722 !important;
            color: #f3f0e8 !important;
            border: 1px solid #292722 !important;
            border-radius: 11px !important;
            padding: 0.72rem 1.5rem !important;
            font-weight: 600 !important;
        }

        div.stButton > button:hover {
            background: #4a463e !important;
            border-color: #4a463e !important;
        }

        /* ---------- Report ---------- */

        .report-label {
            margin-top: 3.5rem;
            margin-bottom: 0.8rem;
            color: #766b5b;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .report-card {
            background: #faf8f3;
            border: 1px solid #d6cec0;
            border-radius: 22px;
            padding: 2.7rem 3rem;
            box-shadow: 0 10px 30px rgba(41, 39, 34, 0.08);
        }

        .report-card h1 {
            font-family: Georgia, "Times New Roman", serif;
            color: #292722;
            font-size: 2.5rem;
            line-height: 1.1;
            letter-spacing: -0.025em;
        }

        .report-card h2 {
            font-family: Georgia, "Times New Roman", serif;
            color: #39352f;
            margin-top: 2rem;
        }

        .report-card p {
            color: #4e4941;
            line-height: 1.75;
        }

        .report-card a {
            color: #665947;
        }

        hr {
            border: none !important;
            border-top: 1px solid #ddd5c8 !important;
            margin: 2rem 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Hero ----------

st.markdown(
    '<div class="hero">'
    '<div class="hero-eyebrow">SIFT · Autonomous Research System</div>'
    '<div class="hero-title">Research,<br>without the busywork.</div>'
    '<div class="hero-description">'
    'Give SIFT a question worth exploring. It plans the research, '
    'searches the web, extracts useful evidence, and turns it into '
    'a structured report.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ---------- Input ----------

st.markdown(
    """
    <div class="input-heading">What should I research?</div>
    <div class="input-description">
        Enter a topic and let the research agent take it from there.
    </div>
    """,
    unsafe_allow_html=True,
)

topic = st.text_input(
    "Research topic",
    placeholder="e.g. Impact of AI agents on software engineering",
    label_visibility="collapsed",
)

run_research = st.button("Run research  →")


# ---------- Research ----------

if run_research:

    if not topic.strip():
        st.warning("Enter a research topic first.")

    else:
        graph = get_graph()

        initial_state = {
            "topic": topic.strip(),
            "queries": [],
            "search_results": [],
            "facts": [],
            "report": None,
            "retry_count": 0,
        }

        with st.spinner("Researching your topic..."):
            result = graph.invoke(initial_state)

        report = result["report"]

        if report is None:
            st.error("The agent could not produce a valid report.")

        else:
            st.markdown(
                '<div class="report-label">Research report</div>',
                unsafe_allow_html=True,
            )

            sections_html = "".join(
                f"<h2>{html.escape(section.heading)}</h2>"
                f"<p>{html.escape(section.content)}</p>"
                for section in report.sections
            )

            sources_html = "".join(
                f'<li><a href="{html.escape(source, quote=True)}" '
                f'target="_blank">{html.escape(source)}</a></li>'
                for source in report.sources
            )

            card_html = f"""
<div class="report-card">
<h1>{html.escape(report.title)}</h1>
<p>{html.escape(report.summary)}</p>
<hr>
{sections_html}
<hr>
<h2>Sources</h2>
<ul>
{sources_html}
</ul>
</div>
"""

            st.markdown(card_html, unsafe_allow_html=True)