---
name: project-orchestrator:changelog
description: Use when completing changes to any service - ensures standardized changelog entries with correct format, location, and content.
user-invocable: false
---

# Changelog

## Overview

Write standardized changelog entries after completing changes. Focus on WHY not WHAT.

## Config Loading

1. Check if `.project-orchestrator/project.yml` exists
2. If yes: use `config.services[name].changelog` for the correct file path
3. If no: look for `CHANGELOG.md` in the service directory or project root

## When to Trigger

After completing:
- Bug fixes
- New features
- Refactors affecting behavior
- API changes
- Configuration changes

**Skip for:** typo fixes, comment-only changes, test-only changes

## Format

```markdown
### YYYY-MM-DD - Brief Title

**Summary:** One-line description.

**What prompted the change:**
- Motivation or problem

**Problem solved:**
- What this enables
```

## Location

Write to the affected service's changelog path from `config.services[name].changelog`.

If no changelog path is configured:
- Check if `{service_path}/CHANGELOG.md` exists
- If not, check if `CHANGELOG.md` exists at project root
- If neither exists, ask the user where to write the entry

**Multiple services?** Write entry to EACH affected service's changelog.

## Checklist

- [ ] Date format: YYYY-MM-DD (not "Jan 17")
- [ ] Title: Brief, describes outcome (not implementation)
- [ ] Summary: One line, WHY not WHAT
- [ ] Prompted: What problem existed
- [ ] Solved: What's now possible
- [ ] 10-20 lines max
- [ ] Written to correct service changelog

## Red Flags

| Bad | Good |
|-----|------|
| "Updated code" | "Fix bookmark sync failing silently" |
| "Fixed bug" | "Prevent duplicate records on import" |
| Lists files changed | Explains behavior change |
| 50+ lines | 10-20 lines |
| Entry in root README | Entry in service CHANGELOG.md |

## Example

```markdown
### 2026-01-17 - Fix SSE reconnection dropping notifications

**Summary:** SSE connections now preserve undelivered notifications during reconnect.

**What prompted the change:**
- Users reported missing notifications after connection drops

**Problem solved:**
- Notifications queue during disconnect and deliver on reconnect
```
