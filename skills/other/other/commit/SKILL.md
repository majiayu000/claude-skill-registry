---
name: commit
description: Helps write conventional commit messages, create atomic commits, and follow git best practices. Use when the agent needs to help with git commits, commit message writing, or git workflow guidance.
---

# Commit Skill

## Workflow
1. **Analyze Results**: Review `git status` and `git diff --staged`.
2. **Draft Message**: Follow [Conventional Commits](references/conventional-commits.md).
   - `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
   - Max 50 chars for subject.
   - Explain "why" in body if needed (wrap at 72).
3. **Atomic Commits**: Ensure one logical change per commit.
4. **Templates**: Use `assets/commit-template.txt` for consistency.

## Safe Git Commands
- `git add <files>`
- `git commit -m "message"`
- `git diff --staged`
- `git status`, `git show`, `git log --oneline`

## Limitations
- No interactive commands (`git add -p`, `git rebase -i`).
- No force pushing or amending without explicit user guidance.
- Always confirm before final commit/push.
