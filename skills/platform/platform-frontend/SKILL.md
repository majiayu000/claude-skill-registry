---
name: platform-frontend
description: "Framework-agnostic frontend architecture patterns. Extends core-coding-standards with UI-specific rules. Use when building any web frontend."
---

# Principles

- Start with local state — lift only when shared
- Organize code by feature, not by type
- Use named exports for better refactoring and searchability
- Never use barrel files (index.ts re-exports) — they break tree-shaking and slow builds
- Measure before memoizing — don't optimize what isn't slow

# Rules

See `rules/` for detailed patterns.
