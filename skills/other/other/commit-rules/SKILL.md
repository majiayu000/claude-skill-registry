---
name: commit-rules
description: "Shared commit message rules and technical constraints referenced by /stage-commit and /commit-staged. Not typically invoked directly."
---

# Commit Rules

## Commit Message Rules

- Match the style from `git log -n 10 --oneline`
- Concise and descriptive
- Imperative mood, present tense
- No commit description—summarize everything in the message

## Technical Constraints

- Use `git commit -m "message"` directly—do not use heredoc syntax (sandbox blocks temp file creation)
- Never bypass commit signing (`--no-gpg-sign`, `-c commit.gpgsign=false`). If signing fails, use `AskUserQuestion` to let the user resolve it—they may need to approve a key prompt.
