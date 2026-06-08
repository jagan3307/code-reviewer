"""Code refactoring feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def generate_refactored(code: str, language: str, focus: list) -> Optional[str]:
    focus_str = ", ".join(focus) if focus else "general improvements"
    prompt = f"""Refactor this {language} code focusing on: {focus_str}.

Original code:
```{language.lower()}
{code}
```

Provide:
1. **Refactored Code** — clean, well-structured, production-ready code in a code block
2. **Change Log** — bullet list of every change made and why
3. **Before/After Comparison** — key improvements highlighted

Make the code exemplary. Apply modern best practices and idioms for {language}."""
    return query_ai(prompt)
