---
name: doc-discovery
description: Loads feature docs, workflow docs, and invariants before planning any task. Use when starting complex work, changing multiple features, or when unsure about constraints. Essential first step for non-trivial changes.
allowed-tools: Read, Glob, Grep
---

# Doc Discovery

Load only necessary documentation before planning. Understand feature landscape BEFORE coding.

## When to Use

- Starting any task touching server actions, database, or AI
- Before creating a plan for non-trivial changes
- When uncertain about feature boundaries
- After user describes a bug or feature request

## Process

1. **Identify Primary Feature**: Read `docs/features/FEATURE_INDEX.md` → find owner
2. **Map Coupling**: Check "Couples with" entries → list secondary features
3. **Load Feature Docs**: Read primary + coupled feature docs → extract invariants
4. **High-Risk Check**: Auth/RLS? AI? Billing? Schema? Org-scoped? New Pages? → load specialized docs
5. **Workflow Impact**: Read `docs/workflows/WORKFLOW_INDEX.md` → identify affected journeys

## High-Risk Areas — Required Doc Loading

| Area | Trigger | Load |
|------|---------|------|
| AI Context Engine | Changes to RAG, embeddings, context | `docs/features/ai-context-engine.md` |
| Org-Scoped Content | New org-specific data, org filtering | `docs/architecture/org-scoped-content.md` |
| New Page Creation | Any new page or layout | `docs/frontend/PAGE_STANDARDS.md` |
| Auth/RLS | Permission changes, policy updates | `docs/foundation/auth-roles-rls.md` |
| Billing | Credits, subscriptions, entitlements | `docs/features/billing-subscription.md` |
| Schema | New tables, columns, migrations | Load relevant feature docs |

## Output

```markdown
## Doc Discovery Complete

### Primary Feature
- **Name**: [feature-name]
- **Risk**: [low/medium/high]

### Coupled Features
| Feature | Coupling Type |
|---------|--------------|
| [name] | [data/API/UI] |

### Key Invariants
1. [Invariant from primary]
2. [Invariant from coupled]
3. [Invariant from coupled]

### High-Risk Areas
- Auth/RLS: [yes/no]
- AI/Prompts: [yes/no]
- Billing: [yes/no]
- Schema: [yes/no]

### Workflows Affected
- [workflow]: Steps [X, Y, Z]

### Ready for Planning
[Yes / No - missing: X]
```

## Validation

Before proceeding:
- [ ] Primary feature identified and doc loaded
- [ ] All coupled features identified
- [ ] Invariants extracted (minimum 3)
- [ ] High-risk areas checked
- [ ] Workflow impact assessed

## Related

- Examples: See [reference/examples.md](reference/examples.md)
- High-risk areas guide: See [reference/high-risk-areas.md](reference/high-risk-areas.md)
- Next step: `/plan-lint`
