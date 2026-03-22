---
name: create-commit-message
description: Generate a Conventional Commit message from staged git changes when the user asks to write a commit message, create a commit, or format a commit
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[optional: additional context about why this change was made]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: git, vcs, automation
---

# Create Commit Message

## Overview

Generate a precise, Conventional Commits-formatted commit message by analyzing the staged git diff. The message classifies the change type, infers the scope from changed files, writes a clear subject line under 72 characters, and adds a body for complex changes explaining *why* the change was made.

## Workflow

1. **Read project context** -- Check for `.chalk/docs/engineering/` files, especially:
   - Commit message conventions or contributing guides
   - Any custom commit types or scopes used by this project
   - Check for a `commitlint.config.js` or similar configuration that defines allowed types and scopes
   - If custom conventions exist, follow those instead of the defaults below

2. **Get the staged diff** -- Run:
   - `git diff --cached --stat` for a high-level overview of changed files
   - `git diff --cached` for the full diff content
   - `git status` to check for unstaged changes the user may have forgotten to stage
   - If nothing is staged, inform the user and suggest staging commands

3. **Classify the change type** -- Analyze the diff content (not just file names) to determine the primary type:

   | Type | When to Use |
   |------|-------------|
   | `feat` | New functionality visible to users or consumers of the module |
   | `fix` | Corrects a bug -- behavior was wrong, now it is right |
   | `refactor` | Code restructuring with no behavior change |
   | `docs` | Documentation only -- README, JSDoc, comments, guides |
   | `test` | Adding or updating tests with no production code change |
   | `chore` | Maintenance tasks: dependency updates, config changes, tooling |
   | `perf` | Performance improvement with no functional change |
   | `ci` | CI/CD pipeline changes (GitHub Actions, CircleCI, etc.) |
   | `build` | Build system changes (webpack, tsconfig, Dockerfile, etc.) |
   | `style` | Code formatting only -- whitespace, semicolons, no logic change |
   | `revert` | Reverts a previous commit |

   **Decision rules:**
   - If the diff includes both a feature and tests for that feature, the type is `feat` (tests are part of the feature)
   - If the diff includes both a fix and a test that reproduces the bug, the type is `fix`
   - If you are genuinely unsure, ask the user -- do not guess

4. **Infer the scope** -- Determine the scope from the changed files:
   - If all changes are in `src/auth/` or `lib/auth/`, scope is `auth`
   - If all changes are in `components/Button/`, scope is `button`
   - If changes span multiple directories but share a domain, use the domain name
   - If changes are truly cross-cutting, omit the scope
   - Match existing scope conventions -- run `git log --oneline -50` and extract scopes from prior commits
   - Scope should be lowercase, typically one word

5. **Write the subject line** -- Format: `type(scope): description`
   - Total length: 72 characters maximum (including type and scope)
   - Start with a lowercase imperative verb: "add", "fix", "remove", "update", "refactor"
   - Do not end with a period
   - Describe the *what* concisely -- the body explains *why*
   - Be specific: "fix null pointer in user lookup" not "fix bug"

6. **Write the body (if needed)** -- Add a body separated by a blank line when:
   - The change is not obvious from the subject line alone
   - There is important context about *why* this change was made
   - The approach was non-obvious and the reasoning should be documented
   - The body should explain motivation, not repeat the diff
   - Wrap lines at 72 characters

7. **Write the footer (if needed)** -- Add footers for:
   - Breaking changes: `BREAKING CHANGE: <description of what breaks and migration path>`
   - Issue references: `Fixes #123` or `Closes #456` or `Refs #789`
   - Co-authors: `Co-authored-by: Name <email>`

8. **Present the commit message** -- Output the complete commit message in a code block. Also output the git command to create the commit so the user can copy-paste it.

## Commit Message Format

```
type(scope): subject line under 72 chars

Optional body explaining WHY this change was made, not WHAT changed
(the diff shows what changed). Wrap at 72 characters.

Motivation: explain the problem or opportunity.
Approach: explain why this approach was chosen over alternatives.

BREAKING CHANGE: description of what breaks and how to migrate

Fixes #123
```

## Examples

### Simple Feature

```
feat(auth): add password reset via email link
```

### Bug Fix with Context

```
fix(checkout): prevent double-charge on retry after timeout

When a payment request timed out, the retry logic did not check whether
the original charge succeeded. This caused double-charges for ~0.3% of
transactions. Now we query the payment provider for existing charges
before retrying.

Fixes #892
```

### Refactor

```
refactor(api): extract validation middleware from route handlers

Validation logic was duplicated across 12 route handlers with slight
variations. Extracted into a shared middleware that takes a Zod schema,
reducing duplication and ensuring consistent error responses.
```

### Breaking Change

```
feat(api): require API key for all public endpoints

Previously, rate limiting on public endpoints relied on IP-based
throttling, which was easily circumvented. All public endpoints now
require an API key passed via the X-API-Key header.

BREAKING CHANGE: All API requests must include an X-API-Key header.
Existing clients need to register for an API key at /developer/keys
before upgrading.

Refs #1045
```

### Chore

```
chore(deps): upgrade express from 4.18 to 4.19

Includes security patch for CVE-2024-XXXXX (prototype pollution in
query parser). No breaking changes per the changelog.
```

## Subject Line Rules

| Rule | Good | Bad |
|------|------|-----|
| Imperative mood | `add user search` | `added user search` |
| Lowercase start | `fix timeout` | `Fix timeout` |
| No period | `update readme` | `update readme.` |
| Specific | `fix null pointer in user lookup` | `fix bug` |
| Under 72 chars | `feat(auth): add OAuth2 PKCE flow` | `feat(authentication-service): add the OAuth2 PKCE flow for single-page applications` |
| Describes what, not how | `add retry logic for payments` | `add try-catch block around payment call` |

## Type Classification Decision Tree

```
Is there new user-visible functionality?
├── Yes → feat
└── No
    Was behavior incorrect before?
    ├── Yes → fix
    └── No
        Did only tests change?
        ├── Yes → test
        └── No
            Did only docs/comments change?
            ├── Yes → docs
            └── No
                Did behavior change?
                ├── No (same behavior, different structure) → refactor
                └── No (same behavior, faster) → perf
                    Is it CI/CD config?
                    ├── Yes → ci
                    └── Is it build config?
                        ├── Yes → build
                        └── Is it formatting only?
                            ├── Yes → style
                            └── chore
```

## Anti-patterns

- **Meaningless subjects** -- "fix stuff", "WIP", "update", "changes", "misc" communicate nothing. Every commit message must describe a specific change. If you cannot describe it specifically, the commit is doing too many things -- split it.
- **Scope that does not match the changed area** -- `fix(auth): update button color` is wrong. The scope must reflect the area of code that actually changed. If the scope does not match, either the scope is wrong or the files are in the wrong directory.
- **Body that repeats the diff** -- "Changed line 45 from X to Y" is useless as a body. The body explains *why* -- the *what* is in the diff. If the subject line fully explains the change, omit the body entirely.
- **Multiple unrelated changes in one commit** -- If you cannot describe the commit in one subject line, it should be multiple commits. A commit that "add search and fix login and update deps" is three commits.
- **Missing BREAKING CHANGE footer** -- If the change breaks backwards compatibility for any consumer, the `BREAKING CHANGE:` footer is mandatory. Omitting it means consumers get surprised at deploy time.
- **Past tense** -- "fixed", "added", "updated" instead of "fix", "add", "update". Conventional Commits uses the imperative mood because commit messages complete the sentence "This commit will...".
- **Overly broad scope** -- `feat(app): ...` or `fix(src): ...` are not useful scopes. The scope should identify the module, component, or domain -- not the top-level directory.
- **Commit message longer than the change** -- A one-line config change does not need a 10-line body. Scale the message to the complexity of the change.
