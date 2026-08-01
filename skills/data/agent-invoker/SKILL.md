---
name: agent-invoker
description: 'Quick reference for invoking CasareRPA agents via Task tool. AUTO-CHAIN
  ENABLED by default. Use when: invoking agents, running agent chains, task routing,
  choosing the right agent, understanding agent'
---

---
name: agent-invoker
description: Quick reference for invoking CasareRPA agents via Task tool. AUTO-CHAIN ENABLED by default. Use when: invoking agents, running agent chains, task routing, choosing the right agent, understanding agent auto-chaining, Task tool usage.
---

# Agent Invoker

Reference for invoking CasareRPA agents. **All agents now auto-chain by default.**

**For comprehensive task routing, see [TASK_ROUTING.md](../TASK_ROUTING.md)**

## AUTO-CHAIN MODE (Default)

When you invoke an agent, it **automatically runs the full chain** with parallel execution:

| Agent | Auto-Chain Flow |
|-------|----------------|
| `architect` | EXPLORE×3 → ARCHITECT → BUILDER+UI+INTEGRATIONS → QUALITY+DOCS → REVIEWER |
| `builder` | BUILDER → QUALITY → REVIEWER |
| `refactor` | EXPLORE → REFACTOR → QUALITY → REVIEWER |
| `ui` | EXPLORE → UI → QUALITY → REVIEWER |
| `integrations` | EXPLORE → INTEGRATIONS → QUALITY → REVIEWER |

## Agent Catalog

| Agent | System Name | Purpose | Auto-Chain |
|-------|-------------|---------|------------|
| `explore` | `explore` | Fast codebase search | No (used in chains) |
| `architect` | `architect` | Implementation + design | Yes (full chain) |
| `builder` | `builder` | Code writing | Yes (quality+reviewer) |
| `quality` | `quality` | Testing + performance | No (used in chains) |
| `reviewer` | `reviewer` | Code review gate | No (used in chains) |
| `refactor` | `refactor` | Code cleanup | Yes (full chain) |
| `researcher` | `researcher` | Research | No (standalone) |
| `docs` | `docs` | Documentation | No (used in chains) |
| `ui` | `ui` | Canvas UI design | Yes (full chain) |
| `integrations` | `integrations` | External APIs | Yes (full chain) |

## Usage Patterns

### Default: Auto-Chain (Recommended)

```python
# Architect runs FULL chain automatically
Task(subagent_type="architect", prompt="""
Implement HTTPRequestNode for browser automation.
- Location: src/casare_rpa/nodes/browser/
- Follow BaseNode pattern
""")

# This automatically runs:
# 1. EXPLORE ×3 (parallel)
# 2. ARCHITECT (plan)
# 3. BUILDER + UI + INTEGRATIONS (parallel)
# 4. QUALITY + DOCS (parallel)
# 5. REVIEWER (gate with loop on ISSUES)
```

### Skip Auto-Chain (Single Agent Mode)

```python
# Add single=true to run just this agent
Task(subagent_type="architect", prompt="""
single=true: Review this design only, don't run full chain.
""")
```

### Manual Full Chain Control

For complete control, use the `/chain` command or `parallel-exec` skill:

```python
# Via command
/chain implement "Add login feature" --parallel

# Via skill
Skill(skill="parallel-exec", args="Implement login feature with UI and tests")
```

## Quick Lookup

| Task | Use Agent | Auto-Chain |
|------|-----------|------------|
| Implement feature | `architect` | Yes (full chain) |
| Fix bug | `builder` | Yes (quality+reviewer) |
| Refactor code | `refactor` | Yes (full chain) |
| Design UI | `ui` | Yes (full chain) |
| API integration | `integrations` | Yes (full chain) |
| Research only | `researcher` | No |
| Quick explore | `explore` | No |
| Docs only | `docs` | No |

## Parallel Execution Details

### Phase 1: EXPLORE (Parallel ×3)
- Codebase patterns search
- Test patterns search
- Rules/docs search

### Phase 3: Implementation (Parallel)
- `builder` - Core logic
- `ui` - Presentation layer
- `integrations` - External APIs

### Phase 4: Validation (Parallel)
- `quality` - Tests and linting
- `docs` - Documentation updates

### Reviewer Gate (With Loop Recovery)
- If `APPROVED` → Chain complete
- If `ISSUES` → Loop back to BUILDER (max 3 iterations)
- If max exceeded → Escalation

## Error Recovery Loop

```
Iteration 1/3
  ARCHITECT → Plan approved
  BUILDER → Implementation
  QUALITY → Tests pass
  REVIEWER → ISSUES (2 found)
    ↓ Loop back to BUILDER
  BUILDER → Fixes applied
  QUALITY → Tests pass
  REVIEWER → APPROVED
✓ Chain complete
```
