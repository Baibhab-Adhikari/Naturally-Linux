"""Prompt → command generator (Groq LLM integration)."""

import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = (
    "You are a Linux command generator. "
    "Return ONLY the exact shell command to accomplish the user's task. "
    "Do NOT include explanations, markdown, code fences, or extra text. "
    "If multiple commands are required, chain them with &&. "
    "Assume a POSIX shell."
)


def generate_command(prompt: str) -> str:
    """
    Generate a shell command from a natural language prompt using Groq.

    Requires the GROQ_API_KEY environment variable to be set.
    """

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")

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
