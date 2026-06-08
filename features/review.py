"""Full code review feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def full_review(code: str, language: str, context: str, review_depth: str) -> Optional[str]:
    depth_map = {"Quick": "concise", "Standard": "thorough", "Deep Dive": "extremely detailed and comprehensive"}
    prompt = f"""Perform a {depth_map.get(review_depth, 'thorough')} code review on the following {language} code.
Context/Purpose: {context or 'Not provided'}

```{language.lower()}
{code}
```

Provide a structured review covering:

## 🎯 Overall Assessment
Rate the code quality (1-10) and give a 2-3 sentence executive summary.

## 🔴 Critical Issues
List bugs, security vulnerabilities, or correctness problems. For each: describe the issue, why it matters, and the fix.

## 🟡 Warnings & Code Smells
Anti-patterns, poor practices, maintainability concerns.

## 🔵 Optimization Opportunities
Performance improvements, algorithmic enhancements, memory efficiency.

## ✅ Strengths
What the code does well (be specific).

## 📋 Recommendations Summary
Prioritized action items (P1/P2/P3).
"""
    return query_ai(prompt)
