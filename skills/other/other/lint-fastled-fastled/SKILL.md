---
name: lint
description: Run code linting and formatting checks across the codebase. Use after modifying source files to ensure coding standards are met.
context: fork
agent: lint-agent
---

Run linting and formatting checks across the codebase using `bash lint`.

Report results in a clear, actionable format showing any formatting or linting violations found.

For JavaScript files, also run `bash lint --js`.
