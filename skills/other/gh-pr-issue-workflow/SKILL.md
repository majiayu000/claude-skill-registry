---
name: gh-pr-issue-workflow
description: Create or update GitHub issues and PRs using the gh CLI, especially when writing Markdown bodies (backticks, code blocks, lists) that must be preserved. Use this when asked to create/edit issues or PRs, or to fix PR/issue formatting. Emphasize --body-file or single-quoted heredocs to avoid shell interpolation, and follow the repo's PR/issue structure (summary, testing, closing keywords).
---

# GitHub PR/Issue Workflow

## Rules of thumb

- Use `--body-file` or a single-quoted heredoc to avoid bash interpreting backticks.
- Prefer editing existing items with `gh issue edit` / `gh pr edit` rather than recreating.
- Keep PR and issue bodies concise and structured.
- All GitHub issues/PRs must be written in English.
- Always apply labels when creating issues. Use `type/*`, `priority/*`, and `area/*` labels.
- If the type or priority is unclear, ask; if you must proceed, default to `type/triage`.
- PRs must always include a closing keyword for the corresponding issue (e.g., `Closes #<issue>`).
- **ALWAYS link child issues as GitHub sub-issues** when creating issues under an epic/parent. After creating child issues, use the Sub-Issues API (see below) to add them as sub-issues of the parent. Never rely on "Part of #N" text alone — always create the actual sub-issue relationship via the API.

## Issue template (example)

```text
## Description
[Problem and impact]

## Context
[Where/when it happens]

## Repro
1) ...
2) ...

## Proposed Fix
- ...

## Acceptance Criteria
- ...
```

## PR template (example)

```text
## Summary
- ...

## Testing
- Not run (not requested)

Closes #<issue>
```

## Safe gh commands

Create an issue (with labels):

```bash
cat > /tmp/issue.md <<'EOF_ISSUE'
## Description
...
EOF_ISSUE

gh issue create --title "<title>" --body-file /tmp/issue.md \
  --label "type/feature,priority/p2,area/insights"
```

Create a PR:

```bash
cat > /tmp/pr.md <<'EOF_PR'
## Summary
- ...

## Testing
- ...

Closes #123
EOF_PR

gh pr create --title "<title>" --body-file /tmp/pr.md --base <base> --head <branch>
```

Update a PR/issue body:

```bash
gh pr edit <number> --body-file /tmp/pr.md
# or
gh issue edit <number> --body-file /tmp/issue.md
```

## Sub-Issues (Parent-Child Relationships)

GitHub supports native sub-issues for creating hierarchical issue structures (epics → sub-epics → tasks).

### Get Database IDs for Issues

Sub-issues API requires database IDs (integers), not node IDs. Get them via GraphQL:

```bash
gh api graphql -f query='
{
  repository(owner: "anyeloamt", name: "expense-ai") {
    issue(number: 165) { databaseId }
  }
}' | jq -r '.data.repository.issue.databaseId'
```

For multiple issues at once:

```bash
gh api graphql -f query='
{
  repository(owner: "anyeloamt", name: "expense-ai") {
    i1: issue(number: 165) { databaseId }
    i2: issue(number: 166) { databaseId }
    i3: issue(number: 167) { databaseId }
  }
}' | jq -r '.data.repository'
```

### Add Sub-Issue to Parent

```bash
# Add issue as sub-issue of parent
gh api repos/{owner}/{repo}/issues/{parent_number}/sub_issues \
  -X POST \
  -F sub_issue_id={child_database_id}

# Example: Add #165 (db_id: 3883231808) as sub-issue of #162
gh api repos/anyeloamt/expense-ai/issues/162/sub_issues \
  -X POST \
  -F sub_issue_id=3883231808
```

### Batch Add Sub-Issues

```bash
# Add multiple sub-issues to a parent epic
PARENT=162
for child_db_id in 3883231808 3883232262 3883232716; do
  gh api repos/anyeloamt/expense-ai/issues/$PARENT/sub_issues \
    -X POST \
    -F sub_issue_id=$child_db_id
done
```

### List Sub-Issues of a Parent

```bash
gh api repos/{owner}/{repo}/issues/{parent_number}/sub_issues \
  | jq -r '.[] | "#\(.number): \(.title)"'
```

### Remove Sub-Issue from Parent

```bash
gh api repos/{owner}/{repo}/issues/{parent_number}/sub_issues/{child_number} \
  -X DELETE
```

### Typical Epic Hierarchy

```
📦 Super Epic (e.g., #161)
├── 📁 Sub-Epic A (e.g., #162)
│   ├── Task 1 (#165)
│   ├── Task 2 (#166)
│   └── Task 3 (#167)
├── 📁 Sub-Epic B (e.g., #163)
│   └── ...
└── 📁 Sub-Epic C (e.g., #164)
    └── ...
```

### Workflow for Creating Issue Hierarchy (MANDATORY for epics)

Whenever creating child issues under a parent/epic, ALWAYS follow ALL steps — especially steps 4-6. Skipping the API linking step is NOT acceptable.

1. Create the parent/epic issue
2. Create child issues (sub-epics or tasks)
3. Get database IDs for all child issues via GraphQL
4. **Link children as sub-issues via the REST API** (this step is REQUIRED, not optional)
5. Verify links via `gh api repos/{owner}/{repo}/issues/{parent}/sub_issues`

```bash
# Step 1-3: Create issues normally with gh issue create

# Step 4: Get database IDs
gh api graphql -f query='{ repository(owner: "anyeloamt", name: "expense-ai") {
  e162: issue(number: 162) { databaseId }
  e163: issue(number: 163) { databaseId }
}}' | jq '.data.repository'

# Step 5-6: Add sub-issues
gh api repos/anyeloamt/expense-ai/issues/161/sub_issues -X POST -F sub_issue_id=<db_id>
```
