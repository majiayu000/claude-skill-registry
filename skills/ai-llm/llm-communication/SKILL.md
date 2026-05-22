---
name: llm-communication
description: "Write effective LLM prompts, commands, and agent instructions. Goal-oriented over step-prescriptive. Role + Objective + Latitude pattern. Use when writing prompts, designing agents, building Claude Code commands, or reviewing LLM instructions. Keywords: prompt engineering, agent design, command writing."
---

# Talking to LLMs

This skill helps you write effective prompts, commands, and agent instructions.

## Core Principle

LLMs are intelligent agents, not script executors. Talk to them like senior engineers.

## Anti-Patterns

### Over-Prescriptive Instructions

Bad:
```
Step 1: Run `sentry-cli issues list --status unresolved`
Step 2: Parse the JSON output
Step 3: For each issue, calculate priority score using formula...
Step 4: Select highest priority issue
Step 5: Run `git log --since="24 hours ago"`
...700 more lines
```

This treats the LLM like a bash script executor. It's brittle, verbose, and removes the LLM's ability to adapt.

### Excessive Hand-Holding

Bad:
```
If the user says X, do Y.
If the user says Z, do W.
Handle edge case A by doing B.
Handle edge case C by doing D.
```

You can't enumerate every case. Trust the LLM to generalize.

### Defensive Over-Specification

Bad:
```
IMPORTANT: Do NOT do X.
WARNING: Never do Y.
CRITICAL: Always remember to Z.
```

If you need 10 warnings, your instruction is probably wrong.

## Good Patterns

### State the Goal, Not the Steps

Good:
```
Investigate production errors. Check all available observability (Sentry, Vercel, logs).
Correlate with git history. Find root cause. Propose fix.
```

Let the LLM figure out how.

### Provide Context, Not Constraints

Good:
```
You're a senior SRE investigating an incident.
The user indicated something broke around 14:57.
```

Frame the situation, don't micromanage the response.

### Trust Recovery

Good:
```
Trust your judgment. If something doesn't work, try another approach.
```

LLMs can recover from errors. Let them.

### Role + Objective + Latitude

The best prompts follow this pattern:
1. **Role**: Who is the LLM in this context?
2. **Objective**: What's the end goal?
3. **Latitude**: How much freedom do they have?

Example:
```
You're a senior engineer reviewing this PR.           # Role
Find bugs, security issues, and code smells.          # Objective
Be direct. If it's fine, say so briefly.              # Latitude
```

## When Writing Claude Code Commands

Commands are prompts. The same rules apply:

**Bad command (700 lines):**
- Exhaustive decision trees
- Exact CLI commands to copy
- Every edge case enumerated
- No room for judgment

**Good command (20 lines):**
- Clear objective
- Context about what tools exist
- Permission to figure it out
- Trust in agent judgment

## When Building Agentic Systems

Same principles scale up:

**Bad agent design:**
- Rigid state machines
- Exhaustive action lists
- No error recovery
- Brittle integrations

**Good agent design:**
- Goal-oriented
- Self-correcting
- Minimal constraints
- Natural language interfaces

## The Test

Before finalizing any LLM instruction, ask:

> "Would I give these instructions to a senior engineer?"

If you'd be embarrassed to hand a colleague a 700-line runbook for a simple task, don't give it to the LLM either.

## Remember

The L in LLM stands for Language. Use it.
