---
name: pr-review
description: AI-driven deep code review of pull requests with intelligent bug detection, architecture analysis, constitution compliance checking, and mermaid logic flow diagrams. Supports standard mode (post to GitHub), local mode (create task list), and loop mode (iterative review + auto-fix). Use when reviewing PRs, analyzing code changes, or checking architecture compliance.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(gt:*), Bash(pnpm:*), Read, Edit, Write, Glob, Grep, Task, TaskOutput, TaskCreate, TaskUpdate
---

# PR Review Skill

This skill provides comprehensive pull request analysis with deep semantic understanding of code changes using **parallel specialized auditors**.

## Capabilities

1. **Parallel Sub-Agent Architecture** - 5 specialized auditors run concurrently for faster, deeper analysis:
   - Security Auditor - Injection vulnerabilities, auth gaps, data exposure, race conditions
   - Architecture Auditor - Import boundaries, monorepo structure, file organization, naming
   - Constitution Auditor - All 14 project principles compliance verification
   - Code Quality Auditor - Complexity, code smells, performance, testing gaps
   - API Stability Auditor - oRPC compliance (Principle IX), breaking changes (Principle XIII)
2. **Smart Aggregation** - Findings merged, deduplicated, and sorted by severity
3. **PR Metadata Updates** - Automatically updates PR title and description (never just recommends)
4. **Logic Flow Visualization** - Mermaid diagrams for complex workflows
5. **Local Mode** - Create task list for local fixes instead of posting to GitHub

## Usage Modes

### Standard Mode (default)
Posts review directly to GitHub PR:
- `/pr-review` or `/pr-review 123`

### Local Mode (`--local`)
Creates a task list of issues to fix locally without posting to GitHub:
- `/pr-review --local` or `/pr-review 123 --local`

Use local mode when you want to:
- Fix issues before requesting a formal review
- Self-review changes before pushing
- Iterate on fixes without cluttering PR comments

### Loop Mode (`--loop`)
Iteratively reviews, auto-fixes all findings, and re-reviews until 0 findings or max 5 iterations:
- `/pr-review --loop` or `/pr-review 123 --loop`

Use loop mode when you want to:
- Auto-fix all review findings without manual intervention
- Iterate until the PR is clean before posting to GitHub
- Get a fully automated review-fix-review cycle

On approval (0 findings), fixes are committed and the review is automatically posted to GitHub.
On max iterations or stall, fixes are committed and a local task list of remaining findings is created.
If no fixes were applied (all findings skipped), the commit is skipped.

**Note:** `--loop` and `--local` are mutually exclusive. If both are passed, the skill errors out.

## Quick Start

When a pull request needs review, ask Claude to:
- "Review this pull request"
- "Analyze the changes in this PR"
- "Check if these changes follow our constitution"
- "Review this PR locally" (uses `--local` mode)

Claude will automatically use this skill to perform comprehensive analysis.

## Autonomous Execution

This skill runs **fully autonomously** without user interaction. When invoked:

- **Do NOT ask for user confirmation** at any step
- **Do NOT pause** between tasks or wait for approval
- **Proceed directly** through all workflow tasks
- **Only stop** if a critical error occurs (gh CLI not authenticated, invalid PR number, or API failure)

Execute the entire workflow from start to finish:
- **Standard mode**: Posts review to GitHub automatically
- **Local mode**: Creates task list for local fixes (no GitHub posting)

## Operating Constraints

- **GitHub CLI Required**: Must have `gh` authenticated and be in a git repository
- **Parallel Execution**: Uses Task tool to launch 5 specialized auditors concurrently
- **AI-Driven Analysis**: All findings generated through semantic analysis
- **Constitution Knowledge**: Understands all 14 project principles (v1.0.0)
- **Completion Criteria**: See [WORKFLOW.md](WORKFLOW.md) Tasks 7 and 8 for success criteria

## Specialized Auditors

| Auditor | Focus Area | Key Checks |
|---------|------------|------------|
| **Security** | Vulnerabilities | Injection, XSS, auth gaps, data exposure, race conditions |
| **Architecture** | Structure | Import boundaries, file organization, naming conventions |
| **Constitution** | 14 Principles | Full compliance with all project principles |
| **Code Quality** | Maintainability | Complexity, code smells, performance, testing |
| **API Stability** | oRPC/APIs | Principle IX & XIII, breaking changes |

Each auditor runs independently via the Task tool and returns findings in a structured format for aggregation.

## Workflow

For the detailed workflow with parallel auditors, see [WORKFLOW.md](WORKFLOW.md).

## Analysis Guide

For analysis criteria, finding formats, and templates, see [ANALYSIS_GUIDE.md](ANALYSIS_GUIDE.md).

## Output

The skill **directly updates** the PR (not just recommends):
1. **PR Title** - Updated via `gh pr edit --title` with conventional commit format
2. **PR Description** - Updated via `gh pr edit --body` with structured markdown
3. **Review Comment** - Posted via `gh pr comment` with categorized findings
