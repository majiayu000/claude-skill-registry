---
name: planning
description: Research-backed implementation planning skill. This skill should be used when the /plan command is executed, when creating implementation plans, roadmaps, or architectural designs, or when tasks have high uncertainty requiring research before coding. Transforms user requests into execution-ready plans (PRP) using R.P.I.V workflow (Research → Plan → Implement → Validate).
---

# Planning Skill

Research-first planning methodology that eliminates unknowns before implementation.

> **Core Principle:** Context Density > Brevity | Research First > Implementation | Planning > Coding

## Activation Triggers

This skill is **mandatory** when:

1. User executes `/plan` command
2. Building plans, roadmaps, or architecture for new features/systems
3. High uncertainty or risk of hallucination without research
4. Multi-step execution requiring task decomposition
5. Third-party integrations (APIs, frameworks, infrastructure)

**Skip for:** Simple Q&A, pure copywriting, tasks solvable from provided context.

---

## R.P.I.V Workflow

### Phase 0: RESEARCH (Always First)

Eliminate unknowns and lock in best-practice approach.

**Priority order:**

1. Search codebase for patterns, conventions
2. Query Context7 for official docs
3. Tavily web search for best practices
4. Sequential Thinking for complex decisions

**Required outputs:**

- Findings Table: `| # | Finding | Confidence (1-5) | Source | Impact |`
- Knowledge Gaps: What remains unknown
- Assumptions to Validate: Explicit assumptions needing confirmation
- Edge Cases: Minimum 5 for L4+ complexity

> See `references/mcp-usage.md` for detailed MCP tool guidance.

### Phase 1: PLAN (Before Implementation)

Convert research into execution runbook with atomic tasks.

**Each task must have:**

- Clear action verb + specific target
- Validation command
- Rollback steps
- Dependencies mapped
- Mark `⚡ PARALLEL-SAFE` when independent

**Output:** `docs/PLAN-{task-slug}.md`

> See `references/plan-template.md` for complete template structure.

### Phase 2: IMPLEMENT (Only If Requested)

Execute per atomic tasks with validation gates.

**Pattern:** Implement → Validate → Commit (or Rollback)

**Quality gates after each task:**

- `bun run check` (TypeScript)
- `bun run format` (Prettier)
- `bun test` (Unit tests)

### Phase 3: VALIDATE (Always)

- Build: zero errors
- Lint: zero warnings
- Tests: all passing
- Consult specialists if security or schema changes involved

---

## Operating Modes

| Mode                               | Behavior                      | Output                |
| ---------------------------------- | ----------------------------- | --------------------- |
| CONSERVATIVE (default for `/plan`) | Research + plan only, no code | `docs/PLAN-{slug}.md` |
| PROACTIVE (for implementation)     | Research → plan → implement   | Code + plan file      |

---

## Complexity Levels

| Level  | Indicators                | Research Depth |
| ------ | ------------------------- | -------------- |
| L1-L2  | Bug fix, single function  | Repo-only      |
| L3-L5  | Feature, multi-file       | Docs + repo    |
| L6-L8  | Architecture, integration | Deep research  |
| L9-L10 | Migrations, multi-service | Comprehensive  |

> See `references/complexity-guide.md` for detailed classification.

---

## Anti-Patterns

| Bad                  | Good                                                     |
| -------------------- | -------------------------------------------------------- |
| "Implement auth"     | Research → Search codebase → Query docs → Then implement |
| Skip research        | ALWAYS research first, even for "simple" tasks           |
| Guess file paths     | Search and verify paths before referencing               |
| Speculate about code | Read files before making claims                          |

---

## Quick Reference

```
R.P.I.V: RESEARCH → PLAN → IMPLEMENT → VALIDATE

GOLDEN RULES:
✓ RESEARCH FIRST — never implement blind
✓ Be EXPLICIT — agent follows literally
✓ Explain WHY — enables generalization
✓ ATOMIC TASKS — small, validated, rollback-ready
✓ REFLECT AFTER TOOLS — think before next action
```

---

## Post-Planning Message

After creating the plan file:

```
✅ Plan created: docs/PLAN-{slug}.md

Next steps:
- Review the plan
- Run `/implement` to start implementation
- Or modify plan manually
```

---

## Resources

- `references/plan-template.md` — Complete PRP template structure
- `references/complexity-guide.md` — Task complexity classification
- `references/mcp-usage.md` — When and how to use MCP tools
