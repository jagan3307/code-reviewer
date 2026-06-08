"""Auth guard — enforces authentication before rendering the main app."""
import streamlit as st


def require_auth() -> bool:
    """
    Returns True if the user is authenticated.
    If not, redirects to login page and returns False.
    """
    if st.session_state.get("user"):
        return True
    st.session_state["redirect_to"] = "login"
    st.rerun()
    return False


def is_authenticated() -> bool:
    return bool(st.session_state.get("user"))
