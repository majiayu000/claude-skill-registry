---
name: enrich-issues
categories: [github]
description: >
  Backfill structured requirements on existing GitHub issues triaged with
  recipe:implementation labels. Scans candidates, skips already-enriched issues,
  performs codebase-grounded analysis, and appends a Requirements section in
  REQ-{GRP}-NNN format via gh issue edit.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: enrich-issues] Enriching issues...'"
          once: true
---

# enrich-issues Skill

Backfill `## Requirements` sections on existing GitHub issues labelled
`recipe:implementation`. Complements `prepare-issue` (which enriches at creation
time) by handling the pre-existing backlog.

## Interface

```
/autoskillit:enrich-issues [--issue N] [--batch N] [--dry-run] [--repo owner/repo]
```

- `--issue N` — enrich a single issue by number
- `--batch N` — filter by `batch:N` label in addition to `recipe:implementation`
- `--dry-run` — preview generated requirements without editing issues
- `--repo owner/repo` — override the default repository

## Workflow

### Step 0: Parse Arguments

Parse ARGUMENTS for:
- `--issue N` → set `issue_number = N`
- `--batch N` → set `batch = N`
- `--dry-run` → set `dry_run = true`
- `--repo owner/repo` → set `repo = "owner/repo"`

### Step 1: Authenticate

```bash
gh auth status
```

Fail fast with a clear error if authentication is not available. Do not proceed
past this step if auth fails.

### Step 2: Resolve Repo

If `--repo owner/repo` was provided, use it. Otherwise use `gh`'s default repo
context:

```bash
gh repo view --json nameWithOwner -q .nameWithOwner
```

### Step 3: Fetch Candidates

**Single issue (`--issue N`):**
```bash
gh issue view N --json number,title,body,labels
```
Wrap as a single-element list.

**Batch (`--batch N`):**
```bash
gh issue list \
    --label "recipe:implementation" \
    --label "batch:N" \
    --json number,title,body,labels \
    --limit 100
```

**Default (no flags):**
```bash
gh issue list \
    --label "recipe:implementation" \
    --json number,title,body,labels \
    --limit 100
```

### Step 4: Idempotency Filter

For each candidate issue, check whether its body already contains
`## Requirements`.

- If the body **already contains** `## Requirements`: skip it, add its number to
  `skipped_already_enriched`. Log: `"Issue #N already enriched — skipping."`
- If the body **does not contain** `## Requirements`: add to candidates list.

If no candidates remain after filtering, emit the result block immediately and exit.

### Step 5: Per-Issue Analysis

Process up to 8 candidates in parallel using subagents (`model: "sonnet"`).
For each candidate:

#### 5a. Fetch Full Content

```bash
gh issue view N --comments --json body,comments,title,labels
```

#### 5b. Codebase Cross-Reference

Search the codebase for files, modules, and system names mentioned in the issue
title and body. Verify claims against actual code before incorporating them into
requirements. Do not invent codebase details.

#### 5c. Assess Enrichability

Classify the issue into one of three categories:

**Too vague** — cannot extract clear acceptance criteria (e.g., "improve X", no
measurable outcome, contradictory claims):
- Post a clarifying comment:
  ```bash
  gh issue comment N --body "This issue needs more detail before requirements
  can be generated. Consider: What is the expected outcome? What signals success?
  If the goal is unclear, relabeling to \`recipe:remediation\` may be appropriate
  for investigation first."
  ```
- Add to `skipped_too_vague`. Do not edit the issue body.

**Mixed concerns** — the issue describes two or more independently-completable
sub-features or mixes a bug fix with a new feature:
- Post a comment:
  ```bash
  gh issue comment N --body "This issue mixes independent concerns. Consider
  running \`/autoskillit:issue-splitter\` to split it into focused sub-issues
  before enrichment."
  ```
- Add to `skipped_mixed_concerns`. Do not edit the issue body.

**Well-defined** — a single, coherent goal with extractable acceptance criteria:
- Proceed to requirement generation (Step 5d).

#### 5d. Generate Requirements

Requirements are **acceptance criteria**, not implementation steps.

Rules:
- State observable, testable outcomes: "The system must X" not "Do X"
- Group by co-implementation concern. Name each group with a short uppercase
  abbreviation (2–5 letters, e.g., AUTH, API, DATA, CLI, UI)
- Format: `**REQ-{GRP}-NNN:** {single-sentence condition}.`
  - NNN is zero-padded and resets per group (001, 002, ...)
- Include a brief per-group background paragraph before the requirement list
- Verify all codebase references against actual code found in Step 5b

Example output structure:
```
## Requirements

### API Layer

The API layer exposes skill execution to MCP clients through the headless executor.

- **REQ-API-001:** The `enrich_issues` tool must accept `issue_number`, `batch`,
  `dry_run`, and `repo` parameters.
- **REQ-API-002:** The tool must be gated behind `open_kitchen`.

### Data Model

...
```

#### 5e. Apply or Preview

- If `--dry-run`: print the generated `## Requirements` section to stdout. Do
  **not** call `gh issue edit`. Set `dry_run: true` in the result.
- Otherwise: append the section to the original issue body:
  ```bash
  gh issue edit N --body "$(gh issue view N --json body -q .body)

## Requirements

$(generated_requirements_section)"
  ```

  Always fetch the current body immediately before editing to avoid overwriting
  concurrent changes.

### Step 6: Emit Result Block

After processing all candidates, emit to stdout:

```
---enrich-issues-result---
{
  "enriched": [{"issue_number": N, "requirements_count": M, "groups": ["GRP1", "GRP2"]}],
  "skipped_already_enriched": [N, ...],
  "skipped_too_vague": [N, ...],
  "skipped_mixed_concerns": [N, ...],
  "dry_run": true|false
}
---/enrich-issues-result---
```

## Critical Constraints

**NEVER:**
- Edit an issue body without first fetching its current content immediately before
  the edit
- Force requirements when the issue is too vague — comment and move on
- Apply `## Requirements` to an issue that already has one (idempotency)
- Skip the result block — always emit it, even on dry-run or when all issues were
  skipped

**ALWAYS:**
- Respect `--dry-run`: never call `gh issue edit` when this flag is set
- Verify codebase claims before incorporating them into requirements
- Use `model: "sonnet"` for per-issue analysis subagents
- Emit the `---enrich-issues-result---` block as the final output
