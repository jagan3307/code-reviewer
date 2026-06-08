"""Security audit feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def find_security(code: str, language: str) -> Optional[str]:
    prompt = f"""Perform a thorough security audit of this {language} code.

```{language.lower()}
{code}
```

Analyze for:
- **Injection vulnerabilities** (SQL, command, XSS, etc.)
- **Authentication/Authorization flaws**
- **Insecure data handling** (secrets, PII, passwords)
- **Cryptographic weaknesses**
- **Input validation issues**
- **OWASP Top 10** relevant issues
- **Dependency risks** (if visible)

For each finding:
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **CWE ID** (if applicable)
- **Description**: What the vulnerability is
- **Attack Scenario**: How it could be exploited
- **Remediation**: Exact fix with code example

End with an overall **Security Score (0-100)** and **Risk Summary**."""
    return query_ai(prompt)
