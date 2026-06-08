"""Complexity analysis feature."""
from __future__ import annotations
from typing import Optional
from core.ai_router import query_ai


def complexity_analysis(code: str, language: str) -> Optional[str]:
    prompt = f"""Analyze the computational complexity of this {language} code.

```{language.lower()}
{code}
```

Provide:
## ⏱ Time Complexity Analysis
- Overall: Big-O notation
- Per function/loop: breakdown
- Best / Average / Worst case

## 💾 Space Complexity Analysis
- Stack space, heap allocations
- Per data structure used

## 🔄 Algorithmic Patterns
Identify patterns (DP, divide & conquer, greedy, etc.)

## 🚀 Optimization Potential
Concrete algorithmic improvements with expected complexity gains

## 📊 Scalability Assessment
How does this code behave as input size grows? At what scale does it become problematic?"""
    return query_ai(prompt)
