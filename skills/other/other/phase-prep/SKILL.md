---
name: phase-prep
description: Check prerequisites before starting a phase. Use before /phase-start to verify dependencies are met and context is loaded.
argument-hint: [phase-number]
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

I want to execute Phase $1 from EXECUTION_PLAN.md. Before starting, read EXECUTION_PLAN.md and check:

## Workflow

Copy this checklist and track progress:

```
Phase Prep Progress:
- [ ] Step 1: Run pre-flight checks 1-7
- [ ] Step 2: Verify all prerequisites pass
- [ ] Step 3: Load phase context and task list
- [ ] Step 4: Check for blocking dependencies
- [ ] Step 5: Make auto-advance decision
- [ ] Step 6: Report readiness status
```

## External Tool Documentation Protocol

**CRITICAL:** Before providing setup instructions for any external service (Supabase, Stripe, Firebase, Auth0, Vercel, etc.), you MUST read the latest official documentation first.

### When to Fetch Docs

Fetch documentation when ANY of these apply:
- Pre-Phase Setup mentions an external service
- You're about to provide step-by-step setup instructions
- The phase involves integrating with a third-party API
- Environment variables reference external services (e.g., `STRIPE_API_KEY`, `SUPABASE_URL`)

### How to Fetch Docs

1. **Identify the service** from Pre-Phase Setup items or EXECUTION_PLAN.md
2. **Fetch official docs** using WebFetch or WebSearch:
   - Primary: Official quickstart/setup guide
   - Secondary: API reference for specific integrations
3. **Cache per session** — Don't re-fetch the same docs within one session
4. **Handle failures gracefully:**
   - Retry with exponential backoff (2-3 attempts)
   - If all retries fail: warn user and proceed with best available info
   - Never block entirely on doc fetch failure

### Documentation URLs by Service

See [SERVICES.md](SERVICES.md) for the full list of service documentation URLs and setup patterns.

### Integration with Setup Instructions

When generating detailed setup guides (see "Detailed Setup Instructions" section below):
1. Fetch docs FIRST
2. Cross-reference fetched content with your instructions
3. Update any outdated steps (UI changes, renamed fields, new requirements)
4. Include version/date context: "As of {date}, the Supabase dashboard..."


## Context Detection

Determine working context:

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Directory Guard (Wrong Directory Check)

Before starting, confirm the required files exist:
- `EXECUTION_PLAN.md` exists in the current working directory
- `PROJECT_ROOT/AGENTS.md` exists

- If either does not exist, **STOP** and tell the user:
  - They are likely in the toolkit repo (or the wrong folder)
  - They should `cd` into their project/feature directory (the one containing `EXECUTION_PLAN.md`) and re-run `/phase-prep $1`

## Context Check

**Before starting:** If context is below 40% remaining, run `/compact` first. This ensures the full command instructions remain in context throughout execution. Compaction mid-command loses procedural instructions.

## Pre-Flight Checks

1. **Pre-Phase Setup** — Check the "Pre-Phase Setup" section for Phase $1:
   - For each setup item, run its `Verify:` command if provided
   - Mark each item as PASS/FAIL/BLOCKED based on command output
   - **Auto-generate Verify commands** if missing (see below)
   - Identify environment variables or secrets needed
   - Note any external services that must be configured

   **Auto-Verify Generation:**
   If a setup item lacks a `Verify:` line, infer one based on item type.
   See [SERVICES.md](SERVICES.md) for the auto-verify command templates.
   After auto-generating, add the `Verify:` line to EXECUTION_PLAN.md for future runs.

2. **Dependencies** — Verify prior phases are complete:
   - Check that all tasks from previous phases have checked boxes
   - Flag any incomplete dependencies

3. **Verification Config** — Check `.claude/verification-config.json`:
   - If file is completely missing → run `/configure-verification` to auto-detect
   - If file exists but some command keys are omitted → treat as "not configured
     for that check" (don't block, don't ask to configure)
   - If upcoming phase has `BROWSER:*` criteria in EXECUTION_PLAN.md and config
     has no `auth` or `deployment` section → emit warning (non-blocking):
     ```
     WARNING: Phase $1 has browser criteria but no auth/deployment configured.
     Browser tests will run against localhost without authentication.
     Configure these in verification-config.json if needed.
     ```

4. **Git Status** — Check repository state:
   - Run `git status` to verify clean working tree (or understand current state)
   - Note the current branch

5. **Tool Availability** — Check optional tools by attempting a harmless call:

   | Tool | Check | If Unavailable |
   |------|-------|----------------|
   | ExecuteAutomation Playwright | Check for `mcp__playwright__*` or `mcp__executeautomation__*` | Next in chain |
   | Browser MCP | Check for `mcp__browsermcp__*` tools | Next in chain |
   | Microsoft Playwright MCP | Check for `mcp__playwright__*` tools | Next in chain |
   | Chrome DevTools MCP | Call `mcp__chrome-devtools__list_pages` | Manual verification |
   | code-simplifier | Check agent type available | Skip code simplification |
   | Trigger.dev MCP | `mcp__trigger__list_projects` | Skip Trigger.dev features |

   **Browser tool fallback chain:** ExecuteAutomation Playwright → Browser MCP → Microsoft Playwright → Chrome DevTools → Manual

   Only check tools relevant to this project's tech stack.

6. **Criteria Audit** — Run `/criteria-audit` when preparing Phase 1:
   - If `$1` is 1, run `/criteria-audit`
   - If FAIL, block phase start until metadata is fixed
   - If `$1` is not 1, skip unless EXECUTION_PLAN.md was edited since last phase

7. **Permissions** — Review the tasks in Phase $1:
   - Identify any tools or permissions needed for autonomous execution
   - Check if any tasks require browser verification

## Detailed Setup Instructions (When Items Incomplete)

If any Pre-Phase Setup items are FAIL or BLOCKED, provide detailed step-by-step instructions for each:

### For Each Incomplete Item

1. **Identify the service/tool involved** (e.g., Supabase, Stripe, Firebase)

2. **Research if needed** — Use WebFetch/WebSearch to get current setup steps

3. **Generate a complete guide** including:
   - Direct links to dashboards/consoles
   - Exact field values to enter
   - What to copy and where to paste
   - Verification steps to confirm completion

### Example Transformation

Instead of:
```
Pre-Phase Setup:
- [ ] Create Supabase project — BLOCKED
```

Output:
```
PRE-PHASE SETUP GUIDE
=====================

## Create Supabase Project

1. Go to https://supabase.com/dashboard
2. Sign in or create account
3. Click "New Project" (green button, top right)
4. Fill in:
   - Organization: Select or create one
   - Name: `{project-name}` (or your preference)
   - Database Password: Click "Generate" and SAVE THIS
   - Region: Choose closest to your users
5. Click "Create new project"
6. Wait 2-3 minutes for provisioning

## Get Credentials

1. In Supabase dashboard, click "Project Settings" (gear icon)
2. Click "API" in the left menu
3. Copy these values:
   - Project URL: `https://xxxxx.supabase.co` → SUPABASE_URL
   - anon public key: `eyJ...` → SUPABASE_ANON_KEY

## Update .env File

Add to `.env`:
```
SUPABASE_URL=<paste Project URL>
SUPABASE_ANON_KEY=<paste anon public key>
```

## Verify Setup

Run `/phase-prep $1` again to confirm all items complete.
```

### Common Service Templates

See [SERVICES.md](SERVICES.md) for setup patterns for: Supabase, Firebase, Stripe, Auth0, Vercel/Netlify, and other common services.

---

## Future Phase Preview

After showing current phase prerequisites, scan ALL remaining phases and show human-required items.

### What to Extract

For each phase after $1, extract ONLY human-required setup items:
- Account creation (external services)
- API key acquisition
- Manual configuration tasks
- External service setup

Do NOT include:
- Automated checks
- Code-related tasks
- Verification steps

### Output Format

```
## Future Phase Preview

Items below require human action. Complete now to avoid blockers later.

### Phase {N+1}: {Phase Title}
Human Setup Required:
- {Human item 1}
- {Human item 2}

### Phase {N+2}: {Phase Title}
Human Setup Required:
- {Human item 1}

### Phase {N+3}: {Phase Title}
(No human setup items)

---
TIP: Complete future setup now to avoid blockers later.
Run `/phase-prep {N}` for detailed instructions on any item.
```

If no future phases have human items, omit this section.

---

## Report

```
PHASE $1 PREREQUISITES
======================

Documents:
- EXECUTION_PLAN.md: ✓ | ✗
- AGENTS.md (at PROJECT_ROOT): ✓ | ✗
- Prior phases: Complete | N/A

Verification Config:
- verification-config.json: ✓ | ✗
- Configured: {list only commands that ARE in config, e.g., "test, lint, build"}
- Not configured: {list omitted commands, or "none" if all present}

Git: {branch}, {clean | dirty}

Pre-Phase Setup:
- {items with PASS/FAIL/BLOCKED}

[If any FAIL/BLOCKED, show detailed setup guide above]

Environment:
- {env vars or "None required"}

Tools:
- ExecuteAutomation Playwright: ✓ | ✗ (primary)
- Browser MCP Extension: ✓ | ✗
- Microsoft Playwright MCP: ✓ | ✗
- Chrome DevTools MCP: ✓ | ✗
- code-simplifier: ✓ | ✗
- Trigger.dev MCP: ✓ | ✗ | N/A

Criteria Audit: PASS | WARN | FAIL

Status: READY | BLOCKED | READY WITH NOTES
{Details if not READY}

---

## Future Phase Preview

[Show human items for all remaining phases]
```

After reporting, append the pre-phase results to `.claude/verification-log.jsonl`
with timestamps and any evidence paths (if collected).

Example log entry:
```json
{
  "timestamp": "{ISO timestamp}",
  "scope": "phase-prep",
  "phase": "$1",
  "check": "pre-phase-setup",
  "status": "PASS",
  "evidence": null
}
```

## Auto-Advance (After Prep Passes)

Check if auto-advance is enabled and this prep passes all checks.

### Configuration Check

Read `.claude/settings.local.json` for auto-advance configuration:

```json
{
  "autoAdvance": {
    "enabled": true      // default: true
  }
}
```

If `autoAdvance` is not configured, use defaults (`enabled: true`).

### Auto-Advance Conditions

Auto-advance to `/phase-start $1` ONLY if ALL of these are true:

1. ✓ All Pre-Phase Setup items are PASS (none FAIL or BLOCKED)
2. ✓ Dependencies (prior phases) are complete
3. ✓ Verification config file exists (omitted keys are OK — treated as not applicable)
4. ✓ Criteria audit passed (for Phase 1)
5. ✓ `--pause` flag was NOT passed to this command
6. ✓ `autoAdvance.enabled` is true (or not configured, defaulting to true)

**Rationale:** Auto-advance only proceeds when all prerequisites are verified (PASS). Re-running `/phase-prep` after completing human setup confirms readiness and allows auto-advance.

### If Auto-Advance Conditions Met

1. **Show brief notification:**
   ```
   AUTO-ADVANCE
   ============
   All Phase $1 prerequisites verified. Proceeding to execution...
   ```

2. **Execute immediately:**
   - Track this command in auto-advance session log
   - Invoke `/phase-start $1` using the Skill tool
   - Phase-start will continue, and its checkpoint will continue the chain

### If Auto-Advance Conditions NOT Met

Stop and report why:

```
AUTO-ADVANCE STOPPED
====================

Reason: {one of below}
- Pre-Phase Setup items failed or blocked
- Prior phases not complete
- Verification config not configured
- Criteria audit failed (Phase 1 only)
- Auto-advance disabled via --pause flag
- Auto-advance disabled in settings

{If human items exist:}
Human setup required:
- [ ] {human item 1} — See detailed instructions above
- [ ] {human item 2}

Next steps:
1. Complete the setup items above
2. Run /phase-start $1 manually when ready
```

### Auto-Advance Session Tracking

If this is part of an auto-advance chain (`.claude/auto-advance-session.json` exists), append this command to the session log:

```json
{
  "commands": [
    // ... previous commands
    {"command": "/phase-prep $1", "status": "PASS", "timestamp": "{ISO}"}
  ]
}
```

If auto-advance stops here, generate the session report (see phase-checkpoint for format) and clean up the session file.
