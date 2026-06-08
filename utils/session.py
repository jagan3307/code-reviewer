"""Session state initializer and helpers."""
import os
import streamlit as st


def init_session():
    """Initialize all required session_state keys with defaults."""
    _ENV_GROQ_KEY = os.getenv("GROQ_API_KEY", "")
    _ENV_PROVIDER = os.getenv("DEFAULT_PROVIDER", "Groq")
    _ENV_MODEL = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")

    defaults = {
        "review_history": [],
        "chat_history": [],
        "last_result": None,
        "provider": _ENV_PROVIDER if _ENV_PROVIDER in ["Groq", "Gemini"] else "Groq",
        "api_key": _ENV_GROQ_KEY,
        "model": _ENV_MODEL,
        "user": None,
        "access_token": None,
        "oauth_state": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val
