---
name: github-issue
description: Use when creating GitHub issues, breaking down work into issues, or when asked to file a bug report or feature request
---

# Creating GitHub Issues

Create focused, self-contained GitHub issues that an external contributor could implement without additional context.

## Decision Flow

```
Work requested
    │
    ▼
Single clear goal? ──yes──> Create single issue
    │
    no
    │
    ▼
Spans multiple layers? ──yes──> Create epic with sub-issues
```

## Scope Boundaries (CRITICAL)

**Stick to what was requested.** Create issues ONLY for the requested feature. Do NOT expand into adjacent features.

When Feature X depends on Feature Y:

- Create minimal stub for Y (just enough to unblock X)
- ASK user if they want a separate epic for Y

**ASK before proceeding when:**

1. Adjacent features detected
2. Ambiguous boundaries
3. Multiple interpretations possible
4. Feature seems too large (10+ issues)

## Workflow

### 1. Clarify Scope

ASK user about boundaries before drafting.

### 2. Review Preference

Use `AskUserQuestion`:

- **"Review first" (Recommended)**: Create preview file in scratchpad for feedback before creating issues
- **"Create directly"**: Create issues immediately with `needs-review` label added via `gh issue edit <num> --add-label "needs-review"` after creation

### 3. Create Issues (Single Script)

Use GraphQL API for reliable creation (see `./graphql-api.md`).

**CRITICAL**: Execute ALL operations in a SINGLE bash script to minimize permission prompts. This includes:

1. Getting repo info
2. Getting repo ID
3. Creating epic
4. Creating all sub-issues
5. Linking sub-issues to epic
6. Adding labels

```bash
#!/bin/bash
# ALL OPERATIONS IN ONE SCRIPT - Single permission prompt

set -e

# 1. Get repo info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
OWNER=$(echo "$REPO" | cut -d'/' -f1)
NAME=$(echo "$REPO" | cut -d'/' -f2)

# 2. Get repo ID
REPO_ID=$(gh api graphql -f query="query { repository(owner: \"$OWNER\", name: \"$NAME\") { id } }" -q '.data.repository.id')

# 3. Create epic
EPIC=$(gh api graphql -f query='
mutation($repoId: ID!, $title: String!, $body: String!) {
  createIssue(input: { repositoryId: $repoId, title: $title, body: $body }) {
    issue { number id }
  }
}' -f repoId="$REPO_ID" -f title="[Context] Epic: Feature Name" -f body="$(cat <<'EOF'
## Objective
Epic description here...

## Sub-Issues
- [ ] Sub-issue 1
- [ ] Sub-issue 2
EOF
)")
EPIC_NUM=$(echo "$EPIC" | jq -r '.data.createIssue.issue.number')
EPIC_ID=$(echo "$EPIC" | jq -r '.data.createIssue.issue.id')

# 4. Create sub-issues
ISSUE1=$(gh api graphql -f query='
mutation($repoId: ID!, $title: String!, $body: String!) {
  createIssue(input: { repositoryId: $repoId, title: $title, body: $body }) {
    issue { number id }
  }
}' -f repoId="$REPO_ID" -f title="[Context] Sub-issue 1" -f body="Issue body...")
ISSUE1_NUM=$(echo "$ISSUE1" | jq -r '.data.createIssue.issue.number')
ISSUE1_ID=$(echo "$ISSUE1" | jq -r '.data.createIssue.issue.id')

# Continue for all sub-issues...

# 5. Link sub-issues (attempt - may not be available on all repos)
gh api graphql \
  -H "GraphQL-Features: sub_issues" \
  -f query='mutation($parentId: ID!, $childId: ID!) {
    addSubIssue(input: { issueId: $parentId, subIssueId: $childId }) {
      issue { number }
    }
  }' \
  -f parentId="$EPIC_ID" \
  -f childId="$ISSUE1_ID" 2>/dev/null || true

# 6. Add labels
for issue in $EPIC_NUM $ISSUE1_NUM; do
  gh issue edit "$issue" --add-label "needs-review" --repo "$REPO" 2>/dev/null || true
done

echo "Created Epic #$EPIC_NUM with sub-issues"
```

## Issue Structure

### Title Convention

Issue titles MUST include context prefix from the user's request. Extract the context (e.g., "Seller", "Buyer", "Payments") and prefix all issues:

```
[Context] Issue title
```

Examples:

- User asks: "create issues for the Seller" → `[Seller] Seller Registration`, `[Seller] Create Product Listing`
- User asks: "create issues for checkout flow" → `[Checkout] Cart Summary`, `[Checkout] Payment Processing`
- Epic title: `[Seller] Epic: Seller Experience`

### Required Sections

Every issue MUST include:

| Section                 | Purpose                           |
| ----------------------- | --------------------------------- |
| **Objective**           | Single, clear goal (one sentence) |
| **Scope**               | What's included                   |
| **Acceptance Criteria** | Checkboxes for "done"             |
| **Out of Scope**        | Explicit boundaries               |
| **How to Test**         | Verification steps                |

Optional: Examples, Technical Notes, Dependencies, Related

## Common Mistakes

| Mistake                          | Fix                                   |
| -------------------------------- | ------------------------------------- |
| Vague objective                  | Specific goal with measurable outcome |
| Missing acceptance criteria      | Add checkboxes                        |
| Expanding into adjacent features | ASK if separate epic needed           |
| Using only labels to link issues | Use GraphQL `addSubIssue`             |

## Reference Files

Load these on-demand as needed:

- `./graphql-api.md` - GraphQL mutations for creating issues and sub-issues (RECOMMENDED)
- `./cli-reference.md` - Quick gh CLI commands reference
- `./templates.md` - Issue body templates and examples
