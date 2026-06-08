"""Google Gemini API client wrapper."""
from __future__ import annotations
from typing import Optional
import requests
import streamlit as st


def call_gemini(
    api_key: str,
    prompt: str,
    model: str = "gemini-2.0-flash",
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> Optional[str]:
    """Call the Gemini generateContent endpoint."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "maxOutputTokens": max_tokens},
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.error(f"Gemini API Error {r.status_code}: {r.text[:200]}")
        return None
    except Exception as e:
        st.error(f"Gemini connection error: {e}")
        return None
