---
name: plan
description: 'Epic decomposition into trackable issues. Triggers: "create a plan", "plan implementation", "break down into tasks", "decompose into features", "create beads issues from research", "what issues should we create", "plan out the work".'
skill_api_version: 1
metadata:
  tier: execution
  dependencies:
    - research   # optional - checks for prior research
    - beads      # optional - creates issues via bd CLI (fallback: plain markdown plan)
    - pre-mortem # optional - suggested before crank
    - crank      # optional - suggested for execution
    - implement  # optional - suggested for single issue
context:
  window: fork
  intent:
    mode: task
  intel_scope: topic
output_contract: ".agents/plans/YYYY-MM-DD-*.md, beads (via bd create)"
---

# Plan Skill

> **Quick Ref:** Decompose goal into trackable issues with waves. Output: `.agents/plans/*.md` + bd issues.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

**CLI dependencies:** bd (issue creation). If bd is unavailable, write the plan to `.agents/plans/` as markdown with issue descriptions, and use TaskList for tracking instead. The plan document is always created regardless of bd availability.

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--auto` | off | Skip human approval gate. Used by `/rpi --auto` for fully autonomous lifecycle. |
| `--fast-path` | off | Force Minimal detail template (see Step 3.2) |
| `--skip-symbol-check` | off | Skip symbol verification in Step 3.6 (for greenfield plans) |
| `--skip-audit-gate` | off | Skip baseline audit gate in Step 6 (for documentation-only plans) |

## Execution Steps

Given `/plan <goal> [--auto]`:

### Step 0: Bead-Input Pre-Flight (Stale-Scope Gate)

When the input to `/plan` is a bead ID (matches pattern `[a-z]{2,6}-[0-9a-z.]+`) AND **any** of the following conditions hold, automatically run `ao beads verify <bead-id>` as the **very first action** before any other planning step:

- complexity is `"full"`
- the bead is older than 7 days
- the bead description was filed by a prior session (e.g., handoff-sourced, deferred, or reopened)

```bash
# Example guard — run before Step 1
if [[ "$INPUT" =~ ^[a-z]{2,6}-[0-9a-z.]+$ ]]; then
    ao beads verify "$INPUT" || true
fi
```

If `ao beads verify` reports any STALE citations, present them to the user (or log them to the execution packet in `--auto` mode) and ask for scope re-validation before proceeding to Step 1. Do not decompose against stale evidence.

This implements the shared stale-scope validation rule — re-validate inherited scope estimates against HEAD before acting on deferred beads, handoff docs, or prior-session plans.

### Step 1: Setup
```bash
mkdir -p .agents/plans
```

### Step 2: Check for Prior Research + Knowledge Flywheel

`ls -la .agents/research/` and use Grep to find prior research. If found, read it before planning.

Then run `ao search` / `ao lookup` for prior planning patterns and **apply** (not just retrieve) any relevant learnings as planning constraints. Record citations with `ao metrics cite --type applied|retrieved`.

Read [references/pre-decomposition.md](references/pre-decomposition.md) for full flywheel-search commands, the apply-retrieved-knowledge contract, and section-evidence handling.

### Step 2.1: Load Compiled Prevention First (Mandatory)

Load compiled planning rules from `.agents/planning-rules/*.md` (primary) and fall back to `.agents/findings/registry.jsonl`. Match by finding ID, `applicable_when`, language, literal goal-text overlap, and changed-file overlap. Cap at top 5.

Record applied finding IDs and how they changed the plan. Fail open on missing/malformed files. Read [references/pre-decomposition.md](references/pre-decomposition.md) for the full ranked-packet contract.

Active findings from `.agents/findings/registry.jsonl` are a fallback planning input. Every written plan must include an `Applied findings:` line, even when the value is `none`.

### Step 2.2: Read and Validate Research Content

If research files exist, read the most recent one and verify it contains substantive sections (Summary, Findings, Architecture, Executive Summary, Recommendations) before proceeding. See [references/pre-decomposition.md](references/pre-decomposition.md) for the validation grep and warning behavior.

### Step 3: Explore the Codebase (if needed)

Dispatch an Explore sub-agent (Task tool) with a prompt that demands symbol-level detail: file inventory, function/method signatures, struct/type definitions, reuse points with `file:line`, test file locations and naming conventions, import paths. Read [references/pre-decomposition.md](references/pre-decomposition.md) for the canonical explore prompt.

#### Pre-Planning Baseline Audit (Mandatory)

Before decomposing, run grep/wc/ls commands to quantify files to change, sections to add/remove, LOC to modify, coverage gaps. Record commands alongside results. File size limits (800-line SKILL.md lint limit) and test fixture counts are mandatory checks. Ground truth with numbers prevents scope creep.

Read [references/pre-decomposition.md](references/pre-decomposition.md) for the bad/good examples table and the full audit recipe.

### Step 3.2: Scale Detail by Complexity

Auto-select plan detail level based on issue count and goal complexity:

| Level | Criteria | Template | Description |
|-------|----------|----------|-------------|
| **Minimal** | 1-2 issues, fast complexity | Bullet points per issue | Title, 2-line description, acceptance criteria, files list |
| **Standard** | 3-6 issues, standard complexity | Current plan format | Full implementation specs, tests, verification |
| **Deep** | 7+ issues, full complexity, or `--deep` | Extended format | Symbol-level specs, data transformation tables, design briefs, cross-wave registry |

Read [references/detail-templates.md](references/detail-templates.md) for the template definitions.

**Override:** `--deep` forces Deep regardless of issue count. `--fast-path` forces Minimal.

### Step 3.5: Generate Implementation Detail (Mandatory)

After exploring the codebase, generate symbol-level implementation detail for EVERY file in the plan. A worker reading the plan should know exactly what to write without rediscovering function names, parameters, or code locations.

Read [references/implementation-detail.md](references/implementation-detail.md) for the full contract: file inventory table, per-section implementation specs (function signatures, reuse points, inline code blocks, struct fields, CLI flag definitions), named test functions with pyramid levels, verification procedures, data transformation mapping tables, and symbol verification.

### Step 3.6: Symbol Verification (Mandatory)

See the **Symbol Verification** section in [references/implementation-detail.md](references/implementation-detail.md). For each symbol cited in the plan, grep the codebase to verify it exists. If >20% of cited symbols are stale, WARN (do not block) and log them under `## Stale Symbol Warnings`. Opt-out: `--skip-symbol-check`.

### Step 4: Decompose into Issues

Analyze the goal and break it into discrete, implementable issues. For each issue define:
- **Title**: Clear action verb (e.g., "Add authentication middleware")
- **Description**: What needs to be done
- **Dependencies**: Which issues must complete first (if any)
- **Acceptance criteria**: How to verify it's done
- **Test levels**: Which pyramid levels (L0–L3) this issue's tests cover

Read [references/decomposition.md](references/decomposition.md) for: anti-pattern pre-flight, design briefs for rewrites, issue granularity rules, operationalization heuristics, conformance checks, and schema strictness pre-flight.

### Step 5: Compute Waves

Group issues by dependencies for parallel execution:
- **Wave 1**: Issues with no dependencies (can run in parallel)
- **Wave 2**: Issues depending only on Wave 1
- **Wave 3**: Issues depending on Wave 2
- Continue until all issues assigned

**Planning Rules Compliance (Mandatory Gate):** After computing waves, fill in the Planning Rules Compliance checklist (PR-001 through PR-007) in the plan document — see the table in [references/plan-document-template.md](references/plan-document-template.md). Read [references/planning-rules.md](references/planning-rules.md) for detection questions and evidence. Every rule MUST have an explicit justification or N/A rationale. If any row has an empty Justification column, mark the plan output as **INCOMPLETE** and do not proceed to Step 6.

Read [references/wave-matrices.md](references/wave-matrices.md) for the **mandatory** file-level dependency matrix, cross-wave shared file registry, and dependency-necessity validation rules.

### Step 6: Write Plan Document

**Write to:** `.agents/plans/YYYY-MM-DD-<goal-slug>.md`

Read [references/plan-document-template.md](references/plan-document-template.md) for the full canonical template (Context, Files to Modify, Boundaries, Baseline Audit, Implementation, Tests, Conformance Checks, Verification, Issues, Execution Order, Planning Rules Compliance, Post-Merge Cleanup, Next Steps) and the **Baseline Audit Gate** (BLOCK if missing, WARN if incomplete, `--skip-audit-gate` to opt out).

### Step 7: Create Tasks for In-Session Tracking

Read [references/task-creation.md](references/task-creation.md) for the full TaskCreate + beads creation workflow, including: persistent beads issues for ratchet tracking, embedding conformance checks as fenced `validation` blocks in issue bodies, cross-cutting constraint injection on the epic, wave formation via `blocks` dependencies, and the **Step 7b post-creation validation-block verification** gate.

### Step 8: Request Human Approval (Gate 2)

**Skip this step if `--auto` flag is set.** In auto mode, proceed directly to Step 9.

**USE AskUserQuestion tool:**

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Plan complete with N tasks in M waves. Approve to proceed?"
      header: "Gate 2"
      options:
        - label: "Approve"
          description: "Proceed to /pre-mortem or /crank"
        - label: "Revise"
          description: "Modify the plan before proceeding"
        - label: "Back to Research"
          description: "Need more research before planning"
      multiSelect: false
```

**Wait for approval before reporting completion.**

### Step 9: Record Ratchet Progress

```bash
ao ratchet record plan 2>/dev/null || true
```

### Step 10: Report to User

Tell the user:
1. Plan document location
2. Number of issues identified
3. Wave structure for parallel execution
4. Tasks created (beads issue IDs or file-backed task refs)
5. Next step: `/pre-mortem` for failure simulation, then `/crank` for execution

## Key Rules

- **Read research first** if it exists
- **Explore codebase** to understand current state
- **Identify dependencies** between issues
- **Compute waves** for parallel execution
- **Always write the plan** to `.agents/plans/`

## Examples

**`/plan "add user authentication"`** — Reads research, decomposes into 5 issues (middleware, session store, token validation, tests, docs), creates epic with 2 waves, writes plan to `.agents/plans/`.

**`/plan --auto "refactor payment module"`** — Skips approval gates, creates 3-wave/8-issue epic autonomously, ready for `/crank`.

**`/plan "remove dead code"`** — Runs quantitative audit (3,003 LOC), creates issues with exact file/LOC targets, includes deletion verification checks.

**`/plan "add stale run detection to RPI status"`** — Symbol-level detail: names exact functions, struct fields, JSON tags, test names. Implementer executes in a single pass.

See [references/examples.md](references/examples.md) for full walkthroughs.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| bd create fails | Run `bd init --prefix <prefix>` first |
| Plan too large (>20 issues) | Narrow goal or split into multiple epics |
| Wave structure incorrect | Review dependencies: does blocked issue modify blocker's files? |
| Conformance checks missing | Add `files_exist`, `content_check`, `tests`, or `command` checks |

See [references/examples.md](references/examples.md) for more troubleshooting scenarios.

## Reference Documents

- [references/planning-rules.md](references/planning-rules.md) — seven compiled planning rules (mechanical enforcement, external validation, feedback loops, separation, process gates, cross-layer consistency, phased rollout).
- Shared stale-scope validation rule — re-validate inherited scope estimates against HEAD before acting on deferred beads, handoff docs, or prior-session plans. Invoked by Step 0 via `ao beads verify`.
- [references/implementation-detail.md](references/implementation-detail.md) — symbol-level implementation specs, test pyramid classification, verification procedures, data transformation tables, symbol verification.
- [references/decomposition.md](references/decomposition.md) — anti-pattern pre-flight, design briefs, issue granularity, conformance checks, schema strictness.
- [references/wave-matrices.md](references/wave-matrices.md) — file-conflict matrix, cross-wave shared file registry, dependency-necessity validation.
- [references/plan-document-template.md](references/plan-document-template.md) — canonical `.agents/plans/*.md` document template with baseline audit gate.
- [references/task-creation.md](references/task-creation.md) — TaskCreate/beads creation, validation-block embedding, post-creation verification.
- [references/plan-mutations.md](references/plan-mutations.md)
- [references/complexity-estimation.md](references/complexity-estimation.md)
- [references/detail-templates.md](references/detail-templates.md)
- [references/examples.md](references/examples.md)
- [references/sdd-patterns.md](references/sdd-patterns.md)
- [references/templates.md](references/templates.md)
