---
name: learning-loop
description: Capture new learnings discovered during code exploration or user interaction that were not present in context, memories, or codebase documentation. This skill should be invoked when Claude discovers something new about the codebase, tools, workflows, or domain knowledge that could benefit future sessions.
---

# Learning Loop

Log new knowledge discovered during work sessions that was not already documented in context, memories, or Markdown files in the codebase.

## When to Use

Invoke this skill when discovering something new during:

- **Code exploration**: Found undocumented behavior, hidden configuration, or implicit patterns
- **User interaction**: User shared information not captured in existing documentation
- **Tool discovery**: Learned about tools, commands, or workflows not previously documented
- **Domain knowledge**: Gained understanding of business logic or domain concepts not in codebase docs

**Do NOT invoke** when:

- The information is already in CLAUDE.md, rules, or other documentation
- The learning is project-agnostic (general programming knowledge)
- The information was explicitly provided in the current conversation context

## How to Log

Run the logging script with the learning summary:

```bash
.claude/skills/learning-loop/scripts/log-learning.sh "<summary>"
```

### Arguments

| Argument  | Description                             | Example                                      |
| --------- | --------------------------------------- | -------------------------------------------- |
| `summary` | Concise description of what was learned | "API rate limits are 100 req/min per tenant" |

### Examples

```bash
# Learned about undocumented configuration
.claude/skills/learning-loop/scripts/log-learning.sh "Feature flags are stored in Redis, not the database"

# Discovered implicit pattern during exploration
.claude/skills/learning-loop/scripts/log-learning.sh "All background jobs use the BaseJob class from libs/jobs"

# User shared domain knowledge
.claude/skills/learning-loop/scripts/log-learning.sh "Tenant IDs starting with 'demo_' are test accounts"
```

## Output

Learnings are appended to `.claude/learning.yaml` with timestamp:

```yaml
- date: '2025-01-20T14:30:00Z'
  summary: 'Feature flags are stored in Redis, not the database'
```

## Notes

- Keep summaries concise but informative (1-2 sentences max)
- Focus on actionable or context-critical information
- The file is intended for periodic review to identify documentation gaps
