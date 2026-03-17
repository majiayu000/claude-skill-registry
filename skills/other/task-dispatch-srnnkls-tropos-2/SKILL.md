---
name: task-dispatch
description: Subagent-driven task execution with TDD workflow. Dispatches tester subagent (writes failing tests) then implementer subagent (makes tests pass), with batch review.
---

# Subagent-Driven Task Execution

Execute specs with proper TDD: tester writes failing tests, implementer makes them pass, reviewers validate.

**Core principle:** Three-phase batches with fresh subagents. No batch completes without review.

---

## When to Use

**Use when:**
- Executing an implementation spec (created with `spec-create`)
- Tasks are mostly independent
- Want TDD enforcement with quality gates

**Don't use when:**
- No spec exists yet (use `spec-validate` → `spec-create` first)
- Tasks are tightly coupled (manual execution better)
- Single small task (just do it directly)
- Initiative spec has failed gates (resolve first via /clarify)

---

## The Three-Phase Pipeline

Each batch executes three phases. **A batch is NOT complete until all three phases finish.**

```
┌─────────────────────────────────────────────────────────────────┐
│                         BATCH N                                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase A: TESTERS (parallel)                                    │
│  ├── Dispatch N task-tester subagents (opus)                    │
│  ├── Each writes failing tests (RED)                            │
│  └── Wait for ALL testers                                       │
│                          ↓                                      │
│  Phase B: IMPLEMENTERS (parallel)                               │
│  ├── Dispatch N task-implementer subagents (opus)               │
│  ├── Each receives its tester's report                          │
│  ├── Each makes tests pass (GREEN)                              │
│  └── Wait for ALL implementers                                  │
│                          ↓                                      │
│  Phase C: REVIEWERS (parallel)                                  │
│  ├── Dispatch 1 native Claude reviewer (opus) [required]        │
│  ├── Dispatch 0-N OpenCode reviewers (from validation.yaml)     │
│  ├── Each reviews ALL changes from batch                        │
│  ├── Wait for ALL reviewers                                     │
│  └── Synthesize feedback                                        │
│                          ↓                                      │
│  Gate: Issues found?                                            │
│  ├── Critical/High → Fix before proceeding                      │
│  └── None/Medium → Commit and continue                          │
└─────────────────────────────────────────────────────────────────┘
```

**CRITICAL:** All three phases are mandatory. Reviewers are not optional.

---

## Workflow

### 1. Load Spec and Populate TodoWrite

1. Find most recent spec in `./specs/active/*/`
2. Read `tasks.yaml` from that directory
3. Parse tasks with `status: pending` or `status: in_progress`
4. Create TodoWrite with ALL uncompleted tasks:
   - First uncompleted task: "in_progress"
   - Others: "pending"
   - content: task text
   - activeForm: present continuous form

**CRITICAL:** Always populate TodoWrite before dispatching any subagents.

5. **Create/checkout spec branch:**
   - Branch name: `feat/<spec-directory-name>`
   - If branch exists, checkout and pull
   - If not, create from main/master

### 2. Pre-Implementation Gate Check

Before dispatching any tasks, verify validation.yaml gates:

1. Read `validation.yaml` from spec directory
2. Check `metadata.issue_type`
3. **If Initiative:**
   - Check all gates in `gates` section
   - If any gate has `status: failed`:
     - Report which gates failed with reasons
     - Prompt: "Resolve via /clarify or proceed anyway?"
     - If user chooses to proceed: document override in validation.yaml
   - Check `markers` section for `status: open`
   - If blocking markers exist:
     - Report marker count and summaries
     - Prompt: "Resolve markers first or proceed?"
4. **If Feature/Task:** Skip gate check (gates marked n/a)

### 3. Analyze Task Dependencies

Parse `dependencies.yaml` to identify execution batches:

**Dependency rules:**
- Tasks in Phase N depend on Phase N-1 completion
- Tasks with `[P]` marker AND different file paths can run in parallel
- Tasks with same file path must run sequentially
- Phase boundaries force batch breaks

### 4. Execute Batches (Three-Phase Pipeline)

**For each batch, execute ALL THREE phases:**

#### Phase A: Dispatch Testers

**Single task:**
```
Dispatch 1 task-tester (opus) → wait for completion
```

**Parallel batch (N tasks):**
```
Dispatch N task-testers in SINGLE message → wait for ALL
```

Each tester:
- Invokes `code-test` skill
- Writes failing tests (RED)
- Reports: test paths, failure output

#### Phase B: Dispatch Implementers

**Single task:**
```
Dispatch 1 task-implementer (opus) with tester report → wait for completion
```

**Parallel batch (N tasks):**
```
Dispatch N task-implementers in SINGLE message → wait for ALL
Each receives its corresponding tester's report
```

Each implementer:
- Invokes `code-implement` skill
- Makes tests pass (GREEN)
- Reports: impl files, test pass output

#### Phase C: Dispatch Reviewers

**CRITICAL:** Reviewers are mandatory. Every batch gets reviewed.

**Get batch diff before dispatching:**
```bash
# Diff of changes made in this batch (since last batch commit)
git diff <last_batch_commit>..HEAD
```

**Always dispatch ALL reviewers in a SINGLE message for true parallelism:**

```
Dispatch:
  - 1 native Claude reviewer (task-reviewer, opus) [required]
  - 0-N OpenCode reviewers (models from validation.yaml)
→ Wait for ALL reviewers
```

Each reviewer:
- Invokes `code-review --diff` (batch diff, not full files)
- Reviews the diff of changes from this batch
- Checks against spec requirements for batch tasks
- Produces YAML report with issues by severity

**Review prompt includes:**
1. Git diff of batch changes (not full files)
2. Implementer reports (what was done)
3. Task specs from tasks.yaml (what was required)

**Reviewer dispatch configuration:**

**CRITICAL:** Dispatch ALL reviewers in a SINGLE message for true parallelism.

```
# Single message with multiple tool calls:

# 1. Native Claude reviewer (Task tool) [required]
Task(
  subagent_type="task-reviewer",
  model={claude_model},  # from review_config (opus)
  prompt=review_prompt   # includes: batch diff + implementer reports + task specs
)

# 2. OpenCode reviewers (Bash tool, background) [from validation.yaml]
Bash(run_in_background=true):
  timeout 1200 opencode run --model "openai/gpt-5.2-codex" --variant {reasoning_effort}-medium "{review_prompt}"

Bash(run_in_background=true):
  timeout 1200 opencode run --model "google/gemini-3-pro-preview" --variant {reasoning_effort}-medium "{review_prompt}"
```

All models and reasoning effort are configured in `validation.yaml` under `review_config`.

### 5. Synthesize Review Feedback and Write review.yaml

After ALL reviewers complete:

1. **Parse reports** - Extract YAML from all reviewer outputs
2. **Merge issues:**
   - Deduplicate by description similarity
   - Combine issues flagged by multiple reviewers (higher confidence)
   - Note which reviewer(s) found each issue
3. **Aggregate severity:**
   - Issue severity is the HIGHEST across all reviewers
   - Critical by any reviewer = Critical overall
4. **Write review.yaml** (append batch review):
   ```yaml
   # ./specs/active/<spec>/review.yaml
   batch_reviews:
     - batch: <N>
       timestamp: <ISO_TIMESTAMP>
       commit: <SHA>
       tasks: [T001, T002]
       reviewers:
         - id: claude-opus
           status: completed
           gates: { correctness: pass, style: pass, ... }
         - id: opencode-codex
           status: completed | timeout | failed
           gates: { ... }
       synthesized:
         gates: { correctness: pass, style: fail, ... }
         critical_issues: <N>
         high_issues: <N>
         medium_issues: <N>
       outcome: approved | changes_requested
   issues:
     critical: [...]
     high: [...]
     medium: [...]
   deferred_issues: [...]  # medium severity
   ```
5. **Present unified feedback:**
   - Gate summary table
   - Issues grouped by severity
   - Show which reviewers found each issue

**Gate Summary Table:**

```
| Gate         | Claude | Codex  | Gemini |
|--------------|--------|--------|--------|
| Correctness  | pass   | fail   | pass   |
| Style        | pass   | pass   | pass   |
| Performance  | pass   | pass   | pass   |
| Security     | fail   | pass   | fail   |
| Architecture | pass   | pass   | pass   |
```

### 6. Apply Review Feedback

**If Critical/High issues found:**
1. Dispatch fix subagent(s) (task-implementer, opus)
2. Verify fixes with targeted review
3. Update review.yaml with resolution
4. Only proceed when issues resolved

**If only Medium issues:**
1. Add to review.yaml deferred_issues
2. Proceed to commit

### 7. Commit, Checkpoint, and Continue

When batch completes successfully (all phases, review passed):

1. Update TodoWrite (mark tasks as "completed")
2. Edit tasks.yaml: Change `status: in_progress` to `status: completed`
3. **Write checkpoint.yaml** (enables session recovery):
   ```yaml
   checkpoint:
     spec_name: <spec>
     spec_path: ./specs/active/<spec>
     branch: feat/<spec>
     timestamp: <ISO_TIMESTAMP>
     last_batch: <N>
     last_commit: <SHA>
     tasks:
       completed: [...]
       pending: [...]
     next_batch:
       number: <N+1>
       tasks: [...]
     deferred_issues: [...]  # medium severity, noted for later
     review_config:
       reviewers: [...]  # from validation.yaml
   ```
4. **Commit the batch changes:**
   - Stage: implementation + tests + tasks.yaml + checkpoint.yaml + review.yaml
   - Commit message format:
     ```
     <type>(<scope>): <description>

     Tasks: <task-ids>
     Batch: <N>/<total>
     ```
   - Example: `feat(cache): add TTL expiry\n\nTasks: PH2-003, PH2-004\nBatch: 2/5`
5. Move to next batch (or use `/continue` in new session)

### 8. Final Review

After ALL batches complete, invoke `code-review` skill in **final mode**:

```
/code.review --final <spec-name>
```

Or dispatch multi-reviewer pass directly:

```
Dispatch (in same message):
  - 1 native Claude reviewer (opus) [required]
  - 0-N OpenCode reviewers (from validation.yaml)
```

**Final review checks:**
- All spec requirements met (cross-reference spec.md)
- All tasks complete (verify tasks.yaml)
- Acceptance criteria satisfied
- Overall architecture sound
- Deferred issues addressed or documented
- Tests passing

**Write final_review section in review.yaml:**
```yaml
final_review:
  status: completed
  timestamp: <ISO_TIMESTAMP>
  reviewers: [claude-opus, opencode-codex, ...]
  gates: { correctness: pass, style: pass, ... }
  spec_compliance:
    all_tasks_complete: true
    acceptance_criteria_met: true
    edge_cases_handled: true
  issues: [...]
  strengths: [...]
  overall_assessment: "Implementation complete and verified"
  recommendation: ready_to_merge | changes_requested
readiness:
  all_batches_reviewed: true
  critical_issues_resolved: true
  high_issues_resolved: true
  final_review_passed: true
  tests_passing: true
```

---

## Subagent Configuration

| Role | Subagent Type | Model | Skill |
|------|---------------|-------|-------|
| Tester | task-tester | opus | code-test |
| Implementer | task-implementer | opus | code-implement |
| Reviewer | task-reviewer | from review_config (opus) | code-review |

**CRITICAL:** Always specify `model: opus` for testers, implementers, and reviewers.

---

## Quality Gates

| Gate | When | Action if Failed |
|------|------|------------------|
| Pre-impl gate | Before any dispatch | Block if Initiative gates failed |
| RED verification | After tester | Verify tests actually fail |
| GREEN verification | After implementer | Verify tests pass |
| **Batch review** | **After all implementers** | **Fix before next batch** |
| Final review | After all batches | Address gaps |

---

## Red Flags

**Never:**
- Skip the tester phase (implementer must receive failing tests)
- **Skip the reviewer phase (every batch must be reviewed)**
- Use sonnet for subagents (always opus)
- Dispatch parallel subagents on same file
- Let implementer write tests (tester's job)
- Ignore failed pre-impl gates for Initiatives
- Batch commits across multiple batches

**If tester can't write tests:**
- Don't skip to implementer
- Handle the gap (consult spec, ask user)
- Re-dispatch tester with clarification

**If reviewers timeout:**
- Continue with available reviews (minimum 1)
- Note partial results in output
- Consider re-running batch

---

## Example Workflow

```
[Load spec, create TodoWrite, checkout branch]

Batch 1: Task 1 (single task)
├── Phase A: Dispatch tester (opus)
│   └── Tester: Wrote 3 tests, all failing (RED)
├── Phase B: Dispatch implementer (opus) + tester report
│   └── Implementer: Made tests pass (GREEN)
├── Phase C: Dispatch reviewers (3 in parallel)
│   ├── Claude: approved, no issues
│   ├── Codex: approved, 1 minor issue
│   └── Gemini: approved, no issues
├── Synthesize: 1 minor issue (note for later)
└── Commit: feat(cache): add caching layer

Batch 2: Tasks 2, 3, 4 ([P] parallel batch)
├── Phase A: Dispatch 3 testers (single message)
│   └── All testers complete with failing tests
├── Phase B: Dispatch 3 implementers (single message)
│   └── All implementers complete, tests passing
├── Phase C: Dispatch reviewers (3 in parallel)
│   ├── Claude: changes_requested, 1 critical
│   ├── Codex: changes_requested, 1 critical (same issue)
│   └── Gemini: approved
├── Synthesize: 1 critical issue (found by 2 reviewers)
├── Fix: Dispatch fix subagent → verify
└── Commit: feat(api): add endpoints for tasks 2, 3, 4

...

[Final review - 3 reviewers in parallel]
All requirements met
```

---

## Integration

**Use with:**
- `spec-validate` → `spec-create` - Create spec before dispatch
- `clarify` - Resolve markers/gates before dispatch
- `code-test` - Tester invokes for TDD methodology
- `code-implement` - Implementer invokes for language guidelines
- `code-review` - Reviewer invokes for review methodology
- `task-completion-verify` - Verify before claiming done

---

## Reference

- [subagent-workflow.md](reference/subagent-workflow.md) - Dispatch templates and YAML reports
- [report.md](reference/report.md) - YAML report schemas
- [checkpoint-format.md](reference/checkpoint-format.md) - Session checkpoint schema
- [review.md](reference/review.md) - Implementation review schema (review.yaml)
- [roles/tester.md](reference/roles/tester.md) - Test-writing subagent
- [roles/implementer.md](reference/roles/implementer.md) - Implementation subagent
- [roles/reviewer.md](reference/roles/reviewer.md) - Review subagent
