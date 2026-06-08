"""Signup page for CodeSage AI."""
import streamlit as st
from ui.auth_styles import AUTH_CSS
from .google_auth import get_google_auth_url


def render_signup():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    # ── Generate the Google auth URL exactly ONCE per page load ─────────────
    if "signup_google_url" not in st.session_state:
        st.session_state["signup_google_url"] = get_google_auth_url()
    google_url = st.session_state["signup_google_url"]

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class='auth-card'>
            <div class='auth-logo'>
                <span class='auth-logo-icon'>🔬</span>
                <div class='auth-logo-name'>CodeSage AI</div>
                <div class='auth-logo-sub'>Intelligent Code Review</div>
            </div>
            <div class='auth-title'>Create account</div>
            <div class='auth-subtitle'>Get started for free</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <a href='{google_url}' class='google-btn' target='_self'>
            <svg width='18' height='18' viewBox='0 0 18 18'>
                <path fill='#4285F4' d='M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.874 2.684-6.615z'/>
                <path fill='#34A853' d='M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332A8.997 8.997 0 009 18z'/>
                <path fill='#FBBC05' d='M3.964 10.707A5.41 5.41 0 013.682 9c0-.593.102-1.17.282-1.707V4.961H.957A8.996 8.996 0 000 9c0 1.452.348 2.827.957 4.039l3.007-2.332z'/>
                <path fill='#EA4335' d='M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0A8.997 8.997 0 00.957 4.961L3.964 7.293C4.672 5.163 6.656 3.58 9 3.58z'/>
            </svg>
            Sign up with Google
        </a>
        """, unsafe_allow_html=True)

        st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)

        with st.form("signup_form", clear_on_submit=False):
            full_name = st.text_input("Full Name", placeholder="Jane Doe")
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="Min 8 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)

        if submitted:
            _handle_signup(full_name, email, password, confirm)

        st.markdown("""
        <div class='auth-footer'>
            Already have an account?
            <a href='?page=login' class='auth-link'>Sign in</a>
        </div>
        """, unsafe_allow_html=True)


def _handle_signup(full_name: str, email: str, password: str, confirm: str):
    if not all([full_name, email, password, confirm]):
        st.error("Please fill in all fields.")
        return
    if len(password) < 8:
        st.error("Password must be at least 8 characters.")
        return
    if password != confirm:
        st.error("Passwords do not match.")
        return
    try:
        from database.supabase_client import get_supabase
        sb = get_supabase()
        res = sb.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"full_name": full_name}},
        })
        if res.user:
            st.success("✅ Account created! Please check your email to confirm, then sign in.")
            # Clear cached Google URL
            st.session_state.pop("signup_google_url", None)
        else:
            st.error("Signup failed. Please try again.")
    except Exception as e:
        st.error(f"Signup error: {e}")