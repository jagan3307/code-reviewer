"""Documentation generation feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def generate_docs(code: str, language: str, doc_style: str) -> Optional[str]:
    prompt = f"""Generate comprehensive {doc_style} documentation for this {language} code.

```{language.lower()}
{code}
```

Include:
- Module/file-level docstring explaining purpose and usage
- Function/method docstrings with parameters, return types, raises, and examples
- Inline comments for complex logic
- A **Usage Examples** section with realistic code examples
- Any important **Notes** or **Warnings**

Return the fully documented code."""
    return query_ai(prompt)
