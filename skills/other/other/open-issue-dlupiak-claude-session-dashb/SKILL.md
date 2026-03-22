---
name: open-issue
description: Analyze a change request, ask clarifying questions, and create a well-structured GitHub issue with acceptance criteria. Use this skill whenever the user wants to create an issue, write a ticket, log a bug, propose a feature request, or capture requirements — even if they say "let's track this" or "add this to the backlog".
user-invocable: true
argument-hint: "<description>"
---

# Open GitHub Issue

You are creating a GitHub issue for the **Claude Session Dashboard** — a read-only local observability app that scans `~/.claude` to display session data. No database. No auth. Filesystem reads only.

## Step 1: Explore

Before asking anything, read relevant code to understand what exists today:
- Read `CLAUDE.md` for project conventions
- Find the affected feature slice(s) in `apps/web/src/features/` (sessions, session-detail, stats)
- Check `apps/web/src/lib/` for relevant scanner/parser/utils code
- Look at related routes in `apps/web/src/routes/`
- Skim recent commits: `git log --oneline -10`

This groundwork means your clarifying questions will be sharper and the issue will reference real file paths.

## Step 2: Ask Clarifying Questions

Use `AskUserQuestion` to fill gaps. Focus on what's genuinely ambiguous — don't ask about things you can infer from the code or the description. Typical areas:

- **Scope**: What should change? What should stay the same?
- **UX**: How should this look or behave from the user's perspective?
- **Edge cases**: Empty states, missing data, large datasets, parse errors
- **Priority**: Must-have or nice-to-have?

One round is usually enough. Skip questions you can answer from the code.

## Step 3: Draft & Confirm

Draft the issue using this template, then show it to the user for approval before creating:

```
## Summary
<1-2 sentences: what changes and why it matters>

## Context
<Current state — what exists today, why it's insufficient, relevant code locations>

## Affected Areas
<List slices and files, e.g.:
- `apps/web/src/features/sessions/` — session list UI
- `apps/web/src/lib/scanner/` — file scanner
- `apps/web/src/routes/_dashboard/` — route>

## Requirements
1. <Specific, testable requirement>
2. ...

## Acceptance Criteria
- [ ] <Binary pass/fail condition>
- [ ] <Another condition>
- [ ] Quality gates pass (typecheck, lint, test, build)

## Out of Scope
<What this explicitly does NOT cover>

## Technical Notes
<Implementation hints — relevant patterns, file paths, gotchas.
Remember: no database, no auth, no external APIs. Data comes from ~/.claude filesystem reads via createServerFn → React Query → UI.>
```

Ask: "Does this look right? Any changes before I create it?"

## Step 4: Create

Once approved:
```bash
gh issue create --title "<title>" --body "<body>"
```

Report the issue URL and number.

## Tips for good issues

- Acceptance criteria should be things you can check off with a yes/no — avoid "should feel fast" or "looks good"
- Reference actual file paths from your Step 1 exploration — it saves the implementer time
- If it's a bug, include reproduction steps
- Keep "Out of Scope" honest — it prevents scope creep later
