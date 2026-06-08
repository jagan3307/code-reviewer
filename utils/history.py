"""History helpers (in-memory + optional DB persistence)."""
from __future__ import annotations
from datetime import datetime
import streamlit as st


def save_to_session(feature: str, language: str, code_input: str):
    """Append a review to the in-memory session history."""
    st.session_state.review_history.append({
        "feature": feature,
        "language": language,
        "time": datetime.now().strftime("%H:%M"),
        "code_preview": code_input[:80],
    })


def save_to_db(feature: str, language: str, code_input: str, result: str):
    """Persist a review result to Supabase if a user is logged in."""
    user = st.session_state.get("user")
    if not user:
        return
    try:
        from database.reports import save_report
        save_report(
            user_email=user["email"],
            feature=feature,
            language=language,
            code_snippet=code_input,
            result=result,
        )
    except Exception:
        pass   # DB persistence is best-effort


def save_history(feature: str, language: str, code_input: str, result: str = ""):
    """Save to both session and DB."""
    save_to_session(feature, language, code_input)
    if result:
        save_to_db(feature, language, code_input, result)
