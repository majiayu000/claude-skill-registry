---
name: subagent-driven-development
description: Use fresh agents for focused subtasks to avoid context pollution
version: 1.0.0
author: Ariff
when_to_use: When tasks need isolation or fresh perspective
---

# Subagent Driven Development

## Core Concept

```
FRESH AGENT = FRESH CONTEXT
Use subagents for focused work without baggage
```

## When to Use Subagents

| Situation | Why Subagent Helps |
|-----------|-------------------|
| Complex subtask | Focused context, clear scope |
| Going in circles | Fresh perspective breaks loops |
| Parallel work | Multiple things at once |
| Context pollution | Main agent too cluttered |
| Specialized task | Pass only relevant info |
| Research/exploration | Keep main context clean |

## How to Launch Subagent

**The Handoff:**
```
1. DEFINE clear scope - what exactly to do
2. PROVIDE needed context - files, constraints, requirements
3. SPECIFY deliverable - what to return
4. SET success criteria - how to know it's done
```

**Template:**
```
Task: [Specific action to take]

Context:
- Working in [repo/directory]
- Relevant files: [list]
- Constraints: [any limits]

Deliverable:
- [Exact output expected]

Success when:
- [Criteria 1]
- [Criteria 2]
```

## Anti-Patterns

❌ **Vague handoffs**
```
Bad: "Look into this bug"
Good: "Find root cause of TypeError in user.ts:45"
```

❌ **Context dumping**
```
Bad: Passing entire conversation history
Good: Passing only relevant files and specific question
```

❌ **No success criteria**
```
Bad: "Make it better"
Good: "Refactor to reduce duplication, all tests must pass"
```

❌ **Too broad scope**
```
Bad: "Implement the whole feature"
Good: "Implement the validation logic for email field"
```

## Good Subagent Tasks

✅ **Research:**
- "Find how X is implemented in this codebase"
- "Search for similar patterns in the repo"
- "Understand the data flow from A to B"

✅ **Focused fixes:**
- "Fix the specific test failure in X"
- "Resolve the lint error in file Y"
- "Update function Z to handle edge case"

✅ **Generation:**
- "Generate tests for this function"
- "Create documentation for this module"
- "Write migration for schema change"

✅ **Analysis:**
- "Analyze dependencies of this module"
- "Identify all usages of this API"
- "Review this PR for issues"

## Receiving Subagent Results

When subagent returns:
```
1. READ the full response
2. VERIFY against success criteria
3. INTEGRATE results into main context
4. CONTINUE from where you left off
```

## Integration with Checkers

Before launching subagent:
- `scope-boundary-checker` → Is scope clear and bounded?
- `assumption-checker` → Are handoff assumptions valid?

After receiving results:
- `fact-checker` → Verify subagent claims
- `pre-action-verifier` → Before using results

## Context Management

Main agent responsibilities:
- High-level plan
- User communication
- Final integration
- Overall progress

Subagent responsibilities:
- Focused execution
- Detailed work
- Return clean results
- No side conversations
