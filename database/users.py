"""User-related database operations."""
from __future__ import annotations
from typing import Optional
from .supabase_client import get_supabase


def get_or_create_user(email: str, full_name: str = "", avatar_url: str = "") -> dict:
    """Upsert a user record and return it."""
    sb = get_supabase()
    result = sb.table("users").upsert(
        {"email": email, "full_name": full_name, "avatar_url": avatar_url},
        on_conflict="email"
    ).execute()
    return result.data[0] if result.data else {}


def get_user_by_email(email: str) -> Optional[dict]:
    sb = get_supabase()
    result = sb.table("users").select("*").eq("email", email).single().execute()
    return result.data


def update_user_profile(email: str, **kwargs) -> dict:
    sb = get_supabase()
    result = sb.table("users").update(kwargs).eq("email", email).execute()
    return result.data[0] if result.data else {}
