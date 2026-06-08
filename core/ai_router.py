"""AI router — delegates to Groq or Gemini based on session state."""
from __future__ import annotations
from typing import Optional
import streamlit as st

from .groq_client import call_groq
from .gemini_client import call_gemini

SYSTEM_EXPERT = """You are CodeSage, an expert senior software engineer and code reviewer with 20+ years
of experience across all major languages and paradigms. You provide deeply insightful, actionable,
professional code reviews. You are direct, precise, and constructive.
Always format your output in clean Markdown."""


def query_ai(
    prompt: str,
    system: str = SYSTEM_EXPERT,
    temperature: float = 0.3,
) -> Optional[str]:
    """Route an AI call to the active provider using session-state credentials."""
    provider = st.session_state.get("provider", "Groq")
    api_key = st.session_state.get("api_key", "")
    model = st.session_state.get("model", "llama-3.3-70b-versatile")

    if not api_key:
        st.error("⚠️ Please enter your API key in the sidebar.")
        return None

    if provider == "Groq":
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        return call_groq(api_key, messages, model, temperature)

    # Gemini: concatenate system + prompt
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    return call_gemini(api_key, full_prompt, model, temperature)


def query_ai_with_history(
    messages: list,
    system: str = SYSTEM_EXPERT,
) -> Optional[str]:
    """
    Route a multi-turn chat. `messages` is a list of {"role": ..., "content": ...} dicts.
    System prompt is prepended automatically for Groq.
    """
    provider = st.session_state.get("provider", "Groq")
    api_key = st.session_state.get("api_key", "")
    model = st.session_state.get("model", "llama-3.3-70b-versatile")

    if not api_key:
        return "Please enter your API key."

    if provider == "Groq":
        full_messages = [{"role": "system", "content": system}] + messages
        return call_groq(api_key, full_messages, model)

    # Gemini: flatten history to plain text
    flat = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in [{"role": "system", "content": system}] + messages)
    return call_gemini(api_key, flat, model)
