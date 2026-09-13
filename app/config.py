import os

from dotenv import load_dotenv


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ValueError(f"Missing required environment variable: {name}")

    return value


GROQ_API_KEY = get_required_env("GROQ_API_KEY")
TAVILY_API_KEY = get_required_env("TAVILY_API_KEY")
LANGSMITH_API_KEY = get_required_env("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = get_required_env("LANGSMITH_PROJECT")