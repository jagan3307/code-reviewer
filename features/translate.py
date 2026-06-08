"""Code translation feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def translate_code(code: str, source_lang: str, target_lang: str) -> Optional[str]:
    prompt = f"""Translate this {source_lang} code to idiomatic {target_lang}.

```{source_lang.lower()}
{code}
```

Requirements:
1. **Preserve all functionality** exactly
2. Use **{target_lang} idioms and conventions** (not a literal translation)
3. Apply language-specific **best practices**
4. Handle **type system differences** appropriately
5. Note any **behavioral differences** between languages

Return:
- The translated code in a proper code block
- A **Translation Notes** section explaining key adaptations"""
    return query_ai(prompt)
