---
name: start
description: "Session initialization and lifecycle management: bootstraps session context, organizes files, generates CLAUDE.md, manages soul purpose lifecycle with completion protocol and active context harvesting. Use when user says /start, /init, bootstrap session, initialize session, or organize project."
user-invocable: true
---

# Session Init & Lifecycle Skill

> User runs `/start`. Questions upfront. Everything else silent. Then seamlessly continue working.

All session operations use `atlas-session` MCP tools directly (prefixed `session_*` and `contract_*`). Use `ToolSearch` to discover them.

## Directive Capture

Capture any text after `/start` as `DIRECTIVE`. If empty, the soul purpose is the directive.
The skill NEVER finishes with "ready to go" and stops. After setup, immediately begin working.

## UX Contract (MANDATORY)

1. **NEVER announce step names** — no "Init Step 1", no "Wave 2"
2. **NEVER narrate internal process** — no "Detecting environment..."
3. **NEVER explain what you're about to do** — just ask questions, then do it silently
4. **User sees ONLY**: questions and seamless continuation into work
5. **Batch questions** — as few rounds as possible
6. **No "done" message that stops** — after setup, immediately begin working

## Hard Invariants

1. **User authority is absolute** — AI NEVER closes a soul purpose. Only suggests; user decides.
2. **Zero unsolicited behavior** — Skill ONLY runs when user types `/start`.
3. **Human-visible memory only** — All state lives in files.
4. **Idempotent** — Safe to run multiple times.
5. **Templates are immutable** — NEVER edit bundled template files.
6. **NEVER** auto-invoke doubt agent. Only offer it.
7. **Trust separation** — for bounty verify, spawn a separate finality Task agent. Never the same agent that submits.
8. **AtlasCoin is optional** — if the service is down, tell the user and continue without bounty tracking.

## Service Availability (MANDATORY)

1. **NEVER run `claude mcp list`** — assume atlas-session is available, handle errors on first call
2. **NEVER block on external services** — log the gap and continue with degraded mode
3. **Fallback hierarchy**: try tool → if error/timeout → tell user what's degraded → continue

| Service | If Unavailable | Action |
|---------|---------------|--------|
| atlas-session MCP | `session_start` errors/times out | STOP — required for /start |
| AtlasCoin | `contract_health()` fails | Continue without bounty tracking |
| Perplexity | Research queries fail | Context7 + WebSearch fallback |
| Context7 | Doc queries fail | Perplexity results only |
| Bitwarden | Vault locked/unavailable | Tell user, skip credential fetch |

---

# INIT MODE

> Triggered when `session_start` returns `preflight.mode == "init"`.

## Step 1: Preflight + Assessment (composite)

**MCP AVAILABILITY** — assume atlas-session is available (do NOT run `claude mcp list`):

1. Call `session_start(project_dir, DIRECTIVE)` — returns combined preflight + validate + read_context + git_summary + classify_brainstorm + clutter check in ONE call.
2. If the call **errors or times out**, STOP and inform user:
   ```
   atlas-session MCP is not responding. /start requires this MCP to function.

   To fix:
   1. Check ~/.claude.json or project .mcp.json has atlas-session entry
   2. Verify Python module: python3 -c "from atlas_session import server"
   3. Restart Claude Code after fixing
   ```
   Do NOT proceed with any other steps if session_start fails.
3. Extract results: `preflight = result["preflight"]`, `read_context = result["read_context"]`, `git_summary = result["git_summary"]`, `classify_brainstorm = result["classify_brainstorm"]`, `clutter = result["clutter"]`.

## Step 2: Brainstorm Weight + File Organization

1. Extract `BRAINSTORM_WEIGHT` from `result["classify_brainstorm"]["weight"]` for Step 4.

**File organization** (only if `result["clutter"]` is present and `status` is "cluttered"):

Present the grouped move map from `result["clutter"]`:
- "Your project root has [N] misplaced files. Proposed cleanup: [summary]. Approve?"
- Options: "Yes, clean up", "Show details first", "Skip"
- If approved, execute moves via `git mv` (if `is_git`) or file operations.

## Step 3: Silent Bootstrap + CI/CD Detection

1. Call `session_init(project_dir, DIRECTIVE_OR_PENDING)`
2. Call `session_ensure_governance(project_dir)`
3. Call `session_cache_governance(project_dir)`
4. Run `/init` (Claude Code built-in — refreshes CLAUDE.md. Must run in main thread.)
5. Call `session_restore_governance(project_dir)`

**CI/CD Scaffold Detection** (smart, zero-friction):

Use `project_signals` from `result["preflight"]` (already available from Step 1).

Determine CI/CD action based on these rules:

| Condition | Action |
|-----------|--------|
| `has_ci == true` | Skip — already has CI/CD |
| `has_code_files == false` OR `is_empty_project == true` | Skip — no code to test |
| Simple script only (1-2 `.py`/`.sh` files, no package manifest) | Skip — toy project |
| Has package manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) | **Prompt user** (see below) |
| 3+ code files but no package manifest | **Prompt user** (see below) |

**Prompt when needed**:

"This project has code files but no CI/CD. Atlas-Copilot can scaffold GitHub Actions workflows (CI tests + Claude review). Enable?"

Options:
- "Yes, full CI" — scaffold both CI and review workflows
- "CI only" — scaffold CI workflow only
- "Skip" — don't scaffold, don't ask again this session

**Scaffold logic** (if user accepts):

Detect language/stack from `project_signals`:
- `has_package_json` → Node.js
- `has_pyproject` → Python
- `has_go_mod` → Go
- `has_cargo_toml` → Rust
- Default → Python if `.py` files exist, else generic

Create `.github/workflows/` directory, then:
1. **CI workflow** (`ci.yml`): calls `anombyte93/atlas-copilot/.github/workflows/reusable-ci.yml@v1` with appropriate inputs
2. **Review workflow** (`claude-review.yml`): calls `anombyte93/atlas-copilot/.github/workflows/reusable-claude-review.yml@v1`

Use language-specific defaults:
| Stack | test-command | build-command | install-command |
|-------|--------------|---------------|-----------------|
| Node.js | `npm test -- --coverage --ci` | `npm run build` | `npm ci` |
| Python | `pytest tests/ -x --tb=short` | (empty) | `pip install -e ".[dev]"` |
| Go | `go test ./... -v -race` | (empty) | `go mod download` |
| Rust | `cargo test --verbose` | `cargo build --verbose` | (empty) |

6. Read `custom.md` if it exists, follow instructions under "During Init".

## Step 4: Quick Clarify + Activate + Continuation

**Quick Clarify runs first (always)**:

Invoke `skill: "quick-clarify"` with the DIRECTIVE.
This asks 3 questions: deliverable type, done criteria, and size.
For Medium/Large tasks, it also runs research.

After brainstorm completes:

1. Call `session_activate(project_dir, DERIVED_SOUL_PURPOSE, DIRECTIVE_OR_PENDING)` — sets soul purpose, enables stop hook, and returns feature claims in ONE call.
2. Extract feature claims from the result for tracking.

**Bounty creation** (optional):

Call `contract_health()`. If healthy, call `contract_create(project_dir, DERIVED_SOUL_PURPOSE, escrow, criteria)` using `contract_draft_criteria` for suggestions.

Default escrow: 100. Increase for complex soul purposes at AI's discretion.

If AtlasCoin is down, tell user and continue without bounty.

### Before Starting Work (MANDATORY)

1. Count independent tasks in the soul purpose.
2. If 2+ independent tasks:
   - `TeamCreate("{project}-work")` — assign directory-level file ownership per teammate
   - Lead coordinates via SendMessage — does NOT implement
   - On completion: `SendMessage(type: "shutdown_request")` then `TeamDelete`
3. If single task: proceed without team.
4. NEVER spawn ad-hoc background Task agents for implementation.
5. Invoke `superpowers:test-driven-development` if soul purpose involves code.
6. Invoke `superpowers:writing-plans` if soul purpose has 3+ steps.

### Auto-Invocation of Soul Loop (MANDATORY for code tasks)

**Detect if Soul Loop should be enabled:**

1. **Check if soul purpose involves code** — Look for keywords: "implement", "build", "fix", "add", "create", "refactor", "update", "write"
2. **Determine intensity from task size** (from quick-clarify):
   - Small → `--intensity small`
   - Medium → `--intensity medium`
   - Large → `--intensity long`

3. **Configure gates from project structure**:
   ```bash
   GATES="research,deterministic"

   # Add E2E gate if tests/e2e/ exists
   if [[ -d "$PROJECT_DIR/tests/e2e" ]]; then
     GATES="$GATES,e2e"
   fi

   # Add Acceptance gate if config/trello-testing.json exists
   if [[ -f "$PROJECT_DIR/config/trello-testing.json" ]]; then
     GATES="$GATES,acceptance"
   fi
   ```

4. **Invoke Soul Loop**:
   ```
   /soul-loop "$DERIVED_SOUL_PURPOSE" --intensity $INTENSITY --gates "$GATES"
   ```

**This is automatic** — do not ask the user. Soul Loop provides the backpressure guardrails for iterative development.

### Ralph Loop Invocation (optional, for iterative work)

If iterative development is appropriate for the soul purpose, use `/ralph-loop`:

```
/ralph-loop "DERIVED_SOUL_PURPOSE" --max-iterations N --completion-promise "TEXT"
```

The user controls iterations and completion promises.

**CRITICAL**: you must call the `Skill` tool — not just mention it in text.

### Soul Loop Invocation (backpressure-enforced iteration)

Soul Loop enforces hierarchical backpressure gates on each iteration. Use for iterative development that needs quality guardrails.

| Intensity | Invocation |
|-----------|------------|
| **Small** | `/soul-loop "SOUL_PURPOSE" --intensity small` |
| **Medium** | `/soul-loop "SOUL_PURPOSE" --intensity medium` |
| **Long** | First `skill: "prd-taskmaster"`, then `/soul-loop "SOUL_PURPOSE" --intensity long` |

**Gate Hierarchy:**
- **Critical (hard block)**: Max iterations, state corruption, 10+ failures
- **Quality (soft warning)**: Test failures, feature proof failures
- **Progressive (friction)**: 5+ failures warns, 10+ hard stops
- **Agentic (allow exit)**: Completion promise matched via `<promise>` tag

**To complete**: Output `<promise>YOUR_COMPLETION_PROMISE</promise>` when done.

**CRITICAL**: Soul loop enforces backpressure. Test failures allow continued iteration with warnings. After 10 failures, hard block.

---

# RECONCILE MODE

> Triggered when `session_start` returns `preflight.mode == "reconcile"`.
>
> **UX**: Everything in Steps 1-2 is invisible to the user. First visible interaction is a question (Step 3) or seamless work continuation (Step 4).

## Step 0: Sync Previous State

Before any assessment, save the current session state so context files reflect reality:

1. Invoke `/sync` — updates all session-context files and MEMORY.md with current progress.
2. This is silent — no output shown to user.

## Step 1: Silent Assessment + Context Reality Check (composite)

**MCP AVAILABILITY** — assume atlas-session is available (do NOT run `claude mcp list`):

1. Call `session_start(project_dir, DIRECTIVE)` — returns combined assessment in one call.
2. If the call **errors or times out**, STOP and inform user (same message as Init Mode). Do NOT proceed.
3. Extract: `preflight`, `validate`, `read_context`, `git_summary`, `classify_brainstorm`, `clutter` from the result.
4. Call `session_cache_governance(project_dir)`
5. Run `/init` in main thread.
6. Call `session_restore_governance(project_dir)`
7. **Compare** `read_context` against `git_summary`: if context is stale (commits exist that aren't reflected in active context), update `session-context/CLAUDE-activeContext.md` with real progress.
8. Check capability inventory: call `session_capability_inventory(project_dir)` and check response.
   - If `cache_hit == True` and `git_changed == False`: inventory is current, skip extraction.
   - If `needs_generation == True`: inventory requires generation. The MCP tool returns `inventory_path` when ready.
9. Read `CLAUDE-capability-inventory.md` if it exists. Extract untested code, security claims, and feature claims with gaps.
10. Check bounty: if `session-context/BOUNTY_ID.txt` exists, call `contract_get_status(project_dir)`.
11. Read `custom.md` if it exists, follow instructions under "During Reconcile".

### Root Cleanup

If `result["clutter"]` is present and `status` is "cluttered", present move map to user (same flow as Init Step 2).

## Step 2: Directive + Features + Self-Assessment

**If DIRECTIVE is non-empty (3+ words) AND `status_hint` is `no_purpose`**:
- Call `session_archive(project_dir, "(pending)", DIRECTIVE)` to set soul purpose
- Skip Step 3, go to Step 4 with lightweight brainstorm

**If DIRECTIVE is non-empty (3+ words) AND soul purpose exists**:
- Skip Step 3, go to Step 4 — work on directive (overrides for this session)

**Otherwise** (no directive):

1. Call `session_features_read(project_dir)` — check feature claim status.
2. Using `read_context` + `features_read` + `git_summary`, classify:
   - `clearly_incomplete`: open tasks non-empty, active blockers, criteria not met
   - `probably_complete`: no open tasks, artifacts exist, criteria met
   - `uncertain`: mixed signals

## Step 3: User Interaction (conditional)

**If `clearly_incomplete`**: No questions. Skip to Step 4.

**If `probably_complete` or `uncertain`**:
Ask ONE question: "Soul purpose: '[text]'. [1-2 sentence assessment]. [Bounty: active/none]. What would you like to do?"
- Options: "Continue", "Verify first", "Close", "Redefine"
- **"Verify first"**: Invoke `superpowers:verification-before-completion`, fold findings into re-presented question.
- **"Close"**: Run Settlement Flow below.
- **"Redefine"**: Ask for new purpose, then run Settlement Flow with new purpose.

## Step 4: Continuation

Transition directly into work. No "session reconciled" message.

- **DIRECTIVE provided**: Begin working on directive.
- **Soul purpose redefined**: Begin working on new purpose.
- **`clearly_incomplete`**: Pick up where last session left off using active context.
- **No active soul purpose**: Ask user what to work on, set as new soul purpose via `session_archive`.

### Before Starting Work (MANDATORY)

1. Count independent tasks in the soul purpose.
2. If 2+ independent tasks:
   - `TeamCreate("{project}-work")` — assign directory-level file ownership per teammate
   - Lead coordinates via SendMessage — does NOT implement
   - On completion: `SendMessage(type: "shutdown_request")` then `TeamDelete`
3. If single task: proceed without team.
4. NEVER spawn ad-hoc background Task agents for implementation.
5. Invoke `superpowers:test-driven-development` if soul purpose involves code.
6. Invoke `superpowers:writing-plans` if soul purpose has 3+ steps.

### Ralph Loop Check (Reconcile)

Check if a Ralph Loop is already active:

```bash
test -f ~/.claude/ralph-loop.local.md && echo "active" || echo "inactive"
```

Note: Ralph Loop is no longer auto-invoked. User can manually start it with `/ralph-loop` if needed for iterative work.

---

# SETTLEMENT FLOW

> Triggered when user chooses "Close" in Reconcile Step 3.

Read `custom.md` if it exists, follow instructions under "During Settlement".

## Step 1: Harvest + Promote + Feature Verification (composite)

1. Call `session_close(project_dir)` — returns combined harvest + features_read + hook_deactivate in ONE call.
2. Extract `harvest = result["harvest"]`, `features = result["features"]`, `hook = result["hook"]`.
3. If promotable content exists in `harvest`, assess what to promote (decisions need rationale, patterns must be reusable, troubleshooting must have verified solutions). Present to user for approval.
4. After approval, append promoted content to target files via Edit tool.
5. If pending features exist in `features`, run their proofs (shell commands, file checks).
6. Update feature status in `CLAUDE-features.md`.

## Step 2: Code Review Gate

1. Invoke `superpowers:verification-before-completion` — run doubt review on recent changes.
2. If critical issues found, present to user: "Fix issues first" / "Close anyway" / "Continue working".
3. Invoke `superpowers:requesting-code-review` before PR creation.

## Step 3: PR Creation

1. Push current branch: `git push -u origin HEAD`
2. Create PR: `gh pr create --title "..." --body "..."` with review summary.
3. Return PR URL to user.

## Step 4: Bounty Settlement (if bounty exists)

1. Call `contract_run_tests(project_dir)` — execute all criteria.
2. If tests pass, call `contract_submit(project_dir)`.
3. Spawn a single finality Task agent: `Task(subagent_type: "general-purpose", prompt: "You are finality-agent. Verify bounty [ID] independently. Call contract_verify. Report pass/fail.")`
4. Wait for finality result.
5. If verified: call `contract_settle(project_dir)`. Tell user tokens earned.
6. If failed: present to user — "Fix and re-verify" / "Close anyway (forfeit)" / "Continue working".

## Step 5: Archive + Cleanup

1. Call `session_archive(project_dir, OLD_PURPOSE, NEW_PURPOSE)` — archive soul purpose, reset active context.
2. Remove Ralph Loop indicator: `rm -f ~/.claude/ralph-loop.local.md`
3. Tell user: "Session closed. Soul purpose '[text]' archived." (Include token info if bounty settled.)

---

# Customizations

> Create or edit `custom.md` in the plugin root directory.

The AI reads `custom.md` at each lifecycle phase:
- **During Init**: After session-context is bootstrapped (Step 3)
- **During Reconcile**: After read-context, before assessment (Step 1)
- **During Settlement**: Before harvest + archive (Settlement Step 1)
- **Always**: Applied in all modes
