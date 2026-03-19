---
name: auto-quality
description: Automatically check code quality, logic errors, and security after each feature. Runs silently.
---

# Auto Quality Check

Runs silently after every feature:

1. Review code for logic errors, edge cases, missing validation
2. Check security basics (no hardcoded secrets, input validation)
3. If test framework available, write and run tests
4. If no test framework, do thorough code review
5. Refactor messy code without changing behavior

User never hears "running tests" or "tests failed."
User hears (only if relevant): "I found a small issue and fixed it."

Do NOT claim "all tests passed" unless a test framework actually ran.
