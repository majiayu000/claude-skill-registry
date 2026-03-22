---
name: team-planex
description: |
  Plan-and-execute pipeline with inverted control. Accepts issues.jsonl or roadmap
  session from roadmap-with-file. Delegates planning to issue-plan-agent (background),
  executes inline (main flow). Interleaved plan-execute loop.
---

# Team PlanEx

接收 `issues.jsonl` 或 roadmap session 作为输入，委托规划 + 内联执行。Spawn issue-plan-agent 后台规划下一个 issue，主流程内联执行当前已规划的 issue。交替循环：规划 → 执行 → 规划下一个 → 执行 → 直到所有 issue 完成。

## Architecture

```
┌────────────────────────────────────────────────────┐
│  SKILL.md (主流程 = 内联执行 + 循环控制)             │
│                                                     │
│  Phase 1: 加载 issues.jsonl / roadmap session       │
│  Phase 2: 规划-执行交替循环                          │
│    ├── 取下一个未规划 issue → spawn planner (bg)     │
│    ├── 取下一个已规划 issue → 内联执行               │
│    │   ├── 内联实现 (Read/Edit/Write/Bash)           │
│    │   ├── 验证测试 + 自修复 (max 3 retries)         │
│    │   └── git commit                                │
│    └── 循环直到所有 issue 规划+执行完毕               │
│  Phase 3: 汇总报告                                   │
└────────────────────────────────────────────────────┘

Planner (single reusable agent, background):
  issue-plan-agent spawn once → send_input per issue → write solution JSON → write .ready marker
```

## Beat Model (Interleaved Plan-Execute Loop)

```
Interleaved Loop (Phase 2, single planner reused via send_input):
═══════════════════════════════════════════════════════════════
Beat 1              Beat 2              Beat 3
|                   |                   |
spawn+plan(A)       send_input(C)       (drain)
  ↓                   ↓                   ↓
poll → A.ready      poll → B.ready      poll → C.ready
  ↓                   ↓                   ↓
exec(A)             exec(B)             exec(C)
  ↓                   ↓                   ↓
send_input(B)       send_input(done)    done
  (eager delegate)    (all delegated)
═══════════════════════════════════════════════════════════════

Planner timeline (never idle between issues):
─────────────────────────────────────────────────────────────
Planner:  ├─plan(A)─┤├─plan(B)─┤├─plan(C)─┤ done
Main:     2a(spawn) ├─exec(A)──┤├─exec(B)──┤├─exec(C)──┤
                    ^2f→send(B) ^2f→send(C)
─────────────────────────────────────────────────────────────

Single Beat Detail:
───────────────────────────────────────────────────────────────
  1. Delegate next    2. Poll ready     3. Execute     4. Verify + commit
     (2a or 2f eager)    solutions         inline         + eager delegate
        |                   |                |              |
  send_input(bg)     Glob(*.ready)    Read/Edit/Write   test → commit
                          │                              → send_input(next)
                    wait if none ready
───────────────────────────────────────────────────────────────
```

---

## Agent Registry

| Agent | Role File | Responsibility | Pattern |
|-------|-----------|----------------|---------|
| `issue-plan-agent` | `~/.codex/agents/issue-plan-agent.md` | Explore codebase + generate solutions, single instance reused via send_input | 2.3 Deep Interaction |

> **COMPACT PROTECTION**: Agent files are execution documents. When context compression occurs and agent instructions are reduced to summaries, **you MUST immediately `Read` the corresponding agent.md to reload before continuing execution**.

---

## Subagent API Reference

### spawn_agent

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/issue-plan-agent.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

${taskContext}
`
})
```

### wait

```javascript
const result = wait({
  ids: [agentId],
  timeout_ms: 600000  // 10 minutes
})
```

### send_input

Continue interaction with active agent (reuse for next issue).

```javascript
send_input({
  id: agentId,
  message: `
## NEXT ISSUE

issue_ids: ["<nextIssueId>"]

## Output Requirements
1. Generate solution for this issue
2. Write solution JSON to: <artifactsDir>/<nextIssueId>.json
3. Write ready marker to: <artifactsDir>/<nextIssueId>.ready
`
})
```

### close_agent

```javascript
close_agent({ id: agentId })
```

---

## Input

Accepts output from `roadmap-with-file` or direct `issues.jsonl` path.

Supported input forms (parse from `$ARGUMENTS`):

| Form | Detection | Example |
|------|-----------|---------|
| Roadmap session | `RMAP-` prefix or `--session` flag | `team-planex --session RMAP-auth-20260301` |
| Issues JSONL path | `.jsonl` extension | `team-planex .workflow/issues/issues.jsonl` |
| Issue IDs | `ISS-\d{8}-\d{3,6}` regex | `team-planex ISS-20260301-001 ISS-20260301-002` |

### Input Resolution

| Input Form | Resolution |
|------------|------------|
| `--session RMAP-*` | Read `.workflow/.roadmap/<sessionId>/roadmap.md` → extract issue IDs from Roadmap table → load issue data from `.workflow/issues/issues.jsonl` |
| `.jsonl` path | Read file → parse each line as JSON → collect all issues |
| Issue IDs | Use directly → fetch details via `ccw issue status <id> --json` |

### Issue Record Fields Used

| Field | Usage |
|-------|-------|
| `id` | Issue identifier for planning and execution |
| `title` | Commit message and reporting |
| `status` | Skip if already `completed` |
| `tags` | Wave ordering: `wave-1` before `wave-2` |
| `extended_context.notes.depends_on_issues` | Execution ordering |

### Wave Ordering

Issues are sorted by wave tag for execution order:

| Priority | Rule |
|----------|------|
| 1 | Lower wave number first (`wave-1` before `wave-2`) |
| 2 | Within same wave: issues without `depends_on_issues` first |
| 3 | Within same wave + no deps: original order from JSONL |

---

## Session Setup

Initialize session directory before processing:

| Item | Value |
|------|-------|
| Slug | `toSlug(<first issue title>)` truncated to 20 chars |
| Date | `YYYYMMDD` format |
| Session dir | `.workflow/.team/PEX-<slug>-<date>` |
| Solutions dir | `<sessionDir>/artifacts/solutions` |

Create directories:

```bash
mkdir -p "<sessionDir>/artifacts/solutions"
```

Write `<sessionDir>/team-session.json`:

| Field | Value |
|-------|-------|
| `session_id` | `PEX-<slug>-<date>` |
| `input_type` | `roadmap` / `jsonl` / `issue_ids` |
| `source_session` | Roadmap session ID (if applicable) |
| `issue_ids` | Array of all issue IDs to process (wave-sorted) |
| `status` | `"running"` |
| `started_at` | ISO timestamp |

---

## Phase 1: Load Issues + Initialize

1. Parse `$ARGUMENTS` to determine input form
2. Resolve issues (see Input Resolution table)
3. Filter out issues with `status: completed`
4. Sort by wave ordering
5. Collect into `<issueQueue>` (ordered list of issue IDs to process)
6. Initialize session directory and `team-session.json`
7. Set `<plannedSet>` = {} , `<executedSet>` = {} , `<plannerAgent>` = null (single reusable planner)

---

## Phase 2: Plan-Execute Loop

Interleaved loop that keeps planner agent busy at all times. Each beat: (1) delegate next issue to planner if idle, (2) poll for ready solutions, (3) execute inline, (4) after execution completes, immediately delegate next issue to planner before polling again.

### Loop Entry

Set `<queueIndex>` = 0 (pointer into `<issueQueue>`).

### 2a. Delegate Next Issue to Planner

Single planner agent is spawned once and reused via `send_input` for subsequent issues.

| Condition | Action |
|-----------|--------|
| `<plannerAgent>` is null AND `<queueIndex>` < `<issueQueue>.length` | Spawn planner (first issue), advance `<queueIndex>` |
| `<plannerAgent>` exists, idle AND `<queueIndex>` < `<issueQueue>.length` | `send_input` next issue, advance `<queueIndex>` |
| `<plannerAgent>` is busy | Skip (wait for current planning to finish) |
| `<queueIndex>` >= `<issueQueue>.length` | No more issues to plan |

**First issue — spawn planner**:

```javascript
const plannerAgent = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/issue-plan-agent.md (MUST read first)
2. Read: .workflow/project-tech.json
3. Read: .workflow/project-guidelines.json

---

issue_ids: ["<issueId>"]
project_root: "<projectRoot>"

## Output Requirements
1. Generate solution for this issue
2. Write solution JSON to: <artifactsDir>/<issueId>.json
3. Write ready marker to: <artifactsDir>/<issueId>.ready
   - Marker content: {"issue_id":"<issueId>","task_count":<task_count>,"file_count":<file_count>}

## Multi-Issue Mode
You will receive additional issues via follow-up messages. After completing each issue,
output results and wait for next instruction.
`
})
```

**Subsequent issues — send_input**:

```javascript
send_input({
  id: plannerAgent,
  message: `
## NEXT ISSUE

issue_ids: ["<nextIssueId>"]

## Output Requirements
1. Generate solution for this issue
2. Write solution JSON to: <artifactsDir>/<nextIssueId>.json
3. Write ready marker to: <artifactsDir>/<nextIssueId>.ready
   - Marker content: {"issue_id":"<nextIssueId>","task_count":<task_count>,"file_count":<file_count>}
`
})
```

Record `<planningIssueId>` = current issue ID.

### 2b. Poll for Ready Solutions

Poll `<artifactsDir>/*.ready` using Glob.

| Condition | Action |
|-----------|--------|
| New `.ready` found (not in `<executedSet>`) | Load `<issueId>.json` solution → proceed to 2c |
| `<plannerAgent>` busy, no `.ready` yet | Check planner: `wait({ ids: [<plannerAgent>], timeout_ms: 30000 })` |
| Planner finished current issue | Mark planner idle, re-poll |
| Planner timed out (30s wait) | Re-poll (planner still working) |
| No `.ready`, planner idle, all issues delegated | Exit loop → Phase 3 |
| Idle >5 minutes total | Exit loop → Phase 3 |

### 2c. Inline Execution

Main flow implements the solution directly. For each task in `solution.tasks`, ordered by `depends_on` sequence:

| Step | Action | Tool |
|------|--------|------|
| 1. Read context | Read all files referenced in current task | Read |
| 2. Identify patterns | Note imports, naming conventions, existing structure | — (inline reasoning) |
| 3. Apply changes | Modify existing files or create new files | Edit (prefer) / Write (new files) |
| 4. Build check | Run project build command if available | Bash |

Build verification:

```bash
npm run build 2>&1 || echo BUILD_FAILED
```

| Build Result | Action |
|--------------|--------|
| Success | Proceed to 2d |
| Failure | Analyze error → fix source → rebuild (max 3 retries) |
| No build command | Skip, proceed to 2d |

### 2d. Verify Tests

Detect test command:

| Priority | Detection |
|----------|-----------|
| 1 | `package.json` → `scripts.test` |
| 2 | `package.json` → `scripts.test:unit` |
| 3 | `pytest.ini` / `setup.cfg` (Python) |
| 4 | `Makefile` test target |

Run tests. If tests fail → self-repair loop:

| Attempt | Action |
|---------|--------|
| 1–3 | Analyze test output → diagnose → fix source code → re-run tests |
| After 3 | Mark issue as failed, log to `<sessionDir>/errors.json`, continue |

### 2e. Git Commit

Stage and commit changes for this issue:

```bash
git add -A
git commit -m "feat(<issueId>): <solution-title>"
```

| Outcome | Action |
|---------|--------|
| Commit succeeds | Record commit hash |
| Commit fails (nothing to commit) | Warn, continue |
| Pre-commit hook fails | Attempt fix once, then warn and continue |

### 2f. Update Status + Eagerly Delegate Next

Update issue status:

```bash
ccw issue update <issueId> --status completed
```

Add `<issueId>` to `<executedSet>`.

**Eager delegation**: Immediately check planner state and delegate next issue before returning to poll:

| Planner State | Action |
|---------------|--------|
| Idle AND more issues in queue | `send_input` next issue → advance `<queueIndex>` |
| Busy (still planning) | Skip — planner already working |
| All issues delegated | Skip — nothing to delegate |

This ensures planner is never idle between beats. Return to 2b for next beat.

---

## Phase 3: Report

### 3a. Cleanup

Close the planner agent. Ignore cleanup failures.

```javascript
if (plannerAgent) {
  try { close_agent({ id: plannerAgent }) } catch {}
}
```

### 3b. Generate Report

Update `<sessionDir>/team-session.json`:

| Field | Value |
|-------|-------|
| `status` | `"completed"` |
| `completed_at` | ISO timestamp |
| `results.total` | Total issues in queue |
| `results.completed` | Count in `<executedSet>` |
| `results.failed` | Count of failed issues |

Output summary:

```
## Pipeline Complete

**Total issues**: <total>
**Completed**: <completed>
**Failed**: <failed>

<per-issue status list>

Session: <sessionDir>
```

---

## File-Based Coordination Protocol

| File | Writer | Reader | Purpose |
|------|--------|--------|---------|
| `<artifactsDir>/<issueId>.json` | planner | main flow | Solution data |
| `<artifactsDir>/<issueId>.ready` | planner | main flow | Atomicity signal |

### Ready Marker Format

```json
{
  "issue_id": "<issueId>",
  "task_count": "<task_count>",
  "file_count": "<file_count>"
}
```

---

## Session Directory

```
.workflow/.team/PEX-<slug>-<date>/
├── team-session.json
├── artifacts/
│   └── solutions/
│       ├── <issueId>.json
│       └── <issueId>.ready
└── errors.json
```

---

## Lifecycle Management

### Timeout Protocol

| Phase | Default Timeout | On Timeout |
|-------|-----------------|------------|
| Phase 1 (Load) | 60s | Report error, stop |
| Phase 2 (Planner wait) | 600s per issue | Skip issue, write `.error` marker |
| Phase 2 (Execution) | No timeout | Self-repair up to 3 retries |
| Phase 2 (Loop idle) | 5 min total idle | Break loop → Phase 3 |

### Cleanup Protocol

At workflow end, close the planner agent:

```javascript
if (plannerAgent) {
  try { close_agent({ id: plannerAgent }) } catch { /* already closed */ }
}
```

---

## Error Handling

| Phase | Scenario | Resolution |
|-------|----------|------------|
| 1 | Invalid input (no issues, bad JSONL) | Report error, stop |
| 1 | Roadmap session not found | Report error, stop |
| 1 | Issue fetch fails | Retry once, then skip issue |
| 2 | Planner spawn fails | Retry once, then skip issue |
| 2 | issue-plan-agent timeout (>10 min) | Skip issue, write `.error` marker, continue |
| 2 | Solution file corrupt / unreadable | Skip, log to `errors.json`, continue |
| 2 | Implementation error | Self-repair up to 3 retries per task |
| 2 | Tests failing after 3 retries | Mark issue failed, log, continue |
| 2 | Git commit fails | Warn, mark completed anyway |
| 2 | Polling idle >5 minutes | Break loop → Phase 3 |
| 3 | Agent cleanup fails | Ignore |

---

## User Commands

| Command | Action |
|---------|--------|
| `check` / `status` | Show progress: planned / executing / completed / failed counts |
| `resume` / `continue` | Re-enter loop from Phase 2 |

