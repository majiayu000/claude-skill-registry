---
name: writing-prds-from-charters
description: Use when you have an approved charter and need to produce a detailed PRD that engineering and design can execute.
---

# Writing PRDs from Charters

## Overview

Converts an approved quarterly charter into a detailed Product Requirements Document. Produces executable specs with requirements, edge cases, telemetry, rollout plan, and GTM notes.

## When to Use

- Charter approved, ready to spec
- Eng/design needs detailed requirements
- Starting sprint planning for a charter
- Need to document edge cases and telemetry

## Output Formats

By default, produces full PRD. Use `--format` for audience-specific outputs:

| Format | Command | Audience | Content |
|--------|---------|----------|---------|
| `full` (default) | `writing-prds-from-charters` | Full team | Complete PRD with all sections |
| `exec` | `writing-prds-from-charters --format exec` | Executives | 1-page: problem, metrics, timeline, risks |
| `eng` | `writing-prds-from-charters --format eng` | Engineering | Requirements, data model, edge cases, telemetry only |

### Exec Format (`--format exec`)

Produces a 1-page executive summary:

```markdown
# PRD Summary: [Feature Name]

## At a Glance
| Field | Value |
|-------|-------|
| Problem | [1 sentence] |
| Target Users | [Segment] |
| Success Metric | [KPI + target] |
| Target Release | Q[X] YYYY |

## Key Risks
| Risk | Mitigation |
|------|------------|
| [Top 2-3 risks] |

## Timeline
| Milestone | Date |
|-----------|------|
| Alpha | [Date] |
| GA | [Date] |

## Decisions Needed
[Any leadership decisions required]
```

### Eng Format (`--format eng`)

Produces engineering-focused spec:

```markdown
# Engineering Spec: [Feature Name]

## Functional Requirements
[FR-1 through FR-N with acceptance criteria]

## Non-Functional Requirements
[Performance, security, accessibility]

## Data Model
[Entities, fields, types, constraints]

## Edge Cases & Error Handling
[Full table of scenarios]

## Telemetry
[Events, dimensions, dashboards]

## Feature Flags
[Flags and rollout controls]

## Technical Open Questions
[Questions that need eng input]
```

## Core Pattern

**Step 1: Load the Charter**

Read the specific charter from `outputs/roadmap/Qx-YYYY-charters.md`.

Also read:
- Any relevant VOC from `outputs/insights/voc-synthesis-*.md`
- Any relevant KB from `inputs/knowledge_base/`

**Step 2: Validate Charter Completeness**

Check the charter has:
- [ ] Clear problem statement with evidence
- [ ] Defined target users
- [ ] Success metrics
- [ ] Scope boundaries

**If missing, ask user to update charter first.**

**Step 3: Expand Requirements**

For each scope item, define:

| Requirement Type | Content |
|------------------|---------|
| **Functional** | What the system must do (behavior) |
| **Non-Functional** | Performance, security, accessibility |
| **Edge Cases** | What happens when things go wrong |
| **Data** | What's stored, what's computed |

Use format: "The system SHALL [verb] [object] when [condition]"

**Step 4: Define Telemetry**

For each success metric in the charter:
- What events to track
- What dimensions to capture
- Where data is stored

**Step 5: Plan Rollout**

| Phase | Audience | Duration | Success Gate |
|-------|----------|----------|--------------|
| Alpha | Internal | 1 week | No P0 bugs |
| Beta | 10% users | 2 weeks | Metrics stable |
| GA | 100% | - | Success criteria met |

**Step 6: Note GTM Needs**

- Documentation updates needed
- Support training required
- Sales enablement materials
- Customer communication

**Step 7: Generate Output**

Write to `outputs/delivery/prds/[charter-name]-prd.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: writing-prds-from-charters
sources:
  - outputs/roadmap/Qx-YYYY-charters.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-*.md (if used)
downstream: []
---

# PRD: [Feature Name]

## Overview
| Field | Value |
|-------|-------|
| Charter | [Link to charter section] |
| Status | Draft / In Review / Approved |
| Author | [Name] |
| Last Updated | YYYY-MM-DD |
| Target Release | Q[X] YYYY |

## Problem Statement
[From charter, with evidence citations]

## Target Users
[From charter]

## Success Metrics
| Metric | Current | Target | Tracking Method |
|--------|---------|--------|-----------------|
| [KPI] | [X] | [Y] | [Event/Dashboard] |

---

## Functional Requirements

### FR-1: [Requirement Name]
**Description:** The system SHALL [verb] [object] when [condition].

**Acceptance Criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

**Priority:** Must / Should / Could

### FR-2: [Requirement Name]
...

---

## Non-Functional Requirements

### NFR-1: Performance
- [Latency requirement]
- [Throughput requirement]

### NFR-2: Security
- [Auth requirements]
- [Data handling]

### NFR-3: Accessibility
- [WCAG level]
- [Specific requirements]

---

## Edge Cases & Error Handling

| Scenario | Expected Behavior | Error Message |
|----------|-------------------|---------------|
| [User does X when Y] | [System does Z] | [Message shown] |
| [Data is invalid] | [Validation fails] | [Error text] |
| [Service unavailable] | [Graceful degradation] | [Fallback behavior] |

---

## Data Model

### New/Modified Entities
| Entity | Field | Type | Notes |
|--------|-------|------|-------|
| [Entity] | [field] | [type] | [constraints] |

### Data Flow
[Brief description or diagram reference]

---

## Telemetry & Analytics

### Events to Track
| Event | Trigger | Dimensions | Purpose |
|-------|---------|------------|---------|
| [event_name] | [when fired] | [user_id, action, etc.] | [what it measures] |

### Dashboards Needed
- [Dashboard 1]: [What it shows]

---

## Rollout Plan

| Phase | Audience | Duration | Entry Criteria | Exit Criteria |
|-------|----------|----------|----------------|---------------|
| Alpha | Internal QA | 1 week | Build complete | No P0/P1 bugs |
| Beta | 10% of [segment] | 2 weeks | Alpha exit | Metrics stable |
| GA | All users | - | Beta exit | Success metrics met |

### Feature Flags
| Flag | Default | Description |
|------|---------|-------------|
| [flag_name] | off | [What it controls] |

---

## GTM Requirements

### Documentation
- [ ] KB article: [topic]
- [ ] In-app help: [location]

### Support Training
- [ ] [Training topic]
- [ ] [Escalation path]

### Sales Enablement
- [ ] [Material needed]

### Customer Communication
- [ ] [Release notes]
- [ ] [In-app announcement]

---

## Open Questions
| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | [Question] | [Name/TBD] | [Date] |

## Risks
| Risk | Impact | Mitigation | Status |
|------|--------|------------|--------|
| [From charter + new] | H/M/L | [Action] | Open/Mitigated |

## Out of Scope
[From charter]

---

## Appendix

### User Stories
- As a [persona], I want [action], so that [benefit].

### Wireframes / Mockups
[Links or descriptions]

### Technical Notes
[Any implementation guidance for eng]

---

## Sources Used
- [file paths]

## Claims Ledger
| Claim | Type | Source |
|-------|------|--------|
| [Requirement based on X] | Evidence | [VOC/charter] |
```

**Step 8: Copy to History & Update Tracker**

- Copy to `history/writing-prds-from-charters/[name]-prd-YYYY-MM-DD.md`
- Update `alerts/stale-outputs.md`

## Quick Reference

| Section | Purpose |
|---------|---------|
| Functional Reqs | What system does |
| Non-Functional | How well it does it |
| Edge Cases | What happens when wrong |
| Telemetry | How we measure success |
| Rollout | How we ship safely |
| GTM | What else needs to happen |

## Common Mistakes

- **Vague requirements:** "Improve the UX" → "System SHALL display error within 100ms"
- **Missing edge cases:** "User submits form" → What if invalid? Empty? Duplicate?
- **No telemetry:** "We'll know it works" → Specific events and dimensions
- **No rollout plan:** "Just ship it" → Alpha/Beta/GA phases
- **Forgetting GTM:** Code ships, docs don't → List all GTM needs
- **Disconnected from charter:** PRD scope creep → Trace back to charter

## Verification Checklist

- [ ] Charter loaded and validated
- [ ] All scope items have requirements
- [ ] Requirements are testable (SHALL + acceptance criteria)
- [ ] Edge cases documented
- [ ] Telemetry maps to success metrics
- [ ] Rollout plan has phases and gates
- [ ] GTM needs listed
- [ ] Open questions have owners
- [ ] Risks from charter carried over
- [ ] Out of scope from charter included
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Requirement X] | Evidence | [Charter/VOC reference] |
| [Performance target] | Assumption | [Industry standard / "Need benchmark"] |
| [Rollout duration] | Assumption | [Team estimate] |
