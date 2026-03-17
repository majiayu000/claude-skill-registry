---
name: git-operation
description: Guide for basic Git operations
---

# Git Operation Skill

This skill provides a guide for performing basic Git operations especially for
committing changes.

## Committing Changes

- Git commit messages must always be written in English
- Summarize the changes concisely in the first line of the commit message
- If detailed explanations or additional information are needed in the commit
  message, insert a blank line after the first line, then describe them in
  bullet points
- Always run `mise run fmt` to format the code before committing
- Always run `mise run test` before committing code changes to ensure no tests
  are failing
