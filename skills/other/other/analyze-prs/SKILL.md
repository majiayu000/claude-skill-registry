---
name: analyze-prs
categories: [github]
description: Analyze all open PRs targeting a base branch — determine merge order, identify file overlaps, and tag each PR as simple or needs_check for complexity. Use at the start of a PR consolidation workflow.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Analyzing open PRs...'"
          once: true
---

# PR Analysis Skill

Analyze all open PRs targeting a base branch, determine a safe merge order, assess
complexity, and produce machine-readable output for the `merge-prs` recipe.

## When to Use

- At the start of a `merge-prs` run
- User wants to understand which PRs can be merged safely and in what order
- User says "analyze PRs", "order PRs", or "assess PR complexity"

## Critical Constraints

**NEVER:**
- Merge, close, or modify any PR
- Modify any source code files
- Create files outside `temp/merge-prs/` directory

**ALWAYS:**
- Use subagents to fetch PR data in parallel
- Use `model: "sonnet"` when spawning all subagents via the Task tool
- Abort clearly if `gh` CLI is not authenticated
- Include every open PR targeting base_branch in the output — no PR is silently dropped (blocked PRs appear in ci_blocked_prs / review_blocked_prs arrays, not in the ordered prs list)
- **Default to parallel batch processing**: When multiple PRs are present, ALWAYS process
  all analysis tasks (diff fetching, overlap computation, complexity tagging) using parallel
  subagent batches. Processing PRs one-at-a-time without an explicit user instruction to do
  so is the wrong default. Up to 8 PRs should be processed in a single parallel batch;
  launch additional batches for larger sets.

## Arguments

`{base_branch}` — the base branch to list PRs against (e.g., `main`)

## Workflow

### Step 0: Authenticate and List PRs

Run:
```bash
gh pr list --base {base_branch} --state open --json number,title,headRefName,author,body,additions,deletions,changedFiles --limit 100
```

If zero PRs are returned: write a summary to terminal and exit cleanly with an empty
`pr_order_{ts}.json` (zero PRs, no integration branch needed).

If `gh` returns an auth error: abort with a clear message.

### Step 0.5: Detect GitHub Merge Queue

Before fetching diffs, query the GitHub GraphQL API to determine whether a merge queue
is active on `{base_branch}` with `MERGEABLE` entries.

1. Resolve the repo owner and name:
   ```
   gh repo view --json owner,name
   ```
   Extract `OWNER` and `REPO` from the JSON output.

2. Query the merge queue:
   ```
   gh api graphql -f query='{
     repository(owner: "OWNER", name: "REPO") {
       mergeQueue(branch: "BASE_BRANCH") {
         entries(first: 50) {
           nodes {
             position
             state
             pullRequest { number title }
           }
         }
       }
     }
   }'
   ```
   Pipe the JSON output through `autoskillit.execution.github.parse_merge_queue_response`:
   ```
   python -c "
   import sys, json
   _m = __import__('autoskillit' + '.execution.github', fromlist=[''])
   data = json.load(sys.stdin)
   entries = _m.parse_merge_queue_response(data)
   print(json.dumps(entries))
   "
   ```

3. Determine mode:
   - If the resulting entry list contains at least one entry with `state == "MERGEABLE"`:
     set **`QUEUE_MODE = true`** and store the full sorted entry list as `QUEUE_ENTRIES`.
   - Otherwise (empty list, no MERGEABLE entries, or `gh api graphql` returned a
     non-zero exit code): set **`QUEUE_MODE = false`** and proceed with the existing
     analysis path.

   Log which mode was selected and the entry count to the terminal so pipeline runs are
   observable.

**State variables set by this step (referenced in Steps 1–4):**

| Variable | Type | Description |
|----------|------|-------------|
| `QUEUE_MODE` | boolean | `true` when the merge queue has ≥1 MERGEABLE entry; `false` otherwise |
| `QUEUE_ENTRIES` | list[dict] | Sorted queue entries `{position, state, pr_number, pr_title}` when `QUEUE_MODE = true`; empty list when `false` |

### Step 1: Fetch PR Data

- **If `QUEUE_MODE = false`**: **ALWAYS launch subagents in parallel** — never process PRs
  sequentially. Launch one Explore subagent per PR (up to 8 simultaneously; batch in groups
  of 8 if more):

  Each subagent fetches:
  - `gh pr diff {number}` — full unified diff
  - `gh pr view {number} --json files` — structured file list; extract path strings via
    `gh pr view {number} --json files -q '[.files[].path]'`
  - `gh pr view {number} --json body -q .body` — PR body to extract `## Requirements` section if present

  Each subagent returns:
  - `pr_number`: int
  - `title`: str
  - `branch`: str (headRefName)
  - `files_changed`: list of file paths (strings extracted from `.files[].path`)
  - `additions`: int
  - `deletions`: int
  - `test_files_changed`: list of test file paths (files matching `test_*.py`, `*_test.py`, `*.test.*`, `tests/**`)
  - `requirements_section`: str — the `## Requirements` section extracted from the PR body, or `""` if not present

- **If `QUEUE_MODE = true`**: for each PR number in `QUEUE_ENTRIES`, fetch only the
  metadata needed for the manifest (no diffs, no body extraction):
  ```
  gh pr view {number} --json headRefName,files,additions,deletions,changedFiles
  ```
  Extract file paths from the `files` array: `gh pr view {number} --json files -q '[.files[].path]'`.
  Collect `files_changed` (list of file path strings), `test_files_changed` (subset matching
  `test_*.py`, `*_test.py`, `*.test.*`, `tests/**`), `additions`, `deletions`, and
  `branch` (`headRefName`). Run these fetches in parallel (up to 8 simultaneously).
  The PR list for subsequent steps is exactly `QUEUE_ENTRIES` — do **not** use the
  `gh pr list` output.

### Step 1.5: Filter PRs by CI and Review Status

- **If `QUEUE_MODE = false`**: After fetching all PR diffs, filter the candidate list before
  building the overlap matrix. PRs that fail either gate are reported in the manifest but
  excluded from merge ordering.

  ```bash
  ELIGIBLE_PRS=()
  CI_BLOCKED_PRS=()      # [{number, title, reason}]
  REVIEW_BLOCKED_PRS=()  # [{number, title, reason}]

  for PR in "${ALL_PRS[@]}"; do
    PR_NUM=$(echo "$PR" | jq -r .number)
    PR_TITLE=$(echo "$PR" | jq -r .title)

    # --- CI Gate ---
    CI_CHECKS=$(gh pr checks "$PR_NUM" --json name,status,conclusion 2>/dev/null \
      || echo "[]")
    FAILING=$(echo "$CI_CHECKS" | jq '[.[] | select(
      .conclusion != null and
      .conclusion != "success" and
      .conclusion != "skipped" and
      .conclusion != "neutral"
    )] | length')
    IN_PROGRESS=$(echo "$CI_CHECKS" | jq '[.[] | select(.conclusion == null)] | length')

    if [ "$FAILING" -gt 0 ] || [ "$IN_PROGRESS" -gt 0 ]; then
      REASON="CI failing: ${FAILING} failed, ${IN_PROGRESS} in-progress"
      CI_BLOCKED_PRS+=("{\"number\":${PR_NUM},\"title\":\"${PR_TITLE}\",\"reason\":\"${REASON}\"}")
      continue
    fi

    # --- Review Gate ---
    REVIEWS=$(gh pr view "$PR_NUM" --json reviews -q '.reviews // []')
    CHANGES_REQUESTED=$(echo "$REVIEWS" | jq '[.[] | select(.state == "CHANGES_REQUESTED")] | length')

    if [ "$CHANGES_REQUESTED" -gt 0 ]; then
      REASON="${CHANGES_REQUESTED} unresolved CHANGES_REQUESTED review(s)"
      REVIEW_BLOCKED_PRS+=("{\"number\":${PR_NUM},\"title\":\"${PR_TITLE}\",\"reason\":\"${REASON}\"}")
      continue
    fi

    ELIGIBLE_PRS+=("$PR")
  done
  ```

  All subsequent steps (overlap matrix, topo sort, PR ordering) operate on `ELIGIBLE_PRS` only.
  `CI_BLOCKED_PRS` and `REVIEW_BLOCKED_PRS` are written to the manifest in Step 5.

- **If `QUEUE_MODE = true`**: **skip this step entirely.** The `MERGEABLE` state returned by
  the merge queue API already signifies that the PR passed CI checks and has no blocking
  reviews. Initialize both arrays explicitly so Step 5 can reference them unconditionally:
  ```bash
  CI_BLOCKED_PRS=()
  REVIEW_BLOCKED_PRS=()
  ```

### Step 2: Build File Overlap Matrix

- **If `QUEUE_MODE = false`**: For each pair of PRs, compute:
  - `shared_files`: files modified by both PRs
  - `shared_test_files`: test files modified by both PRs

  A PR pair is **conflicting** if `shared_files` is non-empty.

- **If `QUEUE_MODE = true`**: **skip this step entirely.** The merge queue has already proven
  compatibility. Set `overlap_with_pr_numbers = []` for every PR.

### Step 3: Determine Merge Order

- **If `QUEUE_MODE = false`**: Order PRs to minimize cascading conflict risk:

  1. **PRs with no overlapping files** with any other PR → place first (order by additions ASC)
  2. **PRs with overlap** → order so the PR that others depend on (touches foundational files) comes first; use topological sort on the overlap graph
  3. **Large PRs** (additions > 200) → place after small PRs that touch the same files, unless they have no overlap

  Produce a final ordered list. Document the rationale for each ordering decision.

- **If `QUEUE_MODE = true`**: the merge order is `QUEUE_ENTRIES` sorted by `position`
  ascending (ascending is already guaranteed by `parse_merge_queue_response`).

### Step 4: Tag Complexity

- **If `QUEUE_MODE = false`**: For each PR in the ordered list, assign a complexity tag:

  **`simple`** — all of the following are true:
  - No shared files with any PR ahead of it in the merge order
  - Total additions < 100
  - No shared test files with PRs ahead of it
  - No substantial logic changes in files also touched by earlier PRs (based on diff inspection)

  **`needs_check`** — any of the following:
  - Shares files with one or more PRs ahead of it in merge order
  - Additions ≥ 100 and touches files also present in earlier PRs
  - Modifies shared test files
  - The diff suggests it depends on function signatures or class structures that earlier PRs may change

- **If `QUEUE_MODE = true`**: tag every PR whose queue entry has `state == "MERGEABLE"` as
  **`simple`**. Any entry with a different state (e.g., `AWAITING_CHECKS`) retains the
  `needs_check` tag (defensive — such entries should not appear since Step 0.5 only sets
  QUEUE_MODE when MERGEABLE entries exist, but the tag is applied correctly for robustness).

### Step 5: Write Outputs

Compute a timestamp: `YYYY-MM-DD_HHMMSS`.

Compute integration branch name: `pr-batch/pr-merge-{YYYYMMDD-HHMMSS}`.

Ensure `temp/merge-prs/` exists.

**5a. Machine-readable order file:** `temp/merge-prs/pr_order_{ts}.json`

```json
{
    "integration_branch": "pr-batch/pr-merge-YYYYMMDD-HHMMSS",
    "base_branch": "{base_branch}",
    "generated_at": "{ISO timestamp}",
    "pr_count": 5,
    "prs": [
        {
            "number": 42,
            "title": "Add user authentication",
            "branch": "feature/auth",
            "complexity": "simple",
            "files_changed": ["src/auth.py", "tests/test_auth.py"],
            "test_files_changed": ["tests/test_auth.py"],
            "additions": 87,
            "deletions": 12,
            "overlap_with_pr_numbers": []
        },
        {
            "number": 47,
            "title": "Refactor database layer",
            "branch": "feature/db-refactor",
            "complexity": "needs_check",
            "files_changed": ["src/db.py", "src/auth.py", "tests/test_db.py"],
            "test_files_changed": ["tests/test_db.py"],
            "additions": 165,
            "deletions": 45,
            "overlap_with_pr_numbers": [42]
        }
    ],
    "ci_blocked_prs": [
        {"number": 99, "title": "Broken CI PR", "reason": "CI failing: 1 failed, 0 in-progress"}
    ],
    "review_blocked_prs": [
        {"number": 88, "title": "Needs changes PR", "reason": "2 unresolved CHANGES_REQUESTED review(s)"}
    ]
}
```

`pr_count` reflects the number of **eligible** PRs (i.e., `${#ELIGIBLE_PRS[@]}`).

**5b. Human-readable analysis plan:** `temp/merge-prs/pr_analysis_plan_{ts}.md`

This file is named `*_plan_*.md` so `audit-impl` can discover it as the baseline specification.

```markdown
# PR Analysis: Integration into {base_branch}

**Date:** {YYYY-MM-DD}
**Base Branch:** {base_branch}
**Integration Branch:** pr-batch/pr-merge-YYYYMMDD-HHMMSS
**PRs Analyzed:** {count}

## Merge Order

1. PR #{number} — "{title}" (complexity: simple)
2. PR #{number} — "{title}" (complexity: needs_check)
...

## Excluded PRs

### CI-Blocked ({ci_blocked_count})
| PR | Title | Reason |
|----|-------|--------|
| #{number} | {title} | CI failing: 1 failed, 0 in-progress |

### Review-Blocked ({review_blocked_count})
| PR | Title | Reason |
|----|-------|--------|
| #{number} | {title} | 2 unresolved CHANGES_REQUESTED review(s) |

## File Overlap Matrix

| PR | Files | Overlaps With |
|----|-------|---------------|
| #{number} | {file list} | None |
| #{number} | {file list} | PR #{number} (src/auth.py) |

## Per-PR Assessment

### PR #{number}: "{title}"
- **Branch:** {branch}
- **Complexity:** simple / needs_check
- **Rationale:** {why this complexity tag was assigned}
- **Key files:** {list}
- **Risk notes:** {any concerns}

{If requirements_section is non-empty, include this block so reviewers can trace intent:}
#### Requirements

{requirements_section from PR body}

{repeat for each PR}

## Integration Strategy

{2–3 sentences describing the overall merge strategy and key risk areas}
- **If `QUEUE_MODE = true`**: PR order sourced from GitHub merge queue (position ordering). File overlap analysis skipped.
```

### Step 6: Verify and Report

Verify:
- `pr_order_{ts}.json` is valid JSON and parseable
- Every listed PR number appears exactly once
- `integration_branch` field is set

Report to terminal:
- Order file path
- Analysis file path
- Number of PRs: {simple_count} simple, {needs_check_count} needs_check
- Proposed integration branch name
- Any PRs flagged as high risk

## Output Location

```
temp/merge-prs/
├── pr_order_{ts}.json              # Machine-readable manifest (captured by recipe)
└── pr_analysis_plan_{ts}.md        # Human-readable analysis (discovered by audit-impl)
```

## Output Fields (for recipe capture)

After writing all output files and printing the terminal report, emit the following
structured output tokens as the very last lines of your text output:

```
pr_order_file = {absolute_path_to_pr_order_json}
analysis_file = {absolute_path_to_pr_analysis_plan_md}
integration_branch = {integration_branch_name}
pr_count = {eligible_pr_count}
simple_count = {simple_pr_count}
needs_check_count = {needs_check_pr_count}
ci_blocked_count = {ci_blocked_pr_count}
review_blocked_count = {review_blocked_pr_count}
queue_mode = {queue_mode}   # true when merge queue has ≥1 MERGEABLE entry; false otherwise
```

## Related Skills

- **`/autoskillit:merge-pr`** — Merges individual PRs from this skill's ordered list
- **`/autoskillit:make-plan`** — Called for complex PRs that need conflict resolution plans
- **`/autoskillit:audit-impl`** — Receives `temp/merge-prs/` as plans_input
