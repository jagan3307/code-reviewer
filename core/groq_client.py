"""Groq API client wrapper."""
from __future__ import annotations
from typing import Optional
import requests
import streamlit as st


def call_groq(
    api_key: str,
    messages: list,
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> Optional[str]:
    """Call the Groq chat completions endpoint."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"]
        st.error(f"Groq API Error {r.status_code}: {r.text[:200]}")
        return None
    except Exception as e:
        st.error(f"Groq connection error: {e}")
        return None
