---
name: open-pr-main
categories: [github]
description: >
  Promote the integration branch to main by opening a comprehensive PR. Discovers
  all merged PRs that landed in integration since divergence from main, traces linked
  issues, generates domain analysis and arch-lens diagrams, and composes a rich PR body
  with narrative summary, PR/issue tables, and carried-forward Closes #N references.
---

# Open PR to Main

Promote the `integration` branch to `main`. This skill discovers everything that changed
on integration since it diverged from main — merged PRs, linked issues, domain-level
analysis, and architectural impact — then opens a single promotion PR with a comprehensive
body suitable for final review before landing on main.

## Arguments

```
/autoskillit:open-pr-main [integration_branch] [base_branch]
```

- `integration_branch` (optional) — source branch to promote. Defaults to `integration`.
- `base_branch` (optional) — target branch. Defaults to `main`.

## When to Use

- When the integration branch is semi-stable and ready to be promoted to main
- After feature PRs, bug fixes, and cleanup work have been collected and tested on integration
- This is the final gate before changes land on main

## Critical Constraints

**NEVER:**
- Create files outside `temp/open-pr-main/`
- Modify any source code
- Fail if `gh` is unavailable — output `pr_url = ` (empty) and exit successfully
- Push or merge anything — this skill only creates the PR

**ALWAYS:**
- Check `gh auth status` before any GitHub operations
- Output `pr_url = <url>` on the last output line (empty string when GitHub unavailable)
- Carry forward ALL `Closes #N`, `Fixes #N`, and `Resolves #N` references from merged PR bodies
- Use `gh pr create --body-file` (never inline body via `--body`)

## Workflow

### Step 1: Parse Arguments

Parse optional positional arguments:
- `integration_branch` — default `"integration"` if absent or empty
- `base_branch` — default `"main"` if absent or empty

Validate that both branches exist locally:
```bash
git rev-parse --verify {integration_branch} 2>/dev/null
git rev-parse --verify {base_branch} 2>/dev/null
```
If either fails, try fetching:
```bash
git fetch origin {branch}:{branch} 2>/dev/null
```
If still missing, print error to stderr and exit 1.

### Step 2: Compute Divergence Point

```bash
git merge-base {base_branch} {integration_branch}
```

Store as `merge_base_sha`. This is the point where integration diverged from main.

Get commit count:
```bash
git rev-list --count {merge_base_sha}..{integration_branch}
```
Store as `commit_count`.

### Step 3: Discover Merged PRs

Find all PRs that were merged into the integration branch since the divergence. Run:

```bash
gh pr list --base {integration_branch} --state merged --limit 200 --json number,title,author,mergedAt,body,headRefName,additions,deletions,labels,url
```

Store the full list as `all_merged_prs`.

Filter to only PRs merged after the merge base. To determine the merge base timestamp:

```bash
git show -s --format=%cI {merge_base_sha}
```

Store as `merge_base_date`. Filter `all_merged_prs` to those where `mergedAt >= merge_base_date`.
Store the filtered list as `pr_list`, sorted by `mergedAt` ascending.

If `pr_list` is empty, also try discovering PRs from commit messages:

```bash
git log {merge_base_sha}..{integration_branch} --oneline --grep="(#" --format="%s"
```

Extract PR numbers from patterns like `(#123)` in squash-merge commit subjects. For each
discovered number not already in `pr_list`, fetch its data:

```bash
gh pr view {number} --json number,title,author,mergedAt,body,headRefName,additions,deletions,labels,url 2>/dev/null
```

Add valid results to `pr_list`.

### Step 4: Extract Closing References from PR Bodies

For each PR in `pr_list`, extract every match of `(Closes|Fixes|Resolves)\s+#\d+`
(case-insensitive) from its `body` field.

Deduplicate across all PRs. Store as `closing_refs` (list of strings like `Closes #42`).
Also store the extracted issue numbers as `linked_issue_numbers` (deduplicated list of ints).

### Step 5: Fetch Linked Issue Details (parallel)

For each issue number in `linked_issue_numbers`, run in parallel (all calls in a single
message):

```bash
gh issue view {number} --json number,title,state,url,labels 2>/dev/null
```

Store results as `issue_details: list[dict]`. Skip issues where `gh` fails (log warning).
Partition into:
- `open_issues` — issues with `state == "OPEN"` (will be closed by this PR)
- `closed_issues` — issues already closed (reference only)

### Step 6: Get Changed Files

```bash
git diff --name-only {base_branch}..{integration_branch}
git diff --diff-filter=A --name-only {base_branch}..{integration_branch}
git diff --diff-filter=M --name-only {base_branch}..{integration_branch}
git diff --diff-filter=D --name-only {base_branch}..{integration_branch}
```

Store as `changed_files`, `new_files`, `modified_files`, `deleted_files`.

Also compute a summary:
```bash
git diff --stat {base_branch}..{integration_branch} | tail -1
```
Store as `diff_stat_summary` (e.g., "42 files changed, 1500 insertions(+), 300 deletions(-)").

### Step 7: Partition Files by Domain

```bash
python3 -c "
from autoskillit.execution.pr_analysis import partition_files_by_domain
import json, sys
files = json.loads(sys.argv[1])
result = partition_files_by_domain(files)
print(json.dumps(result))
" '{changed_files_as_json_array}'
```

Store as `domain_partitions`. Skip and set `domain_partitions = {}` if `changed_files`
is empty.

### Step 8: Fetch Domain Diffs (parallel)

For each domain `D` in `domain_partitions` with a non-empty file list, run in parallel
(all Bash calls in a single message):

```bash
git diff {base_branch}..{integration_branch} -- {space-separated files in domain D}
```

Store as `domain_diffs: dict[str, str]`. Truncate diffs exceeding 12 000 characters with
`\n... [truncated — diff exceeds 12 000 chars]`. Drop domains with empty diffs.

### Step 9: Identify PRs per Domain

For each domain `D` in `domain_partitions`, find every PR in `pr_list` whose changes
overlap with files in that domain. Since merged PRs may not have `files_changed` in the
JSON, use the PR's `headRefName` to check:

For each PR, compare its title/body context or use the overlap of the domain file list
with the overall diff. Alternatively, fetch files per PR:

```bash
gh pr view {number} --json files -q '.files[].path' 2>/dev/null
```

Store as `domain_pr_numbers: dict[str, list[int]]`.

### Step 10: Fetch Domain Commits (parallel)

For each domain in `domain_diffs`, run in parallel:

```bash
git log {base_branch}..{integration_branch} --oneline -- {space-separated files in domain D}
```

Store as `domain_commits: dict[str, list[str]]`.

### Step 11: Run Parallel Domain Analysis Subagents

For each domain `D` in `domain_diffs`, spawn a Task subagent (model: sonnet) in a single
parallel message. Each subagent receives:
- Domain name
- File list for the domain
- Diff content (truncated)
- PR numbers and titles for PRs touching this domain
- Commit one-liners for the domain

Each subagent returns ONLY a JSON object:

```json
{
  "domain": "Server/MCP Tools",
  "summary": "3-5 sentence description of what changed and why it matters",
  "key_changes": ["concise description of change 1", "concise description of change 2"],
  "breaking_changes": ["description of any breaking change, or empty array"],
  "pr_numbers": [42, 47],
  "commit_count": 5
}
```

Parse each result. Store as `domain_summaries: list[dict]`.

### Step 12: Generate Executive Summary (subagent)

Spawn a Task subagent (model: sonnet) with:
- The list of all merged PR titles and numbers
- The domain summaries from Step 11
- The diff stat summary
- The count of linked issues

Instruct it to produce a JSON object:

```json
{
  "executive_summary": "3-5 sentence high-level narrative of what this promotion brings to main. Written for a project maintainer reviewing the PR. Focus on themes and impact, not individual changes.",
  "highlights": ["Most significant change 1", "Most significant change 2", "Most significant change 3"],
  "risk_areas": ["Area requiring careful review 1", "Area requiring careful review 2"]
}
```

Store as `executive`. If parsing fails, fall back to a generic summary.

### Step 13: Select Arch-Lens Lenses

Spawn a Task subagent (model: sonnet) with `changed_files` and this lens menu:

```
c4-container, concurrency, data-lineage, deployment, development,
error-resilience, module-dependency, operational, process-flow,
repository-access, scenarios, security, state-lifecycle
```

Return 1–3 lens names. Apply the same selection criteria and `development` lens guard
as `open-pr`:

**Development lens guard:** Only select `development` if at least one changed file matches:
`pyproject.toml`, `Taskfile*`, `conftest.py`, `.github/workflows/*`, `Makefile`,
`setup.cfg`, `setup.py`, `tox.ini`, `noxfile.py`, or files under `ci/`.

For a promotion PR, prefer lenses that show the broadest architectural impact:
- `module-dependency` → if changes span multiple packages
- `process-flow` → if workflow routing or state transitions changed
- `c4-container` → if new services, tools, or integrations were added

### Step 14: Generate Arch-Lens Diagrams

For each selected lens, follow this exact sequence:

**CRITICAL:** Do NOT output any prose status text between lens iterations.
After completing all sub-steps for one lens, immediately begin sub-step 1 for the
next lens.

**1. Write the PR context to a file using the Write tool:**

- **Path:** `temp/open-pr-main/pr_arch_lens_context_{YYYY-MM-DD_HHMMSS}.md`
- **Content:**

```markdown
# PR Context — Integration → Main Promotion

This diagram is for a promotion PR merging the integration branch into main. Focus on the areas of the codebase affected by all accumulated changes. Do not create a generic whole-project diagram.

## New files (use ★ prefix on these nodes):
{list of new_files from Step 6, or "None"}

## Modified files (use ● prefix on these nodes):
{list of modified_files from Step 6, or "None"}

## Deleted files:
{list of deleted_files from Step 6, or "None"}

## Instructions:
- Focus exploration and the diagram on the architectural areas these files belong to
- Use `★` prefix on nodes representing new files/components
- Use `●` prefix on nodes representing modified files/components
- Mark deleted components with strikethrough or a `✗` prefix
- Leave unchanged components unmarked (include only if needed for context/connectivity)
- This is a promotion PR — show the cumulative architectural impact of all changes
```

**2. Immediately call the Skill tool to load the arch-lens skill** (e.g.,
`/autoskillit:arch-lens-module-dependency`).

**3. Follow the loaded skill's instructions** to generate the diagram.

Read the output from `temp/arch-lens-{lens-name}/` and extract the mermaid block(s).

Validate: if the block contains at least one `★` or `●` → add to `validated_diagrams`.
Otherwise discard.

### Step 15: Compose PR Body

Write to `temp/open-pr-main/pr_body_{timestamp}.md` (relative to the current working directory).

```markdown
## Promotion: integration → main

{executive.executive_summary}

**Stats:** {diff_stat_summary} across {commit_count} commits from {len(pr_list)} PRs

### Highlights

{For each item in executive.highlights:}
- {item}

{If executive.risk_areas is non-empty:}
### Areas Requiring Review

{For each item in executive.risk_areas:}
- {item}

## Merged PRs

| PR | Title | Author | Labels |
|----|-------|--------|--------|
{For each pr in pr_list:}
| [#{pr.number}]({pr.url}) | {pr.title} | @{pr.author.login} | {comma-joined label names, or "—"} |

## Linked Issues

{If linked_issue_numbers is non-empty:}
| Issue | Title | Status | Action |
|-------|-------|--------|--------|
{For each issue in issue_details:}
| [#{issue.number}]({issue.url}) | {issue.title} | {issue.state} | {"Will close on merge" if OPEN else "Already closed"} |

{If linked_issue_numbers is empty:}
No linked issues found in PR descriptions.

{If domain_summaries is non-empty:}
## Domain Analysis

{For each entry in domain_summaries (ordered by domain name):}
### {entry.domain}

{entry.summary}

**Key changes:**
{For each item in entry.key_changes:}
- {item}

{If entry.breaking_changes is non-empty:}
**Breaking changes:**
{For each item in entry.breaking_changes:}
- ⚠️ {item}

**Contributing PRs:** {comma-separated [#{N}](url) for each N in entry.pr_numbers, or "—"}
**Commits:** {entry.commit_count} commit(s)

{If validated_diagrams is non-empty:}
## Architecture Impact

{For each validated diagram:}
### {Lens Name} Diagram

```mermaid
{diagram content}
```

{For each item in closing_refs:}
{item}

---

<sub>🤖 Generated with [Claude Code](https://claude.com/claude-code) via AutoSkillit</sub>
```

### Step 16: Check GitHub Availability

```bash
gh auth status 2>/dev/null
```

If exit code non-zero: output `pr_url = ` and exit successfully.

### Step 17: Create Promotion PR

Construct a PR title: `Promote integration → main ({len(pr_list)} PRs, {len(linked_issue_numbers)} issues)`

```bash
gh pr create \
  --base {base_branch} \
  --head {integration_branch} \
  --title "{pr_title}" \
  --body-file temp/open-pr-main/pr_body_{timestamp}.md
```

Capture the PR URL as `pr_url`.

### Step 18: Add Labels (optional)

If the PR was created successfully, attempt to label it:

```bash
gh pr edit {pr_url} --add-label "promotion" 2>/dev/null
```

Continue if this fails (label may not exist).

### Output

```
pr_url = {pr_url}
```
