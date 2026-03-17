---
name: gitlab-tickets
description: Create GitLab issues through conversational brainstorming. Use when user wants to capture ideas, features, bugs, or work items as GitLab tickets. Supports linking related issues, label management, and iterative refinement through dialogue.
---

# GitLab Tickets

Create well-structured GitLab issues through natural conversation using `glab` CLI.

## Prerequisites

- `glab` CLI installed and authenticated
- Run `glab auth status` to verify

## Workflow

### 1. Understand the Idea

Ask clarifying questions **one at a time** to understand:
- What type of work (feature, bug, chore, docs)
- The core problem or need
- Key requirements and constraints
- Acceptance criteria

Prefer multiple-choice questions when possible.

### 2. Summarize Before Creating

Present a brief summary of the ticket before creating:
```
**[Title]**
- Bullet points of key details
- Scope and acceptance criteria
```

Ask: "Does this capture what you want, or should I change something?"

### 3. Create the Issue

Use `glab issue create` with structured description:

```bash
glab issue create \
  --title "Descriptive title" \
  --label "feature" \
  --description "$(cat <<'EOF'
## Summary
Brief description of the work.

## Details
- Key requirements
- Technical approach (if known)

## Acceptance Criteria
- [ ] Criteria 1
- [ ] Criteria 2
EOF
)"
```

### 4. Link Related Issues

When issues are related, add links in the description:
- `Related to #N` - general relationship
- `Blocks #N` - this must be done first
- `Depends on #N` - this needs another issue done first

## Label Management

Check existing labels: `glab label list`

Create labels if needed:
```bash
glab label create -n "label-name" -c "#hex-color" -d "Description"
```

Standard labels:
| Label | Color | Purpose |
|-------|-------|---------|
| feature | #28a745 | New functionality |
| bug | #dc3545 | Something broken |
| chore | #6c757d | Maintenance, CI/CD |
| docs | #0366d6 | Documentation |

## Breaking Down Work

If an issue is large, offer to break it into smaller tickets:
- Create an epic/parent issue for the overall feature
- Create child issues for individual tasks
- Link children to parent with "Part of #N"

## Resuming a Session

To get context when resuming a ticketing session, run `scripts/context.sh` to see:
- Current repository
- Existing labels
- Recent issues

## Commands Reference

```bash
glab issue list                    # List open issues
glab issue view <id>               # View issue details
glab issue create                  # Interactive create
glab issue update <id> --label X   # Add label
glab label list                    # List labels
```
