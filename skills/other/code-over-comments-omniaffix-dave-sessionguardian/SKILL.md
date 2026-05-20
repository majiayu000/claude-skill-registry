---
name: code-over-comments
description: If you need a comment to explain what code does, first try to rewrite the code to be self-explana... Use when enforcing code quality standards. Quality category skill.
metadata:
  category: Quality
  priority: medium
  is-built-in: true
  session-guardian-id: builtin_code_over_comments
---

# Code Over Comments

If you need a comment to explain what code does, first try to rewrite the code to be self-explanatory. Extract complex expressions into well-named variables. Split complex functions into smaller ones with descriptive names. Comments are valuable for explaining WHY something is done (business context, non-obvious constraints), but WHAT the code does should be clear from the code itself.