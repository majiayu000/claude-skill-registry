---
name: using-spectacular
description: Use when starting any conversation in a project using spectacular - establishes mandatory workflows for spec-anchored development, including when to use /spectacular commands and how to work with constitutions
---

<EXTREMELY_IMPORTANT>
You have spectacular.

**The content below is your introduction to using spectacular:**

---

# Using Spectacular

Spectacular extends superpowers with spec-anchored development workflows. Before responding to user requests for features or refactors, you MUST check if spectacular workflows apply.

## MANDATORY FIRST RESPONSE PROTOCOL

Before responding to ANY user message about features, refactors, or implementations:

1. ☐ Does request involve implementing/refactoring features?
2. ☐ Is there a `docs/constitutions/current/` directory in this project?
3. ☐ If yes → Use spectacular workflow (spec → plan → execute)
4. ☐ If no constitution → Ask if user wants to use spectacular

**Responding to feature requests WITHOUT this check = automatic failure.**

## Core Spectacular Workflow

```
User request → /spectacular:spec → /spectacular:plan → /spectacular:execute
```

**Each command has a specific purpose:**

1. **`/spectacular:spec`** - Generate feature specification
   - When: User describes a feature to implement or refactor
   - Output: `specs/{runId}-{feature-slug}/spec.md`
   - Includes: Requirements, architecture, acceptance criteria
   - References: Constitution rules (doesn't duplicate them)

2. **`/spectacular:plan`** - Decompose spec into execution plan
   - When: After spec is reviewed and approved
   - Input: Path to spec.md
   - Output: `specs/{runId}-{feature-slug}/plan.md`
   - Analyzes: Task dependencies, file overlaps
   - Generates: Sequential/parallel phases with time estimates

3. **`/spectacular:execute`** - Execute plan with parallel orchestration
   - When: After plan is reviewed and approved
   - Input: Path to plan.md
   - Creates: Worktrees, spawns subagents, stacks branches
   - Quality gates: Tests/lint after each task, code review after each phase

## Constitutions: Architectural Truth

If `docs/constitutions/current/` exists, it contains **immutable architectural rules**:

- **architecture.md** - Layer boundaries, project structure
- **patterns.md** - Mandatory patterns (e.g., "use Zod for validation")
- **tech-stack.md** - Approved libraries and versions
- **testing.md** - Testing requirements

**Critical:**
- ✅ ALWAYS reference constitution in specs (don't duplicate)
- ✅ ALWAYS validate implementation against constitution
- ❌ NEVER violate constitutional patterns
- ❌ NEVER copy-paste constitution rules into specs

## Common Rationalizations That Mean You're Failing

If you catch yourself thinking ANY of these, STOP and use spectacular:

| Rationalization | Why It's Wrong | What to Do Instead |
|----------------|----------------|-------------------|
| "Request is clear, no spec needed" | Clear request = easier to spec, not permission to skip | Use `/spectacular:spec` |
| "Feature is small, just code it" | Small features drift without specs | Use `/spectacular:spec` |
| "User wants it fast" | Workflow IS faster (parallel + fewer bugs) | Use `/spectacular:spec` |
| "Constitution doesn't apply" | Constitution always applies | Reference in spec |
| "I can plan mentally" | Mental = no review, no parallelization | Use `/spectacular:plan` |
| "Just a bugfix/refactor" | Multi-file changes are features | If complex: use `/spectacular:spec` |

## Workflow Enforcement

**User instructions describe WHAT to build, not permission to skip workflows.**

- "Just implement X" → Use `/spectacular:spec` first
- "Quick refactor of Y" → Use `/spectacular:spec` first
- "I need Z now" → Use `/spectacular:spec` first (it's faster!)

**Why workflows matter:**
- Specs catch requirements drift before code
- Plans enable parallelization (3-5x faster)
- Constitution prevents architectural debt
- Quality gates catch bugs early

## Summary: Mandatory Workflow

**For feature/refactor requests:**

1. ✅ Check if spectacular applies (constitution exists?)
2. ✅ Use `/spectacular:spec` to create specification
3. ✅ User reviews spec (STOP until approved)
4. ✅ Use `/spectacular:plan` to decompose into tasks
5. ✅ User reviews plan (STOP until approved)
6. ✅ Use `/spectacular:execute` to implement with quality gates

**Skipping steps = violating quality standards.**

When in doubt: "Should I use spectacular for this?" → Almost always YES for multi-file changes.

</EXTREMELY_IMPORTANT>
