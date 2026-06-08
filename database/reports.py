"""Review report database operations."""
from __future__ import annotations
from typing import Optional
from datetime import datetime
from .supabase_client import get_supabase


def save_report(
    user_email: str,
    feature: str,
    language: str,
    code_snippet: str,
    result: str,
) -> dict:
    """Save a completed review/feature run to the database."""
    sb = get_supabase()
    record = {
        "user_email": user_email,
        "feature": feature,
        "language": language,
        "code_snippet": code_snippet[:500],   # store preview only
        "result": result,
        "created_at": datetime.utcnow().isoformat(),
    }
    res = sb.table("reports").insert(record).execute()
    return res.data[0] if res.data else {}


def get_user_reports(user_email: str, limit: int = 20) -> list[dict]:
    """Fetch recent reports for a user."""
    sb = get_supabase()
    res = (
        sb.table("reports")
        .select("*")
        .eq("user_email", user_email)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def delete_report(report_id: str) -> None:
    sb = get_supabase()
    sb.table("reports").delete().eq("id", report_id).execute()
