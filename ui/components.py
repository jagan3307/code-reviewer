"""Reusable UI components for CodeSage AI."""
import streamlit as st


def hero_banner():
    st.markdown("""
    <div class='hero-banner'>
        <h1 class='hero-title'>🔬 CodeSage AI</h1>
        <p class='hero-sub'>Enterprise-grade code review, security auditing, documentation & refactoring — powered by LLMs</p>
    </div>
    """, unsafe_allow_html=True)


def check_code(code_input: str) -> bool:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code first!")
        return False
    return True


def save_history(feature: str, language: str, code_input: str):
    from datetime import datetime
    st.session_state.review_history.append({
        "feature": feature,
        "language": language,
        "time": datetime.now().strftime("%H:%M"),
        "code_preview": code_input[:80]
    })


def security_notice():
    st.markdown("""
    <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
         border-radius:8px; padding:0.75rem 1rem; margin-bottom:1rem'>
        <span style='color:#ff4757'>🔒</span>
        <span style='color:#8892b0; font-size:0.9rem'>
            Performs OWASP-aligned security analysis. Results are advisory — always verify with dedicated security tools.
        </span>
    </div>
    """, unsafe_allow_html=True)


def chat_message(role: str, content: str):
    role_icon = "👤" if role == "user" else "🔬"
    bg = "rgba(124,58,237,0.1)" if role == "user" else "rgba(0,212,255,0.05)"
    label = "You" if role == "user" else "CodeSage"
    st.markdown(f"""
    <div style='background:{bg}; border-radius:10px; padding:0.75rem 1rem; margin:0.5rem 0'>
        <div style='color:#4a5568; font-size:0.75rem; margin-bottom:4px'>{role_icon} {label}</div>
        <div style='color:#e8eaf6'>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def footer():
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#2d3748; font-size:0.8rem; padding:1rem 0'>
        CodeSage AI · Built with Streamlit · Powered by Groq & Gemini
    </div>
    """, unsafe_allow_html=True)
