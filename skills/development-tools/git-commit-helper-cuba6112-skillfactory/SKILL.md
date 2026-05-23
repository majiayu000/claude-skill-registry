---
name: git-commit-helper
description: Adherence to Conventional Commits and efficient Git history management using types, scopes, and advanced commit tools like fixup/amend. Triggers: git-commit, conventional-commits, breaking-change, fixup, git-amend, rebase.
---

# Git Commit Helper

## Overview
Conventional Commits provide a standardized format for commit messages, enabling automated versioning and clearer project history. This skill covers formatting, managing breaking changes, and using advanced Git features like `fixup` for a clean history.

## When to Use
- **Professional Collaboration**: To make histories readable and searchable.
- **Automated Releases**: To trigger Semantic Versioning bumps (PATCH/MINOR/MAJOR).
- **Clean History**: To fix small mistakes in previous commits without creating "junk" commits.

## Decision Tree
1. Does the change add a new capability? 
   - YES: Type `feat` (MINOR bump).
2. Does it fix a bug? 
   - YES: Type `fix` (PATCH bump).
3. Does it break backward compatibility? 
   - YES: Append `!` after type/scope OR add `BREAKING CHANGE:` footer (MAJOR bump).
4. Did you forget a small detail in the last commit? 
   - YES: Use `git commit --amend` or `--fixup`.

## Workflows

### 1. Formatting a Feature Commit
1. Start the message with `feat` and an optional scope in parentheses (e.g., `feat(auth):`).
2. Provide a concise description of the new capability.
3. If the change breaks compatibility, append `!` to the type or add a `BREAKING CHANGE:` footer.
4. Run `git commit -m "..."` using the formatted string.

### 2. Using Fixup for Clean History
1. Identify the SHA of the commit needing a minor fix.
2. Run `git commit --fixup <SHA>` to stage the fix as a `fixup!` commit.
3. Later, perform `git rebase -i --autosquash` to automatically merge the fix into the original commit.

### 3. Amending the Last Commit
1. Stage any missed changes using `git add`.
2. Run `git commit --amend --no-edit` to update the last commit with new files while keeping the same message.
3. Alternatively, use `--amend` without `--no-edit` to refine the commit message structure.

## Non-Obvious Insights
- **Case Sensitivity**: Conventional Commit units are not case-sensitive, EXCEPT for `BREAKING CHANGE`, which MUST be uppercase.
- **Breaking Change Indicator**: The `!` indicator is a shorthand for marking API breaks without needing a full footer.
- **Trailers**: Footers should follow the Git trailer convention (`word-token: value`) to be recognized by automated tools.

## Evidence
- "feat: a commit of the type feat introduces a new feature... (this correlates with MINOR in Semantic Versioning)." - [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- "The units... MUST NOT be treated as case sensitive... with the exception of BREAKING CHANGE which MUST be uppercase." - [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- "--fixup=reword:<commit> creates an 'amend!' commit which replaces the log message..." - [Git Docs](https://git-scm.com/docs/git-commit)

## Scripts
- `scripts/git-commit-helper_tool.py`: Script to generate conventional commit messages via CLI.
- `scripts/git-commit-helper_tool.js`: Shell wrapper for executing `fixup` and `amend` commands.

## Dependencies
- `git` (CLI tool)

## References
- [references/README.md](references/README.md)