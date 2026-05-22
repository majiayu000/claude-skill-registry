---
name: create-bug-report
description: Create a structured bug report when the user reports a bug, wants to file an issue, document a defect, or needs help writing a bug report with proper reproduction steps
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash, Write
argument-hint: "[bug description or observed behavior]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: bugs, reporting, triage
---

# Create Bug Report

## Overview

Create a comprehensive, actionable bug report with all the information needed for a developer to reproduce, understand, and fix the issue. Every bug report must include reproduction steps, environment details, and a clear distinction between expected and actual behavior.

## Workflow

1. **Read project context** — Check `.chalk/docs/` for:
   - Architecture docs (to identify the affected component)
   - Previous bug reports (to match format and conventions)
   - Any known issues or recent changes that might be related
   - Version information from `package.json`, `pyproject.toml`, etc.

2. **Gather bug details** — From `$ARGUMENTS` and conversation context, extract:
   - What the user observed (the actual behavior)
   - What the user expected to happen
   - When the bug was first noticed
   - How consistently the bug occurs (always, sometimes, once)
   - Any error messages, logs, or stack traces
   - If details are missing, ask the user targeted questions (see Required Information below)

3. **Determine environment** — Identify or ask for:
   - Application version or commit hash
   - Operating system and version
   - Browser and version (for web apps)
   - Device type (for mobile apps)
   - Relevant configuration (feature flags, user role, locale)
   - Environment (production, staging, local)

4. **Write reproduction steps** — Convert the user's description into numbered, specific steps:
   - Start from a known state (e.g., "logged in as a standard user")
   - Each step is a single, observable action
   - Include specific data used (e.g., "enter 'test@example.com' in the email field" not "enter an email")
   - Note the exact point where the bug manifests
   - If the bug is intermittent, note the approximate reproduction rate

5. **Assign severity** — Using the severity matrix:
   - **Critical**: Data loss, security vulnerability, complete feature outage, no workaround
   - **High**: Major feature broken, significant impact, difficult workaround
   - **Medium**: Feature degraded, workaround exists, moderate impact
   - **Low**: Cosmetic issue, minor inconvenience, easy workaround

6. **Identify bisect hint** — If possible, determine:
   - When did this last work correctly? (version, date, or commit)
   - What changed between "working" and "broken"? (deployment, config change, data migration)
   - This narrows the investigation scope dramatically

7. **Check for related issues** — Search `.chalk/docs/engineering/` for:
   - Similar bug reports (to avoid duplicates)
   - Related bugs that might share a root cause
   - Relevant architecture or design decisions that provide context

8. **Determine the next file number** — List files in `.chalk/docs/engineering/` matching `*_bug_*`. Find the highest number and increment by 1.

9. **Write the bug report** — Save to `.chalk/docs/engineering/<n>_bug_<slug>.md` or format for GitHub issue as requested.

10. **Confirm** — Present the bug report to the user. Highlight any missing information that would improve the report.

## Filename Convention

```
<number>_bug_<snake_case_slug>.md
```

Examples:
- `6_bug_login_timeout_on_slow_connections.md`
- `13_bug_duplicate_orders_on_retry.md`

## Bug Report Format

```markdown
# Bug: <Descriptive Title>

**Reported**: <YYYY-MM-DD>
**Severity**: Critical | High | Medium | Low
**Status**: Open
**Component**: <affected component or module>
**Reporter**: <name or identifier>

## Environment

| Field | Value |
|-------|-------|
| App Version | <version or commit hash> |
| OS | <OS name and version> |
| Browser | <browser and version, if applicable> |
| Device | <device type, if applicable> |
| Environment | Production / Staging / Local |
| User Role | <role or permissions level> |
| Feature Flags | <any relevant flags enabled/disabled> |

## Summary

<1-2 sentence description of the bug. What is broken and what is the user impact.>

## Steps to Reproduce

**Preconditions**: <Starting state, e.g., "Logged in as a user with admin role, on the dashboard page">

1. <Specific action with specific data>
2. <Next specific action>
3. <Action where the bug manifests>

**Reproduction rate**: Always | ~X% of attempts | Intermittent (seen X times out of Y attempts)

## Expected Behavior

<What should happen when following the steps above.>

## Actual Behavior

<What actually happens. Be specific: include error messages, incorrect values, visual glitches.>

## Error Output

<Stack trace, console errors, server logs, or error messages. Use code blocks.>

```
<paste error output here>
```

## Screenshots / Recordings

<Describe what the screenshot or recording would show. Reference attached files if available.>

## Bisect Hint

| Field | Value |
|-------|-------|
| Last Known Working | <version, date, or "unknown"> |
| First Known Broken | <version, date, or "current"> |
| Suspected Cause | <recent deployment, config change, data migration, or "unknown"> |

## Impact Assessment

| Dimension | Assessment |
|-----------|-----------|
| Users Affected | All / Most / Some / Few |
| Frequency | Every time / Often / Sometimes / Rarely |
| Workaround | None / <describe workaround> |
| Data Impact | Data loss / Data corruption / No data impact |
| Revenue Impact | <if applicable> |

## Related Issues

- <Link or reference to related bugs, PRs, or architecture decisions>

## Additional Context

<Any other information that might help: recent changes, similar bugs in the past, relevant configuration, user reports.>
```

## Required Information Checklist

Before submitting, ensure these fields are populated:

| Field | Required | Why |
|-------|----------|-----|
| Descriptive title | Yes | "Login broken" is not actionable; "Login fails with 500 error when password contains special characters" is |
| Environment details | Yes | Bugs are often environment-specific. Without this, developers waste time on "works for me" |
| Steps to reproduce | Yes | The single most important section. Without this, developers cannot verify the fix |
| Expected behavior | Yes | Clarifies whether the bug is a misunderstanding or a real defect |
| Actual behavior | Yes | Must be specific: error messages, incorrect values, not just "it does not work" |
| Severity | Yes | Drives prioritization. Use the matrix, not gut feeling |
| Error output | If available | Stack traces and error messages cut investigation time dramatically |
| Bisect hint | If known | Narrows investigation from "the entire codebase" to "changes in the last week" |

If any required field is missing, ask the user for it before finalizing the report.

## Title Guidelines

A good bug title answers: **What is broken** and **under what condition**.

| Bad Title | Good Title |
|-----------|------------|
| Login broken | Login returns 500 when password contains special characters |
| Slow page | Dashboard takes 30s to load with 1000+ items |
| Error on save | Document save fails silently when title exceeds 255 characters |
| UI issue | Dropdown menu overlaps submit button on mobile viewport |
| It does not work | CSV export produces empty file when date range exceeds 90 days |

## Anti-patterns

- **"It does not work"** — A bug report without specific symptoms is not actionable. What exactly does not work? What error appears? What data is affected? Vague descriptions lead to back-and-forth that delays fixes.
- **No reproduction steps** — "I clicked around and it broke" forces the developer to guess. Numbered, specific steps from a known starting state are mandatory. If the bug cannot be reproduced, say so explicitly and describe the circumstances where it was observed.
- **Wrong severity** — A misaligned button is not Critical. A data loss bug is not Low. Use the severity matrix consistently. Mis-categorized severity causes either panic over minor issues or delayed response to real emergencies.
- **No environment information** — "It broke on my machine" without OS, browser, version, and configuration details wastes debugging time. Environment-specific bugs are common, and developers need this information to reproduce them.
- **Mixing multiple bugs in one report** — Each bug report should describe exactly one defect. If two things are broken, file two reports. Combined reports are hard to track, hard to assign, and hard to mark as resolved.
- **Blaming instead of describing** — "The backend team broke login" is not a bug report. Describe the observable behavior without assigning blame. Root cause analysis happens during investigation, not during filing.
- **No bisect hint when one is available** — If the user knows it worked last week and broke after Tuesday's deploy, that information is gold. Always ask "when did this last work?" — it can narrow investigation from days to hours.
- **Screenshots without context** — A screenshot of an error message is helpful. A screenshot without explanation of what the user was doing or what they expected is not. Always pair visual evidence with textual description.
