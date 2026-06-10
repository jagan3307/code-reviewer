"""Sidebar component for CodeSage AI."""
import streamlit as st
import os


def render_sidebar():
    """Render the main app sidebar."""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style='text-align:center; padding: 1rem 0 1.5rem'>
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style='margin:0 auto; display:block; margin-bottom:0.5rem'>
                <circle cx="20" cy="20" r="18" stroke="url(#grad)" stroke-width="2"/>
                <path d="M20 8v24M14 20h12M17 14l6 12M23 14l-6 12" stroke="url(#grad)" stroke-width="1.5" stroke-linecap="round"/>
                <defs>
                    <linearGradient id="grad" x1="0" y1="0" x2="40" y2="40">
                        <stop offset="0%" stop-color="#00d4ff"/>
                        <stop offset="100%" stop-color="#7c3aed"/>
                    </linearGradient>
                </defs>
            </svg>
            <div style='font-size:1.2rem; font-weight:800; background:linear-gradient(135deg,#00d4ff,#7c3aed);
                 -webkit-background-clip:text; -webkit-text-fill-color:transparent'>CodeSage AI</div>
            <div style='color:#4a5568; font-size:0.75rem; margin-top:2px'>Intelligent Code Review</div>
        </div>
        """, unsafe_allow_html=True)

        # User info (if logged in)
        user = st.session_state.get("user")
        if user:
            name = user.get("full_name") or user.get("email", "User")
            avatar = user.get("avatar_url", "")
            st.markdown(f"""
            <div style='background:#131929; border:1px solid #1e2a45; border-radius:10px;
                 padding:0.75rem; margin-bottom:1rem; display:flex; align-items:center; gap:0.75rem'>
                {'<img src="' + avatar + '" style="width:32px;height:32px;border-radius:50%">' if avatar else '<div style="width:32px;height:32px;border-radius:50%;background:#7c3aed;display:flex;align-items:center;justify-content:center;font-weight:700">'+name[0].upper()+'</div>'}
                <div>
                    <div style='color:#e8eaf6; font-size:0.85rem; font-weight:600'>{name}</div>
                    <div style='color:#4a5568; font-size:0.75rem'>{user.get("email","")}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # API Configuration
        _ENV_GROQ_KEY = os.getenv("GROQ_API_KEY", "")
        _ENV_GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

        provider = st.selectbox("Provider", ["Groq", "Gemini"], key="provider")

        if provider == "Groq":
            st.selectbox("Model", [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it",
            ], key="model")
            api_link = "https://console.groq.com/keys"
            env_key = _ENV_GROQ_KEY
        else:
            st.selectbox("Model", [
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ], key="model")
            api_link = "https://aistudio.google.com/app/apikey"
            env_key = _ENV_GEMINI_KEY

        # ONLY show API key input if no .env key exists
        if not env_key:
            # No .env key → Show input field for user
            st.markdown("""
            <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.5rem'>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="1"/>
                    <path d="M12 1v6m0 6v4M4.22 4.22l4.24 4.24m5.08 0l4.24-4.24M1 12h6m6 0h4M4.22 19.78l4.24-4.24m5.08 0l4.24 4.24M12 23v-4"/>
                </svg>
                <span style='color:#e8eaf6; font-weight:600; font-size:0.95rem'>API Key</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_input(
                "API Key",
                type="password",
                placeholder="Paste your API key",
                key="api_key"
            )
            st.markdown(f"<a href='{api_link}' target='_blank' style='display:flex; align-items:center; gap:0.5rem; color:#7c3aed; font-size:0.8rem; text-decoration:none'><svg width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'><path d='M21 2H3c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 4l-9 7-9-7V4h18v2z'/></svg>Get free API key</a>", unsafe_allow_html=True)
        # If .env key exists → Don't show anything, just use it silently

        st.markdown("---")

        # Session Stats
        st.markdown("""
        <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem'>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
            </svg>
            <span style='color:#e8eaf6; font-weight:600; font-size:0.95rem'>Session Stats</span>
        </div>
        """, unsafe_allow_html=True)
        
        reviews_done = len(st.session_state.get("review_history", []))
        chats_done = len(st.session_state.get("chat_history", []))
        st.markdown(f"""
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem'>
            <div class='metric-card'>
                <div class='metric-number' style='color:#00d4ff; font-size:1.4rem'>{reviews_done}</div>
                <div class='metric-label'>Reviews</div>
            </div>
            <div class='metric-card'>
                <div class='metric-number' style='color:#7c3aed; font-size:1.4rem'>{chats_done}</div>
                <div class='metric-label'>Chats</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Recent history
        if reviews_done > 0:
            st.markdown("---")
            st.markdown("""
            <div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem'>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
                <span style='color:#e8eaf6; font-weight:600; font-size:0.95rem'>Recent Reviews</span>
            </div>
            """, unsafe_allow_html=True)
            
            for item in reversed(st.session_state.review_history[-5:]):
                st.markdown(f"""
                <div class='history-item'>
                    <span class='lang-pill'>{item['language']}</span>
                    <span style='color:#8892b0; font-size:0.8rem; margin-left:0.5rem'>{item['time']}</span>
                    <div style='color:#e8eaf6; font-size:0.85rem; margin-top:4px;
                         white-space:nowrap; overflow:hidden; text-overflow:ellipsis'>{item['feature']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear", use_container_width=True, key="btn_clear"):
                st.session_state.review_history = []
                st.session_state.chat_history = []
                st.session_state.last_result = None
                st.rerun()
        with col2:
            if st.button("Logout", use_container_width=True, key="btn_logout"):
                for key in ["user", "access_token", "review_history", "chat_history", "last_result"]:
                    st.session_state.pop(key, None)
                st.rerun()