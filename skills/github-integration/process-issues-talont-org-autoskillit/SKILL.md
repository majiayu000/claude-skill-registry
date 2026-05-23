---
name: process-issues
description: Execute recipe sessions batch-by-batch for triaged GitHub issues. Reads the triage-issues output manifest, processes each batch sequentially, and launches the appropriate recipe for each issue. Use when user says "process issues", "run issues", or "execute pipeline for issues".
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Processing issues...'"
          once: true
---

# Process Issues Skill

Execute the appropriate implementation recipe for each triaged GitHub issue, respecting the
batch order defined by the `triage-issues` manifest. This skill is the execution counterpart
to `triage-issues` — it consumes the manifest and orchestrates the full lifecycle: load recipe,
execute session, collect result, report.

## When to Use

- After `/autoskillit:triage-issues` has produced a manifest in `temp/triage-issues/`
- User says "process issues", "run issues", "execute pipeline for issues"
- When a triage manifest exists and batched issues need implementation sessions launched

## Critical Constraints

**NEVER:**
- Create files outside `temp/process-issues/` directory
- Apply `batch:N` labels to GitHub issues (batch assignments are internal — they live only
  in the manifest JSON, not on GitHub objects)
- Modify any source code files
- Reimplement recipe steps inline — always use `load_recipe` to load the recipe YAML and
  follow it as an orchestrator
- Process issues that already carry the `in-progress` label — skip them with a warning

**ALWAYS:**
- Process batches in ascending order: batch 1 before batch 2 before batch 3
- Use `load_recipe` to execute the recipe for each issue
- Emit `---process-issues-result---` result block on completion (success or failure)
- Write the summary report to `temp/process-issues/` (relative to the current working directory)
- Use `model: "sonnet"` when spawning subagents via the Task tool
- Use `gh` CLI for all GitHub operations (not raw API calls)
- Include `--force` in all `gh label create` calls

## Arguments

- Positional (optional): path to triage manifest JSON
- `--batch N` — only process batch N (default: process all batches in order)
- `--dry-run` — print the processing plan and exit without launching any recipe sessions
- `--comment` — post a GitHub comment on each issue at pickup and at completion
- `--merge-batch` — after each batch completes, run `analyze-prs` + `merge-pr` to merge
  the batch PRs into the integration branch before starting the next batch

## Workflow

### Step 0: Parse Arguments

Parse arguments:
- If a positional path is given, use it as the manifest path.
- `--batch N`: record the target batch number; process only that batch.
- `--dry-run`: set dry_run flag; print plan then exit after Step 2.
- `--comment`: set comment flag.
- `--merge-batch`: set merge_batch flag.

### Step 1: Locate and Read Manifest

**Locate the manifest:**

1. If a positional path argument was given, use it directly.
2. Otherwise, auto-discover the most recently modified manifest:
   ```bash
   ls -t temp/triage-issues/triage_manifest_*.json 2>/dev/null | head -1
   ```
3. If no manifest is found, abort:
   > "No triage manifest found. Run `/autoskillit:triage-issues` first,
   > or pass the manifest path as the first argument."

**Parse the manifest JSON.** Extract:
- `batches`: ordered list; each entry has `batch` (number) and `issues` (array)
- Per issue: `number`, `title`, `recipe` (`"implementation"` or `"remediation"`)

**Derive the repository reference** for constructing issue URLs. Try in order:
1. Read `github.default_repo` from `.autoskillit/config.yaml` if present.
2. Infer from git remote:
   ```bash
   { git remote get-url upstream 2>/dev/null || git remote get-url origin; } | sed 's|.*github.com[:/]||; s|\.git$||'
   ```
   This yields `owner/repo`.

Construct each issue's URL:
```
https://github.com/{owner}/{repo}/issues/{number}
```

### Step 2: Dry Run Mode

If `--dry-run` is active, print a table:

```
Dry run — would process N issues in M batches:

BATCH  ISSUE  RECIPE           TITLE
------ ------ ---------------- ----------------------------------------
1      #42    implementation   Add user authentication
1      #43    remediation      Fix login redirect bug
2      #44    implementation   Refactor auth module
...

Total: N issues, M batches. No sessions launched.
```

Then emit the `---process-issues-result---` block with `"dry_run": true` and exit.

### Step 2a: Batch Scope Confirmation

Before executing any batch, display the full processing plan and confirm scope with the user:

```
━━━ Process Issues — Batch Scope ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
About to process {N} issues in {M} batches:

BATCH  ISSUE  RECIPE           TITLE
------ ------ ---------------- ----------------------------------------
{batch rows from manifest}

Processing mode: sequential within each batch (batches processed in order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Proceed? [Y/n]
```

- **Y (or Enter):** Proceed to Step 3.
- **n:** Abort. Emit `process-issues-result` with `"aborted": true` and exit cleanly.

Skip this step when `--dry-run` is active (Step 2 already prints the plan and exits) or when
`--batch N` limits scope to a single batch (show only that batch's issues).

### Step 3: Process Batches

For each batch in **ascending order** (batch 1, then batch 2, etc.):

**CRITICAL:** Do NOT output any prose status text between batches. After
completing one batch (all issues processed, optional merge cycle done),
immediately begin the batch header (3a) for the next batch.

- If `--batch N` was given, skip all batches with a different number.

**3a. Log batch header:**
```
━━━ Batch N/M ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Processing X issues:
  #42 — implementation: Add user authentication
  #43 — remediation: Fix login redirect bug
```

**3b. For each issue in the batch (process sequentially):**

**CRITICAL:** Do NOT output any prose status text between issues. After
completing one issue's processing (step 9), immediately begin step 1
(Construct the issue URL) for the next issue. Inter-issue announcements
create end_turn windows that cause stochastic session termination.

1. **Construct the issue URL** (from Step 1 derivation).

2. **Fetch issue content:**
   ```
   fetch_github_issue(issue_url, include_comments=true)
   ```
   On failure: log a warning, record `status: failure`, and advance to the next issue.

3. **Check for `in-progress` label:**
   Inspect the fetched issue's `labels` list. If `in-progress` is present:
   - Log: `"Skipping #N — already claimed (in-progress label present)"`
   - Record `status: skipped`
   - Advance to next issue.

4. **Optionally post pickup comment** (if `--comment` is active):
   ```bash
   gh issue comment {number} \
     --body "Processing in batch {N} — recipe: \`{recipe}\`"
   ```

5. **Determine recipe name and `run_name`:**

   | `recipe` field | Recipe to load | `run_name` | PR Title Prefix |
   |---------------|----------------|------------|-----------------|
   | `implementation` | `implementation` | `feature` | `[FEATURE]` |
   | `remediation` | `remediation` | `fix` | `[FIX]` |

   These values correspond to the GitHub labels applied by `triage-issues`:
   `recipe:implementation` (new features/enhancements) and `recipe:remediation` (bugs).

   The `run_name` encodes recipe origin for the `open-pr` skill, which derives
   the PR title prefix from it by convention (see `open-pr` SKILL.md).

6. **Load the recipe:**
   ```
   load_recipe("{recipe_name}")
   ```
   This returns the recipe YAML. Read it and execute it as an orchestrator —
   follow each step in the recipe, calling the specified MCP tool with the
   specified `with:` arguments.

7. **Execute the recipe** with these ingredient values:
   - `task`: the issue title (the recipe's `make-plan` step detects `issue_url`
     and fetches full content internally)
   - `issue_url`: the constructed issue URL
   - `run_name`: `"feature"` (implementation) or `"fix"` (remediation)
   - `base_branch`: `"integration"` (or read `git rev-parse --abbrev-ref HEAD`)
   - `open_pr`: `"true"`
   - `audit`: `"true"`
   - `review_approach`: `"false"`

   The recipe handles claim/release internally: both `implementation.yaml` and
   `remediation.yaml` call `claim_issue` early in their step graph and
   `release_issue` on both success and failure paths. There is no need to
   call `claim_issue` or `release_issue` from this skill directly.

   If the recipe's `claim_issue` step returns `claimed: false` (issue already
   claimed by another session), the recipe routes to `escalate_stop`. Record
   the outcome and advance to the next issue.

8. **After recipe completes**, record the result:
   - On success path (`done` step reached): `{issue_number, recipe, status: success, pr_url}`
   - On failure path (`escalate_stop` reached): `{issue_number, recipe, status: failure, error}`

9. **Optionally post completion comment** (if `--comment` is active):
   - Success: `"✅ Processing complete — PR: {pr_url}"`
   - Failure: `"❌ Processing failed — manual intervention required"`

**3c. After all issues in batch complete** (if `--merge-batch` is active):

Run the analyze-prs → merge-pr cycle for the batch's PRs:

```
run_skill("/autoskillit:analyze-prs {base_branch}")
```

Parse the `pr_order_file` from the skill output. For each PR in the recommended
merge order:

**CRITICAL:** Do NOT output any prose status text between PRs. After one
merge-pr completes, immediately call run_skill for the next PR.

```
run_skill("/autoskillit:merge-pr {pr_number} {complexity}")
```

Log merge results and proceed to the next batch.

### Step 4: Write Summary Report

Compute timestamp: `YYYY-MM-DD_HHMMSS`.
Create `temp/process-issues/` if it does not exist.

Write `temp/process-issues/process_report_{ts}.md`:

```markdown
# Process Issues Report — {ts}

## Summary

| Metric | Value |
|--------|-------|
| Total issues | N |
| Successes | X |
| Failures | Y |
| Skipped (in-progress) | Z |
| Batches processed | M |

## Results by Batch

### Batch 1

| Issue | Title | Recipe | Status | PR |
|-------|-------|--------|--------|----|
| #42 | Add user auth | implementation | success | #101 |
| #43 | Fix redirect | remediation | failure | — |

### Batch 2
...

## Failures

For each failed issue: error message captured from recipe terminal step.
```

### Step 5: Emit Result Block

Print the structured result for pipeline capture:

```
---process-issues-result---
{
    "report_path": "temp/process-issues/process_report_{ts}.md",
    "total_issues": N,
    "successes": X,
    "failures": Y,
    "skipped": Z,
    "batch_count": M,
    "dry_run": false,
    "pr_urls": ["https://github.com/.../pull/101", ...]
}
---end-process-issues-result---
```

## Output Location

```
temp/process-issues/
  process_report_{ts}.md   # Human-readable summary (created per run)
```

## Related Skills

- **`/autoskillit:triage-issues`** — Produces the manifest that this skill consumes
- **`/autoskillit:analyze-prs`** — Used in `--merge-batch` mode
- **`/autoskillit:merge-pr`** — Used in `--merge-batch` mode
- **`/autoskillit:open-pr`** — Called by each executed recipe; derives `[FEATURE]`/`[FIX]`
  PR title prefix from the `run_name` ingredient