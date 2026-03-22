---
name: project-orchestrator:test-lead
description: "Orchestrates browser test execution — serial agent spawning, result collection, living state doc updates."
user-invocable: false
---

# Test Lead

Orchestrate browser test execution from a design doc's `## Test Plan` section. Spawn test-executor agents one at a time, collect results, update the living state doc, and present a summary.

## 1. Parse Config

Read `.project-orchestrator/project.yml` (use defaults if missing):

| Key | Default | Validation |
|-----|---------|------------|
| `test.model` | `sonnet` | Must be `haiku`, `sonnet`, or `opus` — error otherwise |
| `test.screenshot_on_failure` | `true` | Must be boolean — error otherwise |
| `test.base_url` | `null` | If set, must be a valid URL string — warn if not reachable |

If validation fails, report the error and stop.

## 2. Find & Parse Design Doc

Resolution order:
1. If plan file path provided in `$ARGUMENTS`, use it
2. Otherwise, check `{config.plans_dir}/INDEX.md` for active plans
3. Otherwise, glob for `{config.plans_dir}/*-design.md`

**No design doc found:** "No design doc found. Nothing to test."

**No `## Test Plan` section:** "No test plan found in design doc. Add a Test Plan section first."

Extract from the test plan:
- Base URL from `### App Context`
- Setup steps from `### Prerequisites`
- Scenario table from `### Test Scenarios`
- Scenario details from `### Scenario Details`
- Dependencies between scenarios (from Precondition column)

## 3. Pre-flight Validation

All checks must pass before creating the team. If any fail, abort — no cleanup needed.

1. **MCP check** — attempt `list_pages` via Chrome DevTools MCP.
   - If fails: "Chrome DevTools MCP is not available. Please ensure Chrome is running with DevTools MCP configured, then try again." Abort.

2. **Base URL** — use `test.base_url` from config as default, or base URL from test plan.
   - Ask user to confirm the URL is accessible.
   - If user says it's not accessible, abort.

3. **Setup steps** — present any setup steps from `### Prerequisites` and ask user to confirm they're done.

## 4. Write State File

Write `.project-orchestrator/state.json` (atomic: write `.tmp` then `mv`):

```json
{
  "active_plan": "{relative path to design doc}",
  "slug": "{feature slug}",
  "team": "test-{slug}",
  "phase": "testing",
  "started": "{ISO 8601 timestamp}"
}
```

Ensure `.project-orchestrator/` directory exists before writing. If write fails, report error and exit.

## 5. Create Team

```
TeamCreate("test-{slug}")
```

If TeamCreate fails: delete `.project-orchestrator/state.json`, report error, exit.

## 6. Create Screenshot Directory

Ensure `.project-orchestrator/screenshots/{slug}/` exists:

```bash
mkdir -p .project-orchestrator/screenshots/{slug}/
```

## 7. Execute Scenarios Sequentially

1. **Create tasks** — `TaskCreate` for every scenario in table order (T1, T2, T3, ...). Include scenario title, steps, expected outcomes, and preconditions in each task description.

2. **For each scenario, one at a time:**

   a. **Dependency check** — if the scenario depends on a prior scenario that failed, mark it as `skipped` (reason: "dependency T{N} failed"). Do NOT spawn an agent. Update the living state doc and continue to the next scenario.

   b. **Spawn test-executor agent:**
      ```
      Task(
        subagent_type: "test-executor",
        model: config.test.model,
        team_name: "test-{slug}",
        name: "test-{scenario-slug}"
      )
      ```
      Prompt must include:
      - Scenario number and title
      - Full scenario details (steps + expected outcomes)
      - Living state doc path
      - Base URL
      - `config.test.screenshot_on_failure` value
      - Screenshot directory path: `.project-orchestrator/screenshots/{slug}/`

   c. **Wait for agent to complete or go idle.**

   d. **Collect result** from TaskUpdate metadata:
      ```
      {
        result: "pass" | "fail",
        steps_total: N,
        steps_passed: N,
        failure_step: "Step 2 — ..." | null,
        failure_reason: "..." | null,
        screenshot_path: "..." | null
      }
      ```

   e. **Update living state doc** — mark scenario status and result in the test plan table.

   f. **Shutdown the agent** before spawning the next one.

## 8. Idle Detection

When an agent goes idle without a completion report:

**If `--no-auto-resume` flag is set:** Immediately escalate to user. Do not attempt auto-recovery.

**Otherwise:**

Classify using observable signals:

- **NO_REPORT** — no TaskUpdate and no messages from the agent.
  → Resume with: "Execute the test scenario now. Take a snapshot first to see the current page state."

- **STALLED** — agent sent an error message but went idle without resolving.
  → Resume with the quoted error + "Try an alternative approach or report the failure."

**Progress signals:** Agents send `SendMessage` after each major step (setup complete, each step executed, asserting outcomes). Use these to classify idle state.

**Escalation:** After 2 failed resume attempts (no progress between attempts), escalate to user:
"Test scenario T{N} agent is stuck after 2 resume attempts. Last known state: {agent's last message or 'no messages'}. How to proceed?"

## 9. Update Living State Doc

After all scenarios complete (or are skipped), append a new `### Run:` entry to the `## Test Results` section. Create the section if it doesn't exist.

Format:

```markdown
### Run: {YYYY-MM-DD HH:MM}
**Base URL:** {url}
**Execution:** serial (1 agent at a time)
**Overall:** {X passed, Y failed, Z skipped} / {total}

| # | Scenario | Result | Notes |
|---|----------|--------|-------|
| T1 | {title} | Pass | — |
| T2 | {title} | Fail | {brief reason} |
| T3 | {title} | Skipped | dependency T2 failed |

### Failure Details
#### T2 — {title}
- **Step failed:** {step description}
- **Expected:** {what was expected}
- **Actual:** {what happened}
- **Screenshot:** {path or "N/A"}
```

Previous run entries are preserved — always append, never overwrite.

## 10. Cleanup

1. `TeamDelete("test-{slug}")`
2. Delete `.project-orchestrator/state.json`
3. No scope file to clean up (test agents are read-only)

## 11. Present Summary

Format:

```
Test Results: {X passed, Y failed, Z skipped} / {total}

{If failures, list each with scenario title + brief reason}
{If screenshots captured, list paths}
```

Next steps based on results:
- **All passed:** "All tests passed. Next: `/project:verify` then `/project:finish`"
- **Some failed:** "{X} tests failed. Review failures above, fix issues, and re-run `/project:test`"
- **All skipped:** "All tests were skipped due to dependency failures. Fix the root failure and re-run."
