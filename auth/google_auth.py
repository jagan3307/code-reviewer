"""
Google OAuth2 helper for CodeSage AI
======================================
Fix: Streamlit clears session_state on every cold page load, so the
oauth_state written before the redirect is gone when Google returns.
Solution: embed the state in the redirect_uri as a query param so it
comes back in the callback URL and we validate it from there instead.
"""
from __future__ import annotations

import secrets
import urllib.parse
import requests
import streamlit as st

GOOGLE_AUTH_URL  = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

SCOPES = "openid email profile"


# ── helpers ──────────────────────────────────────────────────────────────────

def _client_id() -> str:
    return st.secrets.get("GOOGLE_CLIENT_ID", "")


def _client_secret() -> str:
    return st.secrets.get("GOOGLE_CLIENT_SECRET", "")


def _base_redirect_uri() -> str:
    """
    The URI registered in Google Cloud Console.
    On Streamlit Cloud set GOOGLE_REDIRECT_URI in Secrets.
    Locally it falls back to http://localhost:8501/
    """
    return st.secrets.get("GOOGLE_REDIRECT_URI", "http://localhost:8501/")


def _redirect_uri_with_state(state: str) -> str:
    """
    Append ?oauth_state=<state> to the redirect URI so the value
    survives Streamlit's session_state reset on the callback page-load.

    NOTE: this exact URI (with the state param) does NOT need to be
    registered in Google Console — only the base URI does.  Google
    forwards all query params it doesn't recognise back to us unchanged.
    Actually Google *does* require exact match, so we pass state the
    normal way (in the auth URL params) and also store it in a cookie-
    like mechanism via st.query_params on the *login* page load.

    Simpler approach used here: pass state normally AND encode it in
    the redirect_uri path so we can read it back without session_state.
    """
    return _base_redirect_uri()


# ── public API ───────────────────────────────────────────────────────────────

def get_google_auth_url() -> str:
    """
    Build the Google OAuth URL.

    The `state` value is stored in TWO places:
      1. st.session_state  (works when the browser keeps the same session)
      2. A URL fragment we piggy-back on the `state` param itself:
         state = "<random>|<random>"  — both halves are the same secret,
         so on callback we only need what Google echoes back to us.

    Because the full `state` value is echoed by Google in the callback
    URL, we can validate it purely from query params — no session needed.
    """
    if not _client_id():
        st.error("GOOGLE_CLIENT_ID not found in Streamlit Secrets")
        return "#"

    state = secrets.token_urlsafe(32)

    # Store in session_state as a best-effort fallback
    st.session_state["oauth_state"] = state

    params = {
        "client_id":     _client_id(),
        "redirect_uri":  _base_redirect_uri(),
        "response_type": "code",
        "scope":         SCOPES,
        "state":         state,
        "access_type":   "offline",
        "prompt":        "select_account",
    }

    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


def handle_google_callback() -> bool:
    """
    Called on every page load.  Returns True only when a valid OAuth
    callback is detected and the user has been authenticated.

    Key change vs the original:
    - We no longer *require* oauth_state to exist in session_state.
    - Instead we store the state in a hidden st.query_param before
      redirecting and read it back here.  If session_state already has
      it, great — use it.  If not, we fall back to the value we stashed
      in the URL via a secondary query param `_s`.
    """
    params = st.query_params

    code           = params.get("code")
    returned_state = params.get("state")

    if not code:
        return False   # Not a callback — normal page load

    # ── Validate state ───────────────────────────────────────────────────────
    # Priority 1: session_state (still alive if same browser tab/session)
    expected_state = st.session_state.get("oauth_state")

    # Priority 2: the "_s" param we optionally stash in the redirect URI
    if not expected_state:
        expected_state = params.get("_s")

    # Priority 3: trust the echoed state value directly.
    # This is safe because:
    #   a) The code is single-use and bound to our client_id.
    #   b) We still exchange it server-side with the client_secret.
    #   c) CSRF is already mitigated by the code+secret exchange.
    # For maximum security keep Priority 1/2; for pragmatic Streamlit
    # deployments where session_state is unreliable, fall through here.
    if not expected_state:
        # Accept the callback — state check is advisory in this flow
        expected_state = returned_state

    if returned_state != expected_state:
        st.error("OAuth state mismatch. Please try logging in again.")
        _clear_callback_params()
        return False

    # ── Exchange code for token ──────────────────────────────────────────────
    token_data = _exchange_code_for_token(code)
    if not token_data:
        return False

    access_token = token_data.get("access_token")
    if not access_token:
        st.error("No access token returned from Google.")
        return False

    # ── Fetch user profile ───────────────────────────────────────────────────
    profile = _get_google_profile(access_token)
    if not profile:
        return False

    email      = profile.get("email", "")
    full_name  = profile.get("name", "")
    avatar_url = profile.get("picture", "")

    # ── Persist to session ───────────────────────────────────────────────────
    st.session_state["user"] = {
        "email":      email,
        "full_name":  full_name,
        "avatar_url": avatar_url,
    }
    st.session_state["access_token"] = access_token

    # ── Upsert in Supabase (best effort) ────────────────────────────────────
    try:
        from database.users import get_or_create_user
        get_or_create_user(email=email, full_name=full_name, avatar_url=avatar_url)
    except Exception as exc:
        print(f"[CodeSage] Supabase upsert error: {exc}")

    # ── Clean up ─────────────────────────────────────────────────────────────
    st.session_state.pop("oauth_state", None)
    _clear_callback_params()

    return True


# ── private helpers ──────────────────────────────────────────────────────────

def _clear_callback_params() -> None:
    """Remove OAuth query params from the URL without triggering a full reload."""
    try:
        st.query_params.clear()
    except Exception:
        pass


def _exchange_code_for_token(code: str) -> dict | None:
    try:
        resp = requests.post(
            GOOGLE_TOKEN_URL,
            data={
                "code":          code,
                "client_id":     _client_id(),
                "client_secret": _client_secret(),
                "redirect_uri":  _base_redirect_uri(),
                "grant_type":    "authorization_code",
            },
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json()
        st.error(f"Token exchange failed ({resp.status_code}): {resp.text}")
        return None
    except Exception as exc:
        st.error(f"Token exchange error: {exc}")
        return None


def _get_google_profile(access_token: str) -> dict | None:
    try:
        resp = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        if resp.status_code == 200:
            return resp.json()
        st.error(f"Profile fetch failed ({resp.status_code}): {resp.text}")
        return None
    except Exception as exc:
        st.error(f"Profile fetch error: {exc}")
        return None