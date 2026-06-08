"""Code explanation feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def explain_code(code: str, language: str, level: str) -> Optional[str]:
    prompt = f"""Explain this {language} code for a {level} audience.

```{language.lower()}
{code}
```

Provide:
## 📖 Overview
What this code does in plain English.

## 🔍 Line-by-Line Walkthrough
Go through each logical section, explaining what it does and why.

## 🧩 Key Concepts Used
List the programming concepts, patterns, or algorithms used with brief explanations.

## 🌊 Data Flow
How data enters, transforms, and exits through the code.

## 💡 Key Insights
Interesting or non-obvious aspects worth noting."""
    return query_ai(prompt, temperature=0.4)
