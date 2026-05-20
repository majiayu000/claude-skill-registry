---
name: explain
description: "Use when explaining code, concepts, patterns, or architecture: engineer-grade technical explanations with 3-tier depth control, ASCII diagrams, and execution traces."
effort: high
argument-hint: "<topic>|--depth brief|standard|deep"
tags: [explanation, teaching, analysis, architecture]
---



# Explain

Engineer-grade technical explanations of code, concepts, patterns, and architecture. 3-tier depth control scales detail to what the developer needs. Anchored in the actual codebase with `file:line` references, ASCII diagrams, and execution traces.

## When to Use

- "How does this work?", "What is this?", "Why does this do X?", "Trace this."
- NOT for generating documentation -- use `/ai-write`.
- NOT for writing/fixing code -- use `ai-build agent` or `/ai-debug`.

## Process

### 1. Identify subject

Classify into: Code, Concept, Pattern, Architecture, Error, or Difference. If ambiguous, ask ONE clarifying question.

### 2. Search codebase

Use Grep/Glob to find real instances. Codebase examples with `file:line` references are primary evidence. If not found, use generic example in project's stack and note it.

### 3. Select depth

| Depth | Trigger cues | Sections |
|-------|-------------|----------|
| Brief | "TL;DR", "brief", "short" | Summary + Walkthrough (3-5 steps) |
| Standard | General question (DEFAULT) | Summary + Walkthrough + Diagram + Gotchas + Trace |
| Deep | "deep dive", "everything", "teach me" | All above + Context Map + Complexity Notes |

### 4. Deliver explanation

**Summary** (all depths): 1-2 technical sentences -- what it does and why it exists.

**Walkthrough** (all depths): numbered steps with `file:line` references, following execution order. Brief: 3-5 steps max.

**Diagram** (standard+deep): ASCII art reflecting actual code structure. Choose type: data flow, call chain, state machine, sequence. Width under 70 chars. No Mermaid.

**Gotchas** (standard+deep): specific pitfalls in this code -- edge cases, performance traps, concurrency hazards. Not generic advice.

**Trace It** (standard+deep): execution trace through a concrete scenario. Show data transformation at each step, highlight decision points.

**Context Map** (deep only): when to use, when NOT to use, alternatives with tradeoff comparison.

**Complexity Notes** (deep only): cyclomatic complexity, nesting depth, time/space complexity of hot paths, concurrency assessment.

### 5. Follow-up

- "What about X?" -- extend at same depth.
- "Go deeper" -- increase one level, deliver only new sections.
- "Trace a different path" -- re-run Trace with different scenario.
- "Show me in my code" -- find the concept via Grep/Glob.

## Quick Reference

```
/ai-explain <topic>                  # standard depth (default)
/ai-explain <topic> --depth brief    # summary + walkthrough only
/ai-explain <topic> --depth deep     # all sections including complexity
```

## Common Mistakes

- Over-explaining standard concepts -- assume technical competence.
- Using Mermaid diagrams -- always ASCII art for terminal readability.
- Generic gotchas ("be careful with null") -- must be specific to the code under review.
- Using "basically", "simply", "just" -- these minimize real complexity.

## Integration

- Shared by `/ai-guide` for teaching mode.
- References actual codebase via Grep/Glob, not idealized examples.
- Read-only -- never writes code, tests, or documentation.

## References

- `.agents/skills/guide/SKILL.md` -- uses explain for teaching interactions.
- `.agents/skills/verify/SKILL.md` -- architecture assessment mode.
$ARGUMENTS
