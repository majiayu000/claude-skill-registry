---
name: agent-design
description: Design AI agents with recommended patterns and architectures
allowed-tools: Read, Write
---

# Agent Design

Skill for designing high-performance AI agents following 2025 patterns.

## Documentation

- [patterns.md](docs/patterns.md) - Multi-agent architecture patterns
- [workflows.md](docs/workflows.md) - Recommended workflows

## Fundamental Distinction

### Workflows vs Agents

| Type | Control | When to use |
|------|---------|-------------|
| **Workflow** | Code orchestrates LLM | Predictable tasks, need for control |
| **Agent** | LLM directs its actions | Flexibility, adaptive decisions |

**Golden rule:** Start simple, add complexity if necessary.

## Agent Architecture

### Minimal Structure

```yaml
Agent:
  identity: Who am I?
  capabilities: What can I do?
  tools: What tools do I have?
  constraints: What are my limits?
  workflow: How should I proceed?
```

### Complete Structure (Production)

```markdown
---
name: my-agent
description: Short description
model: sonnet|opus
tools: [list of tools]
skills: [associated skills]
---

# Identity
[Who the agent is]

# Capabilities
[What it can do]

# Workflow
[Steps to follow]

# Tools
[How to use each tool]

# Constraints
[Limits and rules]

# Examples
[Use cases]

# Forbidden
[What it must NEVER do]
```

## Agent Patterns

### 1. Single Agent (Simple)

```
User → Agent → Response
```

**Usage:** Simple tasks, rapid prototyping.

### 2. Agent + Tools

```
User → Agent ↔ Tools → Response
                ↑
            Tool Results
```

**Usage:** Tasks requiring external access (API, files, DB).

### 3. Orchestrator + Subagents

```
User → Orchestrator → Subagent 1 (specialized)
                   → Subagent 2 (specialized)
                   → Subagent 3 (specialized)
                   ↓
              Synthesis → Response
```

**Usage:** Complex tasks, separation of responsibilities.

### 4. Sequential Pipeline

```
User → Agent 1 → Agent 2 → Agent 3 → Response
       (Analyze)  (Plan)    (Execute)
```

**Usage:** Linear processes (e.g., Analyst → Architect → Developer).

## Fresh Eyes Principle

**Key 2025 concept:** Each sub-agent must have a "fresh" context.

```
❌ Bad: Pass entire history to each sub-agent
✅ Good: Give only necessary information

Orchestrator:
  - Keeps complete history
  - Extracts relevant context for each sub-agent
  - Synthesizes results
```

## Design Checklist

### Before creating an agent

- [ ] Is the objective clear?
- [ ] Would a simple workflow suffice?
- [ ] What tools are needed?
- [ ] What guardrails are required?

### During design

- [ ] Is identity well defined?
- [ ] Is workflow explicit?
- [ ] Are error cases handled?
- [ ] Are examples relevant?

### After creation

- [ ] Standard case tests?
- [ ] Edge case tests?
- [ ] Security tests (jailbreak)?
- [ ] Acceptable performance?

## Claude Code Agent Template

```markdown
---
name: [kebab-case-name]
description: [1-2 lines max]
model: sonnet
color: blue
tools: Read, Edit, Write, Bash, Grep, Glob
skills: [associated-skills]
---

# [Agent Name]

[Purpose description]

## Core Principles

1. **[Principle 1]**: [Short explanation]
2. **[Principle 2]**: [Short explanation]

## Workflow (MANDATORY)

### Phase 1: [Name]
```
[Numbered actions]
```

### Phase 2: [Name]
```
[Numbered actions]
```

## Output Format

[Response structure]

## Forbidden

- [Prohibition 1]
- [Prohibition 2]
```

## Anti-Patterns to Avoid

### ❌ Omniscient agent
```
You know everything and can do anything.
```

### ✅ Specialized agent
```
You are an expert in [specific domain].
For topics outside your domain, redirect to the appropriate agent.
```

### ❌ Implicit instructions
```
Do what's logical.
```

### ✅ Explicit instructions
```
Step 1: Analyze the problem
Step 2: Propose 3 solutions
Step 3: Recommend the best with justification
```

### ❌ No error handling
```
Execute the task.
```

### ✅ Explicit error handling
```
IF the task fails:
  1. Identify the cause
  2. Propose an alternative
  3. Ask for confirmation before retrying
```

## Forbidden

- Never create an agent without explicit workflow
- Never give access to all tools without necessity
- Never ignore the principle of least privilege
- Never forget security guardrails
