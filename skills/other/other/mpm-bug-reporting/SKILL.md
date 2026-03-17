---
name: pm-bug-reporting
version: "1.0.0"
description: Bug reporting protocol for PM and agents to file GitHub issues
when_to_use: Framework bugs, agent errors, skill content errors detected
category: pm-workflow
tags: [bug-reporting, github, issues, pm-required]
---

# PM Bug Reporting Protocol

## When to Report Bugs

Report bugs when you encounter:
- **PM instruction errors** or missing guidance
- **Agent malfunction** or incorrect behavior
- **Skill content errors** or outdated information
- **Framework crashes** or unexpected behavior
- **Missing or incorrect documentation**
- **Configuration errors** or invalid defaults

## GitHub Repositories

Route bugs to the correct repository:

| Bug Type | Repository | Owner/Repo |
|----------|------------|------------|
| Core MPM (CLI, startup, config, orchestration) | claude-mpm | bobmatnyc/claude-mpm |
| Agent bugs (wrong behavior, errors, missing capabilities) | claude-mpm-agents | bobmatnyc/claude-mpm-agents |
| Skill bugs (wrong info, outdated, missing content) | claude-mpm-skills | bobmatnyc/claude-mpm-skills |

## Bug Report Template

When creating an issue, include:

### Title
Brief, descriptive title (50 chars max)
- ✅ "PM delegates to non-existent agent"
- ✅ "Research skill missing web search examples"
- ❌ "Bug in system"
- ❌ "Fix this"

### Labels
Always include:
- `bug` (required)
- `agent-reported` (required)
- Additional context labels:
  - `high-priority` - Critical functionality broken
  - `documentation` - Documentation error
  - `agent-error` - Agent-specific issue
  - `skill-error` - Skill content issue

### Body Structure
```markdown
## What Happened
[Clear description of the bug]

## Expected Behavior
[What should have happened]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

## Context
- Agent: [agent name if applicable]
- Skill: [skill name if applicable]
- Error Message: [full error if available]
- Version: [MPM version if known]

## Impact
[How this affects users/workflow]
```

## Using gh CLI

### Prerequisites Check
```bash
gh auth status
```

If not authenticated:
```bash
gh auth login
```

### Creating Issues

**Delegate to ticketing agent** with:
```
Task:
  agent: ticketing
  task: Create GitHub issue for [bug type]
  context: |
    Repository: bobmatnyc/claude-mpm[-agents|-skills]
    Title: [brief title]
    Labels: bug, agent-reported
    Body: |
      ## What Happened
      [description]

      ## Expected Behavior
      [expected]

      ## Steps to Reproduce
      1. [step 1]
      2. [step 2]

      ## Context
      - Agent: [agent name]
      - Error: [error message]

      ## Impact
      [impact description]
```

## Examples

### Core MPM Bug
```
Task:
  agent: ticketing
  task: Create GitHub issue for core MPM bug
  context: |
    Repository: bobmatnyc/claude-mpm
    Title: PM fails to load configuration on startup
    Labels: bug, agent-reported, high-priority
    Body: |
      ## What Happened
      PM fails to initialize when configuration.yaml contains invalid syntax.
      No clear error message shown to user.

      ## Expected Behavior
      PM should display clear YAML syntax error with line number and fix suggestion.

      ## Steps to Reproduce
      1. Add invalid YAML to .claude-mpm/configuration.yaml
      2. Run `mpm`
      3. Observe generic error without details

      ## Context
      - Component: Configuration loader
      - Error: "Failed to load configuration"
      - Version: 5.4.x

      ## Impact
      Users cannot diagnose configuration errors, requiring manual YAML validation.
```

### Agent Bug
```
Task:
  agent: ticketing
  task: Create GitHub issue for agent bug
  context: |
    Repository: bobmatnyc/claude-mpm-agents
    Title: Research agent fails to search with special characters
    Labels: bug, agent-reported, agent-error
    Body: |
      ## What Happened
      Research agent throws error when search query contains quotes or special chars.

      ## Expected Behavior
      Search queries should be properly escaped and executed.

      ## Steps to Reproduce
      1. Delegate to research: "Search for 'React hooks'"
      2. Research agent attempts search
      3. Error: "Invalid search query"

      ## Context
      - Agent: research
      - Error: grep command fails with unescaped quotes

      ## Impact
      Cannot search for quoted phrases or technical terms with special characters.
```

### Skill Bug
```
Task:
  agent: ticketing
  task: Create GitHub issue for skill content error
  context: |
    Repository: bobmatnyc/claude-mpm-skills
    Title: Git workflow skill contains outdated branch strategy
    Labels: bug, agent-reported, documentation, skill-error
    Body: |
      ## What Happened
      Skill recommends `git flow` branching model, which project no longer uses.
      Current standard is trunk-based development.

      ## Expected Behavior
      Skill should document current trunk-based workflow.

      ## Context
      - Skill: git-workflow.md
      - Section: "Branching Strategy"
      - Line: 45-60

      ## Impact
      Agents follow outdated branching model, creating workflow friction.
```

## Escalation Path

When ticketing agent is unavailable or gh CLI fails:

1. **Log locally** for manual reporting:
   ```
   echo "[BUG] $(date): [description]" >> .claude-mpm/logs/bugs.log
   ```

2. **Report to PM** for alternative action:
   ```
   PM should create ticket in primary ticketing system (Linear/JIRA)
   with note to create GitHub issue once available
   ```

3. **User notification**:
   ```
   "Bug detected: [description]. Logged for manual GitHub issue creation."
   ```

## Success Criteria

Bug reporting successful when:
- ✅ Issue created in correct repository
- ✅ All required labels applied (`bug`, `agent-reported`)
- ✅ Body follows template structure
- ✅ Title is clear and concise
- ✅ Context includes agent/skill name if applicable
- ✅ Issue URL returned for tracking

## PM Enforcement

PM MUST:
- Detect bugs during agent interactions
- Delegate bug reporting to ticketing agent
- NOT attempt to create GitHub issues directly
- Follow escalation path if ticketing unavailable
- Log all bug reports for audit trail

## Related Skills
- [pm-ticketing-integration.md](pm-ticketing-integration.md) - Ticket delegation patterns
- [pm-delegation-patterns.md](pm-delegation-patterns.md) - General delegation guidance
- [ticketing-examples.md](ticketing-examples.md) - Ticketing delegation examples
