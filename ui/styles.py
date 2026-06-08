"""Global CSS styles for CodeSage AI."""

MAIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #0f1629;
    --bg-card: #131929;
    --bg-elevated: #1a2035;
    --accent-cyan: #00d4ff;
    --accent-purple: #7c3aed;
    --accent-green: #00ff88;
    --accent-orange: #ff6b35;
    --accent-red: #ff4757;
    --accent-yellow: #ffd32a;
    --text-primary: #e8eaf6;
    --text-secondary: #8892b0;
    --text-muted: #4a5568;
    --border: #1e2a45;
    --border-glow: rgba(0, 212, 255, 0.3);
}

* { font-family: 'Syne', sans-serif !important; }
code, pre, .stCode * { font-family: 'JetBrains Mono', monospace !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

.stTextArea textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px var(--border-glow) !important;
}

.stTextInput input, .stSelectbox select {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent-purple), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
    padding: 0.5rem 1.5rem !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4) !important;
}

.hero-banner {
    background: linear-gradient(135deg, #0f1629 0%, #1a1035 50%, #0f1629 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), transparent);
}
.hero-title {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.25rem 0;
}
.hero-sub {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin: 0;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s;
}
.metric-card:hover { border-color: var(--accent-cyan); transform: translateY(-2px); }
.metric-number {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.metric-label { color: var(--text-secondary); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
}
.badge-critical { background: rgba(255,71,87,0.15); color: var(--accent-red); border: 1px solid rgba(255,71,87,0.3); }
.badge-warning  { background: rgba(255,211,42,0.15); color: var(--accent-yellow); border: 1px solid rgba(255,211,42,0.3); }
.badge-info     { background: rgba(0,212,255,0.1); color: var(--accent-cyan); border: 1px solid rgba(0,212,255,0.2); }
.badge-success  { background: rgba(0,255,136,0.1); color: var(--accent-green); border: 1px solid rgba(0,255,136,0.2); }

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-elevated) !important;
    color: var(--accent-cyan) !important;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: var(--text-primary) !important; }
.stMarkdown p, .stMarkdown li { color: var(--text-secondary) !important; }
.stMarkdown code {
    background: var(--bg-elevated) !important;
    color: var(--accent-cyan) !important;
    border-radius: 4px !important;
    padding: 1px 5px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.stMarkdown pre { background: var(--bg-elevated) !important; border-radius: 8px !important; }
.stAlert { background: var(--bg-card) !important; border-radius: 8px !important; }

.history-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    transition: all 0.2s;
}
.history-item:hover { border-color: var(--accent-purple); }

.lang-pill {
    background: rgba(124,58,237,0.2);
    color: #a78bfa;
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}

hr { border-color: var(--border) !important; }

[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

.stSlider > div > div { background: var(--accent-purple) !important; }
.stCheckbox label { color: var(--text-primary) !important; }
.stRadio label { color: var(--text-primary) !important; }
</style>
"""
