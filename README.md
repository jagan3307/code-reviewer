# 🔬 CodeSage AI

Enterprise-grade code review, security auditing, documentation & refactoring — powered by Groq & Gemini LLMs.

---

## Features

| Tab | What It Does |
|-----|-------------|
| 🔍 Full Review | Deep analysis: bugs, warnings, optimizations, strengths, prioritized action items |
| ✨ Refactor | Multi-goal refactoring (SOLID, DRY, performance, type safety…) with change log |
| 📚 Docs | Language-specific docstrings — Google/NumPy/Sphinx, JSDoc, Javadoc, etc. |
| 🔒 Security | OWASP Top 10 scan with severity levels (CRITICAL/HIGH/MEDIUM/LOW) + CWE IDs |
| 📖 Explain | Beginner / Intermediate / Expert explanations with data flow walkthrough |
| 📊 Complexity | Big-O time + space analysis, algorithmic pattern detection, scalability notes |
| 🧪 Tests | Full test suite with pytest, Jest, JUnit, Go testing, etc. |
| 🔄 Translate | Idiomatic translation between 15 languages |
| 💬 Chat | Conversational multi-turn Q&A about your specific code |

---

## Project Structure

```
code_review_assistant/
├── app.py                  ← Main Streamlit entry point
├── requirements.txt
├── .env.example            ← Copy to .env and fill in keys
│
├── auth/
│   ├── auth_guard.py       ← Protect routes; check login state
│   ├── google_auth.py      ← Full Google OAuth 2.0 flow
│   ├── login.py            ← Email/password + Google login page
│   ├── signup.py           ← Registration page
│   ├── forgot_password.py  ← Password reset page
│   └── logout.py           ← Clears session + Supabase sign-out
│
├── core/
│   ├── groq_client.py      ← Groq API wrapper
│   ├── gemini_client.py    ← Gemini API wrapper
│   └── ai_router.py        ← Unified query_ai() / multi-turn helper
│
├── database/
│   ├── supabase_client.py  ← Supabase singleton
│   ├── users.py            ← User upsert/fetch
│   ├── reports.py          ← Persist/retrieve review results
│   └── history.py          ← Chat history persistence
│
├── features/
│   ├── review.py           ← Full code review
│   ├── refactor.py         ← Refactoring
│   ├── docs.py             ← Documentation generation
│   ├── security.py         ← Security audit
│   ├── explain.py          ← Code explanation
│   ├── complexity.py       ← Complexity analysis
│   ├── tests.py            ← Test generation
│   ├── translate.py        ← Language translation
│   └── chat.py             ← Conversational chat
│
├── ui/
│   ├── styles.py           ← Main app CSS
│   ├── auth_styles.py      ← Auth page CSS
│   ├── sidebar.py          ← Sidebar component
│   └── components.py       ← Reusable UI helpers
│
└── utils/
    ├── session.py          ← Session state initializer
    └── history.py          ← History save helpers (session + DB)
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
# At minimum, one of these:
GROQ_API_KEY=...       # free at console.groq.com/keys
GEMINI_API_KEY=...     # free at aistudio.google.com/app/apikey

# For user accounts (optional but recommended):
SUPABASE_URL=...
SUPABASE_ANON_KEY=...

# For Google Login (optional):
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
GOOGLE_REDIRECT_URI=http://localhost:8501/
```

### 3. Set up Supabase (optional, for persistent accounts)

Run this SQL in your Supabase SQL editor:

```sql
-- Users table
create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  full_name text,
  avatar_url text,
  created_at timestamptz default now()
);

-- Review reports table
create table if not exists reports (
  id uuid primary key default gen_random_uuid(),
  user_email text references users(email),
  feature text,
  language text,
  code_snippet text,
  result text,
  created_at timestamptz default now()
);

-- Chat history table
create table if not exists chat_history (
  id uuid primary key default gen_random_uuid(),
  user_email text references users(email),
  session_id text,
  role text,
  content text,
  created_at timestamptz default now()
);
```

### 4. Set up Google OAuth (optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project → **APIs & Services** → **Credentials** → **OAuth 2.0 Client ID**
3. Application type: **Web application**
4. Authorised redirect URIs: `http://localhost:8501/` (and your production URL)
5. Copy **Client ID** and **Client Secret** → paste into `.env`

### 5. Run

```bash
streamlit run app.py
```

---

## Usage Without Accounts

The app works fully without Supabase or Google OAuth — just enter your Groq or Gemini API key in the sidebar. Auth is only needed for persistent history across sessions.

---

## Tech Stack

- **Frontend**: Streamlit
- **LLMs**: Groq (Llama 3.3, Mixtral) · Google Gemini
- **Auth**: Supabase Auth + Google OAuth 2.0
- **Database**: Supabase (PostgreSQL)
