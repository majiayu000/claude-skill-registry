---
name: pr-patrol
description: This skill should be used when the user asks to "handle bot comments", "fix PR review feedback", "address CodeRabbit/Greptile/Copilot issues", "respond to review bot suggestions", "process automated review comments", or runs "/pr-patrol". Patrols the PR for bot comments (CodeRabbit, Greptile, Codex, Copilot, Sentry) with state tracking and batch processing through a 7-gate workflow.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Task, AskUserQuestion
---

# PR Patrol

Process automated PR review comments through a 7-gate workflow with phase-based loading.

---

## ⚠️ CRITICAL REMINDERS

1. **READ PHASE FILE FIRST** - Check status in state file, read `phases/gate-{N}.md` for current phase
2. **USE AGENTS FOR VALIDATION** - Use `bot-comment-validator` via Task tool, never manual
3. **ASK ABOUT PR-REVIEW AGENTS** - After checks pass, ask about `code-reviewer`/`silent-failure-hunter`
4. **ISSUE COMMENTS NEED @MENTION** - GitHub issue comments don't support threading
5. **UPDATE STATE FILE** - After EVERY action (use `scripts/update_state.sh`)
6. **NEVER REPLY TO COPILOT** - Silent fix only, no reactions, no replies
7. **TRUST SCRIPT OUTPUT** - When scripts return data, DO NOT make extra API calls to "verify"!

---

## Quick Reference

| Bot | Login | Reaction | Reply |
|-----|-------|----------|-------|
| CodeRabbit | `coderabbitai[bot]` | ❌ | ✅ |
| Greptile | `greptile-apps[bot]` | 👍/👎 FIRST | ✅ THEN |
| Codex | `chatgpt-codex-connector[bot]` | 👍/👎 FIRST | ✅ THEN |
| Copilot | `Copilot` | ❌ NEVER | ❌ NEVER |
| Sentry | `sentry[bot]` | 👍/👎 FIRST | ✅ THEN |

**Ignored:** `vercel[bot]`, `dependabot[bot]`, `renovate[bot]`, `github-actions[bot]`

---

## Workflow Diagram

```
/pr-patrol [PR#]
       │
       ▼
┌─ GATE 0: Init ──────────────────────┐
│ [AskUserQuestion] Mode, scope       │ → phases/gate-0-init.md
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 1: Collect ───────────────────┐
│ [AskUserQuestion] Proceed?          │ → phases/gate-1-collect.md
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 2: Validate ──────────────────┐
│ [Task: bot-comment-validator]       │ → phases/gate-2-validate.md
│ [AskUserQuestion] Which to fix?     │
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 3: Fix & Check ───────────────┐
│ Apply fixes → typecheck → lint      │ → phases/gate-3-fix.md
│ [AskUserQuestion] Run pr-review?    │ ← Gate 3.5!
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 4: Commit ────────────────────┐
│ [AskUserQuestion] Review & commit?  │ → phases/gate-4-commit.md
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 5: Reply ─────────────────────┐
│ [AskUserQuestion] Post replies?     │ → phases/gate-5-reply.md
│ Also read: bot-formats.md           │
└─────────────────────────────────────┘
       │
       ▼
┌─ GATE 6: Push ──────────────────────┐
│ [AskUserQuestion] Push? Cycle 2?    │ → phases/gate-6-push.md
└─────────────────────────────────────┘
```

---

## Phase Routing (FOLLOW THIS!)

### Step 1: Check State File

```bash
STATE_FILE=".claude/bot-reviews/PR-{N}.md"
```

### Step 2: Read Current Phase

| Status | Read This Phase File |
|--------|----------------------|
| (no file) | `phases/gate-0-init.md` |
| `initialized` | `phases/gate-1-collect.md` |
| `collected` | `phases/gate-2-validate.md` |
| `validated` | Check `next_gate` field: if `5` → `phases/gate-5-reply.md`, else `phases/gate-3-fix.md` |
| `fixes_planned` | `phases/gate-3-fix.md` |
| `fixes_applied` | `phases/gate-3-fix.md` (run checks) |
| `checks_passed` | `phases/gate-4-commit.md` |
| `committed` | `phases/gate-5-reply.md` |
| `replies_sent` | `phases/gate-6-push.md` |
| `pushed` | Check for new comments → Cycle 2? |

### Step 3: Follow Phase Instructions

Each phase file contains:
- Detailed step-by-step actions
- MANDATORY AskUserQuestion prompts
- Edge cases and error handling
- State file update commands

---

## Scripts Location

```bash
SCRIPTS="${CLAUDE_PLUGIN_ROOT}/skills/pr-patrol/scripts"

# Core scripts
"$SCRIPTS/fetch_pr_comments.sh" owner repo pr              # Parallel API fetch + normalize
cat normalized.json | "$SCRIPTS/detect_thread_states.sh"   # State detection (reads stdin)
"$SCRIPTS/check_new_comments.sh" owner repo pr [since]     # New since push
"$SCRIPTS/check_reply_status.sh" owner repo pr             # Reply tracking
"$SCRIPTS/update_state.sh" file field value                # State updates
"$SCRIPTS/update_billboard.sh" file status gate action     # Billboard + frontmatter update
"$SCRIPTS/build_greptile_summary.sh" file cycle            # Greptile summary comment
"$SCRIPTS/parse_coderabbit_embedded.sh" [file]             # Extract embedded comments (stdin or file)

# jq libraries (used by scripts above, not called directly)
# bot-detection.jq        — shared bot detection functions
# normalize_comments.jq   — transform raw API → normalized structure
# severity_detection.jq   — add severity to comments
# detect_states.jq        — thread state detection (NEW/PENDING/RESOLVED/REJECTED)
```

---

## Reference Files Location

```bash
SKILL_ROOT="${CLAUDE_PLUGIN_ROOT}/skills/pr-patrol"

# Read these files with their FULL paths:
"$SKILL_ROOT/phases/gate-{N}.md"    # Phase instructions
"$SKILL_ROOT/bot-formats.md"        # Bot protocols (CRITICAL for Gate 5!)
"$SKILL_ROOT/templates.md"          # Reply templates
```

| File | Purpose | When to Read |
|------|---------|--------------|
| `phases/gate-{N}.md` | Phase-specific instructions | Based on status |
| `bot-formats.md` | Bot-specific protocols | **MUST READ before Gate 5** |
| `templates.md` | Reply message templates | Gate 5 (replies) |
| `examples/sample-*.md` | State file examples at each stage | When unsure about state file format |
| `examples/sample-*.json` | Script output shapes | When working with script output |

---

## Critical Rules

1. **EVERY gate requires AskUserQuestion** - Never skip user approval
2. **ALL comments must be validated** - Severity only affects priority
3. **Copilot gets NO response** - Silent fix only, no reactions, no replies
4. **NEVER commit/push without approval** - Explicit consent required
5. **NEVER force push** - Blocked completely
6. **Typecheck/lint are MANDATORY** - Block on failure
7. **ALWAYS use --paginate** - Default GitHub API returns only 30 comments
8. **Fetch BOTH endpoints** - Review comments (`/pulls/{pr}/comments`) AND issue comments (`/issues/{pr}/comments`)
9. **Extract embedded CodeRabbit comments** - Use `"$SCRIPTS/parse_coderabbit_embedded.sh"` for nitpicks, duplicates, outside-diff
10. **Issue vs PR review comments** - Different reply methods! Issue comments need @mention (no threading)
11. **Reaction BEFORE reply** - For Greptile/Codex/Sentry, add reaction first, then reply
12. **Short reply format** - "Fixed in commit {sha}: {description}" NOT verbose essays
13. **Use helper scripts** - `${CLAUDE_PLUGIN_ROOT}/skills/pr-patrol/scripts/` has utilities
14. **TRUST SCRIPT OUTPUT** - When scripts return data, DO NOT make verification queries

---

## jq Escaping Warning

**Shell escaping corrupts jq `!=` operators.** For any jq with `!=` or complex logic, use the `.jq` files in `scripts/` instead of inline jq. For negation, use `| not` (e.g., `select(.bot == "Copilot" | not)`).
