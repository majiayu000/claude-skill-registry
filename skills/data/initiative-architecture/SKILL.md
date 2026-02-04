---
name: initiative-architecture
description: Use for MASSIVE work requests requiring multi-epic planning. Creates research spikes, documents all unknowns and decisions, builds resumable architecture documents, and structures work into epics and milestones.
---

# Initiative Architecture

## Overview

When work is too large for a single epic, it becomes an **initiative**. This skill methodically investigates, documents, and structures massive requests into a resumable, tractable plan.

**Core principle:** Document everything. Every unknown answered, every decision made, every assumption validated. The architecture must be resumable by a fresh context.

**Announce at start:** "I'm using initiative-architecture to plan this massive request. This will involve investigation, documentation, and structured decomposition."

## What is an Initiative?

An initiative is work that:
- Spans multiple epics (feature areas)
- Requires significant research before planning
- May need new infrastructure or capabilities
- Will take weeks to months to complete
- Has many unknowns that need investigation

## The Architecture Process

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INITIATIVE RECEIVED                               │
│              (from work-intake as MASSIVE)                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 1: DOCUMENT UNKNOWNS                            │
│  List everything we don't know                                      │
│  Prioritize by: blocks other decisions                              │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 2: RESEARCH SPIKES                              │
│  Create issues for each unknown                                     │
│  Time-box investigations                                            │
│  Document findings in issues                                        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 3: DECISION LOG                                 │
│  Record all decisions made                                          │
│  Document alternatives considered                                   │
│  Note constraints and trade-offs                                    │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 4: EPIC STRUCTURE                               │
│  Group deliverables into epics                                      │
│  Define dependencies between epics                                  │
│  Create epic tracking issues                                        │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│               PHASE 5: MILESTONE PLANNING                           │
│  Create delivery milestones                                         │
│  Assign epics to milestones                                         │
│  Establish order of work                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
                    READY FOR IMPLEMENTATION
                    (via epic-management per epic)
```

## Phase 1: Document Unknowns

### Create Initiative Tracking Issue

```bash
gh issue create \
  --title "[Initiative] [NAME]: Architecture & Planning" \
  --label "initiative,planning" \
  --body "## Initiative: [NAME]

## Original Request
[The original user request verbatim]

## Goal
[What success looks like at the highest level]

## Current Understanding
[What we know so far]

## Unknowns (To Be Investigated)

### Critical Unknowns (Block Architecture)
- [ ] Unknown 1: [Question]
- [ ] Unknown 2: [Question]

### Important Unknowns (Block Implementation)
- [ ] Unknown 3: [Question]
- [ ] Unknown 4: [Question]

### Nice-to-Know (Inform Decisions)
- [ ] Unknown 5: [Question]

## Research Spikes
[Will be populated as spikes are created]

## Decisions Log
[Will be populated as decisions are made]

## Epic Structure
[Will be populated after research]

## Milestones
[Will be populated after epic structure]

---
**Status:** 🔬 Investigating
**Last Updated:** [DATE]
**Context Recovery:** Read this issue + linked spikes + decision log"
```

### Unknown Categories

| Category | Definition | Action |
|----------|------------|--------|
| **Critical** | Blocks architecture decisions | Research spike immediately |
| **Important** | Blocks implementation | Research spike before epic |
| **Nice-to-Know** | Informs decisions | Research during implementation |

## Phase 2: Research Spikes

### Create Spike Issues

For each critical/important unknown:

```bash
gh issue create \
  --title "[Spike] [INITIATIVE]: [UNKNOWN QUESTION]" \
  --label "spike,research,initiative-[NAME]" \
  --body "## Research Spike

**Parent Initiative:** #[INITIATIVE_NUMBER]
**Unknown:** [The question we're answering]
**Time-box:** [X hours/days]

## Investigation Plan
1. [ ] Check existing codebase for [X]
2. [ ] Review documentation for [Y]
3. [ ] Test/prototype [Z]
4. [ ] Document findings

## Findings
[To be filled during research]

## Recommendation
[To be filled after research]

## Decision Needed
[What decision this enables]

---
**Status:** 🔬 Investigating
**Started:** [DATE]
**Due:** [DATE]"
```

### Spike Execution

Each spike should:
1. **Time-box** - Don't over-investigate
2. **Document as you go** - Findings in the issue
3. **Conclude with recommendation** - Clear next step
4. **Update initiative** - Mark unknown as resolved

### Spike Completion

```bash
# Update spike issue with findings
gh issue comment [SPIKE_NUMBER] --body "## Findings Summary

**Answer:** [The answer to the unknown]

**Evidence:**
- [Finding 1]
- [Finding 2]

**Recommendation:** [Recommended approach]

**Confidence:** [High/Medium/Low]

**Trade-offs:**
- Pro: [X]
- Con: [Y]"

# Close spike
gh issue close [SPIKE_NUMBER]

# Update initiative issue
gh issue comment [INITIATIVE_NUMBER] --body "## Spike Complete: #[SPIKE_NUMBER]

**Unknown:** [Question]
**Answer:** [Answer summary]
**Decision enabled:** [What we can now decide]"
```

## Phase 3: Decision Log

### Record Every Decision

In the initiative issue, maintain a decision log:

```markdown
## Decisions Log

### Decision 1: [Topic]
**Date:** [DATE]
**Context:** [Why this decision was needed]
**Options Considered:**
1. Option A: [Description] - [Pros/Cons]
2. Option B: [Description] - [Pros/Cons]
3. Option C: [Description] - [Pros/Cons]

**Decision:** Option [X]
**Rationale:** [Why this option]
**Implications:** [What this means for implementation]
**Spike:** #[SPIKE_NUMBER] (if applicable)

---

### Decision 2: [Topic]
...
```

### Decision Template

Use this for each decision:

```markdown
### Decision: [TITLE]
**Date:** YYYY-MM-DD
**Decided by:** [Agent/Human/Both]

**Context:**
[Why this decision was needed now]

**Options:**
| Option | Pros | Cons |
|--------|------|------|
| A: [X] | [+] | [-] |
| B: [Y] | [+] | [-] |

**Decision:** [Chosen option]

**Rationale:**
[Why this option was chosen]

**Reversibility:** [Easy/Hard/Irreversible]

**Related:**
- Spike: #[N] (if applicable)
- Depends on: Decision [X]
- Enables: Decision [Y]
```

## Phase 4: Epic Structure

### Identify Epics

After research spikes complete, group work into epics:

```markdown
## Epic Structure

### Epic 1: [NAME]
**Goal:** [What this epic delivers]
**Dependencies:** None
**Estimated Issues:** [X-Y]
**Key Deliverables:**
- Deliverable A
- Deliverable B

### Epic 2: [NAME]
**Goal:** [What this epic delivers]
**Dependencies:** Epic 1
**Estimated Issues:** [X-Y]
**Key Deliverables:**
- Deliverable C
- Deliverable D

### Epic 3: [NAME]
**Goal:** [What this epic delivers]
**Dependencies:** Epic 1, Epic 2
**Estimated Issues:** [X-Y]
**Key Deliverables:**
- Deliverable E
```

### Create Epic Labels

```bash
# Create initiative label
gh label create "initiative-[NAME]" --color "6E40C9" \
  --description "Part of [INITIATIVE NAME] initiative"

# Create epic labels
gh label create "epic-[EPIC1-NAME]" --color "0E8A16" \
  --description "[Epic 1 description]"
gh label create "epic-[EPIC2-NAME]" --color "1D76DB" \
  --description "[Epic 2 description]"
```

### Create Epic Tracking Issues

For each epic, use `epic-management` skill to create the epic structure.

## Phase 5: Milestone Planning

### Create Milestones

```bash
# Create milestones for delivery phases
gh api repos/{owner}/{repo}/milestones -X POST \
  -f title="[Initiative] Phase 1: [NAME]" \
  -f description="[Description of what Phase 1 delivers]" \
  -f due_on="YYYY-MM-DDTHH:MM:SSZ"
```

### Assign Epics to Milestones

| Milestone | Epics | Goal |
|-----------|-------|------|
| Phase 1 | Epic 1 | [Foundation] |
| Phase 2 | Epic 2, 3 | [Core Features] |
| Phase 3 | Epic 4 | [Polish & Launch] |

## Resumability

### Context Recovery Document

The initiative issue must always contain enough information for a fresh context to continue:

```markdown
## Context Recovery

**To continue this initiative:**

1. Read this issue completely
2. Review open spikes: [links]
3. Review decision log above
4. Check current epic status: [links]
5. Current phase: [Investigation/Architecture/Implementation]
6. Next action: [Specific next step]

**Key files:**
- [Path to any architecture docs]
- [Path to any design docs]

**Key decisions made:**
1. [Decision 1 summary]
2. [Decision 2 summary]
```

### Memory Integration

```bash
# Store initiative in knowledge graph
mcp__memory__create_entities([{
  "name": "Initiative-[NAME]",
  "entityType": "Initiative",
  "observations": [
    "Created: [DATE]",
    "Goal: [GOAL]",
    "Tracking Issue: #[NUMBER]",
    "Status: [STATUS]",
    "Epics: [LIST]",
    "Current Phase: [PHASE]"
  ]
}])
```

## Example: Mobile Push Login Initiative

**Request:** "Add the ability for users to log in by clicking on a popup in their phone."

### Phase 1: Unknowns

Critical:
- [ ] Does a mobile app exist?
- [ ] What push notification infrastructure exists?
- [ ] What authentication system is in use?

Important:
- [ ] What are security requirements for push auth?
- [ ] What platforms need support (iOS/Android)?

### Phase 2: Spikes Created

1. #201 - [Spike] Mobile App Status Investigation
2. #202 - [Spike] Push Notification Infrastructure Review
3. #203 - [Spike] Authentication System Analysis
4. #204 - [Spike] Push Authentication Security Requirements

### Phase 3: Decisions Made

1. **Mobile App:** Need to build (doesn't exist) → React Native
2. **Push Infrastructure:** Use Firebase Cloud Messaging
3. **Auth Flow:** Magic link via push with JWT

### Phase 4: Epic Structure

1. Epic: Mobile App Foundation (10 issues)
2. Epic: Push Notification System (8 issues)
3. Epic: Push Authentication Flow (12 issues)
4. Epic: Backend Auth Integration (6 issues)
5. Epic: Testing & Security Audit (5 issues)

### Phase 5: Milestones

1. Phase 1: App + Push Infrastructure (Epics 1, 2)
2. Phase 2: Auth Implementation (Epics 3, 4)
3. Phase 3: Hardening (Epic 5)

## Checklist

- [ ] Created initiative tracking issue
- [ ] Documented all unknowns
- [ ] Categorized unknowns (Critical/Important/Nice-to-Know)
- [ ] Created research spikes for critical unknowns
- [ ] Completed research spikes
- [ ] Documented all decisions with rationale
- [ ] Defined epic structure
- [ ] Created epic labels
- [ ] Created milestones
- [ ] Added context recovery section
- [ ] Stored in knowledge graph
