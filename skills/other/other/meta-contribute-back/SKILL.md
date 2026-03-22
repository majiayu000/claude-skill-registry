---
version: 1.0.0
name: meta-contribute-back
description: >
  Package universal skill learnings from a project and contribute them back to
  the agentic-workflow source repo via a git branch. Creates a contrib/ branch with
  the adaptation details for review. Use when the user says "contribute back",
  "push learnings", "send adaptations upstream", or after /meta-continuous-learning
  flags pending contributions.
disable-model-invocation: true
user-invocable: true
argument-hint: "[skill-name | --all | --list]"
---

# Contribute Back — Push Learnings to Source

Package universal and stack-specific skill adaptations from this project and
stage them in the agentic-workflow repo as a contribution branch for review.

## Prerequisites

- `workflow.json` must exist with `workflowRepo` set
- `context/adaptations.md` must exist with at least one `pending-contribution` entry
- The agentic-workflow repo must be accessible locally

## Step 1: Read Adaptations

1. Read `context/adaptations.md`
2. Filter entries by status:
   - If a skill name is given: show only that skill's adaptations
   - If `--all`: show all `pending-contribution` entries
   - If `--list`: show a summary table and stop (read-only)
3. If no `pending-contribution` entries found, report and exit

## Step 2: Prepare Contributions

4. For each `pending-contribution` adaptation:
   a. Read the local skill's SKILL.md (the modified version)
   b. Resolve the agentic-workflow repo path via `workflow.json` → `workflowRepo` and `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <workflowRepo>`
   c. Read the source skill's SKILL.md from agentic-workflow
   d. Identify the differences (the adaptation)
   e. Generate a contribution file

### Contribution File Format

```
# Contribution: {short description}

- **Skill:** {skill-name}
- **From project:** {project name from workflow.json}
- **Date:** {YYYY-MM-DD}
- **Classification:** {universal | stack-specific}
- **Installed version:** {version from local catalog}

## What changed

{Description of the adaptation — what was added, modified, or restructured}

## Proposed changes

{The actual content to add or modify in the source SKILL.md.
Not a git diff — readable sections that a reviewer can understand and apply.}

## Context

{Why this came up, what problem it solved, any edge cases discovered.
Include enough context that someone reviewing in agentic-workflow understands
the motivation without needing to see the project.}
```

## Step 3: Create Contribution Branch

5. Switch to the agentic-workflow repo directory
6. Determine the branch name: `contrib/{project-name}/{skill-name}`
   - Sanitize project name: lowercase, replace spaces/dots with hyphens
   - Example: `contrib/my-project/dev-tdd-backend`
7. Check if the branch already exists:
   - If yes: switch to it and rebase on main
   - If no: create it from main
8. Create the `contributions/` directory if it doesn't exist
9. Create `contributions/{skill-name}/` directory

## Step 4: Commit Contributions

10. Write the contribution file: `contributions/{skill-name}/{date}-{slug}.md`
    - Slug: lowercase, hyphens, from the short description
    - Example: `contributions/dev-tdd-backend/2026-03-18-aspire-integration-tests.md`
11. Stage and commit:
    - Message: `contrib: {skill-name} from {project-name} — {short description}`
12. Switch back to main branch in agentic-workflow (leave the contrib branch for review)

## Step 5: Update Source Project

13. Back in the source project, update `context/adaptations.md`:
    - Change status from `pending-contribution` to `contributed`
    - Add note: `Contributed on {date} to branch contrib/{project}/{skill}`
14. Log to today's daily memory:
    - What was contributed
    - Branch name in agentic-workflow
    - Suggested next step

## Step 6: Report

15. Show summary:

```
### Contributions Staged

| Skill | Description | Branch |
|-------|-------------|--------|
| dev-tdd-backend | Aspire integration tests | contrib/my-project/dev-tdd-backend |

Next steps:
1. In agentic-workflow, review with: git log main..contrib/my-project/dev-tdd-backend
2. Merge with: /meta-merge-contributions --skill dev-tdd-backend
```

## Flags

| Flag | Behavior |
|------|----------|
| `--all` | Contribute all pending adaptations |
| `--list` | Show pending adaptations without contributing (read-only) |
| (skill-name) | Contribute adaptations for a specific skill only |

## Safety Rules

- **Never force-push** to the agentic-workflow repo
- **Never commit directly to main** in agentic-workflow — always use contrib/ branches
- **Never modify source skills** — only write to contributions/ directory
- **Always confirm** with user before creating branches in another repo
- **Clean up** — switch agentic-workflow back to main after creating the branch
