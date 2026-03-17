---
name: audit
description: Parallel quality audit with 7 specialized agents (Opus) including deploy readiness. Use when assessing app quality or before major releases.
triggers:
  - audit
allowed-tools: Bash, Read, Grep, Glob, Task, TaskCreate, TaskUpdate, TaskList, Write, Edit
model: opus
user-invocable: true
argument-hint: "[scope: full|auth|dashboard|latest]"
---

# Audit

**Before running:** Check if the user ran `/compact` recently in this session (look for "Compacted" output in recent messages). If they did, launch immediately — no need to suggest it again. If they did NOT compact recently, tell the user: "Audit spawns 7 parallel agents — this is token-heavy. Type `/compact` first to free context, then say `audit` again. Or say `go` to launch now." Wait for the user to respond. Do NOT try to invoke `/compact` yourself — it is a built-in CLI command only the user can type.

**Philosophy:** Rate each aspect of the app (or specific feature), then auto-create stories from findings.

## Existing Tasks
!`node -e "try{const p=require('./prd.json');const sp=p.sprints?p.sprints[p.sprints.length-1]:p;Object.entries(sp.stories||p.stories||{}).forEach(([k,v])=>console.log(k,v.passes===true?'done':v.passes==='deferred'?'deferred':'pending',v.title))}catch(e){}"`

## Swarm Architecture

```
User says "audit"
    │
    ├─► Agent 1: Security Audit (Opus) - secrets, XSS, CORS, injection
    ├─► Agent 2: Performance Audit (Opus) - memo, effects, re-renders
    ├─► Agent 3: Accessibility Audit (Opus) - WCAG, keyboard, contrast
    ├─► Agent 4: Type Safety Audit (Opus) - any, ts-ignore, conflicts
    ├─► Agent 5: UX/UI Audit (Opus) - states, tokens, feedback
    ├─► Agent 6: Test Coverage Audit (Opus) - critical paths, gaps
    └─► Agent 7: Deploy Readiness Audit (Opus) - PWA, env vars, runtime

    [All run in parallel via Task tool with run_in_background: true]

    ▼
Wait for completion → Aggregate Results → Present Report
```

## Execution

Launch all 7 agents in a single message:

```typescript
Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Security audit for [PROJECT_PATH]. Scan: exposed secrets (check src/ AND supabase/migrations/ for hardcoded keys, passwords, service_role, cron secrets), dangerouslySetInnerHTML, eval(), missing Zod validation, SQL injection, XSS vectors, CORS config. ALSO check Supabase RLS policy quality: tables with PII (emails, tokens) that allow SELECT without auth.uid() restriction, OAuth tokens accessible via public policies, profiles without row-level restriction. Report: Severity, File:line, Issue, Fix." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Performance audit for [PROJECT_PATH]. Scan: missing React.memo on list items, useEffect without cleanup, inline objects in JSX, missing lazy loading, N+1 queries. Report: Severity, File:line, Issue, Fix." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Accessibility audit for [PROJECT_PATH]. Scan: images without alt, missing aria-labels, onClick without onKeyDown, missing form labels, hardcoded colors, undersized touch targets (<44px), div/span with onClick (should be button), outline-none without focus-visible replacement, user-scalable=no or maximum-scale=1, missing autocomplete on form inputs, inputs without correct type/inputmode, onPaste with preventDefault, missing prefers-reduced-motion support, transition: all (should list properties), autoFocus without justification. Report: Severity, File:line, Issue, Fix." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Type safety audit for [PROJECT_PATH]. Scan: 'any' usage (skip test files), @ts-ignore, type assertions without guards, conflicting type definitions, untyped API responses. Report: Severity, File:line, Issue, Fix." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "UX/UI audit for [PROJECT_PATH]. Scan: missing loading states, missing empty states, missing error states, hardcoded colors instead of tokens, missing toast feedback, images without width/height (causes CLS), missing loading=lazy on below-fold images, large lists without virtualization (50+ items .map). ALSO check responsive layout: sidebars without mobile hide/toggle (must use hidden md:block pattern), grids without mobile breakpoints (need grid-cols-1 md:grid-cols-2), fixed-width containers that overflow on mobile, touch targets under 44px, missing mobile navigation (hamburger/drawer), modals not full-screen on mobile. ALSO check: hardcoded date/number formats (should use Intl.*), missing text truncation on user-generated content, flex children without min-w-0. Report: Severity, File:line, Issue, Fix." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Test coverage audit for [PROJECT_PATH]. Scan: auth flows without tests, data mutations without tests, hooks without test files, utilities without tests. List critical gaps. Report: Severity, What needs testing, Priority." })

Task({ subagent_type: "Explore", model: "opus", run_in_background: true,
  prompt: "Deploy readiness audit for [PROJECT_PATH]. Scan for runtime issues that unit tests miss: 1) PWA manifest (manifest.json/site.webmanifest) - check every icon/screenshot path references a file that actually exists in public/. 2) Environment variables - check all process.env/import.meta.env references have values set (no trailing newlines/whitespace). 3) Supabase config - check anon key for trailing newline characters that break WebSocket URLs. 4) Asset references - grep for paths like /icons/, /images/, /screenshots/ in source and verify the files exist in public/. 5) next.config/vercel.json - check for mismatched rewrites or missing headers. Report: Severity, File:line, Issue, Fix." })
```

## Output Format

```markdown
## Audit Report

**Scan Time:** ~3 min | **Agents:** 7 parallel | **Files Scanned:** ~250

### Summary

| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | X | X | X | X | XX |
| Performance | X | X | X | X | XX |
| Accessibility | X | X | X | X | XX |
| Type Safety | X | X | X | X | XX |
| UX/UI | X | X | X | X | XX |
| Test Coverage | X | X | X | X | XX |
| Deploy Ready | X | X | X | X | XX |
| **TOTAL** | **X** | **X** | **X** | **X** | **XX** |

### Critical Issues (Fix Immediately)

| # | Category | File:Line | Issue | Fix |
|---|----------|-----------|-------|-----|
| 1 | Security | src/api/auth.ts:45 | Exposed API key | Move to env var |
| 2 | A11y | src/components/Button.tsx:12 | No keyboard handler | Add onKeyDown |

### High Priority (Top 10)

1. [Category] File:line - Issue
2. ...

### Ratings

| Category | Score | Notes |
|----------|-------|-------|
| Security | 5/10 | 2 critical vulnerabilities |
| Performance | 7/10 | Missing memoization |
| Accessibility | 6/10 | Keyboard nav gaps |
| Type Safety | 7/10 | 12 'any' types |
| UX/UI | 6/10 | Missing loading states |
| Test Coverage | 2/10 | 95% hooks untested |
| **Overall** | **5.5/10** | |
```

## Severity Definitions

| Severity | Definition | Example |
|----------|------------|---------|
| **Critical** | Security vulnerability or app-breaking | XSS, auth bypass, crash |
| **High** | Significant UX degradation or major debt | 5s load, no error handling |
| **Medium** | Noticeable but not blocking | Missing loading state |
| **Low** | Nice to have, polish | console.log left in |

## Persist Findings to prd.json

After aggregating results, write ALL findings to prd.json so they persist across sessions.

### Step 1: Read current prd.json

```bash
# Get current sprint number and existing story IDs
node -e "try{const p=require('./prd.json');const sp=p.sprints?p.sprints[p.sprints.length-1]:p;console.log('sprint:',sp.id||sp.name||p.sprint||'unknown','stories:',Object.keys(sp.stories||p.stories||{}).length)}catch{console.log('no prd.json')}"
```

If no prd.json exists, create one with `sprint: 1`.

### Step 2: Deduplicate against existing stories

Before adding, check if a similar story already exists:

```javascript
// Match by title similarity (first 25 chars) or same file:line
const isDuplicate = (title, file) => Object.values(stories).some(s =>
  s.title.toLowerCase().includes(title.toLowerCase().slice(0, 25)) ||
  (file && s.notes?.includes(file))
);
```

### Step 3: Add new stories to prd.json

Use ID format: `S{sprint}-AUD-{number}` (e.g., `S3-AUD-001`)

```json
{
  "S3-AUD-001": {
    "id": "S3-AUD-001",
    "title": "Fix XSS vulnerability in user input",
    "priority": 0,
    "passes": null,
    "type": "fix",
    "category": "security",
    "notes": "src/api/auth.ts:45 - dangerouslySetInnerHTML with user data",
    "resolution": ""
  }
}
```

**Category → type mapping:**

| Audit Category | prd.json type | Critical | High | Medium | Low |
|---------------|---------------|----------|------|--------|-----|
| Security | fix | 0 | 1 | 2 | 3 |
| Performance | perf | 0 | 1 | 2 | 3 |
| Accessibility | fix | 0 | 1 | 2 | 3 |
| Type Safety | fix | 0 | 1 | 2 | 3 |
| UX/UI | fix | 0 | 1 | 2 | 3 |
| Test Coverage | qa | 0 | 1 | 2 | 3 |
| Deploy Readiness | fix | 0 | 1 | 2 | 3 |

### Step 4: Also create session Tasks

Create native TaskCreate entries for the current session so "auto" can immediately start fixing:

```typescript
TaskCreate({
  subject: "Fix XSS vulnerability in user input",
  description: "src/api/auth.ts:45 - dangerouslySetInnerHTML with user data",
  metadata: { type: "security", priority: 0, prdId: "S3-AUD-001" }
});
```

### Step 5: Report

```
Created [X] stories in prd.json from audit findings.
- [N] Critical (priority 0)
- [N] High (priority 1)
- [N] Medium (priority 2)
- [N] Low (priority 3)
- [N] skipped (duplicates of existing stories)

Say "auto" to start fixing (works Critical→Low), or "audit [feature]" to audit specific area.
```

## Focused Audit

User can audit specific features:
- `audit auth` → Only scan auth-related files
- `audit dashboard` → Only scan dashboard components
- `audit latest` → Audit files changed in last 3 commits

## Quick Validation (No Agents)

For consistency checks only (triggers, descriptions, versions, frontmatter), run:
```bash
node validate.js
```
This is instant and free — use it before committing. The full agent audit is for deep analysis (security, UX, performance) that static checks can't find.

## Token Cost

- 7 parallel Opus agents. Token cost varies by codebase size.
- Time: 2-4 minutes (parallel execution)
- Context efficient: agents run in background, results aggregated

## Real Results (From Production Test)

Last audit of Data Globe (247 files):

| Category | Critical | High | Total |
|----------|----------|------|-------|
| Security | 2 | 5 | 14 |
| Performance | 0 | 4 | 8 |
| Accessibility | 2 | 5 | 7 |
| Type Safety | 1 | 2 | 8 |
| UX/UI | 3 | 4 | 10 |
| Test Coverage | 23 | 15 | 38 |
| **Overall Score** | **5.5/10** | - | **85 issues** |

Key findings:
- Test coverage is the biggest gap (95% hooks untested)
- 68 components use hardcoded colors
- Edge Functions lack input validation
- 530 console statements in production

## Quality Framework Reference

When rating findings, apply principles from related skills:

| Skill | What to Reference |
|-------|-------------------|
| `standards` | Type safety, design tokens, all UI states, React patterns, error handling |
| `design` | Color tokens vs hardcoded, typography consistency, structural integrity for UI changes |

**UX/UI Agent should check:**
- Hardcoded colors → Reference `design` (avoid purple gradients, avoid Inter/Roboto)
- Missing states → Reference `standards` (loading, empty, error)
- Design tokens → Reference `standards` design system rules

**Type Safety Agent should check:**
- Against `standards` patterns (single source of truth, complete Records, strict mode, no any)

## Log Patterns to Mistakes

When audit finds repeated issues (3+ files):
```markdown
## Pattern: [Category]
- **Task:** Audit finding
- **Root cause:** Why pattern violated
- **Prevention:** Rule to add
```
Log to `.claude/mistakes.md` for future reference.

## Plan Mode for Critical Fixes

When audit finds 5+ Critical/High severity issues, suggest plan mode:

**Suggestion format:**
```
⚠️ Found [N] Critical/High issues across [M] files.

These fixes may have cascading effects. Would you like me to enter plan mode to:
1. Analyze dependencies between fixes
2. Design fix order to prevent regressions
3. Identify shared root causes

Say "plan" to design fix strategy, or "auto" to fix immediately.
```

**In plan mode:**
1. Group related issues by root cause
2. Identify fix order (security first, then stability)
3. Map file dependencies
4. Present staged fix plan
5. Execute fixes in safe order
