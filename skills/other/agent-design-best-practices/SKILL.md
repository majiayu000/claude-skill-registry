---
name: agent-design-best-practices
description: Best practices for designing Claude Code agent files (.claude/agents/*.md). This skill should be used when writing or reviewing agent markdown files to ensure proper design with focused domains, correct tool access, reusable definitions, and separation of capabilities from lifecycle. Combines Anthropic's official guidance with battle-tested patterns from agent team usage.
---

# Agent Design Best Practices

## Overview

This skill defines best practices for designing Claude Code agent files (`.claude/agents/*.md`). Agent files define reusable roles that can be spawned as subagents or teammates. The core principle is that **agent files define capabilities, not lifecycle** -- the team lead's spawn prompt controls when and how the agent runs.

## Principles

### 1. Define Capabilities, Not Lifecycle

Agent files describe *what* an agent can do. The spawn prompt from the team lead controls *when* it runs and *what to focus on*.

```markdown
<!-- Wrong: Hardcodes workflow phase and interaction pattern -->
# Security Planner Agent

You are a security specialist in a plan-create Agent Team.
Given a Research Brief from the team lead, identify security
considerations for the planned changes.

## Output Format

Send your sub-plan to the team lead via `SendMessage` with this structure:
...
```

```markdown
<!-- Correct: Defines domain expertise, team lead controls usage -->
# Security Specialist Agent

You are a security specialist who identifies vulnerabilities,
evaluates threats, and recommends mitigations for code changes.

## Analysis Process
1. Read affected files
2. STRIDE analysis
3. Check input validation
...
```

The wrong version is coupled to one workflow ("plan-create Agent Team", "Given a Research Brief", "Send via SendMessage"). The correct version works in any context -- planning, review, ad-hoc analysis -- because the team lead's spawn prompt provides the specific instructions.

### 2. One Agent Per Domain, Not Per Phase

Prefer a single agent that covers a domain over multiple agents split by workflow phase. The team lead specializes the agent per phase via the spawn prompt.

| Wrong | Right |
|-------|-------|
| `security-planner` + `security-reviewer` | `security-specialist` |
| `test-strategist` + `test-coverage-agent` | `test-specialist` |
| `architecture-planner` + `architecture-reviewer` | `architecture-specialist` |

The same agent type can be spawned multiple times with different prompts for different phases. A `security-specialist` spawned during planning gets "evaluate this plan for security risks" while the same type spawned during review gets "review these code changes for vulnerabilities."

### 3. Design Focused Domains

Each agent should excel at one specific domain. The domain should be broad enough to avoid workflow coupling but narrow enough to provide real expertise.

```yaml
# Too narrow (coupled to one workflow step)
description: Performs STRIDE analysis on Research Briefs during plan-create Phase 2

# Too broad (no clear expertise)
description: General-purpose agent that can do anything

# Just right (focused domain, reusable across workflows)
description: Security specialist. Performs threat modeling (STRIDE), reviews code for OWASP Top 10 vulnerabilities, checks auth/validation/secrets handling.
```

### 4. Write Detailed Descriptions

Claude uses the `description` field in YAML frontmatter to decide when to delegate tasks. Be specific about what the agent does and when it adds value.

```yaml
# Bad: Vague, Claude can't decide when to use it
description: Reviews code

# Good: Specific domain, clear trigger conditions
description: Security specialist. Performs threat modeling (STRIDE), reviews code for OWASP Top 10 vulnerabilities, checks auth/validation/secrets handling, and recommends mitigations.
```

### 5. Limit Tool Access

Grant only the tools necessary for the agent's domain. This enforces focus and prevents agents from exceeding their intended scope.

| Agent Type | Appropriate Tools | Rationale |
|-----------|-------------------|-----------|
| Researcher / Reviewer | `Read, Grep, Glob, Bash` | Read-only analysis, no file modifications |
| Implementer | `Read, Write, Edit, Bash, Grep, Glob` | Needs to modify code |
| Planner | `Read, Grep, Glob` | Research only, no execution |

Read-only agents cannot implement code. Do not assign implementation tasks to agents without `Write` and `Edit` tools.

### 6. No Hardcoded Interaction Patterns

Do not prescribe how the agent communicates or what input format it expects. The team lead's spawn prompt handles interaction patterns.

```markdown
<!-- Wrong: Hardcodes communication protocol -->
## Input
You receive a **Research Brief** from the team lead containing...

## Output Format
Send your sub-plan to the team lead via `SendMessage` with this structure:
```

```markdown
<!-- Correct: Defines output structure without prescribing delivery mechanism -->
## Output Format
Structure your findings as:

### Threat Model (STRIDE)
| Threat | Applies? | Description | Mitigation |
...
```

The output format itself is fine to define -- it provides structure. But how the agent receives input and delivers output should be left to the team lead.

### 7. Context Window Isolation

Each teammate has its own context window. Teammates do not share context and cannot see what other teammates have done. Account for this in agent design:

- Do not assume the agent has seen previous analysis from other agents
- Include enough domain knowledge in the agent file for independent operation
- The team lead bridges context between agents via spawn prompts and messages

### 8. File Ownership in Teams

When agents work in teams, each teammate should own distinct files or directories. Two teammates editing the same file leads to conflicts and lost work.

Design agent domains so their file ownership naturally separates:

| Agent | Owns |
|-------|------|
| `implementer` | Source files (`src/`) |
| `test-specialist` | Test files (`tests/`) |
| `quality-specialist` | No files (read-only) |

## Agent File Structure

### Required Frontmatter

```yaml
---
name: agent-name           # lowercase with hyphens
description: When and why to use this agent. Be specific.
tools: Read, Grep, Glob     # comma-separated, minimal set
---
```

### Optional Frontmatter

```yaml
model: sonnet              # sonnet, opus, haiku, or inherit (default)
permissionMode: default     # default, acceptEdits, plan, bypassPermissions, etc.
maxTurns: 50               # limit agentic turns
skills:                     # skills to preload
  - skill-name
memory: user                # persistent memory: user, project, or local
```

### Body Structure

The markdown body becomes the agent's system prompt. Structure it as:

1. **Role statement** -- one sentence describing what the agent is
2. **Analysis/workflow process** -- numbered steps for the agent's approach
3. **Output format** -- structure for findings (without prescribing delivery mechanism)
4. **Rules/constraints** -- guardrails for the agent's behavior

## Anti-Patterns

### Don't Create Phase-Specific Agents

```markdown
<!-- Wrong: Two agents for the same domain, split by phase -->
# Pre-Implementation Security Planner
...
# Post-Implementation Security Reviewer
...

<!-- Correct: One agent, team lead controls timing -->
# Security Specialist
...
```

### Don't Hardcode Workflow Dependencies

```markdown
<!-- Wrong: Agent assumes specific workflow context -->
You are part of the plan-create Phase 2 team.
Wait for the Research Brief from Phase 1.
After your analysis, the Consistency Checker will validate your output.

<!-- Correct: Agent is self-contained -->
You are a security specialist who identifies vulnerabilities
and recommends mitigations for code changes.
```

### Don't Over-Specify the Model

Only set `model` when there's a clear reason. Most agents work well with `inherit` (the default), which uses the same model as the parent session. Use `haiku` for fast, simple tasks (exploration, search). Use `sonnet` or `opus` only when the domain requires stronger reasoning.

## Verification Checklist

Before committing an agent file, verify:

1. **Description is specific** -- Claude can determine when to delegate from the description alone
2. **Tools are minimal** -- only the tools the agent actually needs
3. **No workflow coupling** -- no references to specific team structures, phases, or input formats
4. **No hardcoded communication** -- no "send via SendMessage" or "given a Research Brief"
5. **Domain is reusable** -- the agent works in planning, review, and ad-hoc contexts
6. **Role statement is clear** -- first line of body explains what the agent is
7. **Output format is defined** -- structured output without prescribing delivery
