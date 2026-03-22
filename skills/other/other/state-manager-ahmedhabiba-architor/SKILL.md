---
name: state-manager
description: Manages architecture project state in .arch/state.json and .arch/decisions.md. Activates when reading or updating project phase state, tracking component acceptance, logging decisions, or validating phase transitions.
---

# State Manager

## State File: `.arch/state.json`

This file is the single source of truth for project progress. ALWAYS read it before responding to architecture queries. ALWAYS update it after state changes.

### Reading State
- Parse the JSON file
- Check `current_phase` to know where we are
- Check phase-specific status fields for detail
- For Phase 2, check `sub_phase` and individual acceptance flags (pattern_accepted, components_overview_accepted, cross_cutting_accepted)
- For Phase 3, check `components` object for per-component status
- Check `reopens.count` and `reopens.max` for reopen availability

### Valid Phase Transitions
```
not_started → evaluation     (when /analyze-prd runs)
evaluation → methodology     (when Phase 1 is accepted)
methodology → components     (when Phase 2 is fully accepted: pattern + components + cross-cutting)
components → finalization    (when ALL components accepted)
```

Backward transitions are ONLY allowed via /reopen (max 2 per project).

### Phase 2 Sub-Phases
```
pattern → components_overview → cross_cutting
```
Each sub-phase is accepted independently via /accept. All three must be accepted for Phase 2 to be complete.

### Component Status Values
```
pending → in_progress        (when /design-component starts)
in_progress → awaiting_acceptance  (when design is presented)
awaiting_acceptance → accepted     (when user accepts)
awaiting_acceptance → in_progress  (when user refines)
needs-review → in_progress         (after a reopen cascades)
```

### Updating State
When updating state.json:
1. Read current state
2. Validate the transition is legal
3. Write the updated state
4. Increment `decision_count` if a decision was made

## Decision Log: `.arch/decisions.md`

Append-only file. Never edit previous entries. Format:

```markdown
### [DEC-NNN] Phase X | Category
- **Decision:** [What was decided]
- **Rationale:** [Why this choice]
- **Alternatives:** [What else was considered]
- **Trade-offs:** [What was sacrificed]
- **Risk:** [Any residual risk]
- **Supersedes:** [DEC-NNN — only if this replaces a previous decision]
- **References:** [FR-NNN, DEC-NNN — only if tracing to requirements or cross-cutting decisions]
- **Date:** [ISO timestamp]
```

Categories: Requirements | Pattern | Technology | Integration | Security | Infrastructure | Process | Reopen

`Supersedes` and `References` are optional. Omit the line entirely when not applicable.

### Supersession and Traceability Fields

**Supersedes** — Use when a decision replaces a previous one:
- `/reopen` creates a new decision that supersedes the original acceptance decision for the reopened target
- `/alternative` creates a new decision that supersedes the previous proposal's decision
- Format: `**Supersedes:** DEC-003` (single) or `**Supersedes:** DEC-003, DEC-007` (multiple)
- NEVER edit the superseded entry — the new entry points backward (like RFC "Obsoletes:" fields)

**References** — Use when a decision traces to requirements or earlier decisions:
- Phase 3 component technology decisions should reference the FR-NNN requirements they satisfy
- Phase 3 component decisions should reference applicable DEC-NNN cross-cutting decisions from Phase 2C
- Phase 2 acceptance decisions should reference the FR-NNN requirements that drove the pattern choice
- Refinement decisions should reference the DEC-NNN of the original proposal being refined
- Format: `**References:** FR-001, FR-003, DEC-005`

**Example — supersession (reopen scenario):**
```
### [DEC-012] Phase 2A | Reopen
- **Decision:** Reopened architecture pattern selection
- **Rationale:** New compliance requirement invalidates serverless approach
- **Alternatives:** Could have added compliance layer on top of existing pattern
- **Trade-offs:** Progress reset on 5 items
- **Risk:** Reopens remaining: 1 of 2
- **Supersedes:** DEC-004
- **Date:** 2026-03-11T14:00:00Z
```

**Example — traceability (component design):**
```
### [DEC-015] Phase 3 | Technology
- **Decision:** Selected PostgreSQL 16 for order-service data store
- **Rationale:** ACID compliance required for financial transactions; team has production experience
- **Alternatives:** MongoDB 7 (flexible schema but lacks native ACID), CockroachDB 24 (distributed but overkill)
- **Trade-offs:** Schema migrations required; less flexibility than document store
- **Risk:** Single-node bottleneck if order volume exceeds 50K TPS
- **References:** FR-003, FR-012, DEC-008, DEC-009
- **Date:** 2026-03-11T15:30:00Z
```

### Automatic Logging Events
Log a decision entry for:
- Phase acceptance
- Phase transition
- Sub-phase acceptance (2A, 2B, 2C)
- Technology selection (per component)
- Refinement requests (what changed and why)
- Alternative requests (what was replaced)
- Review findings (significant concerns raised)
- Reopen operations (with cascade details)
