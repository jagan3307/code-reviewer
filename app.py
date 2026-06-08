"""
CodeSage AI — Main Entry Point
================================
Run with:  streamlit run app.py
"""
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="CodeSage AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrapping ────────────────────────────────────────────────────────────
from utils.session import init_session
init_session()

# ── Google OAuth callback (check before rendering anything) ─────────────────
from auth.google_auth import handle_google_callback

if handle_google_callback():
    st.rerun()

# ── Route to auth pages if not logged in ────────────────────────────────────
from auth.auth_guard import is_authenticated

if not is_authenticated():
    page = st.query_params.get("page", "login")
    if page == "signup":
        from auth.signup import render_signup
        render_signup()
    elif page == "forgot":
        from auth.forgot_password import render_forgot_password
        render_forgot_password()
    else:
        from auth.login import render_login
        render_login()
    st.stop()

# ── Authenticated: render main app ───────────────────────────────────────────
from ui.styles import MAIN_CSS
from ui.sidebar import render_sidebar
from ui.components import hero_banner, check_code, footer
from utils.history import save_history

from features.review import full_review
from features.refactor import generate_refactored
from features.docs import generate_docs
from features.security import find_security
from features.explain import explain_code
from features.complexity import complexity_analysis
from features.tests import generate_tests
from features.translate import translate_code
from features.chat import chat_about_code

st.markdown(MAIN_CSS, unsafe_allow_html=True)

render_sidebar()
hero_banner()

# ── Code Input & Settings ────────────────────────────────────────────────────
col_in, col_cfg = st.columns([3, 1])

with col_in:
    st.markdown("**📝 Code Input**")
    code_input = st.text_area(
        label="code_area",
        label_visibility="collapsed",
        placeholder="# Paste your code here...\n\ndef example():\n    pass",
        height=280,
        key="code_input",
    )

with col_cfg:
    st.markdown("**🔧 Settings**")
    language = st.selectbox("Language", [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go",
        "Rust", "C#", "PHP", "Ruby", "Swift", "Kotlin", "SQL", "Shell",
        "R", "Scala", "Dart", "Haskell", "Other",
    ])
    review_depth = st.select_slider("Review Depth", ["Quick", "Standard", "Deep Dive"], value="Standard")
    context = st.text_input("Context (optional)", placeholder="What does this code do?")

# ── Feature Tabs ─────────────────────────────────────────────────────────────
st.markdown("---")
tabs = st.tabs([
    "🔍 Full Review", "✨ Refactor", "📚 Docs", "🔒 Security",
    "📖 Explain", "📊 Complexity", "🧪 Tests", "🔄 Translate", "💬 Chat",
])

# ── Tab 1: Full Review ───────────────────────────────────────────────────────
with tabs[0]:
    st.markdown("Comprehensive code review covering quality, bugs, style, and best practices.")
    if st.button("🚀 Run Full Review", use_container_width=True, key="btn_review"):
        if check_code(code_input):
            with st.spinner("Analyzing code..."):
                result = full_review(code_input, language, context, review_depth)
            if result:
                save_history("Full Review", language, code_input, result)
                st.markdown(result)

# ── Tab 2: Refactor ──────────────────────────────────────────────────────────
with tabs[1]:
    refactor_focus = st.multiselect(
        "Refactoring Goals",
        ["Readability", "Performance", "DRY principle", "SOLID principles", "Error handling",
         "Type safety", "Modularity", "Naming conventions", "Modern syntax", "Memory efficiency"],
        default=["Readability", "Performance"],
    )
    if st.button("✨ Refactor Code", use_container_width=True, key="btn_refactor"):
        if check_code(code_input):
            with st.spinner("Refactoring..."):
                result = generate_refactored(code_input, language, refactor_focus)
            if result:
                save_history("Refactor", language, code_input, result)
                st.markdown(result)

# ── Tab 3: Documentation ─────────────────────────────────────────────────────
with tabs[2]:
    doc_style_map = {
        "Python": ["Google Style", "NumPy Style", "Sphinx/RST", "Epytext"],
        "JavaScript": ["JSDoc", "TSDoc"],
        "TypeScript": ["TSDoc", "JSDoc"],
        "Java": ["Javadoc"],
    }
    available_styles = doc_style_map.get(language, ["Generic Docstring", "JSDoc", "Google Style"])
    doc_style = st.selectbox("Documentation Style", available_styles)
    if st.button("📚 Generate Docs", use_container_width=True, key="btn_docs"):
        if check_code(code_input):
            with st.spinner("Generating documentation..."):
                result = generate_docs(code_input, language, doc_style)
            if result:
                save_history("Documentation", language, code_input, result)
                st.markdown(result)

# ── Tab 4: Security ───────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown("""
    <div style='background:rgba(255,71,87,0.08); border:1px solid rgba(255,71,87,0.2);
         border-radius:8px; padding:0.75rem 1rem; margin-bottom:1rem'>
        <span style='color:#ff4757'>🔒</span>
        <span style='color:#8892b0; font-size:0.9rem'>
            OWASP-aligned security analysis. Results are advisory — always verify with dedicated tools.
        </span>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔒 Security Audit", use_container_width=True, key="btn_security"):
        if check_code(code_input):
            with st.spinner("Running security audit..."):
                result = find_security(code_input, language)
            if result:
                save_history("Security Audit", language, code_input, result)
                st.markdown(result)

# ── Tab 5: Explain ────────────────────────────────────────────────────────────
with tabs[4]:
    explain_level = st.radio("Audience Level", ["Beginner", "Intermediate", "Expert"], horizontal=True)
    if st.button("📖 Explain Code", use_container_width=True, key="btn_explain"):
        if check_code(code_input):
            with st.spinner("Preparing explanation..."):
                result = explain_code(code_input, language, explain_level)
            if result:
                save_history("Explain", language, code_input, result)
                st.markdown(result)

# ── Tab 6: Complexity ──────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown("Analyze time complexity, space complexity, and algorithmic patterns.")
    if st.button("📊 Analyze Complexity", use_container_width=True, key="btn_complexity"):
        if check_code(code_input):
            with st.spinner("Analyzing complexity..."):
                result = complexity_analysis(code_input, language)
            if result:
                save_history("Complexity Analysis", language, code_input, result)
                st.markdown(result)

# ── Tab 7: Tests ──────────────────────────────────────────────────────────────
with tabs[6]:
    test_framework_map = {
        "Python": ["pytest", "unittest", "hypothesis"],
        "JavaScript": ["Jest", "Vitest", "Mocha + Chai"],
        "TypeScript": ["Jest + ts-jest", "Vitest"],
        "Java": ["JUnit 5", "TestNG", "Mockito"],
        "C#": ["xUnit", "NUnit", "MSTest"],
        "Go": ["testing (stdlib)", "testify"],
        "Rust": ["cargo test (built-in)", "proptest"],
    }
    frameworks = test_framework_map.get(language, ["Generic test framework"])
    test_fw = st.selectbox("Testing Framework", frameworks)
    if st.button("🧪 Generate Tests", use_container_width=True, key="btn_tests"):
        if check_code(code_input):
            with st.spinner("Generating test suite..."):
                result = generate_tests(code_input, language, test_fw)
            if result:
                save_history("Generate Tests", language, code_input, result)
                st.markdown(result)

# ── Tab 8: Translate ──────────────────────────────────────────────────────────
with tabs[7]:
    all_langs = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go",
                 "Rust", "C#", "PHP", "Ruby", "Swift", "Kotlin", "Dart"]
    target_lang = st.selectbox("Translate to", [l for l in all_langs if l != language])
    if st.button("🔄 Translate Code", use_container_width=True, key="btn_translate"):
        if check_code(code_input):
            with st.spinner(f"Translating {language} → {target_lang}..."):
                result = translate_code(code_input, language, target_lang)
            if result:
                save_history(f"Translate → {target_lang}", language, code_input, result)
                st.markdown(result)

# ── Tab 9: Chat ───────────────────────────────────────────────────────────────
with tabs[8]:
    st.markdown("Ask anything about your code — architecture, specific lines, alternatives, or concepts.")

    for msg in st.session_state.chat_history:
        from ui.components import chat_message
        chat_message(msg["role"], msg["content"])

    col_q, col_btn = st.columns([5, 1])
    with col_q:
        question = st.text_input(
            "Ask a question about your code",
            placeholder="e.g. Why is this function slow? How can I make it async?",
            label_visibility="collapsed",
            key="chat_input",
        )
    with col_btn:
        send = st.button("Send", use_container_width=True, key="btn_chat")

    if send and question:
        if not code_input.strip():
            st.warning("⚠️ Paste some code first so I have context!")
        else:
            st.session_state.chat_history.append({"role": "user", "content": question})
            with st.spinner("Thinking..."):
                reply = chat_about_code(code_input, language, question, st.session_state.chat_history[:-1])
            if reply:
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.chat_history = []
        st.rerun()

# ── Footer ───────────────────────────────────────────────────────────────────
footer()