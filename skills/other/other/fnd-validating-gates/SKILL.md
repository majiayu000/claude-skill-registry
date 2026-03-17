---
name: fnd-validating-gates
description: Validates phase transition requirements for Canvas population. Checks G0-G4 gates to determine if prerequisites are met before advancing phases. Use when checking readiness, validating gates, or assessing Canvas completion status.
allowed-tools: Read, Grep, Glob
license: Complete terms in LICENSE.txt
---

# Gate Validating

Validate Canvas phase transitions and assess readiness.

## Phase Definitions

| Phase | Focus | Canvas Sections | Gate Out |
|-------|-------|-----------------|----------|
| 0. Mode | Business model choice | 00 | G0 |
| 1. Discovery | Market understanding | 01-06 | G1 |
| 2. Definition | Value & business model | 07-09, 12-14 | G2 |
| 3. Validation | Assumption testing | 10 | G3 |
| 4. Launch | Market entry | 11, 15 | G4 |
| 5. Execution | Live operations | - | - |

---

## Process

### Step 1: Identify Current Phase

Read existing Canvas files in `strategy/canvas/`. Determine current phase based on which sections exist and are populated.

### Step 2: Identify Target Gate

From request, determine which gate to validate:
- "Ready for definition?" → Check G1
- "Ready for validation?" → Check G2
- "Ready for launch?" → Check G3
- "Ready for execution?" → Check G4

### Step 3: Check Gate Requirements

Load gate requirements (below). For each criterion:
1. Read specified Canvas section
2. Apply check logic
3. Record PASS or FAIL

### Step 4: Report Results

Generate gate check report with status, blockers, and recommendations.

---

## Gate Requirements

### G0: Mode Selection → Discovery

| Requirement | Section | Check |
|-------------|---------|-------|
| **Required** | | |
| Mode declared | 00.mode | Contains VENTURE, BOOTSTRAP, or HYBRID |

### G1: Discovery → Definition

| Requirement | Section | Check |
|-------------|---------|-------|
| **Required** | | |
| Segment defined | 04.segments | At least 1 segment with 2+ filterable criteria |
| Problems ranked | 05.problem | Top 3 problems with severity scores |
| Competition mapped | 06.competitive | Direct + indirect competitors listed |
| **Soft Required** | | |
| Context captured | 01.context | File exists with content |
| Market sized | 03.opportunity | TAM/SAM/SOM estimated |

### G2: Definition → Validation

| Requirement | Section | Check |
|-------------|---------|-------|
| **Required** | | |
| UVP articulated | 07.uvp | Single sentence value prop exists |
| Solution defined | 09.solution | Feature list tied to problems + growth model |
| Pricing set | 12.revenue | At least 1 pricing tier defined |
| Unit economics | 13.metrics | CAC, LTV, LTV:CAC present |
| **Soft Required** | | |
| Defensibility | 08.unfair | Moat identified |
| Cost structure | 14.costs | Costs outlined |

### G3: Validation → Launch

| Requirement | Section | Check |
|-------------|---------|-------|
| **Required** | | |
| Assumptions documented | 10.assumptions | Prioritized list exists |
| Critical identified | 10.assumptions | P0 assumptions marked |
| **Soft Required** | | |
| High-risk validated | 10.assumptions | >50% P1 validated |

### G4: Launch → Execution

| Requirement | Section | Check |
|-------------|---------|-------|
| **Required** | | |
| Channels selected | 11.channels | Primary channel with CAC estimate |
| Motion defined | 15.gtm | Motion type declared with rationale |
| Launch sequence | 15.gtm | At least 2 phases defined |
| **Soft Required** | | |
| First customers | - | Identified or acquired |

---

## Output Format

```markdown
## Gate Check: [G0/G1/G2/G3/G4]

**Transition:** [Phase] → [Phase]
**Status:** [PASS | FAIL]

### Required Criteria

| Section | Criteria | Status |
|---------|----------|--------|
| [section] | [criteria] | ✅/❌ |

### Soft Required

| Section | Criteria | Status |
|---------|----------|--------|
| [section] | [criteria] | ✅/⚠️ |

### Blockers (if FAIL)

- [Specific missing element]
- [What needs to be done]

### Recommendations

- [Suggested next steps]
```

---

## Bypass Rules

Gates can be bypassed with explicit acknowledgment:

```markdown
## Gate Bypass

**Gate:** [G#]
**Missing:** [criteria]
**Reason:** [justification]
**Risk accepted:** [what could go wrong]
**Mitigation:** [how to handle if it fails]

⚠️ Proceeding with incomplete prerequisites
```

Document bypass in `strategy/canvas/00.mode.md` under a Bypasses section.

---

## Quick Reference

| Want To | Must Pass | Key Requirements |
|---------|-----------|------------------|
| Define value prop | G1 | Segments + Problems |
| Set pricing | G2 | UVP + Solution + Growth model |
| Plan channels | G2 | Pricing + Unit economics |
| Plan GTM | G3 | Assumptions + Channels |
| Launch | G4 | Channels + GTM motion |

---

## Canvas Completion Status

For overall status check:

```markdown
## Canvas Status

### Phase Completion

| Phase | Status | Sections |
|-------|--------|----------|
| Mode | ✅/❌ | 00 |
| Discovery | ✅/❌ | 01-06 |
| Definition | ✅/❌ | 07-09, 12-14 |
| Validation | ✅/❌ | 10 |
| Launch | ✅/❌ | 11, 15 |

### Section Detail

| Section | Exists | Complete |
|---------|--------|----------|
| 00.mode | ✅/❌ | ✅/❌ |
| 01.context | ✅/❌ | ✅/⚠️/❌ |
| ... | | |

### Next Gate: [G#]
**Status:** [X/Y required passing]
**Blockers:** [List]
```

## Boundaries

- Does NOT fix issues (reports only)
- Does NOT assess business viability or strategy quality
- Does NOT bypass gates without explicit user acknowledgment
- Validates structural completeness, not content quality
- Gate pass does not guarantee business success
- Bypass documentation required for any gate skip
- Does NOT validate external market conditions