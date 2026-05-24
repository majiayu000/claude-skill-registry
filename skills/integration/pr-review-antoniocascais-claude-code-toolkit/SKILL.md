---
name: pr-review
description: Reviews code changes before merging. Use when reviewing PRs, checking staged changes, reviewing diffs, code review, merge readiness check, or validating changes before commit/push.
allowed-tools: Read Glob Grep Bash(git diff:*) Bash(git status:*) Bash(git log:*) Bash(git show:*) Bash(git branch:*) Bash(gitleaks:*) Bash(trufflehog:*) Bash(trivy:*) Bash(shellcheck:*) Bash(npm audit:*) Bash(yarn audit:*) Bash(pip-audit:*) Bash(safety:*) Bash(tfsec:*) Bash(checkov:*) Bash(hadolint:*) AskUserQuestion
---

# PR Review Skill

Reviews code changes with focus on quality, security, and consistency.

## Default Assumption: Public Repository

Unless explicitly stated otherwise, assume the repository is **publicly available**. This means:
- Any secret, credential, or API key pushed is considered compromised
- Internal URLs, IPs, hostnames should not be exposed
- Comments with sensitive internal context should be flagged
- Error messages should not leak internal architecture
- Be extra cautious with .env files, config files, CI/CD configs

## Phase 1: Determine Scope

**STOP. Use AskUserQuestion before anything else.**

Ask user to choose review scope:
- Staged files only
- Unstaged changes (working directory)
- All uncommitted (staged + unstaged)
- Current branch vs main (PR-style)
- Specific commit or range
- Other (specify)

**Do NOT run any git commands or tools until user responds.**

After selection, get the diff:
- Staged: `git diff --cached`
- Unstaged: `git diff`
- All uncommitted: `git diff HEAD`
- Branch vs main: `git diff main...HEAD`
- Commit: `git show <hash>`
- Range: `git diff <from>..<to>`

Also get changed files list: `git diff --name-only <appropriate args>`

## Phase 2: Understand the Problem

**STOP. Use AskUserQuestion to confirm before proceeding.**

Infer intent from:
1. Branch name: `git branch --show-current`
2. Commit messages: `git log main..HEAD --oneline` (or relevant range)

Then use AskUserQuestion to confirm:
> "Based on branch `feature/xyz` and commits, this PR appears to [inferred description]. Is this correct?"
> - Yes, proceed
> - No, let me explain

**Do NOT proceed until user confirms.**

## Phase 3: Auto-Detect Stack

Check for presence of:
- `package.json` / `yarn.lock` → Node.js
- `requirements.txt` / `pyproject.toml` → Python
- `go.mod` → Go
- `Cargo.toml` → Rust
- `Dockerfile` → Docker
- `*.tf` → Terraform
- `*.yaml` in k8s patterns → Kubernetes
- `.github/workflows/` → GitHub Actions

Note detected stack for context-aware analysis.

## Phase 4: Run Scanners

Execute relevant scanners (skip silently if not installed):

**Always run:**
| Tool | Command |
|------|---------|
| gitleaks | `gitleaks detect --source . --verbose --no-git` |
| trufflehog | `trufflehog filesystem . --only-verified` |

**Stack-specific:**
| Stack | Tool | Command |
|-------|------|---------|
| Node.js | npm audit | `npm audit --json` |
| Node.js | yarn audit | `yarn audit --json` |
| Python | pip-audit | `pip-audit` |
| Python | safety | `safety check` |
| Docker | trivy | `trivy fs .` |
| Docker | hadolint | `hadolint Dockerfile` |
| Terraform | tfsec | `tfsec .` |
| Terraform | checkov | `checkov -d .` |
| Terraform | trivy | `trivy config .` |
| K8s | trivy | `trivy config .` |
| Shell scripts | shellcheck | `shellcheck <file>` |

## Phase 5: Code Review

Analyze the diff for all categories. Be pragmatic—flag likely issues, skip obvious false positives.

### 5.1 Code Quality
- Best practices for detected stack
- Readability and maintainability
- Error handling appropriateness
- Test coverage (if tests exist)
- Idiomatic patterns
- Type safety issues

### 5.2 Codebase Consistency
- Match existing patterns in the repo
- Naming conventions alignment
- File organization consistency
- Don't introduce a 10th way of doing something

### 5.3 Security

**Manual checks:**
- Hardcoded secrets, API keys, passwords, connection strings
- SQL injection, XSS, command injection vectors
- Path traversal risks
- Auth/authz bypasses
- Insecure defaults (http vs https, weak crypto)
- Sensitive data in logs/errors/URLs
- Container: running as root, privileged mode, unverified base images

### 5.4 Bug Detection
- Logic errors, off-by-one
- Null/undefined handling
- Race conditions
- Resource leaks (unclosed handles, connections)
- Breaking changes to existing APIs

### 5.5 Dependencies
- Known vulnerable package versions
- Outdated dependencies with security patches
- Unpinned versions
- Suspicious or typosquatted package names

### 5.6 Performance
- N+1 query patterns
- Sync operations in async contexts
- Unbounded loops/recursion
- Memory leaks
- Missing pagination
- Blocking I/O in hot paths

### 5.7 Deprecations & Drift
- Deprecated APIs, functions, patterns
- Breaking changes in dependencies
- Hardcoded values that should be variables
- Environment-specific configs in shared code
- Configuration diverging from IaC patterns

## Phase 6: Report

Output a succinct markdown report:

```markdown
## PR Review: [brief title]

**Problem:** [1-2 sentences on what this PR solves]

**Scope:** [staged/branch/commits reviewed]

**Stack:** [detected tech stack]

### Scanner Results
| Tool | Result |
|------|--------|
| gitleaks | [clean/N findings] |
| ... | ... |

### Findings

#### CRITICAL
- `file:line` - [issue with brief context]

#### HIGH
- `file:line` - [issue]

#### MEDIUM
- `file:line` - [issue]

#### LOW
- `file:line` - [issue]

### Summary
- Critical: X | High: X | Medium: X | Low: X

### Review Score: X/20
[One sentence justification]

### Action Required
| Priority | Item |
|----------|------|
| blocker | ... |
| should fix | ... |
| consider | ... |
```

## Rating Scale

| Score | Meaning | Action |
|-------|---------|--------|
| 0-10 | Blocker issues | Reject, needs significant rework |
| 11-15 | Acceptable | Merge after addressing fixes |
| 16-17 | Good | Ready to merge, suggestions optional |
| 18-20 | Excellent | Merge immediately |

## Style Guidelines

Keep findings concise but contextual:
- Bad: "should use https here"
- Good: "http exposes data in transit, use https"

- Bad: "fix this null check"
- Good: "`user.email` accessed without null check - crashes if user not found"

Don't write a 50-page report. Focus on what matters.
