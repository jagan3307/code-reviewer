"""Logout helper."""
import streamlit as st


def logout():
    """Clear session state and optionally sign out from Supabase."""
    try:
        from database.supabase_client import get_supabase
        sb = get_supabase()
        sb.auth.sign_out()
    except Exception:
        pass

    for key in ["user", "access_token", "review_history", "chat_history", "last_result", "oauth_state"]:
        st.session_state.pop(key, None)

    st.rerun()
