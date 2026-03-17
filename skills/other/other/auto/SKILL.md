---
disable-model-invocation: true
description: Start autonomous execution with stop hook feedback loop. Works until all tasks complete or max iterations reached. Use when you want continuous unattended execution.
argument-hint: "[INCREMENT_IDS...] [OPTIONS]"
---

# Auto Command

## Project Overrides

!`s="auto"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Project Context

!`.specweave/scripts/skill-context.sh auto 2>/dev/null; true`

**Start autonomous execution session using Claude Code's Stop Hook.**

## Usage

```bash
/sw:auto [INCREMENT_IDS...] [OPTIONS]
```

- `INCREMENT_IDS`: One or more increment IDs (e.g., `0001`, `0001-feature`). If omitted, finds active increments or intelligently creates new ones.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--max-turns N` | Max hook invocations before hard stop | 20 |
| `--simple` | Minimal context mode | false |
| `--dry-run` | Preview without starting | false |
| `--all-backlog` | Process all backlog items | false |
| `--skip-gates G1,G2` | Pre-approve specific gates | None |
| `--no-increment` | Require existing increments (no auto-creation) | false |
| `--yes`, `-y` | Auto-approve increment plan | false |
| `--tdd`, `--strict` | TDD strict mode (RED->GREEN->REFACTOR enforced) | false |
| `--build` | Build must pass before completion | false |
| `--tests` | Tests must pass before completion | false |
| `--e2e` | E2E tests must pass before completion | false |
| `--lint` | Linting must pass before completion | false |
| `--types` | Type-checking must pass before completion | false |
| `--cov <n>` | Code coverage threshold (%) | 80 |
| `--cmd "<command>"` | Custom command must pass | None |

## Core Loop

```
IMPLEMENT task -> TEST -> FAIL? -> FIX -> PASS -> mark complete -> NEXT task -> ... -> ALL DONE -> /sw:done --auto -> CLOSED
```

Stop hook blocks when tasks/ACs remain. When all work is complete, stop hook blocks with `all_complete_needs_closure` to trigger `/sw:done --auto`. Model enforces quality gates (build/tests/lint) before closure.

## Execution

### Step 1: Set Up Auto Session

Use Read/Write/Edit/Glob tools directly (no CLI needed):

**1a. Read config** — `.specweave/config.json`: `auto.enabled`, `auto.maxTurns` (default 20), `testing.defaultTestMode`, `testing.tddEnforcement`

**1b. Find increments:**
- If IDs specified: Glob `.specweave/increments/{ID}*/metadata.json`, verify exists
- If no IDs: find active/in-progress increments. If none, check backlog/planned. If none at all, go to Step 2 (Intelligent Creation).

**1c. Activate increments** — Edit `metadata.json`: set `"status": "active"`, update timestamp

**1d. Write session marker** — `.specweave/state/auto-mode.json`:

```json
{
  "active": true,
  "timestamp": "<ISO>",
  "incrementIds": ["0001-feature"],
  "tddMode": false,
  "requireTests": false,
  "userGoal": null,
  "successCriteria": [
    { "type": "tasks_complete", "description": "All tasks marked complete", "required": true },
    { "type": "acs_satisfied", "description": "All ACs satisfied", "required": true }
  ],
  "successSummary": "All tasks and acceptance criteria complete"
}
```

Map flags to extra `successCriteria` entries:
- `--tests` -> `{ "type": "tests_pass", "required": true }`
- `--build` -> `{ "type": "build_succeeds", "required": true }`
- `--e2e` -> `{ "type": "tests_pass", "description": "E2E tests", "required": true }`
- `--lint` -> `{ "type": "custom_command", "command": "<lint-cmd>", "required": true }`
- `--types` -> `{ "type": "custom_command", "command": "npx tsc --noEmit", "required": true }`
- `--cov N` -> `{ "type": "tests_pass", "threshold": N, "required": true }`
- `--cmd "X"` -> `{ "type": "custom_command", "command": "X", "required": true }`
- `--tdd` -> set `"tddMode": true`

Always include `tasks_complete` and `acs_satisfied` as base criteria. Ensure `.specweave/state/` dir exists.

**`userGoal` field**: Set to the user's stated intent from conversation context. If the user said "fix the auth bug", set `userGoal` to `"fix the auth bug"`. If no clear intent is expressed, set to `null`. This field is read by the stop hook to provide context-aware feedback and guide `/sw:do` to the correct increment.

### Step 1.5a: MANDATORY - Complexity Check for Team-Lead Routing

**Before starting autonomous execution, check if this increment needs team-lead:**

1. Count pending tasks in tasks.md (count `[ ]` markers)
2. Detect domains from file paths in tasks.md and plan.md:
   - Frontend: `.tsx`, `src/components/`, `src/pages/`, React/Vue keywords
   - Backend: `src/api/`, `src/services/`, `src/routes/`, Express/NestJS keywords
   - Database: `prisma/`, `migrations/`, SQL keywords
   - DevOps: `Dockerfile`, `.github/`, `k8s/` keywords
   - Testing: `tests/`, `e2e/`, `.test.` keywords
   - Security: `src/auth/`, auth keywords
   - Mobile: `ios/`, `android/`, React Native keywords

3. **If 3+ domains detected OR domain count suggests multi-agent benefit:**

   ```
   ⚠️  COMPLEXITY ASSESSMENT
   ══════════════════════════════════════════
   Tasks: [N] pending | Domains: [N] ([list])
   ──────────────────────────────────────────
   This increment spans 3+ domains. /sw:team-lead is recommended
   for parallel execution with higher quality results.
   ⚡ Trade-off: ~2-3x more tokens, but parallel agents
      produce better results for multi-domain work.
   ══════════════════════════════════════════
   ```

   Then use AskUserQuestion:
   - Option A: "Use /sw:team-lead (Recommended)" — invoke team-lead and stop auto
   - Option B: "Continue with /sw:auto (sequential)" — proceed normally

   **In auto mode** (no user present): Auto-invoke `/sw:team-lead` for 3+ domains.
   This is the default behavior per CLAUDE.md execution strategy.

### Step 1.5: MANDATORY - Display Stop Conditions

**You MUST output a stop conditions banner BEFORE starting work.** Detect test frameworks, count test files, then show:

```
AUTO MODE STARTING
======================================================================
Increment: [ID] | Tasks: [N] pending
======================================================================
TESTS THAT MUST PASS:
  Unit: [command] - [N] test files ([list key ones])
  E2E: [command] - [N] test files (if applicable)
  [NEW] files to be created during auto mode
======================================================================
COMPLETES WHEN: All tasks done + tests pass + /sw:done passes
STOPS IF: 3 consecutive test failures | /sw:cancel-auto | max turns
======================================================================
```

Fill ALL placeholders with real values. Be specific about test files and commands.

### Step 1.6: TDD Enforcement (if TDD mode enabled)

Check TDD priority: `--tdd` flag > increment `metadata.json` > `config.json`

If TDD enabled, validate tasks.md has `[RED]`/`[GREEN]`/`[REFACTOR]` markers. If no markers found:
- `strict`: BLOCK — cannot proceed, fix tasks first
- `warn`: show warning, continue without enforcement
- `off`: skip silently

Enforcement rules: `[RED]` tasks complete freely. `[GREEN]` requires its `[RED]` done first. `[REFACTOR]` requires its `[GREEN]` done first.

### Step 2: Intelligent Increment Creation (when none found)

Analyze context and decide:
- **Match existing**: find planned/backlog increment matching user intent, activate it
- **Extend existing**: add tasks to active incomplete increment
- **Create new**: invoke `/sw:increment "description"` then set up session
- **Multiple**: activate all matching, include in session marker
- **Ambiguous**: ask user to choose

Then return to Step 1c-1d to set up the session, then Step 1.5 for the banner.

### Step 3: Execute Tasks

1. Run `/sw:do` in a loop (stop hook handles continuation)
2. Mark tasks complete in tasks.md, update spec.md ACs
3. Run tests after each task
4. Before `/sw:done`: verify all quality gates from `successCriteria`
5. **Closure**: When all tasks are complete (stop hook blocks with `all_complete_needs_closure`), run `/sw:done --auto <id>` for each increment in the session
6. **On success**: If `/sw:done` succeeds, clean up session state (`rm -f` auto-mode.json, turn counter, dedup files) and output `<!-- auto-complete:DONE -->`
7. **On failure**: If `/sw:done` fails (gate failure), report the failure and do NOT clean up session state. The stop hook will block again on the next turn for a retry.

## Credential Auto-Execution

In auto mode, execute deployment commands directly using available credentials. Check `.env`, env vars, CLI auth (`wrangler whoami`, `gh auth status`). If credentials missing, ask user — never output manual steps.

## Session Management

- **Status**: `/sw:auto-status`
- **Cancel**: `/sw:cancel-auto`
- **Resume after crash**: `/sw:do` or `claude --continue`
- **Multi-agent**: use `/sw:team-lead` instead

## Safety

| Mechanism | Default |
|-----------|---------|
| Turn limit | 20 |
| Staleness cleanup | 2h |
| Human gates | `deploy`, `migrate`, `publish` patterns |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/sw:auto-status` | Check session status |
| `/sw:cancel-auto` | Cancel session |
| `/sw:do` | Execute tasks (standalone) |
| `/sw:progress` | Show progress |
| `/sw:team-lead` | Multi-agent orchestration |
