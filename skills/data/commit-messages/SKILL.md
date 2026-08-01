---
name: commit-messages
description: Use this skill to draft a commit message for staged changes. Execute
  Skill(sanctum:git-workspace-review) first to capture the repository path, status,
  and diffs. If no changes are staged, stage the relevant files before continuing.
---

---
name: commit-messages
description: |

Triggers: messages, conventional-commits, git, changelog, commit
  Generate conventional commit messages from staged changes with correct type/scope.

  Triggers: commit message, conventional commit, git commit
  Use when: generating commit messages in conventional commits format
  DO NOT use when: full PR preparation - use pr-prep instead.
category: artifact-generation
tags: [git, commit, conventional-commits, changelog]
tools: [Bash, Write, TodoWrite]
complexity: low
estimated_tokens: 600
dependencies:
  - sanctum:shared
  - sanctum:git-workspace-review
version: 1.3.7
---

# Conventional Commit Workflow

## Usage

Use this skill to draft a commit message for staged changes. Execute `Skill(sanctum:git-workspace-review)` first to capture the repository path, status, and diffs. If no changes are staged, stage the relevant files before continuing.

## Required Steps

1. **Validate Code Quality**: Run `make format && make lint`. Fix any reported errors before proceeding. Do not bypass pre-commit hooks with `--no-verify` or `-n`.
2. **Classify the Change**: Choose a type from `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, or `ci`. Select an optional but preferred scope (e.g., `core`, `cli`). Identify breaking changes for the `BREAKING CHANGE:` footer.
3. **Draft the Message**:
    - **Subject**: `<type>(<scope>): <imperative summary>` (≤50 characters).
    - **Body**: Wrap at 72 characters. Explain the "what" and "why" behind the change. Use paragraphs for technical rationale.
    - **Footer**: Include breaking change details or issue references.
4. **Write the Output**: Use a relative path (e.g., `./commit_msg.txt`) to save the message. Overwrite the file with the final message only, without commentary.
5. **Preview**: Display the file contents using `cat` or `sed` for confirmation.

## Guardrails

Do not use `git commit --no-verify` or the `-n` flag. Pre-commit hooks are mandatory; fix issues rather than bypassing them. Commit messages must not include AI attribution or filler words like "leverage" or "seamless." Use a plain-text, human voice with present-tense imperative style for the subject line. Multi-line bodies are required for complex changes to explain the technical reasoning.

## Technical Integration

Combine this skill with `Skill(imbue:catchup)` or `/git-catchup` if additional context is needed. If the type or scope is unclear, re-examine the diffs or consult the project plan before finalizing the draft.

## Troubleshooting

Address specific errors reported by pre-commit hooks. Run `make format` to resolve styling issues and `make lint` for logic or style violations. Fix all detected issues before re-attempting the commit. If a merge conflict occurs, use `git merge --abort` to return to a clean state. A rejected commit indicates a failed quality gate; analyze the output and apply fixes before retrying.
