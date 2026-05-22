---
name: review-ai
description: Review changes made by AI editors (Codex, Claude, etc.). Run git diff, lint, security scan, tests, and provide a code review.
disable-model-invocation: true
---

Review changes made by an AI editor. Follow these steps:

1. Run `git diff` and `git status -s` to see all uncommitted changes (staged, unstaged, and untracked files)
2. For any new untracked files, read them fully
3. Analyze every change for:
   - Bugs or logic errors
   - Security issues (SQL injection, XSS, etc.)
   - Style consistency with the rest of the codebase
   - Missing edge cases
   - Unnecessary or over-engineered code
4. Run CI checks on changed files:
   - `bin/brakeman --no-pager` (scan_ruby: security vulnerabilities)
   - `bin/importmap audit` (scan_js: JS dependency vulnerabilities)
   - `bin/rubocop` (lint: code style)
   - `PARALLEL_WORKERS=0 bin/rails db:test:prepare test test:system` (test: unit/integration/system tests)
   - For reviews, always run the exact command above to include system tests.
5. Provide a structured review:
   - Summary of what changed
   - CI results (pass/fail for each check)
   - File-by-file comments (only where there are issues)
   - Overall verdict: approve / needs fixes
