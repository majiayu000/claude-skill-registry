---
name: phase-start
description: Execute all tasks in a phase autonomously. Use after /phase-prep confirms prerequisites are met.
argument-hint: "<phase-number> [--codex] [--pause]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, WebFetch, WebSearch
---

Execute all steps and tasks in Phase $1 from EXECUTION_PLAN.md.

## Workflow

Copy this checklist and track progress:

```
Phase Start Progress:
- [ ] Parse arguments and detect execution mode
- [ ] Context detection (project root vs feature)
- [ ] Directory guard (EXECUTION_PLAN.md + AGENTS.md)
- [ ] Context check (compact if <40% remaining)
- [ ] Codex mode prerequisites (if --codex)
- [ ] Git setup (commit dirty files, create phase branch)
- [ ] Execute tasks sequentially (test → implement → verify → commit)
- [ ] Track state in phase-state.json
- [ ] Phase completion summary
- [ ] Auto-advance to checkpoint (if conditions met)
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `$1` | Yes | Phase number to execute |
| `--codex` | No | Execute tasks via Codex CLI instead of directly |
| `--pause` | No | Stop after phase completes (skip auto-advance to checkpoint) |

## Execution Modes

**Default mode:** Claude Code executes tasks directly using its tools.

**Codex mode (`--codex`):** Claude Code orchestrates while Codex CLI executes each task:
- Claude Code maintains context, verification, auto-advance logic
- Codex executes individual tasks with documentation research
- Results return to Claude Code for verification and next-task decisions

Use `--codex` when:
- Tasks involve external APIs where current documentation matters
- You want cross-model execution for different perspectives
- Codex's web search during implementation adds value

## External Tool Documentation Protocol

**CRITICAL:** Before implementing code that integrates with external services, you MUST read the latest official documentation first.

### When to Fetch Docs

Fetch documentation when ANY of these apply:
- Task involves integrating with a third-party API (Supabase, Stripe, Firebase, etc.)
- You're writing code that calls external service endpoints
- Task references SDK usage for an external service
- You need to implement webhooks, authentication, or data sync with external services

### How to Fetch Docs

1. **Identify external services** from task description and acceptance criteria
2. **Fetch relevant docs** using WebFetch or WebSearch:
   - SDK/library installation and setup
   - API reference for specific endpoints being used
   - Code examples for the integration pattern
3. **Cache per session** — Don't re-fetch docs already fetched in this session
4. **Handle failures gracefully:**
   - Retry with exponential backoff (2-3 attempts)
   - If all retries fail: warn user and proceed with best available info

### Documentation URLs by Service

| Service | SDK/API Documentation |
|---------|----------------------|
| Supabase | https://supabase.com/docs/reference/javascript |
| Firebase | https://firebase.google.com/docs/reference/js |
| Stripe | https://stripe.com/docs/api |
| Auth0 | https://auth0.com/docs/api |
| Clerk | https://clerk.com/docs/references/javascript |
| Resend | https://resend.com/docs/api-reference |
| OpenAI | https://platform.openai.com/docs/api-reference |
| Anthropic | https://docs.anthropic.com/en/api |
| Trigger.dev | https://trigger.dev/docs |

For services not listed, use WebSearch: `{service name} {language} SDK documentation`

### Integration with Task Execution

When implementing external service integrations:
1. Fetch docs FIRST before writing integration code
2. Use the official SDK patterns (not outdated examples)
3. Follow current authentication methods from docs
4. Reference error handling patterns from official documentation
5. Check for breaking changes if using a newer SDK version

## Context Detection

Determine working context. **For feature work, users should `cd` into `features/<name>/` before running execution commands.** The skill auto-detects feature mode from the path.

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Context

Before starting, read these files:
- **PROJECT_ROOT/AGENTS.md** — Follow all workflow conventions
- **EXECUTION_PLAN.md** — Task definitions and acceptance criteria (from CWD)

## Directory Guard (Wrong Directory Check)

Before starting, confirm the required files exist:
- `EXECUTION_PLAN.md` exists in the current working directory
- `PROJECT_ROOT/AGENTS.md` exists

- If either is missing, **STOP** and tell the user to `cd` into their project/feature directory (the one containing `EXECUTION_PLAN.md`) and re-run `/phase-start $1`.

## Context Check

**Before starting:** If context is below 40% remaining, run `/compact` first. This ensures the full command instructions remain in context throughout execution. Compaction mid-command loses procedural instructions.

## Codex Mode Prerequisites (if `--codex` flag provided)

Skip this section if `--codex` was not provided.

See [CODEX_MODE.md](CODEX_MODE.md) for detailed Codex CLI setup and configuration.

## Execution Rules

1. **Git Workflow (Auto-Commit)**

   **One branch per phase, one commit per task:**
   ```
   main
     └── phase-$1 (branch)
           ├── task(1.1.A): Add user model       ← step 1.1
           ├── task(1.1.B): Add user routes
           ├── task(1.1.C): Add user tests
           ├── task(1.2.A): Add auth middleware   ← step 1.2 continues
           ├── task(1.2.B): Add login endpoint
           └── task(1.3.A): Add session handling  ← step 1.3 continues
   ```

   Before starting the phase (once, at the beginning):
   ```bash
   # Commit any dirty files first (preserves user work)
   git add -A && git diff --cached --quiet || git commit -m "wip: uncommitted changes before phase-$1"
   ```

   **Check for unpushed commits before branching:**
   ```bash
   # Get current branch and check if ahead of remote
   CURRENT_BRANCH=$(git branch --show-current)
   UNPUSHED=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "no-upstream")
   ```

   - If `UNPUSHED` is a number > 0:
     - Ask: "You have {UNPUSHED} unpushed commit(s) on `{CURRENT_BRANCH}`. Push before creating phase branch? (recommended)"
     - If yes: `git push`
     - If no: Continue (user accepts branching from unpushed state)
   - If `UNPUSHED` is "no-upstream" or 0: Continue without prompting

   ```bash
   # Create phase branch from current HEAD
   git checkout -b phase-$1
   ```

   **Verify branch creation:**
   ```bash
   git branch --show-current
   ```
   If the output doesn't match `phase-$1`, the checkout failed. Check if branch already exists and append a suffix.

   After each task completion (sequential commits on same branch):
   ```bash
   git add -A
   git commit -m "task({id}): {description} [REQ-XXX]"
   ```

   **Requirement traceability:** Check the task's `Requirement:` field in EXECUTION_PLAN.md.
   - If a REQ-ID exists (e.g., `REQ-002`), include it: `task(1.2.A): Add auth [REQ-002]`
   - If no REQ-ID or "None", omit brackets: `task(1.1.A): Set up scaffolding`

   **Do NOT push.** Leave pushing to the human after manual verification at checkpoint.

   **Commit discipline:**
   - Every task gets its own commit immediately after verification passes
   - All commits are sequential on the phase branch—each builds on the previous
   - Steps are logical groupings, not separate branches
   - Never batch multiple tasks into one commit
   - Include task ID in commit message for traceability
   - Use conventional commit format: `task({id}): {imperative description}`

2. **Task Execution** (for each task)

   {If `--codex` flag provided}

   **Codex Execution Mode:**

   See [CODEX_MODE.md](CODEX_MODE.md) for full details. Summary:
   - Build task prompt with context and acceptance criteria
   - Execute via `codex exec` with appropriate flags
   - Process results and handle failures
   - Verify and commit (Claude Code verifies Codex's work)

   {Else}

   **Default Execution Mode:**

   - Read the task definition and acceptance criteria
   - **Explore before implementing:**
     - Search for similar existing functionality (don't duplicate)
     - Identify patterns used elsewhere in codebase
     - List reusable utilities/components to leverage
     - Note conventions (naming, error handling, structure)
   - Write tests first (one per acceptance criterion)
   - Implement minimum code to pass tests, following discovered patterns
   - Run verification using /verify-task
   - Update checkboxes in EXECUTION_PLAN.md: `- [ ]` → `- [x]`
   - **Commit immediately** (see Git Workflow above)

   {/If}

3. **Stuck Detection and Recovery**

   Track failures **in `.claude/phase-state.json`** so counters survive context compaction.

   For each task, maintain a `failures` object in the task's state entry:
   ```json
   {
     "consecutive": 0,
     "verification_attempts": {"V-001": 2, "V-003": 1},
     "last_errors": ["error msg 1", "error msg 2"]
   }
   ```

   - **On task failure**: Increment `consecutive`, append to `last_errors` (keep last 3), write to phase-state.json
   - **On task success**: Reset `consecutive` to 0, clear `last_errors`
   - **On verification attempt**: Increment the criterion's count in `verification_attempts`

   **Read these counters before each attempt.** If ANY threshold is met, **STOP and escalate to human**:

   | Trigger | Threshold | Check |
   |---------|-----------|-------|
   | Consecutive task failures | 3 tasks | `failures.consecutive >= 3` |
   | Same error pattern | 2 occurrences | Same error string in `failures.last_errors` twice |
   | Verification loop | 5 attempts on same criterion | `failures.verification_attempts[criterion] >= 5` |
   | Test flakiness | Same test passes then fails | Detected during verification (log to `last_errors`) |

   **When stuck, report:**
   ```
   STUCK: Phase $1, Task {id}
   ─────────────────────────────
   Pattern: {describe what keeps failing}
   Attempts: {N}

   Last 3 errors:
   1. {error summary}
   2. {error summary}
   3. {error summary}

   Possible causes:
   - {hypothesis 1}
   - {hypothesis 2}

   Options:
   1. Skip this task and continue
   2. Modify acceptance criteria
   3. Take a different approach: {suggestion}
   4. Abort phase for manual intervention
   ```

   **Do not:**
   - Keep retrying the same approach
   - Silently skip failing tasks
   - Reduce test coverage to make things pass

4. **Blocking Issues**
   - If blocked, report using the format in AGENTS.md
   - Do not continue past a blocker without resolution

5. **Context Hygiene**
   - Summarize progress between steps if context grows large

## State Tracking

Maintain `.claude/phase-state.json` throughout execution. See [STATE_TRACKING.md](STATE_TRACKING.md) for JSON formats.

Key updates:
1. **At phase start**: Set status to `IN_PROGRESS` with timestamp and execution mode
2. **After each task**: Update task entry with `COMPLETE` status; reset `failures.consecutive` to 0
3. **On task failure**: Increment `failures.consecutive`, append error to `failures.last_errors` (max 3)
4. **On verification attempt**: Increment `failures.verification_attempts[criterion_id]`
5. **If blocked**: Record blocker type and description

If `.claude/phase-state.json` doesn't exist, run `/populate-state` first to initialize it.

---

## Completion

Do not check back until Phase $1 is complete, unless blocked or stuck.

When done, provide:
- Execution mode used (default or Codex)
- Summary of what was built
- Files created/modified
- Git branch and commits created
- Any issues encountered
- Ready for /phase-checkpoint $1

**Note:** Branches are not pushed automatically. After `/phase-checkpoint` passes, the human will review and push.

---

## Auto-Advance (After Phase Completes)

Check if auto-advance is enabled and this phase completes with no manual items.

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

### Pre-Check: Attempt Automation on Manual Items

Before evaluating auto-advance conditions, attempt automation on checkpoint manual items:

1. Extract manual verification items from "Phase $1 Checkpoint" section in EXECUTION_PLAN.md
2. For each manual item, invoke auto-verify skill with item text and available tools
3. Categorize results:
   - **Automated**: Item verified automatically (PASS/FAIL)
   - **Truly Manual (blocking)**: No automation, tagged `MANUAL`, downstream dependency
   - **Truly Manual (deferrable)**: No automation, tagged `MANUAL:DEFER`, no dependency → enqueue to `.claude/deferred-reviews.json`

### Auto-Advance Conditions

Auto-advance to `/phase-checkpoint $1` ONLY if ALL of these are true:

1. ✓ All tasks in Phase $1 are complete
2. ✓ No BLOCKING manual checkpoint items remain
   (MANUAL:DEFER items are queued to `.claude/deferred-reviews.json`, not blocking)
3. ✓ No tasks were marked as blocked or skipped
4. ✓ `--pause` flag was NOT passed to this command
5. ✓ `autoAdvance.enabled` is true (or not configured, defaulting to true)

**Rationale:** Auto-verify attempts automation before blocking. Only items tagged `(MANUAL)` that genuinely require human judgment AND affect downstream work block auto-advance. Items tagged `(MANUAL:DEFER)` are enqueued for later review. Items that can be verified with curl, file checks, or browser automation don't require human presence.

### If Auto-Advance Conditions Met

1. **Show brief notification:**
   ```
   AUTO-ADVANCE
   ============
   All Phase $1 tasks complete. No truly manual verification items.
   {N} checkpoint items can be auto-verified.
   Proceeding to checkpoint...
   ```

2. **Execute immediately:**
   - Track this command in auto-advance session log
   - Invoke `/phase-checkpoint $1` using the Skill tool
   - Checkpoint will continue the chain if it passes

### If Auto-Advance Conditions NOT Met

Stop and report why:

```
PHASE $1 COMPLETE
=================
All tasks finished.

Cannot auto-advance because:
- {reason: e.g., "Phase has blocking manual verification items"}

Checkpoint Verification Preview:
--------------------------------
Automatable ({N} items):
- [auto] "{item}" — can verify with {method}

Blocking Manual ({N} items requiring human judgment):
- [ ] "{item}"
  - Reason: {why this blocks downstream work}

{If deferred items exist:}
Deferred ({N} items queued for later review):
- "{item}" — no downstream dependency
{/If}

Next: Run /phase-checkpoint $1 when ready to verify

Ready to open a PR? Run: /create-pr
```
