---
name: faion-mlp-planning
description: "Transform MVP to MLP (Most Lovable Product). Gap analysis, WOW moments. Triggers: mlp, lovable product."
user-invocable: false
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, TodoWrite
---

# MLP Planning Skill

**Communication: User's language. Docs: English.**

## What is MLP?

**Most Lovable Product** — version users LOVE, not just tolerate.

| MVP | MLP |
|-----|-----|
| "It works" | "This is amazing!" |
| Validate idea | Build emotional connection |

## Agents

| Agent | Purpose |
|-------|---------|
| faion-mvp-scope-analyzer-agent | MVP scope via competitor analysis |
| faion-mlp-spec-analyzer-agent | Extract current MVP state from specs |
| faion-mlp-gap-finder-agent | Compare MVP vs MLP, find gaps |
| faion-mlp-spec-updater-agent | Add MLP requirements to specs |
| faion-mlp-feature-proposer-agent | Propose WOW features (web research) |
| faion-mlp-impl-planner-agent | Create phased implementation plan |

## Workflow

```
1. Analyze MVP scope (competitors)
2. Extract current state from specs
3. Find MLP gaps
4. Propose WOW features
5. Update specs with MLP reqs
6. Create implementation order
```

## Execution

```python
# Sequential agent execution
Task(subagent_type="faion-mvp-scope-analyzer-agent",
     prompt=f"Analyze {product_type} competitors for MVP scope")

Task(subagent_type="faion-mlp-spec-analyzer-agent",
     prompt=f"Read specs in {features_path}")

Task(subagent_type="faion-mlp-gap-finder-agent",
     prompt=f"Compare MVP vs MLP requirements")

Task(subagent_type="faion-mlp-feature-proposer-agent",
     prompt=f"Propose WOW features for {product}")

Task(subagent_type="faion-mlp-spec-updater-agent",
     prompt=f"Update specs with MLP requirements")

Task(subagent_type="faion-mlp-impl-planner-agent",
     prompt=f"Create MLP implementation phases")
```

## Output

```
product_docs/
├── mvp-scope-analysis.md
├── mlp-analysis-report.md
└── mlp-implementation-order.md
```

## MLP Dimensions

- **Delight**: Micro-interactions, animations, polish
- **Ease**: Intuitive UX, zero friction
- **Speed**: Instant feedback, fast performance
- **Trust**: Security signals, reliability
- **Personality**: Brand voice, memorable moments
