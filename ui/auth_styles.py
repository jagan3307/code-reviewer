"""Styles specific to authentication pages."""

AUTH_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f1629;
    --bg-card: #131929;
    --bg-elevated: #1a2035;
    --accent-cyan: #00d4ff;
    --accent-purple: #7c3aed;
    --accent-green: #00ff88;
    --text-primary: #e8eaf6;
    --text-secondary: #8892b0;
    --border: #1e2a45;
}

* { font-family: 'Syne', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] { display: none !important; }

.auth-container {
    max-width: 440px;
    margin: 2rem auto;
    padding: 0 1rem;
}

.auth-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    position: relative;
    overflow: hidden;
}
.auth-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), transparent);
}

.auth-logo {
    text-align: center;
    margin-bottom: 2rem;
}
.auth-logo-icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
.auth-logo-name {
    font-size: 1.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.auth-logo-sub { color: var(--text-secondary); font-size: 0.85rem; }

.auth-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}
.auth-subtitle { color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem; }

.stTextInput input {
    background: var(--bg-elevated) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-size: 0.95rem !important;
}
.stTextInput input:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.2) !important;
}
.stTextInput label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--accent-purple), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 0.65rem !important;
    font-size: 0.95rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important;
}

.google-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    color: var(--text-primary) !important;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s;
    text-decoration: none;
}
.google-btn:hover {
    border-color: var(--accent-cyan) !important;
    background: #1e2a45 !important;
}

.divider {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 1.2rem 0;
    color: var(--text-muted);
    font-size: 0.8rem;
}
.divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

.auth-link {
    color: var(--accent-cyan) !important;
    text-decoration: none !important;
    font-weight: 600;
}
.auth-footer {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.88rem;
    margin-top: 1.5rem;
}

.stAlert { background: var(--bg-elevated) !important; border-radius: 8px !important; }
</style>
"""
