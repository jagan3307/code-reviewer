"""Session history database operations."""
from __future__ import annotations
from .supabase_client import get_supabase


def append_chat_message(user_email: str, session_id: str, role: str, content: str) -> None:
    sb = get_supabase()
    sb.table("chat_history").insert({
        "user_email": user_email,
        "session_id": session_id,
        "role": role,
        "content": content,
    }).execute()


def get_chat_history(user_email: str, session_id: str) -> list[dict]:
    sb = get_supabase()
    res = (
        sb.table("chat_history")
        .select("role,content")
        .eq("user_email", user_email)
        .eq("session_id", session_id)
        .order("created_at")
        .execute()
    )
    return res.data or []


def clear_chat_history(user_email: str, session_id: str) -> None:
    sb = get_supabase()
    sb.table("chat_history").delete().eq("user_email", user_email).eq("session_id", session_id).execute()
