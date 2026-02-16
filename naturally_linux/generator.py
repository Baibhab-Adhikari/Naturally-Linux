"""Prompt → command generator (Groq LLM integration)."""

from dotenv import load_dotenv
from groq import Groq

from .config import get_api_key

load_dotenv()

SYSTEM_PROMPT = (
    "You are a Linux command generator. "
    "Return ONLY the exact shell command to accomplish the user's task. "
    "Do NOT include explanations, markdown, code fences, or extra text. "
    "If multiple commands are required, chain them with &&. "
    "Assume a POSIX shell."
)

EXPLAIN_PROMPT = (
    "You are a Linux command explainer. "
    "Explain succinctly what the command does and any notable risks. "
    "Do NOT include markdown, code fences, or extra text beyond the explanation."
)


def generate_command(prompt: str) -> str:
    """
    Generate a shell command from a natural language prompt using Groq.

    Requires the GROQ_API_KEY environment variable to be set.
    """

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing Groq API key. Run 'naturally-linux config set-key' "
            "or export GROQ_API_KEY."
        )

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=200,
    )

    content = (chat_completion.choices[0].message.content or "").strip()

    # Ensure we return only a single command line.
    return content.splitlines()[0].strip()


def explain_command(command: str) -> str:
    """
    Explain a shell command in plain language using Groq.

    Requires the GROQ_API_KEY environment variable to be set.
    """

    api_key = get_api_key()
    if not api_key:
        raise RuntimeError(
            "Missing Groq API key. Run 'naturally-linux config set-key' "
            "or export GROQ_API_KEY."
        )

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": EXPLAIN_PROMPT},
            {"role": "user", "content": command},
        ],
        temperature=0.2,
        max_tokens=200,
    )

    content = (chat_completion.choices[0].message.content or "").strip()
    return content
