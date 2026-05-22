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
---

# Conventional Commit Workflow

## When to Use
Use this skill to write a commit message for staged changes.
As a prerequisite, run `Skill(sanctum:git-workspace-review)` so the repository path, status, and diffs are already captured. If that skill reveals no staged changes, stage the desired files before continuing.

## Required Steps
1. **Validate code quality (REQUIRED BEFORE DRAFTING)**
   - Run linting and formatting checks: `make format && make lint`
   - If errors are found, FIX THEM before proceeding
   - **NEVER use `git commit --no-verify` or `-n`** - pre-commit hooks exist to maintain quality
   - If hooks fail, the code is not ready to commit
2. **Classify the change**
   - Choose the correct type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, or `ci`.
   - Select a concise scope (directory/module or `core`, `cli`, etc.). The scope is optional but preferred.
   - Decide if the change is breaking. If so, plan a `BREAKING CHANGE:` footer.
3. **Draft the message**
   - Subject: `<type>(<scope>): <imperative summary>` (scope optional, ≤50 characters).
   - Body: Wrap at 72 characters per line, explain the "what" and "why", and list key bullets if useful.
   - Footer: Add `BREAKING CHANGE: …` or issue references if needed.
4. **Write the output**
   - The prompt passes a destination path (e.g., `{0|./commit_msg.txt}`) - always use a relative path in cwd, never an absolute path.
   - Overwrite the file with only the final commit message—no commentary.
5. **Preview**
   - Display the file path and contents (`cat <file>` or `sed -n '1,120p' <file>`) for confirmation.

## Guardrails

We maintain strict quality gates by forbidding the use of `git commit --no-verify` or the `-n` flag. Pre-commit hooks are enforced to maintain code quality, and any reported issues must be fixed rather than bypassed. Commit messages should not include AI attribution lines or filler phrases such as "leverage" or "seamless," which are common markers of AI-generated text. Messages must remain plain text without emojis and be written in a human voice, using present-tense imperative style for the subject line. For non-trivial changes involving multiple files or complex logic, a multi-line body is required to explain the technical rationale.

## Integration Notes
- Combine with `Skill(imbue:catchup)` or `/git-catchup` when you need additional context before drafting.
- If unsure about the type or scope, rerun the diff commands or consult the specification or plan before finalizing.

## Troubleshooting

### Common Issues

If pre-commit hooks fail, you must address the specific errors identified by the hooks instead of using bypass flags. For linting errors, use `make format` to resolve formatting issues and `make lint` to identify logic or style violations. All detected issues should be fixed before you attempt to commit again. In the event of a merge conflict, use `git merge --abort` to return to a clean state and then resolve the conflicts manually. A rejected commit typically provides output from a failed quality gate; analyze this output and apply the necessary fixes before retrying.
