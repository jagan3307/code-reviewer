"""Test generation feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def generate_tests(code: str, language: str, framework: str) -> Optional[str]:
    prompt = f"""Generate comprehensive unit tests for this {language} code using {framework}.

```{language.lower()}
{code}
```

Write tests covering:
- **Happy path** — normal expected usage
- **Edge cases** — boundary values, empty inputs, max values
- **Error cases** — invalid inputs, exceptions
- **Integration points** — external dependencies (mock them)

Make tests:
- Well-named (describe behavior, not implementation)
- Independent and isolated
- Fast and deterministic
- Following AAA pattern (Arrange, Act, Assert)

Return complete, runnable test code with all imports."""
    return query_ai(prompt)
