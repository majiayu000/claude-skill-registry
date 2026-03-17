---
name: in-code-comments
description: "Use when writing or reviewing in-code comments. Explains the 'why not how' standard."
user-invocable: false
---

# In-code Comments

## Purpose

This skill guides you, the AI agent, in writing effective, maintainable, and "Clean Code" compliant in-code comments. It enforces the principle that comments should elucidate what the code *cannot* say on its own, rather than merely summarizing the code's actions. This avoids redundancy and fragility during updates.

## Guiding Principles

- **Explain the "Why", Not the "How"**: Your primary role when commenting is to explain the intent, design decisions, or the rationale behind a piece of code when it's non-obvious. The code itself explains *how* it works; the comment should explain *why* it exists.
- **Clarity Through Context**: Use comments to provide context that is not available in the code, such as clarifying intricate algorithms, business logic, or the purpose of complex regular expressions.
- **Document Non-Obvious Behaviors & Pitfalls**: Proactively highlight potential edge cases, known issues, necessary workarounds, or non-intuitive behaviors. Documenting design trade-offs (e.g., "Chose this approach for performance reasons despite lower readability") is invaluable for future maintenance.
- **Strictly Avoid Redundant Summaries**: NEVER write comments that simply restate what the code is doing (e.g., `// Initialize x to 10` for `const x = 10;`). This adds visual clutter and, more importantly, creates a maintenance burden, as the comment can easily become outdated and misleading.
- **A‑temporal Comments (Required)**: Write comments in a timeless, present‑tense, declarative style. Avoid time-coupled phrasing such as "now", "currently", "recently", "old/new", or historical notes. Use present tense that describes what the code does, NOT what changed: "Validates JWT and returns 401 on failure". Avoid talking about history or the past. E.g. AVOID statements like "Refactored from using the new v2 API to using the new v3 API".

## When This Rule Should Be Followed

The principles in this rule are foundational for all code generation and modification. They must be applied **anytime you write or modify code** within any programming file (e.g., `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.java`, etc.).

**This rule should be considered auto-attached and always active when you are working with source code files.**
