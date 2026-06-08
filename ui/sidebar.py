"""Sidebar component for CodeSage AI."""
import streamlit as st
import os


def render_sidebar():
    """Render the main app sidebar."""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style='text-align:center; padding: 1rem 0 1.5rem'>
            <div style='font-size:2.5rem'>🔬</div>
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
        st.markdown("**⚙️ API Configuration**")
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

        placeholder = "Auto-loaded from .env ✓" if env_key else "Paste your API key here"
        st.text_input("API Key", type="password", value=env_key, placeholder=placeholder, key="api_key")
        if env_key:
            st.markdown("<span style='color:#00ff88; font-size:0.78rem'>✅ Key loaded from <code>.env</code></span>", unsafe_allow_html=True)
        st.markdown(f"<a href='{api_link}' target='_blank' style='color:#7c3aed; font-size:0.8rem'>🔑 Get free API key →</a>", unsafe_allow_html=True)

        st.markdown("---")

        # Session Stats
        st.markdown("**📂 Session Stats**")
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
            st.markdown("**🕐 Recent Reviews**")
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
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.review_history = []
                st.session_state.chat_history = []
                st.session_state.last_result = None
                st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                for key in ["user", "access_token", "review_history", "chat_history", "last_result"]:
                    st.session_state.pop(key, None)
                st.rerun()
