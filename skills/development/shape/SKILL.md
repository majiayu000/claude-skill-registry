---
name: shape
description: Bridge WHAT (intent) to HOW (implementation). Auto-triggers after /hope:intent when spec_score >=5. Discovers relevant aspects, consults anchor experts, outputs SHAPE.md with criteria/mustNot/verification. Triggers on "shape this", "how should I build", "implementation approach".
---

# Shape

Bridge between intent clarification and implementation. Transforms WHAT into HOW.

## When This Skill Activates

- After `/hope:intent` when spec_score >= 5
- Explicit request: "shape this", "how should I build this"
- Implementation approach questions
- Architecture decisions needed before coding

**If spec_score < 5:** Return to `/hope:intent` for clarification first.

---

## Protocol

### 1. Aspect Discovery

Not all aspects apply to every task. Discover which are relevant:

| Aspect | Signal Keywords | When Relevant |
|--------|-----------------|---------------|
| Data | database, schema, storage, persist | Stateful changes |
| API | endpoint, route, request, response | Service boundaries |
| UI | component, display, user, interaction | Visual interfaces |
| Auth | permission, role, access, security | Protected resources |
| Performance | fast, scale, concurrent, cache | High-traffic paths |
| Error | fail, recover, retry, fallback | Resilience needed |
| Testing | verify, confidence, coverage | Quality requirements |
| Migration | existing, legacy, transition | Brownfield work |
| Integration | third-party, external, sync | Cross-system |
| Deployment | release, rollback, feature flag | Delivery concerns |

**Rule:** Only shape aspects that appear in the spec or have clear dependencies.

---

### 2. Expert Consultation

For each relevant aspect, consult the appropriate expert:

| Aspect | Anchor Expert | Philosophy |
|--------|---------------|------------|
| Data | Rich Hickey | Immutability, simplicity, facts over place |
| API | Martin Fowler | Pragmatic patterns, evolvability |
| UI | Don Norman | User-centered, affordances, feedback |
| Auth | OWASP | Defense in depth, least privilege |
| Performance | Brendan Gregg | Measure first, optimize bottlenecks |
| Error | Michael Nygard | Stability patterns, circuit breakers |
| Testing | Kent Beck | Test behavior, not implementation |
| Migration | Sam Newman | Strangler fig, incremental migration |
| Integration | Gregor Hohpe | Messaging patterns, loose coupling |
| Deployment | Jez Humble | Continuous delivery, reversibility |

See [anchor-experts.md](references/anchor-experts.md) for detailed guidance.

---

### 3. Conflict Resolution

When experts disagree, apply the anchor hierarchy:

```
1. Hickey (simplicity) — "Is this genuinely simple, or just familiar?"
2. Fowler (pragmatism) — "Can I change this later without a rewrite?"
3. If still tied — Pick option with fewer dependencies
```

**Document conflicts:** Note which experts disagreed and why one was chosen.

---

### 4. SHAPE.md Output

Generate `.loop/shape/SHAPE.md`:

```markdown
## Shape: [Task Name]

### Relevant Aspects
- [Aspect 1]: [Why relevant]
- [Aspect 2]: [Why relevant]

### Implementation Criteria

criteria:
- [Criterion 1 — Boolean, verifiable]
- [Criterion 2 — Specific outcome]
- [Criterion 3 — Measurable state]

### Must-NOT Constraints

mustNot:
- [Constraint 1 — What to avoid]
- [Constraint 2 — Anti-pattern to prevent]

### Verification Plan

| Criterion | Verification Type | Command/Method |
|-----------|------------------|----------------|
| [Criterion 1] | execution output | `npm test` |
| [Criterion 2] | observation | Visual check in browser |
| [Criterion 3] | measurement | Response time < 100ms |

### Expert Decisions

| Aspect | Expert | Recommendation | Confidence |
|--------|--------|----------------|------------|
| Data | Hickey | Use immutable events | 85% |
| API | Fowler | REST with HATEOAS | 75% |

### Conflicts Resolved

[If any experts disagreed, document here with reasoning]
```

See [shape-template.md](references/shape-template.md) for full template.

---

## Modes

### Present Mode (Default)

Show reasoning, ask user on conflicts:

1. Display discovered aspects with evidence
2. Show expert recommendations
3. Pause on conflicts: "Hickey suggests X, Fowler suggests Y. Which aligns with your goals?"
4. Generate SHAPE.md after user approval

### Autonomous Mode

Apply anchor hierarchy silently:

1. Discover aspects
2. Consult experts
3. Resolve conflicts using hierarchy
4. Generate SHAPE.md
5. Announce: `[SHAPE] Generated .loop/shape/SHAPE.md | N criteria | M mustNot`

**Trigger autonomous:** "shape this autonomously" or fit_score >= 40

---

## Loop Integration

SHAPE.md feeds directly into `/loop:start`:

| SHAPE Field | Loop Field |
|-------------|------------|
| `criteria:` | `criteriaStatus` |
| `mustNot:` | Circuit breaker triggers |
| `verification:` | Verification type per criterion |

**Exit blocked:** If any criterion has verification type "assumption", exit_signal cannot be true.

---

## Quality Footer

After generating SHAPE.md:

```
╭─ [VERDICT] ──────────────────────────────╮
│ Aspects: N shaped | Experts: M consulted │
│ Criteria: X | MustNot: Y                 │
│ Conflicts: Z resolved via hierarchy      │
├──────────────────────────────────────────┤
│ ↳ Alt: [alternative approach]            │
│ ↳ Key assumption: [main uncertainty]     │
╰──────────────────────────────────────────╯
```

---

## References

- `references/aspect-discovery.md` — Detailed aspect signals
- `references/anchor-experts.md` — Expert philosophies and guidance
- `references/shape-template.md` — Full SHAPE.md template
