"""Forgot password page."""
import streamlit as st
from ui.auth_styles import AUTH_CSS


def render_forgot_password():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class='auth-card'>
            <div class='auth-logo'>
                <span class='auth-logo-icon'>🔬</span>
                <div class='auth-logo-name'>CodeSage AI</div>
            </div>
            <div class='auth-title'>Reset password</div>
            <div class='auth-subtitle'>We'll send you a reset link</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("forgot_form"):
            email = st.text_input("Email", placeholder="you@example.com")
            submitted = st.form_submit_button("Send Reset Link", use_container_width=True)

        if submitted:
            _send_reset(email)

        st.markdown("""
        <div class='auth-footer'>
            <a href='?page=login' class='auth-link'>← Back to sign in</a>
        </div>
        """, unsafe_allow_html=True)


def _send_reset(email: str):
    if not email:
        st.error("Please enter your email.")
        return
    try:
        from database.supabase_client import get_supabase
        sb = get_supabase()
        sb.auth.reset_password_email(email)
        st.success("✅ Reset email sent! Check your inbox.")
    except Exception as e:
        st.error(f"Error: {e}")
