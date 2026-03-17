---
name: commit-messages
description: |
  Generate conventional commit messages from staged changes with correct type/scope.

  commit message, conventional commit, git commit
  Use when: generating commit messages in conventional commits format
  DO NOT use when: full PR preparation - use pr-prep instead.
category: artifact-generation
tags: [git, commit, conventional-commits, changelog, slop-free]
tools: [Bash, Write, TodoWrite]
complexity: low
estimated_tokens: 700
dependencies:
  - sanctum:shared
  - sanctum:git-workspace-review
  - scribe:slop-detector
version: 1.4.0
---

# Conventional Commit Workflow


## When To Use

- Generating conventional commit messages from staged changes
- Ensuring commit messages follow project conventions

## When NOT To Use

- Full PR preparation - use sanctum:pr-prep instead
- Amending existing commits - use git directly

## Usage

Use this skill to draft a commit message for staged changes. Execute `Skill(sanctum:git-workspace-review)` first to capture the repository path, status, and diffs. If no changes are staged, stage the relevant files before continuing.

## Required Steps

1. **Validate Code Quality**: Run `make format && make lint`. Fix any reported errors before proceeding. Do not bypass pre-commit hooks with `--no-verify` or `-n`.
2. **Classify the Change**: Choose a type from `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, or `ci`. Select an optional but preferred scope (e.g., `core`, `cli`). Identify breaking changes for the `BREAKING CHANGE:` footer.
3. **Draft the Message**:
    - **Subject**: `<type>(<scope>): <imperative summary>` (≤50 characters).
    - **Body**: Wrap at 72 characters. Explain the "what" and "why" behind the change. Use paragraphs for technical rationale.
    - **Footer**: Include breaking change details or issue references.
4. **Validate Against Slop**: Before finalizing, scan the message for AI-generated content markers:
    - **Tier 1 (BLOCK)**: delve, leverage, seamless, comprehensive, robust, multifaceted, utilize, facilitate, streamline, pivotal, nuanced, intricate
    - **Tier 2 (WARN)**: moreover, furthermore, significantly, fundamentally, notably, revolutionize, elevate, unlock
    - **Phrases (BLOCK)**: "it's worth noting", "at its core", "in essence", "a testament to"
    - If any Tier 1 words or blocked phrases found, replace with plain alternatives before proceeding
5. **Write the Output**: Use a relative path (e.g., `./commit_msg.txt`) to save the message. Overwrite the file with the final message only, without commentary.
6. **Preview**: Display the file contents using `cat` or `sed` for confirmation.

## Guardrails

Do not use `git commit --no-verify` or the `-n` flag. Pre-commit hooks are mandatory; fix issues rather than bypassing them.

### Slop-Free Commit Messages (MANDATORY)

Commit messages must pass slop detection before being accepted. Apply `scribe:slop-detector` vocabulary rules:

**Never use these words** (replace with alternatives):
| Slop Word | Use Instead |
|-----------|-------------|
| leverage | use |
| utilize | use |
| seamless | smooth, easy |
| comprehensive | complete, full |
| robust | solid, reliable |
| facilitate | enable, help |
| streamline | simplify |
| optimize | improve |
| delve | explore, examine |
| multifaceted | varied, complex |
| pivotal | key, important |
| intricate | detailed |

**Avoid these phrases** (delete or rewrite):
- "It's worth noting that..." → just state it
- "At its core..." → delete, start with the point
- "In essence..." → delete
- "A testament to..." → "shows" or "proves"

**Use plain language**: Present-tense imperative for subject lines, technical rationale in body. Write for humans, not to impress. A commit that says "fix auth bug" beats "seamlessly leverage comprehensive authentication optimization."

## Technical Integration

Combine this skill with `Skill(imbue:catchup)` or `/git-catchup` if additional context is needed. If the type or scope is unclear, re-examine the diffs or consult the project plan before finalizing the draft.

## Troubleshooting

Address specific errors reported by pre-commit hooks. Run `make format` to resolve styling issues and `make lint` for logic or style violations. Fix all detected issues before re-attempting the commit. If a merge conflict occurs, use `git merge --abort` to return to a clean state. A rejected commit indicates a failed quality gate; analyze the output and apply fixes before retrying.

## See Also

- `Skill(scribe:slop-detector)` - Full AI slop detection patterns
- `Skill(scribe:doc-generator)` - Slop-free documentation writing
- `/slop-scan` - Direct slop scanning command
