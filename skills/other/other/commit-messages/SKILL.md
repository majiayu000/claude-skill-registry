---
name: commit-messages
description: 'Generate conventional commit messages from staged changes with correct
  type/scope. Use when generating commit messages in conventional commits format.
  DO NOT use when: full PR preparation - use pr-prep instead.'
version: 1.9.0
alwaysApply: false
category: artifact-generation
tags:
- git
- commit
- conventional-commits
tools:
- Bash
- Write
complexity: low
model_hint: fast
estimated_tokens: 350
---

# Conventional Commit Workflow

## When To Use

- Generating conventional commit messages from staged changes

## When NOT To Use

- Full PR preparation: use sanctum:pr-prep
- Amending existing commits: use git directly

## Steps

1. **Gather context** (run in parallel):
   - `git status -sb`
   - `git diff --cached --stat`
   - `git diff --cached`
   - `git log --oneline -5`
   - When sem is available (see `leyline:sem-integration`):
     `sem diff --staged --json` for entity-level changes

   If nothing is staged, tell the user and stop.

   When sem output is available, use entity names
   (function, class, method) in the commit subject and
   body instead of parsing raw diff hunks. For example,
   "add function validate_webhook_url" instead of
   "add validation logic to notify.py".

2. **Classify**: Pick type (`feat`, `fix`, `docs`, `refactor`,
   `test`, `chore`, `style`, `perf`, `ci`) and optional scope.

3. **Draft the message**:
   - **Subject**: `<type>(<scope>): <imperative summary>` (50 chars max)
   - **Body**: What and why, wrapped at 72 chars
   - **Footer**: BREAKING CHANGE or issue refs

4. **Slop check**: reject these words and replace with plain
   alternatives:

   | Reject | Use instead |
   |--------|-------------|
   | leverage, utilize | use |
   | seamless | smooth |
   | comprehensive | complete |
   | robust | solid |
   | facilitate | enable |
   | streamline | simplify |
   | optimize | improve |
   | delve | explore |
   | multifaceted | varied |
   | pivotal | key |
   | intricate | detailed |

   Also reject: "it's worth noting", "at its core",
   "in essence", "a testament to"

5. **Write** to `./commit_msg.txt` and preview.

## Rules

- NEVER use `git commit --no-verify` or `-n`
- Write for humans, not to impress
- If pre-commit hooks fail, fix the issues
