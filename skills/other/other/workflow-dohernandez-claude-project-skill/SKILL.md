---
name: workflow
description: Manage development lifecycle for CI/E2E runner work. Use when user says /workflow start, /workflow status, or /workflow finish.
user-invocable: true
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill workflow"
---

# CI E2E Runner Workflow

## Purpose
Manage the development lifecycle for work on the CI/E2E runner project. This skill handles setup (branch, context) and delegates implementation based on branch type.

## Quick Reference
- **Creates**: Feature branch, workflow context file
- **Requires**: Plain text description of work to do
- **Delegates to**: `/bugfix` (fix branches) or `/task` (feat, chore, docs, ci branches)

## Commands

| Command | Description |
|---------|-------------|
| `/workflow start <description>` | Create branch, set up context, then delegate |
| `/workflow status` | Show current workflow context and progress |
| `/workflow finish` | Cleanup branch after PR is merged |

**Related:** Use `/pr-merge` to merge PRs. Use `/commit` for commits. Use `/pr-create` for PRs.

## When to Start a Workflow

**Only start a new workflow when on `main` branch.**

| Current Branch | User Request | Action |
|----------------|--------------|--------|
| `main` | "fix this bug" | `/workflow start` |
| `main` | "start a workflow for..." | `/workflow start` |
| working branch | "fix this bug" | Fix in current branch (no new workflow) |
| working branch | "let's work on this" | Work in current branch (no new workflow) |
| working branch | "start a **new workflow** for..." | `/workflow start` (explicit request) |

**Key Rules:**
- `main` is the only non-working branch
- Any branch other than `main` is a working branch
- If already on a working branch, continue working there unless user **explicitly** requests a new workflow
- Trigger phrases on `main`: "start a workflow", "let's work on...", "fix this issue...", or any code change task

## Phase 1: Start

```
/workflow start "Add retry logic to E2E pipeline"
/workflow start "Fix webhook reaction step"
```

**Pre-condition:** Must be on `main` branch (or user explicitly requested new workflow)

**Procedure:**
1. Check for uncommitted changes (warn if present)
2. Determine branch type from context: `feat`, `fix`, `chore`, `docs`, `ci`
3. Generate branch name with type prefix:
   - `<type>/<kebab-description>`
4. **Call `workflow-setup`**:
   - Update main branch
   - Create feature branch
   - Create `.claude/workflow/<branch>/` directory
   - Write `context.json`
5. **Delegate based on type:**
   - `fix` -> Invoke `/bugfix` skill
   - `feat`/`chore`/`docs`/`ci` -> Invoke `/task` skill

## Task Delegation

Based on the branch type detected in start:

| Type | Delegate To | Description |
|------|-------------|-------------|
| `fix` | `/bugfix` | Bug fix methodology |
| `feat` | `/task` | Feature implementation |
| `chore` | `/task` | Maintenance work |
| `docs` | `/task` | Documentation updates |
| `ci` | `/task` | CI/workflow changes |

## Retrospective (After Implementation)

After completing the implementation, capture learnings before committing:

**Procedure:**
1. Scan conversation for signals:
   - **Corrections** (high confidence): "No, don't use X, use Y"
   - **Rules** (high confidence): "Always do X", "Never do Y"
   - **Approvals** (medium): "Perfect!", "That's exactly right"
2. Write learnings to `workflow/MEMORY.md` (the only MEMORY.md in this project)

**Learning Quality Rules:**
- Must be actionable (DO/DON'T/USE/AVOID)
- Must be complete sentences, not fragments
- Must NOT be questions
- Must include WHY, not just WHAT

## Commit and PR

After retrospective, use the dedicated skills:

1. **Commit changes**: `/commit`
2. **Create PR**: `/pr-create`

These skills handle conventional commit messages, PR formatting, and CI validation.

## Phase 2: Status

```
/workflow status
```

**Shows:**
- Current branch and work description
- PR status (if created)

## Phase 3: Finish

```
/workflow finish
/workflow finish feat/add-retry-logic    # Explicit branch
```

**Pre-condition:** PR must be merged before finishing.

**Procedure:**
1. Resolve target branch (current branch or argument)
2. Verify PR is merged via `gh pr list --head <branch> --state merged`
3. Switch to main branch and pull latest
4. Delete local branch: `git branch -D <branch>`
5. Delete remote branch: `git push origin --delete <branch>`
6. Clean up workflow context: `rm -rf .claude/workflow/<branch>/`
7. Report completion

See `workflow-finish` skill for detailed procedure and sharp edges.

## Workflow Context

Stored in `.claude/workflow/<branch>/context.json` (gitignored):
```json
{
  "source": "text",
  "title": "Add retry logic to E2E pipeline",
  "branch": "feat/add-retry-logic-to-e2e-pipeline",
  "type": "feat",
  "createdAt": "2026-02-22T..."
}
```

## Branch Naming

Format: `<type>/<kebab-description>`

Branch naming convention:
- Type prefix first (`feat/`, `fix/`, `chore/`, `docs/`, `ci/`)
- Followed by kebab-case description from title

Examples:
- `feat/add-retry-logic-to-e2e-pipeline`
- `fix/webhook-reaction-step`
- `ci/add-profile-selection-to-dispatch`
- `chore/update-runner-setup-script`
- `docs/update-readme-architecture`

## Automation
See `skill.yaml` for the full procedure and patterns.
See `sharp-edges.yaml` for common failure modes.
