---
name: triage-issues
categories: [github]
description: Analyze open GitHub issues and produce a sequenced implementation plan — grouping issues into parallel batches, ordering those batches, and tagging each issue with its recipe route. Use when user says "triage issues", "prioritize issues", or "plan issue order".
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Triaging issues...'"
          once: true
---

# Issue Triage Skill

Analyze open GitHub issues, classify each into a recipe route, group them into parallel implementation batches, and produce a structured triage report.

## When to Use

- User says "triage issues", "prioritize issues", or "plan issue order"
- Before starting a multi-issue implementation sprint
- When a backlog needs sequencing into implementable batches
- As input to a pipeline that processes issues in batch order

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create or edit Python, YAML, or config files
- Guess recipe classification when confidence is low — escalate to user
- Apply GitHub labels when `--no-label` is passed
- Skip human escalation for ambiguous issues
- Add useless comments to the codebase — do not use the codebase as a notepad
- Create files outside `temp/triage-issues/` directory

**ALWAYS:**
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Pause for human input on ambiguous classifications
- Write the triage report and manifest to `temp/triage-issues/` (relative to the current working directory)
- Use `gh` CLI for all GitHub operations (not raw API calls)
- Include rationale for every recipe classification
- Record human decisions in the final report

## Workflow

### Step 0: Parse Arguments

Parse optional arguments from the user's invocation:

- `--batch-size N` — maximum issues per batch (default: 4)
- `--no-label` — skip GitHub label application after triage
- `--dry-run` — run analysis but skip label application even if `--no-label` is not set
- `--collapse` — invoke `collapse-issues` after split analysis to consolidate related issues
- `--enrich` — for each issue classified as `recipe:implementation`, generate and append
               structured requirements (`REQ-{GRP}-NNN` format) to the issue body.
               Skips issues that already have a `## Requirements` section (idempotent).
               No effect on `recipe:remediation` issues.

### Step 0.5 — Code-Index Initialization (required before any code-index tool call)

Call `set_project_path` with the repo root where this skill was invoked (not a worktree path):

```
mcp__code-index__set_project_path(path="{PROJECT_ROOT}")
```

Code-index tools require **project-relative paths**. Always use paths like:

    src/<your_package>/some_module.py

NOT absolute paths like:

    /absolute/path/to/src/<your_package>/some_module.py

> **Note:** Code-index tools (`find_files`, `search_code_advanced`, `get_file_summary`,
> `get_symbol_body`) are only available when the `code-index` MCP server is configured.
> If `set_project_path` returns an error, fall back to native `Glob` and `Grep` tools
> for the same searches — they provide equivalent results without the code-index server.

Agents launched via `run_skill` inherit no code-index state from the parent session — this
call is mandatory at the start of every headless session that uses code-index tools.

### Step 1: Authenticate and Fetch Issues

```bash
# Verify GitHub authentication
gh auth status

# Fetch all open issues with required fields, excluding in-progress issues
gh issue list --state open --json number,title,body,labels,url,assignees --limit 200 \
  | jq '[.[] | select(.labels | map(.name) | contains(["in-progress"]) | not)]'
```

Issues carrying the `in-progress` label are actively being processed by a pipeline session
and are excluded from triage to prevent duplicate work.

If `gh auth status` fails, abort with a clear error message.

If there are zero open issues (after filtering), skip to Step 7 and output an empty report.

### Step 2a: Parallel Split Analysis

Before codebase analysis, run `issue-splitter` for every open issue to detect mixed-concern issues and expand the working set.

Launch up to 8 subagents in parallel (`model: "sonnet"`), one per issue. Each subagent invokes:

```
/autoskillit:issue-splitter --issue {N} --repo {owner/repo} [--no-label if --no-label was passed] [--dry-run if --dry-run was passed]
```

For each subagent result, parse the `---issue-splitter-result---` block and build the **expanded working set**:

- `decision=no-split`: keep the original issue in the working set; note the pre-classified `route` as a seed for Step 3 (Recipe Classification) — Step 3 still re-verifies
- `decision=split`: remove the original issue from the working set; add its `sub_issues` list instead
- `decision=error`: log a warning; keep the original issue as-is (fail-safe)

Proceed to Step 2c (if `--collapse`) or Step 2b with the expanded working set.

**Flag propagation:** When `triage-issues` is invoked with `--no-label`, pass `--no-label` to each `issue-splitter` call. When `--dry-run` is active, pass `--dry-run`. This ensures split analysis is observable without mutating GitHub.

### Step 2c (optional): Collapse Related Issues

If `--collapse` was passed:

Invoke the collapse-issues skill to consolidate related issues before analysis:

```
/autoskillit:collapse-issues --repo {owner/repo} [--dry-run if --dry-run was passed] [--no-label if --no-label was passed]
```

Parse the `---collapse-issues-result---` block from the skill output:
- `groups_formed`: log "Collapsed N groups ({M} issues → {groups_formed} combined issues)"
- Update the working issue list: remove closed originals, add new combined issue numbers
- If the skill returns an error, log a warning but continue triage with the original issue list (fail-safe)

**Flag propagation:** `--dry-run` and `--no-label` are passed through to collapse-issues.

The collapse step runs after splitting is complete so it sees the fully-decomposed issue list.

### Step 2b: Parallel Issue Analysis

Launch parallel subagents (up to 8) to analyze each issue. Each subagent receives one issue and must identify:

- **Affected systems** — which parts of the codebase the issue touches (e.g., `recipe/`, `server/`, `execution/`)
- **Components** — specific modules, classes, or functions referenced or implied
- **File paths** — explicitly mentioned files or files inferred from the description
- **Dependencies** — explicit issue references (`#N`) or inferred dependencies from content overlap

Use `model: "sonnet"` for all subagents.

### Step 3: Recipe Classification

Classify each issue into a recipe route using the primary behavioral criterion — is existing behavior broken?

**Is existing behavior broken?**
- **Yes** — existing code crashes, raises an exception, returns wrong data, or fails an assertion when executed → `recipe:remediation`
- **No** — a capability is missing, a guard doesn't exist yet, a routing path was never built, or behavior needs to be added → `recipe:implementation`

The key distinction is **broken vs. missing**:
- **Remediation** fixes code that runs and errors. The code exists, it executes, and it produces a wrong result or exception.
- **Implementation** fills a gap. Nothing existing is broken — the capability, guard, or behavior simply doesn't exist yet. Even if the gap was discovered during a runtime scenario (e.g., an orchestrator made a wrong choice because no guardrail existed), if the fix is "add something new" rather than "fix something that errors", it routes to implementation.

Examples that route to `remediation`:
- A command that crashes with a traceback
- An API that returns wrong data (e.g., negative duration from clock regression)
- A file parser that raises an exception on valid input
- A test that fails with an assertion error due to a real code bug

Examples that route to `implementation`:
- Adding a new CLI flag, skill, or recipe step
- Adding a missing return field to a response JSON
- Adding orchestrator discipline rules or guardrails that don't exist yet
- A plan/recipe that scoped too narrowly (gap in design, not a crash)
- Improving error messages, refactoring, writing documentation
- Adding support for a new file format — regardless of scope or complexity

**Common misclassification: "the orchestrator did the wrong thing"**
When an LLM orchestrator bypasses routing, retries instead of escalating, or ignores a failure — that is almost always a **gap** (missing guardrail, missing discipline rule), not a runtime error. The orchestrator didn't crash; it made an unguarded choice. Route to `implementation` unless the orchestrator hit an actual exception.

For each issue, record:
- The assigned route (`implementation` or `remediation`)
- Confidence level (`high` or `low`)
- Rationale (1 sentence explaining why)

### Step 3b: Human Escalation for Ambiguous Issues

For each issue where you cannot confidently assign a recipe route, you MUST pause
and present it to the user. Do NOT silently guess.

Present each ambiguous issue as follows:

---
**Ambiguous Issue: #{number} — "{title}"**

**Summary:** {1-2 sentence summary of what the issue asks for}

**Conflicting Signals:**
- Signal A suggests `implementation`: {reason}
- Signal B suggests `remediation`: {reason}

**Decision needed:** Route to `implementation` or `remediation`? (Or type "skip" to exclude)

**Open questions that would change routing:**
- {question that, if answered, would make the route clear}
---

Wait for the user's response before continuing to the next ambiguous issue.
Record all human decisions for inclusion in the triage report.

### Step 3c: Requirement Enrichment (only when `--enrich` is passed)

For each issue in the working set classified as `recipe:implementation`:

1. Fetch issue body:
   ```bash
   gh issue view {N} --json body -q .body
   ```
2. If `## Requirements` section already present in the body: skip (idempotent).
3. In-context requirement generation using the issue title, body, and classification
   rationale already in context:
   - Trace: "What must be true for this functionality to exist?"
   - Group by co-implementation concern (short uppercase abbreviation, 2–5 letters).
   - Format: `**REQ-{GRP}-NNN:** {single-sentence condition statement}.`
4. If `--dry-run` or `--no-label` is active: print generated requirements to stdout
   per issue but skip `gh issue edit`. Record `requirements_generated: true` in manifest.
5. Otherwise, append via:
   ```bash
   gh issue edit {N} --body "$(gh issue view {N} --json body -q .body)

## Requirements

### {Group Name}

- **REQ-{GRP}-001:** ...
..."
   ```
6. If the issue is too vague for clean extraction: skip silently and record
   `requirements_generated: false` in the manifest for that issue.

This step is in-context only — no subagents are spawned for enrichment.

`recipe:remediation` issues are not enriched regardless of the `--enrich` flag.

### Step 4: Build Conflict Graph

Build a conflict graph where:
- Each issue is a node
- Two issues share an edge if they touch overlapping systems, components, or file paths
- Edge weight reflects the degree of overlap (number of shared components)

Issues that touch completely independent systems have no edges and can safely run in parallel.

### Step 5: Greedy Batch Partitioning

Partition issues into batches of at most `batch_size` using a greedy graph-coloring approach:

1. Sort issues by edge count (most conflicts first)
2. For each issue, assign it to the earliest batch where it has no conflicts with existing members
3. If all existing batches conflict, create a new batch
4. Issues with no conflicts go into the earliest batch with remaining capacity

### Step 6: Order Batches

Order the batches for sequential execution:

1. **Dependencies first** — if issue B depends on issue A, A's batch must come before B's batch
2. **Foundation first** — batches touching infrastructure/core come before batches touching consumers
3. **Priority labels** — batches containing `priority:high` issues come earlier (tiebreaker)
4. **Age** — batches containing older issues come earlier (final tiebreaker)

### Step 7: Write Outputs

Compute timestamp: `YYYY-MM-DD_HHMMSS`.
Ensure `temp/triage-issues/` exists.

**7a. Triage report:** `temp/triage-issues/triage_report_{ts}.md`

The report contains:
- Ordered list of batches with issues, recipe assignments, and rationale
- Dependency/conflict notes explaining batch separation
- Summary statistics (total issues, batch count, recipe distribution)
- Human decisions section (which issues were escalated, what was decided)

**7b. Machine-readable manifest:** `temp/triage-issues/triage_manifest_{ts}.json`

```json
{
    "generated_at": "{ISO timestamp}",
    "batch_size": 4,
    "total_issues": 12,
    "batch_count": 3,
    "recipe_distribution": {"implementation": 8, "remediation": 4},
    "batches": [
        {
            "batch": 1,
            "priority": "first",
            "issues": [
                {
                    "number": 42,
                    "title": "Add user auth",
                    "recipe": "implementation",
                    "confidence": "high",
                    "systems": ["auth", "api"],
                    "rationale": "Well-defined feature with clear acceptance criteria",
                    "requirements_generated": true
                }
            ]
        }
    ],
    "skipped_issues": [],
    "human_decisions": [
        {"number": 55, "decision": "remediation", "reason": "User chose investigation-first"}
    ]
}
```

Issues not enriched (`recipe:remediation`, or `--enrich` not passed) emit `"requirements_generated": null`.

**7c. Label application (unless `--no-label` is passed):**

Ensure recipe labels exist (idempotent):

```bash
gh label create "recipe:implementation" --description "Route through implementation recipe" --color "0E8A16" --force
gh label create "recipe:remediation" --description "Route through remediation recipe" --color "D93F0B" --force
```

For each triaged issue, apply its recipe label:

```bash
gh issue edit {number} --add-label "recipe:{recipe}"
```

## Output Location

```
temp/triage-issues/
  triage_report_{ts}.md       # Human-readable triage report
  triage_manifest_{ts}.json   # Machine-readable manifest for downstream pipelines
```

## Output Fields (for recipe capture)

After the triage report and manifest are written, emit the following structured output
tokens as the very last lines of your text output:

```
triage_report = {absolute_path_to_report_file}
triage_manifest = {absolute_path_to_manifest_file}
total_issues = {integer_count}
batch_count = {integer_count}
recipe_distribution = {json_distribution_dict}
```

These emit lines are consumed by `capture:` in orchestrating recipes. The
`triage_manifest` path is the primary output used by downstream recipe steps.

Example emit block:

```
triage_report = temp/triage-issues/triage_report_20260310_120000.md
triage_manifest = temp/triage-issues/triage_manifest_20260310_120000.json
total_issues = 12
batch_count = 3
recipe_distribution = {"implementation": 8, "remediation": 4}
```

## Related Skills

- **`/autoskillit:analyze-prs`** — Similar batch analysis pattern, but for PRs instead of issues
- **`/autoskillit:make-groups`** — Groups requirements for planning; triage-issues groups issues for execution
- **`/autoskillit:investigate`** — Can be used to deep-dive individual issues before triage