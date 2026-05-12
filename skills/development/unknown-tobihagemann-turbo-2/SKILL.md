---
name: audit
description: "Project-wide health audit pipeline that fans out to all analysis skills in parallel, evaluates findings, and produces a unified report at .turbo/audit.md. Use when the user asks to \"audit the project\", \"run a full audit\", \"project health check\", \"audit my code\", \"codebase audit\", or \"comprehensive review\"."
---

# Audit

Project-wide health audit. Fans out to all analysis skills, evaluates findings, and writes `.turbo/audit.md` and `.turbo/audit.html`. Analysis-only — does not apply fixes.

## Task Tracking

At the start, use `TaskCreate` to create a task for each phase:

1. Scope and partition
2. Threat model
3. Run analysis skills
4. Run `/evaluate-findings` skill
5. Generate markdown report
6. Generate HTML report

## Step 1: Scope and Partition

If `$ARGUMENTS` specifies paths, use those directly (skip the question).

Otherwise, use `AskUserQuestion` to confirm scope:

- **All source files** — audit everything
- **Specific paths** — user provides directories or file patterns
- **Critical paths** — heuristically identify high-risk areas (entry points, auth, data handling, payment processing)

Once scope is determined:

1. Glob for source files in the selected scope. Exclude generated and vendored directories (`node_modules/`, `dist/`, `build/`, `vendor/`, `__pycache__/`, `.build/`, `DerivedData/`, `target/`, `.tox/`, and others appropriate to the project).
2. Partition files by top-level source directory. Cap at 10 partitions. If more than 10 top-level directories exist, group related directories or use `AskUserQuestion` to narrow scope. If a single directory contains 50+ files, sub-partition it by its immediate subdirectories.

## Step 2: Threat Model

Check if `.turbo/threat-model.md` exists. If it does, continue to Step 3.

If missing, use `AskUserQuestion` to ask whether to create one before proceeding. The security review benefits from threat model context, but creating one adds time.

- **Yes** — launch an Agent tool call (`model: "opus"`, do not set `run_in_background`) whose prompt instructs it to invoke the `/create-threat-model` skill via the Skill tool. Wait for completion before continuing.
- **No** — continue without a threat model.

## Step 3: Launch All Analysis Agents

Use the Agent tool to launch all analysis agents below in a single assistant message so they run concurrently. Each Agent call uses `model: "opus"` and does not set `run_in_background`. Each Agent's prompt instructs the subagent to invoke its assigned skill via the Skill tool, with the partition's file list passed in for partitioned skills.

Expect (6 partitioned rows × number of partitions, plus 5 project-wide rows) Agent tool calls total. State the count explicitly when emitting the calls.

### Partitioned Skills

For each skill below, launch **one Agent per partition** with the partition's file list in the prompt. Pass `(skip peer review)` annotations through to `/review-code` as an opt-out so it runs internal reviews only — `/peer-review` is scheduled as its own row to avoid duplicate peer-review runs.

| Skill | Scope |
|---|---|
| `/review-code` with `correctness` (skip peer review) | File list |
| `/review-code` with `security` (skip peer review) | File list |
| `/review-code` with `api-usage` (skip peer review) | File list |
| `/review-code` with `consistency` (skip peer review) | File list |
| `/review-code` with `simplicity` (skip peer review) | File list |
| `/peer-review` | File list |

### Project-Wide Skills

| Skill | Notes |
|---|---|
| `/review-code` with `coverage` (skip peer review) | Project-wide |
| `/review-dependencies` | Project-wide |
| `/review-tooling` | Project-wide |
| `/review-agentic-setup` | Project-wide |
| `/find-dead-code` | Has its own partitioning |

## Step 4: Run `/evaluate-findings` Skill

Aggregate all findings from all agents. Run the `/evaluate-findings` skill once on the combined set.

## Step 5: Generate Markdown Report

Write `.turbo/audit.md` using the template below. Populate the dashboard by counting findings per category and applying health thresholds. Output the dashboard as text before writing the file.

### Report Template

```markdown
# Audit Report

**Date:** <date>
**Scope:** <what was audited>

## Dashboard

| Category | Health | Findings | Critical |
|---|---|---|---|
| Correctness | <Pass/Warn/Fail> | <N> | <N> |
| Security | <Pass/Warn/Fail> | <N> | <N> |
| API Usage | <Pass/Warn/Fail> | <N> | <N> |
| Consistency | <Pass/Warn/Fail> | <N> | <N> |
| Simplicity | <Pass/Warn/Fail> | <N> | <N> |
| Test Coverage | <Pass/Warn/Fail> | <N> | <N> |
| Dependencies | <Pass/Warn/Fail> | <N> | <N> |
| Tooling | <Pass/Warn/Fail> | <N> | <N> |
| Dead Code | <Pass/Warn/Fail> | <N> | <N> |
| Agentic Setup | <Pass/Warn/Fail> | <N> | <N> |
| Threat Model | <Present/Missing> | — | — |

### Health Thresholds

- **Pass** — zero P0/P1 findings in this category
- **Warn** — P1 findings present but no P0
- **Fail** — P0 findings present

## Detailed Findings

### Correctness
<findings from /review-code correctness>

### Security
<findings from /review-code security>

### API Usage
<findings from /review-code api-usage>

### Consistency
<findings from /review-code consistency>

### Simplicity
<findings from /review-code simplicity>

### Test Coverage
<findings from /review-code coverage>

### Dependencies
<findings from /review-dependencies>

### Tooling
<findings from /review-tooling>

### Dead Code
<findings from /find-dead-code>

### Agentic Setup
<findings from /review-agentic-setup>

### Threat Model
<status and summary>
```

## Step 6: Generate HTML Report

Convert the markdown report into a styled, interactive HTML page.

1. Run the `/frontend-design` skill to load design principles.
2. Read `.turbo/audit.md` for the full report content.
3. Write a self-contained `.turbo/audit.html` (single file, no external dependencies beyond Google Fonts) that presents all findings from the markdown report with:
   - Dashboard health grid with severity color-coding (red=Fail, amber=Warn, green=Pass)
   - Severity summary bar (P0/P1/P2/P3 counts)
   - Sticky navigation between report sections
   - Collapsible category sections
   - Finding tables with file, line, and description columns
   - Severity badges and color-coded group labels
   - Entrance animations and hover states
   - Print-friendly styles via `@media print`
   - Responsive layout for mobile

## Rules

- If any skill is unavailable or fails, proceed with findings from the remaining skills and note the failure in the report.
- `/peer-review` covers all concerns (correctness, security, api-usage, consistency, simplicity, coverage). Distribute its findings into their matching category sections. Deduplicate findings that overlap with the specialized reviewers.
- Does not modify source code, stage files, or commit.
