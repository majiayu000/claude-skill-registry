---
name: sprint-manager
description: 'This skill orchestrates autonomous sprint execution by coordinating
  subagents to implement GitHub issues serially. It manages the full lifecycle: generating
  implementation plans via Gemini CLI, delega'
---

---
name: sprint-manager
description: This skill orchestrates autonomous sprint execution by coordinating subagents to implement GitHub issues serially. It manages the full lifecycle: generating implementation plans via Gemini CLI, delegating implementation to subagents, reviewing PRs with Codex MCP, merging approved code, and running post-merge integration. Use this skill when asked to "run a sprint", "execute sprint issues", "implement issues autonomously", or "manage sprint workflow".
---

# Sprint Manager

## Purpose

To autonomously execute a sprint by coordinating the implementation of GitHub issues through a structured workflow that leverages subagents for isolated work and maintains a clean context window for sprint-level coordination.

## When to Use

Use this skill in the following situations:

- Starting work on a set of sprint issues from a GitHub milestone
- Implementing multiple issues autonomously with minimal user intervention
- Coordinating a development workflow that requires code review and integration
- Managing serial execution of dependent or independent issues

## Prerequisites

- GitHub repository with issues assigned to a milestone
- Git working directory is clean (no uncommitted changes)
- `gh` CLI tool installed and authenticated
- `gemini` CLI tool installed and authenticated (optional, for plan generation)
- Codex MCP available for PR review
- Project has `issue-executor` and `change-integrator` skills (or equivalent workflow)

## Architecture

The sprint manager operates as a coordinator that delegates work to subagents:

```
Sprint Manager (main context)
│
├── For each issue:
│   ├── 1. Generate implementation plan (Gemini CLI or manual)
│   ├── 2. Create feature branch
│   ├── 3. Launch implementer subagent → creates PR
│   ├── 4. Review PR (Codex MCP)
│   ├── 5. Fix issues if needed (another subagent)
│   ├── 6. Merge on approval
│   └── 7. Launch integrator subagent → cleanup & retrospective
│
└── Report sprint summary
```

## Core Workflow

### Phase 1: Sprint Setup

1. **Identify sprint issues** by querying the GitHub milestone:
   ```bash
   gh issue list --milestone "Sprint X" --state open --json number,title,labels
   ```

2. **Prioritize issues** based on labels (P0 > P1 > P2) and dependencies

3. **Track progress** using the TodoWrite tool with all sprint issues

### Phase 2: Issue Execution Loop

For each issue in priority order:

#### Step 1: Generate Implementation Plan

Option A - Use issue-executor skill (if Gemini available):
```bash
bash scripts/work-on-issue.sh <issue-number>
```

Option B - Manual plan generation:
1. Fetch issue details: `gh issue view <number> --json title,body`
2. Read relevant specs from `docs/specs/` or `docs/changes/`
3. Call Gemini CLI with context to generate a step-by-step plan
4. Create feature branch following convention: `feat/<number>-<kebab-title>`

#### Step 2: Delegate Implementation to Subagent

Launch a Task subagent with a comprehensive prompt including:

- Issue number and acceptance criteria
- Implementation plan from Step 1
- Project conventions (from CLAUDE.md)
- File paths and schema context
- Expected deliverables (PR URL, test results, files created)
- Fallback instructions if tools fail

Select appropriate subagent type based on the issue:
- `backend-architect` - API routes, database schemas, backend logic
- `frontend-developer` - React components, UI, client-side code
- `general-purpose` - Mixed or unclear scope

Example prompt structure (see `references/implementer-prompt-template.md`):
```
## Task: Implement GitHub Issue #<number> - <title>

You are working on branch `<branch-name>` in `<working-directory>`.

### Issue Summary
<brief description>

### Implementation Plan
<step-by-step plan from Gemini or manual>

### Project Conventions
<key conventions from CLAUDE.md>

### Your Deliverables
1. Implement the code
2. Run lint and tests
3. Commit with conventional commit message
4. Push and create PR

### Report Back
<what to return: PR URL, test results, issues encountered>
```

#### Step 3: Review PR with Codex MCP

After subagent returns with PR URL:

```
mcp__codex__codex with prompt:
"Review PR #<number>: <title>
URL: <pr-url>

The PR implements: <summary>

Focus your review on: <relevant concerns>

Say APPROVED if ready to merge, or list issues with severity."
```

#### Step 4: Handle Review Feedback

If Codex finds issues:
1. Launch another subagent to fix the issues
2. Provide specific fix instructions from Codex feedback
3. Re-review after fixes are pushed

If Codex approves:
- Proceed to merge

#### Step 5: Merge PR

```bash
gh pr merge <number> --squash --auto
```

Wait for CI to pass, then verify merge:
```bash
gh pr view <number> --json state
```

#### Step 6: Post-Merge Integration

Launch integrator subagent (see `references/integrator-prompt-template.md`):

1. Switch to main and pull latest
2. Delete feature branch (local and remote)
3. Update retrospective with learnings
4. Close issue if not auto-closed
5. Report completion status

### Phase 3: Sprint Completion

After all issues are processed:

1. Update TodoWrite to mark all issues complete
2. Summarize sprint results:
   - Issues completed
   - PRs merged
   - Key learnings
   - Any blockers encountered
3. Report to user

## Error Handling

### Gemini CLI Fails

If the Gemini CLI fails during plan generation:
- Fall back to manual plan creation
- Read issue details directly via `gh issue view`
- Check relevant specs in `docs/specs/` or `docs/changes/`
- Construct implementation plan based on acceptance criteria

### Subagent Fails

If an implementer subagent fails:
- Review the error reported
- Launch a new subagent with adjusted instructions
- Consider breaking the task into smaller pieces
- Flag for user intervention if repeated failures

### Codex Review Times Out

If Codex MCP doesn't respond:
- Retry the review request
- Fall back to basic automated checks (lint, tests)
- Flag PR for user manual review

### PR Merge Conflicts

If merge fails due to conflicts:
- Rebase the branch on main
- Launch subagent to resolve conflicts
- Re-run tests and review

## Prompt Templates

See the `references/` directory for detailed prompt templates:

- `references/implementer-prompt-template.md` - Template for implementation subagents
- `references/integrator-prompt-template.md` - Template for post-merge integration subagents
- `references/review-prompt-template.md` - Template for Codex PR reviews

## Best Practices

### Context Management

- Keep sprint-level state in the main context (issue tracking, PR URLs, blockers)
- Delegate all implementation details to subagents
- Each subagent gets a fresh context - include all needed info in the prompt

### Prompt Crafting

- Be specific about file paths and existing code context
- Include project conventions explicitly (subagents don't read CLAUDE.md)
- Specify exact deliverables and report format
- Provide fallback instructions for common failure modes

### Serial vs Parallel

- Default to serial execution for safety and easier debugging
- Only parallelize truly independent issues with explicit user approval
- Never parallelize issues with shared file dependencies

### User Communication

- Report progress after each issue completes
- Flag blockers immediately rather than retrying indefinitely
- Provide sprint summary at the end

## Notes

- This skill is designed for serial execution to maintain context clarity
- Each issue gets its own subagent context, keeping the main context clean
- The workflow integrates with existing issue-executor and change-integrator skills
- Codex MCP provides automated code review without user intervention
- Retrospective updates capture learnings for future sprints
