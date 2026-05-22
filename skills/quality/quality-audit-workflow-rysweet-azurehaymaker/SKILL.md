---
name: quality-audit-workflow
description: Comprehensive codebase quality audit with parallel agent orchestration, GitHub issue creation, automated PR generation per issue, and PM-prioritized recommendations. Use for code review, refactoring audits, technical debt analysis, module quality assessment, or codebase health checks.
source_urls:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
---

# Quality Audit Workflow

## Purpose

Orchestrates a systematic, parallel quality audit of any codebase with automated remediation through PR generation and PM-prioritized recommendations.

## When I Activate

I automatically load when you mention:

- "quality audit" or "code audit"
- "codebase review" or "full code review"
- "refactoring opportunities" or "technical debt audit"
- "module quality check" or "architecture review"
- "parallel analysis" with multiple agents

## What I Do

Execute a 6-phase workflow that:

1. **Familiarizes** with the project (investigation phase)
2. **Audits** using parallel agents across codebase divisions
3. **Creates** GitHub issues for each discovered problem
4. **Generates** PRs in parallel worktrees per issue
5. **Reviews** PRs with PM architect for prioritization
6. **Reports** consolidated recommendations in master issue

## Quick Start

```
User: "Run a quality audit on this codebase"
Skill: *activates automatically*
       "Beginning quality audit workflow..."
```

## The 6 Phases

### Phase 1: Project Familiarization

- Run investigation workflow on project structure
- Map modules, dependencies, and entry points
- Understand existing patterns and architecture

### Phase 2: Parallel Quality Audit

- Divide codebase into logical sections
- Deploy multiple agent types per section (analyzer, reviewer, security, optimizer)
- Apply PHILOSOPHY.md standards ruthlessly
- Check module size, complexity, single responsibility

### Phase 3: Issue Assembly

- Create GitHub issue for each finding
- Include severity, location, recommendation
- Tag with appropriate labels

### Phase 4: Parallel PR Generation

- Create worktree per issue (`worktrees/fix-issue-XXX`)
- Run DEFAULT_WORKFLOW.md in each worktree
- Generate fix PR for each issue

### Phase 5: PM Review

- Invoke pm-architect skill
- Group PRs by category and priority
- Identify dependencies between fixes

### Phase 6: Master Report

- Create master GitHub issue
- Link all related issues and PRs
- Prioritized action plan with recommendations

## Philosophy Enforcement

This workflow ruthlessly applies:

- **Ruthless Simplicity**: Flag over-engineered modules
- **Module Size Limits**: Target <300 LOC per module
- **Single Responsibility**: One purpose per brick
- **Zero-BS**: No stubs, no TODOs, no dead code

## Navigation Guide

### When to Read Supporting Files

**reference.md** - Read when you need:

- Detailed phase execution steps
- Agent-to-phase mappings
- Codebase division strategies
- Issue template formats

**examples.md** - Read when you need:

- Working audit examples
- Sample issue/PR formats
- Real-world usage patterns
- Output format examples

## Configuration

Override defaults via environment or prompt:

- `AUDIT_PARALLEL_LIMIT`: Max concurrent worktrees (default: 8)
- `AUDIT_SEVERITY_THRESHOLD`: Minimum severity to create issue (default: medium)
- `AUDIT_MODULE_LOC_LIMIT`: Flag modules exceeding this LOC (default: 300)
