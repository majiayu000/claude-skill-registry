---
name: collapse-issues
categories: [github]
description: >
  Identify clusters of related triaged GitHub issues sharing the same recipe route
  and collapse them into a single combined issue with full content from all originals.
  Closes originals with cross-reference comments. Inverse of issue-splitter.
triggers:
  - /autoskillit:collapse-issues
---

# collapse-issues Skill

Identify clusters of related triaged GitHub issues sharing the same `recipe:*` label
and collapse qualifying clusters into single combined issues. Originals are closed with
cross-reference comments. This is the **inverse** of `issue-splitter` — where splitter
decomposes mixed-concern issues, this consolidates related small issues into fewer,
better-scoped units.

Grouping analysis is performed as in-context LLM reasoning. No parallel sessions are spawned.

## When to Use

- After `issue-splitter` has decomposed issues into focused sub-issues, to re-consolidate
  overly granular results
- Invoked by `triage-issues` via the `--collapse` flag (Step 2c)
- Directly by a user who wants to reduce issue count before an implementation sprint
- With `--dry-run` to preview what would be collapsed without mutating GitHub

## Arguments

```
/autoskillit:collapse-issues [--dry-run] [--min-group 2] [--max-group 5] [--repo owner/repo] [--no-label]
```

- `--dry-run` — show proposed groupings, skip all GitHub mutations
- `--min-group N` — minimum issues per group to justify collapsing (default: 2)
- `--max-group N` — maximum issues per combined issue (default: 5)
- `--repo owner/repo` — explicit repo; if absent, resolve via `gh repo view`
- `--no-label` — skip all label creation and `--label` calls

## Critical Constraints

**NEVER:**
- Close original issues before the combined issue is successfully created
- Apply `batch:N` labels to combined or original issues
- Collapse issues with different `recipe:*` labels into one combined issue
- Delegate grouping to parallel sessions — grouping analysis is in-context LLM reasoning only
- Use parallel session spawning (Agent/Task) for grouping analysis — it is in-context LLM reasoning
- Create files outside `temp/collapse-issues/`
- Skip emitting the `---collapse-issues-result---` block (emit even on error or no-collapse)
- Summarize, paraphrase, truncate, or abbreviate the body of a source issue
- Substitute a hyperlink, URL reference, or cross-reference for inlined body content
- Use angle-bracket placeholder syntax (`<...>`) in the combined issue body — always paste actual retrieved content from fetch_github_issue
- Use the body field from `gh issue list` for body assembly — only fetched_content[N] from per-issue fetch is authoritative

**ALWAYS:**
- Include `--force` on all label creation calls (`gh label create --force`) for idempotency
- Respect `--dry-run` (skip all GitHub mutations when set)
- Respect `--no-label` (skip all label creation and `--label` flags when set)
- Cap groups at `--max-group` (default 5)
- Require at least `--min-group` (default 2) issues to form a group
- Emit `---collapse-issues-result---` block even on dry-run or no-collapse decisions

## Workflow

### Step 0: Parse Arguments

Extract from ARGUMENTS:
- `--dry-run` → `dry_run = true`
- `--min-group N` → `min_group = N` (default: 2)
- `--max-group N` → `max_group = N` (default: 5)
- `--repo owner/repo` → `repo = "owner/repo"` (omit `--repo` flag from gh commands if not provided)
- `--no-label` → `no_label = true`

### Step 1: Authenticate

```bash
gh auth status
```

If auth fails, emit result block with `{"error": "gh auth failed", "groups_formed": 0, "issues_collapsed": 0}` and exit.

### Step 2: Resolve Repo

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

If repo cannot be resolved, emit result block with `{"error": "repo resolution failed", "groups_formed": 0, "issues_collapsed": 0}` and exit.

### Step 3: Fetch Triaged Issues

```bash
gh issue list --state open --json number,title,labels --limit 200 [--repo {repo}]
```

- Filter to issues that carry at least one `recipe:*` label (e.g., `recipe:implementation`, `recipe:remediation`)
- If the filtered list is empty: emit `no-collapse` result block and exit:
  ```
  ---collapse-issues-result---
  {"groups_formed": 0, "issues_collapsed": 0, "combined_issues": [], "standalone_issues": [], "dry_run": false, "reason": "no triaged issues"}
  ---/collapse-issues-result---
  ```

### Step 4: LLM Grouping Analysis (in-context)

This step is pure in-context LLM reasoning — no parallel session spawning.

**4a. Partition by recipe route (hard constraint):**

Separate issues into per-recipe buckets. Issues with `recipe:implementation` form one group;
issues with `recipe:remediation` form another. Issues with different `recipe:*` labels are
**never** collapsed together into a single combined issue.

**4b. Score pairwise relatedness within each bucket:**

For each pair of issues in the same recipe bucket, evaluate:
- Overlapping component mentions (e.g., both mention `recipe/`, `execution/`, `server/`)
- Shared keywords in title/body (similar subsystem vocabulary)
- Complementary scope (e.g., two small enhancements to the same module)
- Size preference: prefer collapsing small/simple issues; large issues (long body, many
  sub-requirements) should remain standalone

**4c. Form candidate groups:**

- Greedily assign issues to groups, starting with most-related pairs
- Enforce `--max-group` cap per group (default: 5)
- Issues that don't fit any qualifying group remain standalone

**4d. Apply minimum-group threshold:**

Groups with fewer than `--min-group` issues (default: 2) are dissolved — their members
remain standalone.

If no groups meet the threshold: emit `no-collapse` result block and exit:
```
---collapse-issues-result---
{"groups_formed": 0, "issues_collapsed": 0, "combined_issues": [], "standalone_issues": [<all issue numbers>], "dry_run": false, "reason": "no qualifying groups"}
---/collapse-issues-result---
```

### Step 5: Fetch Full Issue Content

For each issue in each qualifying group (not standalone issues), call:

    fetch_github_issue(issue_url, include_comments=true)

where `issue_url` is constructed as:
    https://github.com/{repo}/issues/{number}

Do not output any prose between fetch calls — immediately proceed to the next issue.

Store the returned `content` field from the response. If `fetch_github_issue` returns
`success: false` for an issue, log the failure and proceed using the issue title
and a note that full body content was unavailable (do not fabricate body content).

This step produces the `fetched_content[N]` mapping used in Step 7b.

### Step 6: Dry-run Gate

If `--dry-run` is set: print the proposed groups in human-readable form:

```
Group 1 (recipe:implementation): issues #12, #15, #18
  Proposed title: "Combined: <descriptive scope phrase>"

Group 2 (recipe:remediation): issues #7, #9
  Proposed title: "Combined: <descriptive scope phrase>"

Standalone: #3, #22, #25
```

Emit result block with `"dry_run": true` and exit without any GitHub mutations:

```
---collapse-issues-result---
{"groups_formed": 2, "issues_collapsed": 5, "combined_issues": [], "standalone_issues": [3, 22, 25], "dry_run": true}
---/collapse-issues-result---
```

### Step 7: Create Combined Issues

For each qualifying group (in-context LLM reasoning for title synthesis):

Do not emit any prose or status text between groups — immediately proceed to create each combined issue.

**7a. Synthesize title:**

Write a title that describes the combined scope of all issues in the group.
Format: `"Combined: <descriptive scope phrase>"`

**7b. Build combined issue body:**

```
<!-- Collapses: #N, #M, #P -->

This issue combines related work originally tracked in #N, #M, and #P.

## From #N: {original title of issue N}

{Paste the complete, unmodified text of fetched_content[N].body here exactly
as returned by fetch_github_issue. Do not summarize, paraphrase, truncate, or
abbreviate any part of the body. Do not substitute a hyperlink, cross-reference,
or descriptive sentence. Every heading, list item, code block, and paragraph
from the original issue body must appear here without alteration.

SWITCH TO COPY MODE: The preceding title-synthesis step required generative
reasoning. This step requires strict verbatim reproduction — do not compose or
generate new prose. Copy only.}

---

## From #M: {original title of issue M}

{Paste the complete, unmodified text of fetched_content[M].body here exactly
as returned by fetch_github_issue. Do not summarize, paraphrase, truncate, or
abbreviate any part of the body. Do not substitute a hyperlink, cross-reference,
or descriptive sentence. Every heading, list item, code block, and paragraph
from the original issue body must appear here without alteration.

SWITCH TO COPY MODE: The preceding title-synthesis step required generative
reasoning. This step requires strict verbatim reproduction — do not compose or
generate new prose. Copy only.}

---

## From #P: {original title of issue P}

{Paste the complete, unmodified text of fetched_content[P].body here exactly
as returned by fetch_github_issue. Do not summarize, paraphrase, truncate, or
abbreviate any part of the body. Do not substitute a hyperlink, cross-reference,
or descriptive sentence. Every heading, list item, code block, and paragraph
from the original issue body must appear here without alteration.

SWITCH TO COPY MODE: The preceding title-synthesis step required generative
reasoning. This step requires strict verbatim reproduction — do not compose or
generate new prose. Copy only.}
```

**7c. Collect labels:**

Union of all non-`batch:*` labels from the original issues in the group. Typically this
is the shared `recipe:*` label plus any `enhancement`/`bug` labels.

**7d. Ensure labels exist** (skip if `--no-label`):

```bash
gh label create "recipe:implementation" --force [--repo {repo}]
gh label create "enhancement" --force [--repo {repo}]
```

Repeat for each unique label in the collected set (e.g., `recipe:remediation`, `bug`), always with `--force`.

**7e. Create combined issue:**

```bash
gh issue create \
  --title "Combined: <synthesized title>" \
  --body "<combined body>" \
  --label "recipe:implementation" \
  --label "enhancement" \
  [--repo {repo}]
```

Capture the new issue number from the URL in stdout output.

### Step 8: Close Original Issues

For each original issue that was collapsed (one by one, in order):

**8a. Post closing comment:**

```bash
gh issue comment {orig_number} \
  --body "Collapsed into #{combined_number}: {combined_url}" \
  [--repo {repo}]
```

**8b. Close the issue:**

```bash
gh issue close {orig_number} [--repo {repo}]
```

### Step 9: Emit Result Block

```
---collapse-issues-result---
{
  "groups_formed": <count>,
  "issues_collapsed": <total originals closed>,
  "combined_issues": [
    {"number": X, "url": "...", "from": [N, M, P]},
    ...
  ],
  "standalone_issues": [<list of issue numbers NOT collapsed>],
  "dry_run": false
}
---/collapse-issues-result---
```

On error, emit:

```
---collapse-issues-result---
{"error": "<description>", "groups_formed": 0, "issues_collapsed": 0}
---/collapse-issues-result---
```

## Output Location

Dry-run reports (if any): `temp/collapse-issues/`

## Error Handling

- Auth failure → emit error result block, exit
- Repo resolution failure → emit error result block, exit
- No triaged issues → emit no-collapse result block, exit
- No qualifying groups → emit no-collapse result block, exit
- `gh issue create` fails → log the failure, emit partial result with `"error"` in rationale,
  do not abort silently; do not close any originals for this group
- `gh issue close` fails → log the failure and continue with remaining originals

## Related Skills

- **`/autoskillit:issue-splitter`** — Inverse: decomposes mixed-concern issues into focused sub-issues
- **`/autoskillit:triage-issues`** — Invokes this skill via `--collapse` flag (Step 2c)
