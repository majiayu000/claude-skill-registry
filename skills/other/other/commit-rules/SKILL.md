---
name: commit-rules
description: "Shared commit message rules and technical constraints referenced by $stage-commit and $commit-staged. Not typically invoked directly."
---

# Commit Rules

## Commit Message Rules

- Match the style from `git log -n 10 --oneline`
- Concise and descriptive
- Imperative mood, present tense
- Aim for ≤100 characters in the subject
- No commit description—summarize everything in the message
- Don't reference `.turbo/` content (filenames, IDs, headings) in commit messages. `.turbo/` is gitignored, so these references would be opaque to anyone reading without local copies.

## Technical Constraints

- Use `git commit -m "message"` directly—do not use heredoc syntax (sandbox blocks temp file creation)
- Never bypass commit signing (`--no-gpg-sign`, `-c commit.gpgsign=false`). If signing fails, use `request_user_input` to let the user resolve it—they may need to approve a key prompt.
