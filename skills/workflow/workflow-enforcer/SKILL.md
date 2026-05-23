---
name: workflow-enforcer
description: |
  Enforces workflow discipline across ALL projects. Ensures Claude checks for
  specialized agents before responding, announces skill/agent usage, and creates
  TodoWrite todos for multi-step tasks. Activates on every session start.
  Triggers: automatic on all sessions, "use the right agent", "follow workflow".
---

# Workflow Enforcement

## Mandatory Protocol

Before responding to ANY user request, complete this checklist:

1. **Check for specialized agent** - Is there an agent for this task type?
2. **Announce usage** - "I'm using [agent] to [action]"
3. **Create todos** - Use TodoWrite for multi-step work
4. **Track progress** - Mark in_progress before starting, completed after finishing

## Quick Reference

| User Request | Agent to Use |
|--------------|--------------|
| Fix bug / error | `debugging-toolkit:debugger` |
| Review code | `code-documentation:code-reviewer` |
| Write tests | `unit-testing:test-automator` |
| Optimize performance | `performance-engineer` |
| Security audit | `security-auditor` |
| Deploy / CI/CD | `deployment-engineer` |
| Write docs | `docs-architect` |
| Refactor code | `legacy-modernizer` |
| Build AI feature | `ai-engineer` |
| Production incident | `incident-responder` |

For the complete 70+ agent catalog, see `reference/agents-catalog.md`.

## How to Use

### Step 1: Identify Task Type

Categorize the request:
- Debugging? → debugging agents
- Code review? → review agents
- Testing? → test automation agents
- Performance? → performance engineers
- Security? → security auditors
- Deployment? → deployment engineers

### Step 2: Announce

Before starting work:
> "I'm using the [agent-name] to [what you're doing]"

**Examples:**
- "I'm using debugging-toolkit:debugger to trace this authentication error"
- "I'm using python-development:python-pro to refactor this async code"

### Step 3: Create Todos

For multi-step tasks:
1. Break work into specific items
2. Use TodoWrite to create the list
3. Mark one as `in_progress` before starting
4. Mark `completed` immediately after finishing

### Step 4: Follow Agent Discipline

Each agent type has its own methodology:
- **TDD agents** → Write tests first
- **Debugging agents** → Systematic root cause analysis
- **Code review agents** → Follow review checklist
- **Deployment agents** → Follow deployment protocols

## Common Rationalizations to Avoid

If you think any of these, STOP and use the appropriate agent:

- "This is simple, I don't need an agent"
- "Let me just quickly fix this"
- "I can debug this manually"
- "This doesn't need a formal review"
- "I'll skip the test for now"

**The right thought:** "What specialized agent should I use for this task?"

## Guidelines

- This skill applies to EVERY session, EVERY project, EVERY task
- No exceptions, no rationalizations, no shortcuts
- When in doubt, check `reference/agents-catalog.md`
