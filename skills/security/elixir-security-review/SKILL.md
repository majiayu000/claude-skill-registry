---
name: elixir-security-review
description: Reviews Elixir code for security vulnerabilities including code injection, atom exhaustion, and secret handling. Use when reviewing code handling user input, external data, or sensitive configuration.
---

# Elixir Security Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Code.eval_string, binary_to_term | [references/code-injection.md](references/code-injection.md) |
| String.to_atom dangers | [references/atom-exhaustion.md](references/atom-exhaustion.md) |
| Config, environment variables | [references/secrets.md](references/secrets.md) |
| ETS visibility, process dictionary | [references/process-exposure.md](references/process-exposure.md) |

## Review Checklist

### Critical (Block Merge)
- [ ] No `Code.eval_string/1` on user input
- [ ] No `:erlang.binary_to_term/1` without `:safe` on untrusted data
- [ ] No `String.to_atom/1` on external input
- [ ] No hardcoded secrets in source code

### Major
- [ ] ETS tables use appropriate access controls
- [ ] No sensitive data in process dictionary
- [ ] No dynamic module creation from user input
- [ ] Path traversal prevented in file operations

### Configuration
- [ ] Secrets loaded from environment
- [ ] No secrets in config/*.exs committed to git
- [ ] Runtime config used for deployment secrets

## Valid Patterns (Do NOT Flag)

- **String.to_atom on compile-time constants** - Atoms created at compile time are safe
- **Code.eval_string in dev/test** - May be needed for tooling
- **ETS :public tables** - Valid when intentionally shared
- **binary_to_term with :safe** - Explicitly safe option used

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| String.to_atom | Input comes from external source (user, API, file) |
| binary_to_term | Data comes from untrusted source |
| ETS :public | Contains sensitive data |

## Hard gates (before reporting)

Complete **in order** for each finding you intend to report. Do not advance until the pass condition is satisfied.

1. **Location artifact** — The finding includes `[FILE:LINE]` (or a line range) that you copied from the current file contents; the path resolves in this repo.
2. **Scope read** — You read the full surrounding function or module section that contains the flagged code, not only a diff hunk or summary.
3. **External-data claim** (only if the finding depends on “user/untrusted input”) — You can name one concrete ingress (for example `conn.params`, `Jason.decode!/1` result, uploaded file path, message from another node) **or** you drop the finding because the value is compile-time, test-only, or internal per Context-Sensitive Rules.
4. **Protocol** — Pre-report steps in `beagle-elixir:review-verification-protocol` ([skill](../review-verification-protocol/SKILL.md)) are satisfied for this item (no finding if they are not).

## Before Submitting Findings

Use the issue format: `[FILE:LINE] ISSUE_TITLE` for each finding.

Hard gate 4 requires `beagle-elixir:review-verification-protocol` ([skill](../review-verification-protocol/SKILL.md)); use it as the full pre-report checklist and issue-type verification (it extends beyond this skill’s summary).
