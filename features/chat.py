"""Chat-about-code feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai_with_history, SYSTEM_EXPERT


def chat_about_code(
    code: str,
    language: str,
    question: str,
    history: list,
) -> Optional[str]:
    system = (
        f"{SYSTEM_EXPERT}\n\n"
        f"The user has shared this {language} code:\n"
        f"```{language.lower()}\n{code}\n```\n"
        f"Answer questions about it clearly and helpfully."
    )
    messages = list(history[-6:]) + [{"role": "user", "content": question}]
    return query_ai_with_history(messages, system=system)
