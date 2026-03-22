---
name: open-integration-pr
categories: [github]
description: >
  Create an integration PR for the merge-prs. Reads pr_order_file JSON, generates
  a rich PR body with per-PR details, arch-lens diagrams, and carried-forward Closes #N
  references. Closes all collapsed PRs with a comment after creation. Use inside the
  merge-prs after all PRs have been merged into the integration branch.
---

# Open Integration PR

Read `pr_order_file` JSON produced by `analyze-prs`, generate a rich PR description
(per-PR details, complexity tags, merge outcomes, optional audit verdict), generate 1–3
arch-lens diagrams, carry forward `Closes #N`/`Fixes #N` references from original PR
bodies so linked issues auto-close on merge, create the integration PR via
`gh pr create --body-file`, close each collapsed PR with a comment referencing the new
PR, and output `pr_url=<url>`.

## Arguments

```
/autoskillit:open-integration-pr {integration_branch} {base_branch} {pr_order_file} [audit_verdict] [conflict_report_paths]
```

- `integration_branch` — integration branch name (e.g. `pr-batch/pr-merge-20250228-143052`)
- `base_branch` — PR target branch (e.g. `main`)
- `pr_order_file` — absolute path to JSON produced by `analyze-prs`
- `audit_verdict` (optional) — `GO`, `NO GO`, or empty string when audit was skipped
- `conflict_report_paths` (optional) — comma-separated list of absolute paths to conflict resolution report files, produced by `resolve-merge-conflicts`. When provided and non-empty, embed a "Conflict Resolution Decisions" section in the PR body.

## When to Use

- Called by `merge-prs` after all PRs have been merged into the integration branch
- Invoked via `run_skill` as the final step before CI watch

## Critical Constraints

**NEVER:**
- Create files outside `temp/open-integration-pr/` (except the temp body file for `gh pr create --body-file`)
- Modify any source code
- Fail the pipeline if `gh` is unavailable or not authenticated — output `pr_url=` (empty) and exit successfully
- Close original PRs before the integration PR is successfully created

**ALWAYS:**
- Check `gh auth status` before attempting any GitHub operations
- Output `pr_url=<url>` on the last output line (empty string when GitHub unavailable)
- Carry forward ALL `Closes #N` and `Fixes #N` lines found in original PR bodies
- Use `gh pr create --body-file` (never inline body via `--body`)

## Workflow

### Step 1: Parse Arguments

Parse four positional args: `integration_branch`, `base_branch`, `pr_order_file`,
`audit_verdict` (last one may be absent or empty string). Parse the optional fifth
positional argument `conflict_report_paths` (may be absent or empty string). Split on `,`
to get a list of paths; filter out any empty strings. Store as `conflict_report_path_list`.

### Step 2: Read pr_order_file

Read the JSON file. Extract: `prs` array (each: `number`, `title`, `branch`,
`complexity`, `additions`, `deletions`, `overlap_with_pr_numbers`, `files_changed`). Also read
`base_branch` from JSON as confirmation. Store the PR list as `pr_list`.

### Step 3: Fetch Closes/Fixes References from Original PR Bodies

For each PR in `pr_list`:

```bash
gh pr view {number} --json body -q .body 2>/dev/null
```

Extract every line matching `(Closes|Fixes|Resolves)\s+#\d+` (case-insensitive).
Deduplicate across all PRs. Store as `closing_refs` (list of strings like `Closes #42`).
Skip gracefully if `gh` is unavailable — `closing_refs` remains empty.

### Step 4: Get Changed Files

```bash
git diff --name-only {base_branch}..{integration_branch}
git diff --diff-filter=A --name-only {base_branch}..{integration_branch}
git diff --diff-filter=M --name-only {base_branch}..{integration_branch}
```

Store as `changed_files`, `new_files`, `modified_files`.

### Step 4b: Load Conflict Resolution Reports

- If `conflict_report_path_list` is empty: skip — set `conflict_resolution_table = ""`.
- For each path in `conflict_report_path_list`:
  - Read the file.
  - Extract the `## Per-File Resolution Decisions` table (all lines from the `| File |` header
    through the last table row).
- Concatenate all extracted tables (one per report, separated by a blank line if multiple).
- Store as `conflict_resolution_table`.

This step is skipped gracefully if any path is missing — log a warning and exclude that file.

### Step 4c: Partition Files by Domain

```bash
python3 -c "
from autoskillit.execution.pr_analysis import partition_files_by_domain
import json, sys
files = json.loads(sys.argv[1])
result = partition_files_by_domain(files)
print(json.dumps(result))
" '["path/to/file.py", ...]'
```

Pass `changed_files` as a JSON array argument. Store the parsed dict as `domain_partitions`.
Skip entirely and set `domain_partitions = {}` if `changed_files` is empty.

### Step 4d: Fetch Domain Diffs (parallel)

For each domain name `D` in `domain_partitions` where `domain_partitions[D]` is non-empty,
run the following in parallel (issue all Bash calls in a single message):

```bash
git diff {base_branch}..{integration_branch} -- {space-separated list of files in domain D}
```

Store results as `domain_diffs: dict[str, str]` mapping domain name → diff text.
If a domain's diff text exceeds 12 000 characters, truncate to the first 12 000 characters
and append `\n... [truncated — diff exceeds 12 000 chars]`. Domains with empty diffs are
removed from `domain_diffs`.

### Step 4e: Identify PRs per Domain

For each domain `D` in `domain_partitions`, find every PR in `pr_list` whose
`files_changed` list intersects with `domain_partitions[D]`.

```python
domain_pr_numbers = {
    domain: [
        pr["number"]
        for pr in pr_list
        if set(pr.get("files_changed", [])) & set(domain_partitions[domain])
    ]
    for domain in domain_partitions
}
```

Store as `domain_pr_numbers: dict[str, list[int]]`.

### Step 4f: Fetch Domain Commits (parallel)

For each domain `D` in `domain_diffs` (domains that actually have diff content), run in
parallel (all Bash calls in a single message):

```bash
git log {base_branch}..{integration_branch} --oneline -- {space-separated files in domain D}
```

Store as `domain_commits: dict[str, list[str]]` (each entry is a list of `"sha message"` strings).
Empty results are stored as empty lists.

### Step 4g: Run Parallel Domain Analysis Subagents

For each domain `D` in `domain_diffs`, spawn a Task subagent (model: sonnet) in a single
parallel message. **Issue all Task calls in a single message** to maximize parallelism.
**Skip domains with no diff content** (not in `domain_diffs`) — do not spawn subagents for them.

Each subagent receives a prompt with:
- The domain name
- The list of files changed in the domain
- The diff content (already truncated at 12 000 chars)
- The PR numbers and titles for PRs touching this domain (look up titles from `pr_list`)
- The commit one-liners for the domain

The subagent is instructed to return ONLY a JSON object with this exact shape:

```json
{
  "domain": "Server/MCP Tools",
  "summary": "3-4 sentence description of what changed and why it matters",
  "key_changes": ["concise description of change 1", "concise description of change 2"],
  "pr_numbers": [42, 47],
  "commit_count": 5
}
```

Parse each subagent's output as JSON. If parsing fails for a domain, log a warning and
omit that domain from `domain_summaries`. Store the collected results as
`domain_summaries: list[dict]`.

The 7 canonical domain names are: **Server/MCP Tools**, **Pipeline/Execution**,
**Recipe/Validation**, **CLI/Workspace**, **Skills**, **Tests**, **Core/Config/Infra**.

### Step 5: Select Arch-Lens Lenses

Spawn a subagent (Task tool, model: sonnet) with `changed_files` and the same lens
menu as `open-pr`. Instruct it to return 1–3 lens names using the same `development`
lens guard.

### Step 6: Generate Arch-Lens Diagrams

For each selected lens, follow this exact sequence:

**CRITICAL:** Do NOT output any prose status text between lens iterations.
After completing all sub-steps for one lens (including mermaid extraction and
validation), immediately begin sub-step 1 (Write the PR context file) for the
next lens. Progress announcements like "Diagram generated. Now calling X:"
create end_turn windows that cause stochastic session termination.

**1. Write the PR context to a file using the Write tool:**

- **Path:** `temp/open-integration-pr/pr_arch_lens_context_{YYYY-MM-DD_HHMMSS}.md`
- **Content:** The following PR context block, with placeholders filled in:

```markdown
# PR Context — Changed Files

This diagram is for a Pull Request. Focus the diagram on the areas of the codebase affected by these changes. Do not create a generic whole-project diagram.

## New files (use ★ prefix on these nodes):
{list of new_files from Step 4, or "None"}

## Modified files (use ● prefix on these nodes):
{list of modified_files from Step 4, or "None"}

## Instructions:
- Focus exploration and the diagram on the architectural areas these files belong to
- Use `★` prefix on nodes representing new files/components
- Use `●` prefix on nodes representing modified files/components
- Leave unchanged components unmarked (include them only if needed for context/connectivity)
- The diagram should help PR reviewers understand the architectural impact of these specific changes
```

**2. Immediately call the Skill tool to load the arch-lens skill** (e.g., `/autoskillit:arch-lens-module-dependency`).
The loaded skill will read the PR context file written in step 1 above.

**3. Follow the loaded skill's instructions** to explore the codebase and generate the diagram.

The arch-lens skills write their output to `temp/arch-lens-{lens-name}/` (relative to the current working directory). After each skill
runs, read the generated markdown file and extract the mermaid code block(s).

After extracting the mermaid block, inspect its content for `★` or `●` characters:
- If the block contains at least one `★` or `●` → add it to `validated_diagrams`.
- If the block contains neither → discard this diagram; do not add it to the list.

### Step 7: Compose PR Body

Write to `temp/open-integration-pr/pr_body_{timestamp}.md`. (relative to the current working directory)

```markdown
## Integration Summary

Collapsed {N} PRs into `{integration_branch}` targeting `{base_branch}`.

## Merged PRs

| # | Title | Complexity | Additions | Deletions | Overlaps |
|---|-------|-----------|-----------|-----------|---------|
| #{number} | {title} | {complexity} | +{additions} | -{deletions} | {overlap_with_pr_numbers or "—"} |
...

{If domain_summaries is non-empty:}
## Domain Analysis

{For each entry in domain_summaries (ordered by domain name):}
### {entry.domain}

{entry.summary}

**Key changes:**
{For each item in entry.key_changes:}
- {item}

**Contributing PRs:** {comma-separated #{N} for each N in entry.pr_numbers, or "—" if empty}
**Commits:** {entry.commit_count} commit(s)

{If audit_verdict is non-empty:}
## Audit

**Verdict:** {audit_verdict}

{If conflict_resolution_table is non-empty:}
## Conflict Resolution Decisions

The following files had merge conflicts that were automatically resolved during pipeline integration.

{conflict_resolution_table}

{If validated_diagrams non-empty:}
## Architecture Impact

{For each validated diagram:}
### {Lens Name} Diagram

```mermaid
{diagram content}
```

{For each item in closing_refs:}
{Closes #N}

🤖 Generated with [Claude Code](https://claude.com/claude-code) via AutoSkillit
```

### Step 8: Check GitHub Availability

```bash
gh auth status 2>/dev/null
```

If exit code non-zero: output `pr_url=` and exit successfully.

### Step 9: Create Integration PR

```bash
gh pr create \
  --base {base_branch} \
  --head {integration_branch} \
  --title "Integration: collapsed PRs #{numbers} into {base_branch}" \
  --body-file temp/open-integration-pr/pr_body_{timestamp}.md
```

`{numbers}` = comma-separated PR numbers (e.g., `#42, #47, #51`).
Capture the new PR URL as `new_pr_url`. Extract the PR number from the URL as
`new_pr_number`.

### Step 10: Close Original PRs

For each PR in `pr_list`:

```bash
gh pr close {number} --comment "Collapsed into integration PR #{new_pr_number} ({new_pr_url})"
```

Continue even if individual close operations fail (log warning, do not exit).

### Output

```
pr_url = {new_pr_url}
```