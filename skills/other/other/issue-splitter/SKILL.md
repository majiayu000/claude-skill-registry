---
name: issue-splitter
categories: [github]
description: >
  Analyze a GitHub issue for mixed concerns and split it into focused sub-issues
  with proper cross-references. Integrates into triage-issues as a pre-classification step.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: issue-splitter] Analyzing issue for mixed concerns...'"
          once: true
---

# issue-splitter Skill

Analyze a single GitHub issue for distinct concerns, classify each by recipe route, and—when concerns route differently—create focused sub-issues with bidirectional cross-references. The parent issue is left open as a tracking issue.

This skill is intentionally lightweight: concern analysis is performed as in-context LLM reasoning. No subagents are used.

## When to Use

- Invoked by `triage-issues` as a parallel per-issue pre-classification step
- Directly by a user who suspects an issue mixes bug fixes and feature requests
- With `--dry-run` to preview what would be split without mutating GitHub

## Arguments

```
/autoskillit:issue-splitter --issue N [--url URL] [--repo owner/repo] [--no-label] [--dry-run] [--max-sub-issues N]
```

- `--issue N` — issue number to analyze (required, OR `--url`)
- `--url URL` — full GitHub issue URL (alternative to `--issue`; number extracted automatically)
- `--repo owner/repo` — target repository (optional; defaults to `gh` repo context)
- `--no-label` — skip all GitHub label/comment/create mutations; only emit analysis result
- `--dry-run` — analyze and show what would be split, but skip GitHub mutations
- `--max-sub-issues N` — maximum sub-issues to create (default: 4)

## Critical Constraints

**NEVER:**
- Use subagents — concern analysis is in-context LLM reasoning, not subagent delegation
- Close the parent issue — it becomes a tracking issue
- Apply `batch:N` labels to any GitHub object
- Create files outside `temp/issue-splitter/` (for any dry-run reports)

**ALWAYS:**
- Use `--force` on all `gh label create` calls for idempotency
- Respect `--no-label` and `--dry-run` (skip all GitHub mutations when either is set)
- Cap sub-issues at `--max-sub-issues` (default: 4)
- Emit the result block even on dry-run or no-split decisions

## Workflow

### Step 0 — Parse Arguments

Extract from ARGUMENTS:
- `--issue N` → `issue_number = N`
- `--url URL` → extract number with `echo URL | grep -oE '[0-9]+$'` → `issue_number`
- `--repo owner/repo` → `repo = "owner/repo"` (omit `--repo` flag from gh commands if not provided)
- `--no-label` → `no_label = true`
- `--dry-run` → `dry_run = true`
- `--max-sub-issues N` → `max_sub_issues = N` (default: 4)

Fail fast if neither `--issue` nor `--url` is provided:
```
decision = error, rationale = "--issue N or --url URL is required"
```

### Step 1 — Authenticate

```bash
gh auth status
```

If auth fails, emit result block with `decision=error, rationale="gh auth failed"` and exit.

### Step 2 — Fetch Issue

```bash
gh issue view {N} [--repo {repo}] --json number,title,body,labels,url,state
```

Handle these guard conditions:
- If issue not found: emit `decision=error, rationale="issue not found"` and exit.
- If `state == "closed"`: emit `decision=no-split, rationale="issue is closed"` and exit.
- If the label list contains `"split"`: emit `decision=no-split, rationale="already split"` and exit.

### Step 3 — LLM Concern Analysis

Analyze the issue `title + body` to enumerate distinct concerns. For each concern identify:

- **Summary**: one sentence describing the concern
- **Type**: `bug` | `feature` | `investigation` | `refactor` | `docs`
- **Recipe route**: classify using the behavioral heuristic:
  - Existing behavior broken / error traceback / unclear root cause → `recipe:remediation`
  - New capability / enhancement / clearly unimplemented feature → `recipe:implementation`
  - "X doesn't support Y" / missing config / missing validation → `recipe:implementation`
  - "X crashes" / wrong result / unknown cause → `recipe:remediation`
- **Affected component(s)**: brief list

This step is in-context reasoning only — do not spawn subagents.

### Step 4 — Split Decision

Apply these rules in order:

1. If only 1 concern identified → **no-split**, proceed to Step 5.
2. If all concerns share the same recipe route → **no-split**, proceed to Step 5.
3. If concerns route differently → **split**, proceed to Step 6.

**Cap enforcement:** If more than `max_sub_issues` distinct concerns are found, merge the lowest-priority same-route concerns into a single combined sub-issue rather than dropping them.

### Step 5 — No-split Path

Emit result block:

```
---issue-splitter-result---
{
  "decision": "no-split",
  "original_issue": {"number": N, "url": "https://github.com/..."},
  "route": "recipe:implementation",
  "rationale": "All concerns route to recipe:implementation"
}
---/issue-splitter-result---
```

Exit. No GitHub mutations.

### Step 6 — Dry-run / no-label Path

If `--dry-run` or `--no-label` is set, emit the split result block with `sub_issues` populated with what *would* be created, but skip all GitHub mutations. Proceed directly to Step 9.

### Step 7 — Create Sub-issues

For each concern (up to `max_sub_issues`):

```bash
# Ensure the split-from label exists (idempotent)
gh label create "split-from:#N" --force \
  --description "Sub-issue created from parent #N" \
  --color "e4e669" [--repo {repo}]

# Ensure the recipe route label exists (idempotent)
gh label create "recipe:implementation" --force \
  --description "Route through implementation recipe" \
  --color "0E8A16" [--repo {repo}]
# or:
gh label create "recipe:remediation" --force \
  --description "Route through remediation recipe" \
  --color "D93F0B" [--repo {repo}]

# Create the sub-issue
gh issue create \
  --title "{concern summary} (from #{N})" \
  --body "{concern description}\n\n---\n_Split from #{parent_url}_" \
  --label "split-from:#N" \
  --label "recipe:{route}" \
  [--repo {repo}]
```

Capture the new issue URL and number from stdout.

### Step 8 — Label Parent and Add Tracking Comment

```bash
# Ensure the split label exists (idempotent)
gh label create "split" --force \
  --description "Issue decomposed into focused sub-issues" \
  --color "0075ca" [--repo {repo}]

# Label the parent as split
gh issue edit {N} --add-label "split" [--repo {repo}]

# Add tracking comment with cross-references
gh issue comment {N} \
  --body "## Split into sub-issues

This issue covers multiple concerns and has been decomposed into focused sub-issues:

{bullet list of sub-issue links with route labels}

This issue remains open as a tracking issue." \
  [--repo {repo}]
```

Do **not** close the parent — it serves as a tracking issue for all sub-issues.

### Step 9 — Emit Result Block

Output to stdout for `triage-issues` subagent parsing:

**Split result:**
```
---issue-splitter-result---
{
  "decision": "split",
  "original_issue": {"number": N, "url": "https://github.com/.../issues/N"},
  "sub_issues": [
    {
      "number": M,
      "url": "https://github.com/.../issues/M",
      "route": "recipe:implementation",
      "concern": "One-sentence summary of this concern",
      "title": "Concern title (from #N)"
    }
  ],
  "rationale": "Issue contained both a bug (remediation) and a feature request (implementation)"
}
---/issue-splitter-result---
```

**No-split result:**
```
---issue-splitter-result---
{
  "decision": "no-split",
  "original_issue": {"number": N, "url": "https://github.com/.../issues/N"},
  "route": "recipe:implementation",
  "rationale": "All concerns route to recipe:implementation"
}
---/issue-splitter-result---
```

**Error result:**
```
---issue-splitter-result---
{
  "decision": "error",
  "original_issue": {"number": N, "url": null},
  "rationale": "Description of what went wrong"
}
---/issue-splitter-result---
```

## Output Location

Dry-run reports (if any): `temp/issue-splitter/`

## Error Handling

- Auth failure → emit error result, exit
- Issue not found → emit error result, exit
- `gh issue create` fails → log the failure, emit partial split result with `"error"` noted in rationale, do not abort silently
