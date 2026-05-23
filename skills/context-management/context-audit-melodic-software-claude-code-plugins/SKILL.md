---
name: context-audit
description: Audit current context composition and identify optimization opportunities. Use when context window is overloaded, agents are underperforming, or applying the R&D framework to optimize token usage.
allowed-tools: Read, Grep, Glob
---

# Context Audit Skill

Audit a codebase's context engineering health and identify optimization opportunities.

## Purpose

A focused agent is a performant agent. This skill helps you understand what's consuming your context window and where to apply the R&D framework.

## When to Use

- Starting work on a new codebase
- Agent performance feels sluggish
- Context warnings appearing
- Before optimizing context strategy
- Periodic context health checks

## Audit Process

### 1. Memory File Analysis

Scan for CLAUDE.md and related memory files:

```text
Check:
- Root CLAUDE.md size (target: <2KB)
- Number of imports
- Per-directory CLAUDE.md files
- Total memory file tokens
```

Score memory health:

| Size | Score | Assessment |
| --- | --- | --- |
| <1KB | Excellent | Minimal and focused |
| 1-2KB | Good | Within target range |
| 2-5KB | Needs Review | Growing, audit content |
| >5KB | Action Required | Bloated, needs R&D |

### 2. MCP Server Analysis

Check MCP configurations:

```text
Check:
- .mcp.json existence
- Number of MCP servers configured
- Per-server token estimate (2-5% each)
- Active vs unused servers
```

Score MCP health:

| Servers | Score | Assessment |
| --- | --- | --- |
| 0 | Excellent | No MCP bloat |
| 1-2 | Good | Targeted usage |
| 3-5 | Review | May be over-provisioned |
| >5 | Action Required | Likely consuming 15%+ |

### 3. Commands Analysis

Review .claude/commands/:

```text
Check:
- Number of commands
- Command complexity (simple vs complex)
- Priming commands present?
- Task-type coverage
```

Score command health:

| Commands | Score | Assessment |
| --- | --- | --- |
| Has priming | Excellent | Dynamic context loading |
| No priming | Needs Attention | Relying on static memory |

### 4. Hooks Analysis

Check for context-consuming hooks:

```text
Check:
- Number of hooks
- Hook event types
- Potential context injection
```

### 5. Overall Context Score

Calculate overall context engineering score:

| Component | Weight | Max Points |
| --- | --- | --- |
| Memory Files | 30% | 30 |
| MCP Configuration | 25% | 25 |
| Command Infrastructure | 25% | 25 |
| Context Patterns | 20% | 20 |

## Output Format

```json
{
  "score": 75,
  "grade": "B",
  "components": {
    "memory": {
      "score": 20,
      "max": 30,
      "files_found": ["CLAUDE.md"],
      "total_tokens": 1500,
      "issues": ["No priming commands detected"]
    },
    "mcp": {
      "score": 25,
      "max": 25,
      "servers_found": 0,
      "estimated_consumption": "0%"
    },
    "commands": {
      "score": 15,
      "max": 25,
      "count": 5,
      "has_priming": false,
      "issues": ["Missing /prime command"]
    },
    "patterns": {
      "score": 15,
      "max": 20,
      "issues": ["No output styles defined"]
    }
  },
  "recommendations": [
    "Create /prime command for dynamic context loading",
    "Reduce CLAUDE.md size by delegating to priming",
    "Consider output styles for token efficiency"
  ]
}
```

## Grading Scale

| Score | Grade | Status |
| --- | --- | --- |
| 90-100 | A | Elite context engineering |
| 80-89 | B | Good practices, minor optimizations |
| 70-79 | C | Functional, needs attention |
| 60-69 | D | Significant issues |
| <60 | F | Context bloat, major rework needed |

## Recommendations Framework

Based on findings, recommend:

### For Memory Bloat (Reduce)

- Identify content that can move to priming commands
- Flag outdated or contradictory guidance
- Suggest minimal CLAUDE.md structure

### For Missing Infrastructure (Delegate)

- Recommend priming command creation
- Suggest output styles for verbosity control
- Propose agent expert patterns

## Cross-References

- @rd-framework.md - Reduce and Delegate strategies
- @context-layers.md - Understanding context composition
- @context-rot-vs-pollution.md - Diagnosing context problems
- @context-priming-patterns.md - Dynamic context loading

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
