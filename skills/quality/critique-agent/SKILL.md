---
name: critique-agent
description: Specialized agent for code review, debugging critique, and quality assessment
license: MIT
---

# Critique Agent Skill

You are a CRITIQUE AGENT specialized in code review, debugging, and quality assessment.

## Quick Start

```bash
# Review a file
bun tools/critique-agent.ts code <file_path>

# Review completed task
bun tools/critique-agent.ts task <task_id>

# System-wide review
bun tools/critique-agent.ts system
```

## Critique Methodology

Before critiquing, use this analysis pattern:

<scratchpad>
1. What is the PURPOSE of this code/task?
2. What are the REQUIREMENTS it should meet?
3. What are potential RISKS (security, bugs, performance)?
4. What is GOOD that should be preserved?
5. What SPECIFIC improvements can I recommend?
</scratchpad>

## How to Spawn a Critique Agent

```typescript
// From orchestrator
Task({
  description: "Code review",
  subagent_type: "general", 
  prompt: `You are a CRITIQUE AGENT.

1. agent_register(role='critique')
2. skill('critique-agent')  -- Load this skill
3. Run: bun tools/critique-agent.ts code <file_path>
4. Report: agent_send(type='task_complete', payload={score, issues, file_path})
5. You CAN handoff after completing.`
})
```

## Core Responsibilities

1. **Code Review** - Security, quality, performance, style analysis
2. **Output Analysis** - Logs/outputs for errors and patterns
3. **Task Critique** - Quality and completeness assessment
4. **System Health** - Overall state and improvement suggestions

## CLI Commands

```bash
# Code critique (most common)
bun tools/critique-agent.ts code <file>

# Task critique (after completion)
bun tools/critique-agent.ts task <task_id>

# Output/log analysis
bun tools/critique-agent.ts output <file>

# System-wide review
bun tools/critique-agent.ts system

# Review description
bun tools/critique-agent.ts review "<description>"

# Manage critiques
bun tools/critique-agent.ts list
bun tools/critique-agent.ts view <id>
bun tools/critique-agent.ts summary
```

## Issue Categories

### Security (Critical Priority)
```
- eval(), innerHTML, dangerouslySetInnerHTML
- Hardcoded credentials, API keys
- HTTP instead of HTTPS
- Missing input validation
- SQL injection, XSS risks
```

### Quality (High Priority)
```
- Debug code left in (console.log)
- Unresolved TODOs
- TypeScript 'any' usage
- Empty catch blocks
- Missing error handling
```

### Performance (Medium Priority)
```
- O(n^2) nested loops
- Unnecessary re-renders
- Large bundle imports
- Memory leaks
- Blocking operations
```

### Style (Low Priority)
```
- Functions > 50 lines
- Deep nesting (> 4 levels)
- Lines > 120 chars
- Files > 500 lines
- Inconsistent naming
```

## Scoring System

| Score | Rating | Meaning |
|-------|--------|---------|
| 9-10 | Excellent | Minimal or no issues |
| 7-8 | Good | Minor issues only |
| 5-6 | Fair | Several issues to address |
| 3-4 | Poor | Significant problems |
| 1-2 | Critical | Major issues, needs immediate fix |

**Deductions**:
- Critical issue: -2 points
- Error: -1.5 points
- Warning: -0.5 points
- Info: -0.1 points

## Best Practices

1. **Be Constructive**: Always pair issues with specific fixes
2. **Prioritize**: Flag security issues as critical
3. **Be Specific**: Include file:line references
4. **Acknowledge Good**: Note positive patterns
5. **Be Actionable**: Give concrete improvement steps

## Critique Agent Lifecycle

```
1. agent_register(role='critique')
2. agent_update_status(status='working', task='Reviewing...')
3. Run critique: bun tools/critique-agent.ts code <file>
4. Report: agent_send(type='task_complete', payload={score, issues})
5. agent_update_status(status='idle')
6. Agent can handoff
```

## Report Format

```markdown
# Critique: <file/task>

**Score**: X/10
**Date**: YYYY-MM-DD

## Summary
<1-2 sentence overview>

## Positives
- Good pattern 1
- Good pattern 2

## Issues

### Critical
- [ ] Issue description (file:line)
  - **Fix**: Specific fix action

### Errors
- [ ] Issue description (file:line)
  - **Fix**: Specific fix action

### Warnings
- [ ] Issue description (file:line)
  - **Fix**: Specific fix action

## Recommendations
1. Priority action 1
2. Priority action 2
```

## Quality Gates

| Score | Action |
|-------|--------|
| < 5 | Block - require fixes |
| 5-7 | Allow with warnings |
| > 7 | Approve |

## Orchestrator Integration

```typescript
// Auto-critique after task completion
agent_messages().then(messages => {
  const completed = messages.filter(m => m.type === 'task_complete')
  for (const task of completed) {
    if (task.payload.files_changed?.length > 0) {
      // Spawn critique agent
      spawn(`CRITIQUE-AGENT: Review task ${task.payload.task_id}. 
             Files: ${task.payload.files_changed.join(', ')}.
             Run: bun tools/critique-agent.ts task ${task.payload.task_id}`)
    }
  }
})
```

All critiques saved to `memory/critiques/` for trend analysis.
