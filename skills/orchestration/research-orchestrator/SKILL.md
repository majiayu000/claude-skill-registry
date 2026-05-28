---
name: research-orchestrator
description: Orchestrates parallel research subagents to gather context for a ticket. Use after ticket-intake completes and ticket.json exists.
---

# Research Orchestrator

Dispatches parallel research subagents to gather comprehensive context for implementing a ticket, then compiles findings into a research report.

## Prerequisites

- `ticket-intake` completed - `runs/{ticket-id}/ticket.json` exists
- `gh` CLI authenticated for GitHub research
- Notion MCP connected (for related pages research)

## Quick Start

1. Load ticket data from run directory
2. Determine which research areas to dispatch
3. Prepare and dispatch subagents in parallel
4. Compile results into research report
5. Update status and prompt for human review

## Workflow

### Step 1: Load Ticket Data

Read `ticket.json` from the current run directory:

```
$HOME/repos/ticket-to-pr-pipeline/runs/{ticket-id}/ticket.json
```

Extract:

- `title` - Ticket title
- `description` - Full description
- `slackLink` - Slack thread URL (if present)
- `relatedTasks` - Linked Notion pages (if present)
- `area` - Category/area

Generate keywords from title and description for search queries.

### Step 2: Determine Research Scope

**Always dispatch:**

- `git-history` - Commits, blame, file history
- `github-prs-issues` - Related PRs and issues
- `codebase-analysis` - Patterns and affected files

**Conditional dispatch:**

- `notion-related` → Only if `relatedTasks` has entries or linked pages exist
- `slack-thread` → Only if `slackLink` exists
- `external-research` → Only if new patterns/libraries/technologies involved

### Step 3: Handle Slack Content

If `slackLink` exists in ticket.json, prompt the user:

```
📋 This ticket has a linked Slack thread:
   {slackLink}

Please copy and paste the thread content, or type "skip" to continue without it.
```

Wait for user input before proceeding.

### Step 4: Dispatch Subagents

Use Task tool to dispatch each research area in parallel.

**Target repository:**
The repository being worked on. Read from `ticket.json` or the current working directory.

**Prompt templates location:**

```
$HOME/repos/ticket-to-pr-pipeline/prompts/research/
```

**Template variables to fill:**

- `{{TICKET_TITLE}}` - From ticket.json
- `{{TICKET_DESCRIPTION}}` - From ticket.json
- `{{KEYWORDS}}` - Extracted from title/description
- `{{AFFECTED_FILES}}` - Estimated from description or "TBD"

**Subagent task format:**

```
You are a research subagent for the ticket-to-PR pipeline.

TICKET: {title}
DESCRIPTION: {description}
KEYWORDS: {keywords}
AFFECTED FILES: {affected_files}

YOUR TASK: {content from prompt template or inline task description}

REPOSITORY: {target repository path from ticket.json or current working directory}

OUTPUT FORMAT: {format section from prompt template}

When complete, return your findings in the specified format. Be thorough but concise.
```

### Step 5: Compile Research Report

Wait for all subagents to complete. If a subagent fails, note the failure but continue with others.

Create `research-report.md` in the run directory:

```markdown
# Research Report: {Ticket Title}

**Ticket ID:** {id}
**Generated:** {timestamp}

## Summary

- **Key findings:** [overview of most important discoveries]
- **Affected files:** [list of files identified]
- **Recommended reviewers:** [based on git blame/PR history]
- **Risk areas:** [potential challenges identified]

## Git History Findings

{git-history subagent output}

## GitHub PRs & Issues

{github-prs-issues subagent output}

## Codebase Analysis

{codebase-analysis subagent output}

## External Research

{external-research subagent output if dispatched, otherwise "Not applicable - no new patterns/libraries involved"}

## Slack Context

{slack-thread subagent output if dispatched, otherwise "Not applicable - no Slack thread linked"}

## Notion Related Pages

{notion-related subagent output if dispatched, otherwise "Not applicable - no related pages linked"}

## Research Failures

{List any subagents that failed and why, or "None - all research completed successfully"}

## Next Steps

Based on this research, recommended approach for planning phase:

1. {recommendation 1}
2. {recommendation 2}
3. {recommendation 3}
```

### Step 6: Update Status

Update `status.json` in run directory:

```json
{
  "status": "planning",
  "lastUpdated": "{timestamp}",
  "researchCompletedAt": "{timestamp}"
}
```

### Step 7: Output Summary

Print summary for human:

```markdown
## Research Complete

**Ticket:** {title}
**Research Report:** {path to research-report.md}

### Findings Summary

- {key finding 1}
- {key finding 2}
- {key finding 3}

### Affected Files Identified

- {file 1}
- {file 2}

### Recommended Reviewers

- @{reviewer1} - {reason}
- @{reviewer2} - {reason}

---

📋 **Human Review Required**

Please review the research report before continuing:
{path to research-report.md}

When ready, load the `plan-generator` skill to begin planning.
```

## Subagent Dispatch Reference

### git-history Subagent

Searches commits, blame, file history for relevant context.

Key tasks:

- Recent commits (90 days) touching affected files or keywords
- File history and blame for ownership
- Patterns from similar changes

### github-prs-issues Subagent

Searches GitHub for related PRs and issues.

Key tasks:

- Open PRs that might conflict
- Merged PRs with relevant patterns
- Issues with useful context
- Review patterns from similar PRs

Uses `gh` CLI commands.

### codebase-analysis Subagent

Analyzes target repository codebase structure.

Key tasks:

- Identify affected files
- Understand existing patterns
- Check AGENTS.md guidelines
- Find related code patterns
- Map dependencies

### external-research Subagent

Researches external sources for best practices.

Only dispatch when:

- New library/dependency introduced
- Complex pattern needing research
- UI/UX best practices needed
- Performance optimization required

Sources: Relevant framework documentation, library docs, project-specific resources

### notion-related Subagent

Researches linked Notion pages and related tasks.

Requires Notion MCP. Fallback: ask human to copy content.

### slack-thread Subagent

Extracts context from linked Slack thread.

Currently manual: ask human to paste thread content.

## Error Handling

### Subagent Failure

```
⚠️ {subagent-name} research failed:
{error message}

Continuing with remaining research...
```

Note failure in research report but don't block other subagents.

### Missing ticket.json

```
❌ ticket.json not found in run directory.

Expected location: $HOME/repos/ticket-to-pr-pipeline/runs/{ticket-id}/ticket.json

Please run ticket-intake first.
```

### No Dispatch Possible

If no subagents can be dispatched:

```
❌ Unable to dispatch any research subagents.
Check prerequisites and run directory setup.
```

## Notes

- Focus on actionable context, not exhaustive documentation
- Human checkpoint after research is critical - do not auto-continue to planning
- Failed subagents should not block the overall process
- Research report should be comprehensive but scannable
