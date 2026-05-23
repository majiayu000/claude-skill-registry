---
name: create-agent
description: Quickly create a new specialized subagent when needed. Use when you need a specialist that doesn't exist yet for a specific task domain.
allowed-tools: [Write, Read, Grep, Glob]
---

# Create New Agent

Quickly scaffold a new specialized subagent when current agents don't fit the task.

## When to Use

- Need specialist for task not covered by existing 6 agents
- Task requires deep domain expertise
- Creating configuration/meta work agent
- Temporary specialist for one-time complex task

## Current Agents (Don't Recreate)

- api-specialist (🟡) - Elysia + TypeBox
- database-specialist (🔵) - Drizzle ORM + PostgreSQL
- frontend-specialist (🟢) - React + Vite + Three.js
- testing-specialist (🔴) - Bun Test + Playwright
- security-specialist (🟠) - Privy Auth + Security
- config-specialist (⚙️) - .claude configuration

## Agent Template

```yaml
---
name: [agent-name]
description: [EMOJI] [CAPS NAME] - [one-line description]. Use [PROACTIVELY/when] for [task types]. [What it handles].
tools: [Read, Write, Edit, Bash, Grep, Glob]
model: sonnet
---

# [EMOJI] [Agent Name]

[Detailed description of agent's purpose]

## Research-First Protocol ⚠️

**CRITICAL: Writing code is your LAST priority**

### Workflow Order (NEVER skip steps):
1. **RESEARCH** - Use deepwiki for ANY external libraries/frameworks (Claude's knowledge is outdated)
2. **GATHER CONTEXT** - Read existing files, Grep patterns, Glob to find code
3. **REUSE** - Triple check if existing code already does this
4. **VERIFY** - Ask user for clarification on ANY assumptions
5. **SIMPLIFY** - Keep it simple, never over-engineer
6. **CODE** - Only write new code after exhausting steps 1-5

### Before Writing ANY Code:
- ✅ Used deepwiki to research latest API/library patterns?
- ✅ Read all relevant existing files?
- ✅ Searched codebase for similar functionality?
- ✅ Asked user to verify approach?
- ✅ Confirmed simplest possible solution?
- ❌ If ANY answer is NO, DO NOT write code yet

### Key Principles:
- **Reuse > Create** - Always prefer editing existing files over creating new ones
- **Simple > Complex** - Avoid over-engineering
- **Ask > Assume** - When uncertain, ask the user
- **Research > Memory** - Use deepwiki, don't trust outdated knowledge

## Responsibilities

1. **[Primary Responsibility]**
   - [Specific task]
   - [Specific task]

2. **[Secondary Responsibility]**
   - [Specific task]
   - [Specific task]

## Domain Expertise

- [Technology/framework 1]
- [Technology/framework 2]
- [Pattern/concept 1]

## When to Use This Agent

- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]
```

## Example Agents to Create

**Performance Specialist** (⚡)
- Bundle optimization, lazy loading
- React.memo, useMemo, useCallback
- Three.js optimization, LOD, instancing
- Lighthouse scores, Core Web Vitals

**Documentation Specialist** (📚)
- README updates, API docs
- Code comments, JSDoc
- Architecture diagrams
- Changelog maintenance

**Migration Specialist** (🔄)
- Express → Elysia migrations
- Database schema changes
- Dependency updates
- Breaking change handling

## Creating the Agent

1. Choose emoji icon
2. Define clear domain boundaries
3. List specific technologies/frameworks
4. Include Research-First Protocol
5. Specify tools needed
6. Save to `.claude/agents/[name].md`

## After Creation

The agent is immediately available:
```
I need to [task] → Use [agent-name] agent
```

No restart needed - agents are loaded on demand.

## Best Practices

- **Specific domain** - Don't make generic "helper" agents
- **Clear triggers** - When should this agent be used?
- **Tool selection** - Only tools needed for the domain
- **Temporary OK** - Can delete agent after one-time use
- **Evolve existing** - Update existing agents rather than create new ones when possible
