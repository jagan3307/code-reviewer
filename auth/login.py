"""Login page for CodeSage AI."""
import streamlit as st
from ui.auth_styles import AUTH_CSS
from .google_auth import get_google_auth_url


def render_login():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    # Generate the Google auth URL exactly ONCE per session
    if "login_google_url" not in st.session_state:
        st.session_state["login_google_url"] = get_google_auth_url()
    google_url = st.session_state["login_google_url"]

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class='auth-card'>
            <div class='auth-logo'>
                <span class='auth-logo-icon'>🔬</span>
                <div class='auth-logo-name'>CodeSage AI</div>
                <div class='auth-logo-sub'>Intelligent Code Review</div>
            </div>
            <div class='auth-title'>Welcome back</div>
            <div class='auth-subtitle'>Sign in to continue</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Google button via st.link_button (Streamlit-native, always works) ──
        st.link_button(
            " 🌐 Continue with Google",
            url=google_url,
            use_container_width=True,
        )

        st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

        if submitted:
            _handle_email_login(email, password)

        st.markdown("""
        <div class='auth-footer'>
            Don't have an account?
            <a href='?page=signup' class='auth-link'>Sign up</a>
            &nbsp;·&nbsp;
            <a href='?page=forgot' class='auth-link'>Forgot password?</a>
        </div>
        """, unsafe_allow_html=True)


def _handle_email_login(email: str, password: str):
    if not email or not password:
        st.error("Please enter both email and password.")
        return
    try:
        from database.supabase_client import get_supabase
        sb = get_supabase()
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        user_meta = res.user
        st.session_state["user"] = {
            "email": user_meta.email,
            "full_name": user_meta.user_metadata.get("full_name", ""),
            "avatar_url": user_meta.user_metadata.get("avatar_url", ""),
        }
        st.session_state["access_token"] = res.session.access_token
        st.session_state.pop("login_google_url", None)
        st.rerun()
    except Exception as e:
        st.error(f"Login failed: {e}")