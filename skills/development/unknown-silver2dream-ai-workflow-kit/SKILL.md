---
name: create-issues
description: Systematic GitHub issue creation from requirements. Analyzes codebase, breaks down requirements into multiple issues with dependencies, proposes detailed issues for review, and creates them after user approval. Triggers: /create-issues, create issues, batch issue creation, requirement breakdown.
allowed-tools: Read, Grep, Glob, Bash
---

# Create Issues Skill

Systematic workflow for creating well-structured GitHub issues from high-level requirements.

## Overview

This skill transforms user requirements into a set of well-structured, dependency-aware GitHub issues. It follows a 5-phase workflow with a mandatory user approval gate before creating any issues.

## When to Use

Use this skill when:
- User invokes `/create-issues`
- User describes a feature or requirement that needs multiple issues
- User wants to plan work breakdown systematically
- User needs help decomposing a complex requirement

## Workflow

### Phase 1: Codebase Analysis

**Read** `phases/analyze.md`

Scan the project to understand:
- Repository structure and languages
- Module organization and patterns
- Existing test coverage
- Configuration from workflow.yaml

### Phase 2: Requirement Breakdown

**Read** `phases/breakdown.md`

Systematically decompose the requirement:
- Identify discrete tasks
- Detect dependencies between tasks
- Assign complexity scores (1-5)
- Assign priorities (P0/P1/P2)
- Group by execution phase

### Phase 3: Issue Proposal Generation

**Read** `phases/propose.md`

Generate detailed proposals:
- Full issue content with all fields
- Scope with specific file paths
- Acceptance criteria
- Verification commands
- Dependency graph visualization

### Phase 4: User Approval Gate

**Read** `phases/approval.md`

Present proposals and wait for confirmation:
- Display formatted proposals
- User responds: yes/no/edit
- **Only proceed if user explicitly approves**

### Phase 5: Issue Creation

**Read** `phases/create.md`

Create issues via GitHub CLI:
- Execute `gh issue create` for each issue
- Capture returned issue numbers
- Update dependency references
- Generate final report with links

## Critical Rules

1. **NEVER create issues without user approval**
2. **ALWAYS show full proposal details before asking for approval**
3. **Respect dependency order** - issues with dependencies must reference actual issue numbers
4. **Follow commit format** - `[type] subject` (no colon)
5. **Include verification commands** - Go projects use `go test ./...` and `go build ./...`

## Integration with AWK Workflow

Issues created by this skill will have the `ai-task` label and can be processed by:
- `awkit kickoff` - AWK principal workflow (spec-driven)
- `/run-issues` - Batch issue processing skill

**⚠️ WARNING**: Do NOT run `/run-issues` and `awkit kickoff` simultaneously on the same issues.

**Recommended workflow:**
```
/create-issues → (user approves) → issues created
        ↓
    Choose ONE:
        ├─ awkit kickoff (structured, spec-driven)
        └─ /run-issues (autonomous, batch processing)
```

## Self-Check

On each phase entry, output:
```
[CREATE-ISSUES] <timestamp> | <phase> | loaded: <filename>
```

## Quick Reference

| Phase | Action | File |
|-------|--------|------|
| 1. Analyze | Scan codebase structure | `phases/analyze.md` |
| 2. Breakdown | Decompose requirement | `phases/breakdown.md` |
| 3. Propose | Generate detailed proposals | `phases/propose.md` |
| 4. Approval | Wait for user confirmation | `phases/approval.md` |
| 5. Create | Execute gh issue create | `phases/create.md` |
