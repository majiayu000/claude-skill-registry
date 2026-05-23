---
name: codebase-research
description: Orchestrates comprehensive codebase research by decomposing user queries into parallel sub-agent tasks and synthesizing findings. This skill should be used when users ask questions about how code works, where functionality exists, how components interact, or need comprehensive documentation of existing implementations. It focuses exclusively on documenting and explaining the codebase as it exists today.
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep, Bash
---

# Codebase Research

## Overview

This skill enables comprehensive codebase research through parallel sub-agent orchestration. It decomposes research questions into focused sub-tasks, executes them in parallel for efficiency, and synthesizes findings into structured research documents.

## Critical Constraint

**THE ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY.**

Do NOT:
- Suggest improvements unless explicitly requested
- Perform uninvited root cause analysis
- Propose enhancements or optimizations
- Critique implementation choices or identify problems
- Recommend refactoring or architectural changes

DO:
- Describe what exists
- Explain where functionality lives
- Document how components work
- Map component interactions and dependencies

## Initial Response

When this skill is invoked, respond:

> "I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections."

## Available Sub-Agents

### Codebase Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `codebase-locator` | Finds files by topic/feature | Need to locate all files related to a feature |
| `codebase-analyzer` | Traces implementation with file:line refs | Need to understand how code works |
| `codebase-pattern-finder` | Finds code patterns with examples | Need to see how patterns are implemented |

### Documentation Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `docs-locator` | Finds docs, ADRs, design documents | Need to find documentation about a topic |
| `docs-analyzer` | Extracts decisions and specs from docs | Need to understand documented decisions |

### External Research

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `web-search-researcher` | Researches external documentation | Explicitly requested or need external context |

## Research Workflow

### Step 1: Read Mentioned Files

Read any files directly mentioned by the user completely (without limit/offset parameters) before spawning sub-tasks. This establishes baseline context.

### Step 2: Analyze and Decompose

Analyze the research question considering:
- Patterns and architectural implications
- Related components and dependencies
- Potential sub-questions to explore
- Whether documentation exists that provides context

Create a research plan using TodoWrite with specific investigation areas.

### Step 3: Spawn Parallel Sub-Agents

Use the Task tool to spawn parallel sub-agents. Match agents to research needs:

**For "Where is X?** questions:
```
Task(subagent_type="codebase-locator", prompt="Find all files related to [topic]...")
```

**For "How does X work?"** questions:
```
Task(subagent_type="codebase-analyzer", prompt="Trace the implementation of [feature]...")
```

**For "How should I implement X?"** questions:
```
Task(subagent_type="codebase-pattern-finder", prompt="Find patterns for [type] including examples...")
```

**For "Why was X done this way?"** questions:
```
Task(subagent_type="docs-locator", prompt="Find design docs and ADRs related to [topic]...")
Task(subagent_type="docs-analyzer", prompt="Extract decisions and rationale for [topic]...")
```

**For external documentation needs** (only if explicitly requested):
```
Task(subagent_type="web-search-researcher", prompt="Research [library/API] documentation for [topic]...")
```

**Spawn multiple agents in parallel** (single message with multiple Task tool calls) for efficiency.

### Step 4: Await and Compile Results

Wait for all sub-agents to complete using AgentOutputTool, then compile results with:
- Live codebase findings as **primary source**
- Documentation findings as supplementary context
- Historical context from design documents

### Step 5: Generate Research Document

Create a structured research document with the following format:

```markdown
# Research: [Topic]

**Date:** YYYY-MM-DD
**Branch:** [current branch]
**Commit:** [current commit hash]

## Research Question

[The original question being investigated]

## Summary

[2-3 paragraph executive summary of findings]

## Detailed Findings

### [Finding Category 1]

[Detailed explanation with code references]

### [Finding Category 2]

[Detailed explanation with code references]

## Code References

| Component | File | Purpose |
|-----------|------|---------|
| [Name] | `path/to/file.ts:line` | [What it does] |

## Architecture

[How components interact - can include ASCII diagrams]

## Historical Context

[Relevant decisions from documentation, if any]

## Related Files

- `path/to/related1.ts` - [Purpose]
- `path/to/related2.ts` - [Purpose]

## Open Questions

- [Any unresolved questions or areas needing further investigation]
```

### Step 6: Present Findings

Present the research document to the user. For follow-up questions:
- Append to the same document structure
- Update metadata as needed
- Reference previous findings when relevant

## Agent Selection Guide

### Question Type → Agent Mapping

| Question Pattern | Primary Agent | Supporting Agents |
|-----------------|---------------|-------------------|
| "Where is X implemented?" | codebase-locator | - |
| "How does X work?" | codebase-analyzer | codebase-locator |
| "How is X typically done here?" | codebase-pattern-finder | codebase-locator |
| "Why was X designed this way?" | docs-analyzer | docs-locator, codebase-analyzer |
| "What are all the files for X?" | codebase-locator | - |
| "Trace the flow of X" | codebase-analyzer | codebase-locator |
| "Find examples of X" | codebase-pattern-finder | codebase-locator |
| "What's documented about X?" | docs-locator | docs-analyzer |

### Complex Questions

For complex questions that span multiple concerns, spawn multiple specialized agents:

**Example: "How does authentication work and why was JWT chosen?"**
```
Task(subagent_type="codebase-locator", prompt="Find all auth-related files...")
Task(subagent_type="codebase-analyzer", prompt="Trace auth flow implementation...")
Task(subagent_type="docs-locator", prompt="Find auth design docs and ADRs...")
Task(subagent_type="docs-analyzer", prompt="Extract auth decisions and rationale...")
```

## Best Practices

### Parallel Execution
Always spawn multiple sub-agents in parallel when investigating different aspects of the same question. This significantly reduces research time.

### Code References
Include precise file:line references for all findings:
- `src/services/auth.service.ts:45` - Good
- `the auth service` - Insufficient

### Stay Factual
Focus on observable facts:
- "The function accepts two parameters: userId and options"
- "This service is injected in 5 controllers"
- "Data flows from controller → service → repository"

Avoid speculation or judgment:
- ~~"This could be improved by..."~~ - Not allowed unless requested
- ~~"The naming is inconsistent"~~ - Not allowed unless requested

### Scope Management
For broad questions, structure the research in layers:
1. High-level architecture overview
2. Component-level details
3. Implementation specifics

For narrow questions, go directly to specifics with supporting context.

### Include Documentation Context
When relevant, include findings from documentation:
- ADR decisions that explain "why"
- Design documents that provide context
- Specifications that define constraints

## Example Research Questions

This skill handles questions like:

- "How does the authentication flow work?"
- "Where is the research pipeline implemented?"
- "What files handle API routing?"
- "How do the frontend and backend communicate?"
- "What database models exist and how are they related?"
- "Trace the data flow for a user login"
- "How should I implement a new service? Show me patterns."
- "Why was this architecture chosen? What was documented?"
- "What are the conventions for error handling here?"
