---
name: fdd-feature-design
description: |
  Feature Design Document (FDD) methodology for structured feature development.
  Three-phase approach: Statement of Intent → Feature Requirements → Feature Realization.
  Ensures traceability from vision to implementation through explicit backlinks.
triggers:
  - "fdd"
  - "feature.*design.*document"
  - "statement.*intent"
  - "feature.*requirement"
  - "feature.*realization"
  - "frp"
  - "frd"
  - "soi"
  - "design.*document"
---

# Feature Design Document (FDD) Methodology

## Philosophy: Traceability from Vision to Code

FDD is a **structured documentation discipline** where:

1. **Intent precedes requirements** - Why before what
2. **Requirements precede solutions** - What before how
3. **Every artifact backlinks** - No orphaned decisions
4. **Documents are living** - Evolve with the feature

**Canonical principle:** If you cannot trace a line of code back to a stated intent, you have implementation drift.

---

## Document Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    STATEMENT OF INTENT (SOI)                    │
│                                                                 │
│  "Why does this feature exist? What problem does it solve?"     │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ ◄── FRD references SOI
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               FEATURE REQUIREMENT DOCUMENT (FRD)                │
│                                                                 │
│  "What must the feature do? What constraints exist?"            │
│                                                                 │
│  [REQ-001] ← backlinks to SOI intent                            │
│  [REQ-002] ← backlinks to SOI intent                            │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ ◄── FRP references FRD requirements
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              FEATURE REALIZATION PROPOSAL (FRP)                 │
│                                                                 │
│  "How will we implement the requirements?"                      │
│                                                                 │
│  Solution A → satisfies [REQ-001], [REQ-003]                    │
│  Solution B → satisfies [REQ-002], [REQ-004]                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Statement of Intent (SOI)

### Purpose

The SOI answers: **"Why are we building this?"**

It captures:
- The problem being solved
- The value proposition
- The stakeholders affected
- The success criteria

### Template

```markdown
# Statement of Intent: [Feature Name]

**Document ID:** SOI-[YYYYMMDD]-[feature-slug]
**Author:** [Name]
**Created:** [Date]
**Status:** Draft | Review | Approved | Superseded

---

## 1. Problem Statement

[Describe the problem or opportunity that motivates this feature.
Be specific about pain points and current limitations.]

### Current State

[What exists today? What is inadequate about it?]

### Desired State

[What does the ideal future look like?]

---

## 2. Stakeholders

| Stakeholder | Role | Impact |
|-------------|------|--------|
| [Who]       | [Their role] | [How they're affected] |

---

## 3. Value Proposition

[Why is solving this problem valuable? Quantify if possible.]

### Business Value

[Revenue, efficiency, competitive advantage, etc.]

### User Value

[Time saved, friction removed, capabilities gained, etc.]

### Technical Value

[Maintainability, performance, scalability improvements, etc.]

---

## 4. Success Criteria

| Criterion | Measurement | Target |
|-----------|-------------|--------|
| [What defines success] | [How we measure] | [Goal] |

---

## 5. Scope Boundaries

### In Scope

- [What this feature WILL address]

### Out of Scope

- [What this feature WILL NOT address]

### Deferred

- [What might be addressed in future iterations]

---

## 6. Risks and Assumptions

### Assumptions

- [What we're assuming to be true]

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | Low/Med/High | Low/Med/High | [How to mitigate] |

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | | | |
| Reviewer | | | |
| Approver | | | |
```

### SOI Example

```markdown
# Statement of Intent: Real-Time Collaboration

**Document ID:** SOI-20260117-realtime-collab
**Author:** Prime
**Created:** 2026-01-17
**Status:** Draft

---

## 1. Problem Statement

Users working in TMNL documents cannot see each other's changes in real-time.
This leads to:
- Duplicate work when two people edit the same section
- Merge conflicts that require manual resolution
- Poor collaboration experience compared to modern tools

### Current State

Documents are single-user. Changes sync on save, leading to overwrites.

### Desired State

Multiple users can edit simultaneously with live cursors, presence
indicators, and automatic conflict resolution.

---

## 2. Stakeholders

| Stakeholder | Role | Impact |
|-------------|------|--------|
| End Users | Document editors | Primary beneficiaries |
| DevOps | Infrastructure | Must provision CRDT sync servers |
| Security | Compliance | Must audit real-time data flows |

---

## 3. Value Proposition

### Business Value

Enables team workflows, increasing TMNL adoption for teams of 3+.
Competitive parity with Google Docs, Notion, Figma.

### User Value

Eliminates merge conflicts. Enables pair programming workflows.
Reduces "wait for sync" friction.

### Technical Value

CRDT foundation enables offline-first architecture.
Event sourcing enables audit trails.

---

## 4. Success Criteria

| Criterion | Measurement | Target |
|-----------|-------------|--------|
| Latency | Time to see peer changes | < 100ms |
| Conflicts | User-facing merge dialogs | 0 |
| Adoption | Teams using collab features | 50% in 90 days |

---

## 5. Scope Boundaries

### In Scope

- Real-time text synchronization (CRDT)
- Cursor presence indicators
- User awareness (who's viewing what)

### Out of Scope

- Video/audio collaboration
- Comments and annotations (separate feature)
- Version history UI

### Deferred

- Offline mode with sync-on-reconnect
- Granular permissions per section

---

## 6. Risks and Assumptions

### Assumptions

- Users have stable internet connections
- Backend can handle 10+ concurrent editors per document

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| CRDT complexity | Medium | High | Use proven library (Yjs) |
| Server costs | Medium | Medium | Implement connection pooling |
```

---

## Phase 2: Feature Requirement Document (FRD)

### Purpose

The FRD answers: **"What must the feature do?"**

It captures:
- Functional requirements (features, behaviors)
- Non-functional requirements (performance, security, etc.)
- Constraints and dependencies
- **Explicit backlinks to SOI**

### Requirement ID Convention

```
[REQ-CATEGORY-NNN]

Categories:
  FUNC  - Functional requirement
  PERF  - Performance requirement
  SEC   - Security requirement
  USAB  - Usability requirement
  COMPAT - Compatibility requirement
  DATA  - Data requirement
  INTEG - Integration requirement
```

### Template

```markdown
# Feature Requirement Document: [Feature Name]

**Document ID:** FRD-[YYYYMMDD]-[feature-slug]
**SOI Reference:** [SOI-YYYYMMDD-feature-slug]
**Author:** [Name]
**Created:** [Date]
**Status:** Draft | Review | Approved | Implemented

---

## 1. Overview

**SOI Backlink:** This FRD implements the intent described in [SOI-YYYYMMDD-feature-slug].

[Brief summary of what this FRD covers]

---

## 2. Functional Requirements

### [REQ-FUNC-001] [Requirement Name]

**Priority:** Must Have | Should Have | Nice to Have
**SOI Trace:** Addresses [SOI Section X.Y]

**Description:**
[Clear, testable statement of what the system must do]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Notes:**
[Any clarifications or edge cases]

---

### [REQ-FUNC-002] [Requirement Name]

...

---

## 3. Non-Functional Requirements

### 3.1 Performance

#### [REQ-PERF-001] [Requirement Name]

**Priority:** Must Have
**SOI Trace:** Addresses Success Criterion "Latency < 100ms"

**Specification:**
| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| [Metric] | [Ideal] | [OK] | [Fail] |

---

### 3.2 Security

#### [REQ-SEC-001] [Requirement Name]

**Priority:** Must Have
**SOI Trace:** Addresses Stakeholder "Security Team"

**Specification:**
[Security requirement details]

---

### 3.3 Usability

#### [REQ-USAB-001] [Requirement Name]

...

---

## 4. Constraints

### Technical Constraints

- [Constraint from existing architecture]
- [Technology limitations]

### Business Constraints

- [Timeline requirements]
- [Budget limitations]

### Regulatory Constraints

- [Compliance requirements]

---

## 5. Dependencies

| Dependency | Type | Status | Impact if Unavailable |
|------------|------|--------|----------------------|
| [What we depend on] | Internal/External | Available/Pending | [Impact] |

---

## 6. Glossary

| Term | Definition |
|------|------------|
| [Term] | [Definition as used in this document] |

---

## 7. Requirement Traceability Matrix

| Requirement ID | SOI Section | FRP Solution | Test Case |
|----------------|-------------|--------------|-----------|
| REQ-FUNC-001 | 3.1 Value | Solution A | TC-001 |
| REQ-FUNC-002 | 4 Success | Solution B | TC-002 |
```

### FRD Example

```markdown
# Feature Requirement Document: Real-Time Collaboration

**Document ID:** FRD-20260117-realtime-collab
**SOI Reference:** SOI-20260117-realtime-collab
**Author:** Prime
**Created:** 2026-01-17
**Status:** Draft

---

## 1. Overview

**SOI Backlink:** This FRD implements the intent described in SOI-20260117-realtime-collab,
enabling multiple users to edit TMNL documents simultaneously.

---

## 2. Functional Requirements

### [REQ-FUNC-001] Document Synchronization

**Priority:** Must Have
**SOI Trace:** Addresses SOI Section 1 (Problem Statement - "changes sync on save")

**Description:**
When User A makes an edit, User B must see that edit reflected in their view
without requiring a page refresh or manual sync action.

**Acceptance Criteria:**
- [ ] Edits appear on peer devices within 200ms (target: 100ms)
- [ ] Character-level granularity (not block-level)
- [ ] Supports concurrent edits to same paragraph
- [ ] No data loss during rapid concurrent typing

**Notes:**
CRDT (Conflict-free Replicated Data Type) approach recommended.
See Yjs or Automerge.

---

### [REQ-FUNC-002] Cursor Presence

**Priority:** Must Have
**SOI Trace:** Addresses SOI Section 3.2 (User Value - "friction removed")

**Description:**
Users must see where other collaborators' cursors are positioned,
with visual differentiation per user.

**Acceptance Criteria:**
- [ ] Cursor position updates within 50ms
- [ ] Each user has a distinct cursor color
- [ ] Cursor shows user name on hover
- [ ] Stale cursors (> 5s no movement) fade to 50% opacity

---

### [REQ-FUNC-003] User Awareness Panel

**Priority:** Should Have
**SOI Trace:** Addresses SOI Section 3.2 (User Value)

**Description:**
A panel showing who is currently viewing the document.

**Acceptance Criteria:**
- [ ] Shows avatar/name of each active user
- [ ] Indicates user status (viewing, editing, idle)
- [ ] Updates within 1 second of state change
- [ ] Supports up to 20 concurrent users visually

---

## 3. Non-Functional Requirements

### 3.1 Performance

#### [REQ-PERF-001] Sync Latency

**Priority:** Must Have
**SOI Trace:** Addresses Success Criterion "Latency < 100ms"

**Specification:**
| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Edit-to-render | 100ms | 200ms | > 500ms |
| Cursor update | 50ms | 100ms | > 200ms |
| Presence update | 500ms | 1000ms | > 2000ms |

---

#### [REQ-PERF-002] Concurrent Users

**Priority:** Must Have
**SOI Trace:** Addresses Assumption "10+ concurrent editors"

**Specification:**
| Metric | Target | Acceptable | Unacceptable |
|--------|--------|------------|--------------|
| Max concurrent | 50 users | 20 users | < 10 users |
| Memory per user | 50KB | 100KB | > 500KB |

---

### 3.2 Security

#### [REQ-SEC-001] Connection Authentication

**Priority:** Must Have
**SOI Trace:** Addresses Stakeholder "Security Team"

**Specification:**
- All WebSocket connections must be authenticated via JWT
- Tokens must expire within 1 hour
- Document access must respect existing permission model

---

## 4. Constraints

### Technical Constraints

- Must work with existing TipTap editor integration
- Must not require database schema migration for MVP
- WebSocket server must be horizontally scalable

### Business Constraints

- MVP must ship within Q1 2026
- Infrastructure cost increase capped at $500/month

---

## 5. Dependencies

| Dependency | Type | Status | Impact if Unavailable |
|------------|------|--------|----------------------|
| TipTap Collab Extension | External | Available | Would need custom sync |
| Y-Sweet Server | External | Evaluating | Fallback to Hocuspocus |
| Auth Service | Internal | Available | Cannot authenticate |

---

## 6. Requirement Traceability Matrix

| Requirement ID | SOI Section | Priority | Test Case |
|----------------|-------------|----------|-----------|
| REQ-FUNC-001 | 1 Problem | Must Have | TC-SYNC-001 |
| REQ-FUNC-002 | 3.2 Value | Must Have | TC-CURSOR-001 |
| REQ-FUNC-003 | 3.2 Value | Should Have | TC-PRESENCE-001 |
| REQ-PERF-001 | 4 Success | Must Have | TC-PERF-001 |
| REQ-SEC-001 | 2 Security | Must Have | TC-SEC-001 |
```

---

## Phase 3: Feature Realization Proposal (FRP)

### Purpose

The FRP answers: **"How will we implement the requirements?"**

It captures:
- Proposed technical solutions
- Architecture decisions
- Trade-offs considered
- **Explicit backlinks to FRD requirements**

### Template

```markdown
# Feature Realization Proposal: [Feature Name]

**Document ID:** FRP-[YYYYMMDD]-[feature-slug]
**FRD Reference:** [FRD-YYYYMMDD-feature-slug]
**Author:** [Name]
**Created:** [Date]
**Status:** Draft | Review | Approved | Implemented

---

## 1. Executive Summary

**FRD Backlink:** This FRP proposes solutions for requirements in FRD-[YYYYMMDD]-feature-slug.

[Brief summary of the proposed approach]

---

## 2. Requirements Coverage

| Requirement | FRP Solution | Section |
|-------------|--------------|---------|
| [REQ-FUNC-001] | Solution A | 3.1 |
| [REQ-FUNC-002] | Solution A | 3.1 |
| [REQ-PERF-001] | Solution B | 3.2 |

---

## 3. Proposed Solutions

### 3.1 Solution A: [Name]

**Satisfies:** REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003

#### Overview

[High-level description of the solution]

#### Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Component A   │────▶│   Component B   │
└─────────────────┘     └─────────────────┘
```

#### Key Decisions

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|
| [What] | [Chosen] | [Why] | [Other options] |

#### Implementation Notes

- [Key implementation detail]
- [Integration point]
- [Migration consideration]

---

### 3.2 Solution B: [Name]

**Satisfies:** REQ-PERF-001, REQ-PERF-002

...

---

## 4. Alternatives Considered

### Alternative 1: [Name]

**Why Not Chosen:**
[Reason this was rejected]

### Alternative 2: [Name]

**Why Not Chosen:**
[Reason this was rejected]

---

## 5. Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Technical risk] | Low/Med/High | Low/Med/High | [Mitigation] |

---

## 6. Implementation Plan

### Phase 1: [Name]

**Duration:** [Estimate]
**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Validates:** REQ-FUNC-001

### Phase 2: [Name]

...

---

## 7. Success Metrics

| Metric | Source Requirement | Target | Measurement Method |
|--------|-------------------|--------|-------------------|
| [Metric] | REQ-PERF-001 | [Target] | [How to measure] |

---

## 8. Open Questions

- [ ] [Question needing resolution]
- [ ] [Decision pending stakeholder input]

---

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Author | | | |
| Tech Lead | | | |
| Architect | | | |
```

### FRP Example

```markdown
# Feature Realization Proposal: Real-Time Collaboration

**Document ID:** FRP-20260117-realtime-collab
**FRD Reference:** FRD-20260117-realtime-collab
**Author:** Prime
**Created:** 2026-01-17
**Status:** Draft

---

## 1. Executive Summary

**FRD Backlink:** This FRP proposes solutions for requirements in FRD-20260117-realtime-collab.

We propose a **CRDT-based synchronization** architecture using **Yjs** for
conflict-free data merging, integrated with TipTap's collaboration extension.
The sync server will use **Y-Sweet** for WebSocket transport and
persistence, deployed as a horizontally-scalable service behind our
existing load balancer.

---

## 2. Requirements Coverage

| Requirement | FRP Solution | Section |
|-------------|--------------|---------|
| REQ-FUNC-001 (Doc Sync) | Yjs CRDT + TipTap Collab | 3.1 |
| REQ-FUNC-002 (Cursors) | TipTap CollaborationCursor | 3.1 |
| REQ-FUNC-003 (Awareness) | Yjs Awareness Protocol | 3.2 |
| REQ-PERF-001 (Latency) | WebSocket Direct Connect | 3.3 |
| REQ-PERF-002 (Concurrent) | Y-Sweet Horizontal Scale | 3.3 |
| REQ-SEC-001 (Auth) | JWT Middleware on WS | 3.4 |

---

## 3. Proposed Solutions

### 3.1 Solution: Yjs + TipTap Collaboration

**Satisfies:** REQ-FUNC-001, REQ-FUNC-002

#### Overview

Integrate Yjs CRDT library with TipTap's `@tiptap/extension-collaboration`.
This provides character-level sync with automatic conflict resolution.

#### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   TipTap     │◄──▶│ Yjs Y.Doc    │◄──▶│ WebSocket    │      │
│  │   Editor     │    │ (CRDT State) │    │ Provider     │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ WebSocket
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Y-SWEET SERVER                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   WS Handler │◄──▶│ Room Manager │◄──▶│ Persistence  │      │
│  │   + Auth     │    │ (per-doc)    │    │ (S3/Postgres)│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

#### Key Decisions

| Decision | Choice | Rationale | Alternatives |
|----------|--------|-----------|--------------|
| CRDT Library | Yjs | Most mature, TipTap integration exists | Automerge (heavier) |
| Transport | Y-Sweet | Rust server, built-in persistence | Hocuspocus (Node) |
| Persistence | S3 + Postgres | Durability + queryability | Redis (volatile) |

#### Implementation Notes

- TipTap Collaboration extension handles cursor rendering
- Y.Doc snapshots stored in S3 for large documents
- Postgres stores document metadata and permissions

---

### 3.2 Solution: Awareness Protocol

**Satisfies:** REQ-FUNC-003

#### Overview

Yjs Awareness protocol broadcasts ephemeral user state (cursor position,
selection, status) without persisting to CRDT.

#### Integration

```typescript
// Client-side awareness
const awareness = yjsProvider.awareness

// Update local state
awareness.setLocalState({
  user: {
    name: currentUser.name,
    color: currentUser.color,
    avatar: currentUser.avatar,
  },
  cursor: editor.state.selection.anchor,
  status: 'editing', // 'viewing' | 'editing' | 'idle'
})

// Subscribe to remote states
awareness.on('change', () => {
  const states = Array.from(awareness.getStates().values())
  setActiveUsers(states.filter(s => s.user))
})
```

---

### 3.3 Solution: Performance Optimization

**Satisfies:** REQ-PERF-001, REQ-PERF-002

#### WebSocket Direct Connect

- Bypass HTTP for all sync traffic
- Single persistent connection per client
- Binary encoding (Yjs updates are Uint8Array)

#### Horizontal Scaling

```
                     ┌─────────────┐
                     │   HAProxy   │
                     │  (sticky)   │
                     └──────┬──────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
    ┌──────────┐      ┌──────────┐      ┌──────────┐
    │ Y-Sweet  │      │ Y-Sweet  │      │ Y-Sweet  │
    │ Node 1   │      │ Node 2   │      │ Node 3   │
    └──────────┘      └──────────┘      └──────────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                     ┌─────────────┐
                     │   Redis     │
                     │  (PubSub)   │
                     └─────────────┘
```

- Sticky sessions route same document to same node
- Redis PubSub for cross-node sync when needed
- Target: 50 concurrent users per document

---

### 3.4 Solution: Authentication

**Satisfies:** REQ-SEC-001

#### JWT Middleware

```typescript
// Y-Sweet connection with auth
const provider = new YSweetProvider(
  wsUrl,
  documentId,
  yjsDoc,
  {
    auth: async () => {
      const token = await authService.getToken()
      return { Authorization: `Bearer ${token}` }
    },
  }
)
```

- Token validated on WebSocket upgrade
- Token refresh handled client-side
- Document permissions checked against existing ACL service

---

## 4. Alternatives Considered

### Alternative 1: Operational Transformation (OT)

**Why Not Chosen:**
- More complex to implement correctly
- Requires central server for transformation
- CRDT provides offline support for free

### Alternative 2: ShareDB

**Why Not Chosen:**
- OT-based (see above)
- Less active maintenance than Yjs ecosystem
- No native TipTap integration

### Alternative 3: Liveblocks

**Why Not Chosen:**
- SaaS dependency (vendor lock-in)
- Cost at scale ($400+/month for 50 MAU)
- Cannot self-host for compliance

---

## 5. Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Yjs memory bloat on large docs | Medium | Medium | Implement garbage collection, doc splitting |
| Y-Sweet stability (newer project) | Low | High | Evaluate Hocuspocus as fallback |
| Cross-node sync latency | Low | Medium | Tune Redis PubSub, consider NATS |

---

## 6. Implementation Plan

### Phase 1: Core Sync (2 weeks)

**Deliverables:**
- [ ] Yjs integration with TipTap
- [ ] Y-Sweet server deployment
- [ ] Basic authentication

**Validates:** REQ-FUNC-001

### Phase 2: Presence & Cursors (1 week)

**Deliverables:**
- [ ] Cursor rendering with colors
- [ ] User awareness panel
- [ ] Idle detection

**Validates:** REQ-FUNC-002, REQ-FUNC-003

### Phase 3: Performance & Scale (1 week)

**Deliverables:**
- [ ] Load testing to 50 users
- [ ] Horizontal scaling config
- [ ] Monitoring dashboards

**Validates:** REQ-PERF-001, REQ-PERF-002

---

## 7. Success Metrics

| Metric | Source | Target | Measurement |
|--------|--------|--------|-------------|
| Edit latency | REQ-PERF-001 | < 100ms | Client-side timing |
| Max concurrent | REQ-PERF-002 | 50 users | Load test |
| Conflicts | REQ-FUNC-001 | 0 | Error logging |

---

## 8. Open Questions

- [ ] Should we support offline mode in MVP?
- [ ] How do we handle document recovery if Y-Sweet crashes mid-sync?
- [ ] Do we need audit logging for compliance?
```

---

## Workflow: Using FDD

### Step 1: Start with SOI

```bash
# Create SOI file
touch assets/documents/fdd/SOI-20260117-feature-name.md
```

**Ask yourself:**
- Why does this feature need to exist?
- Who benefits?
- How will we know it's successful?

### Step 2: Derive FRD from SOI

```bash
# Create FRD file
touch assets/documents/fdd/FRD-20260117-feature-name.md
```

**For each SOI section, ask:**
- What specific capability satisfies this intent?
- What constraints does this create?
- How do we test this requirement?

**Ensure every requirement backlinks to SOI.**

### Step 3: Propose Solutions in FRP

```bash
# Create FRP file
touch assets/documents/fdd/FRP-20260117-feature-name.md
```

**For each FRD requirement, ask:**
- How do we implement this?
- What alternatives exist?
- What are the trade-offs?

**Ensure every solution backlinks to requirements.**

### Step 4: Maintain Traceability

Use the **Requirement Traceability Matrix** in FRD:

```markdown
| Requirement ID | SOI Section | FRP Solution | Test Case | Status |
|----------------|-------------|--------------|-----------|--------|
| REQ-FUNC-001 | 1 Problem | Yjs CRDT | TC-SYNC-001 | Implemented |
```

Update status as implementation progresses:
- Defined → In Progress → Implemented → Verified

---

## Anti-Patterns

### ❌ SOI Without Success Criteria

```markdown
# BAD - No way to know if we succeeded
## Success Criteria
We'll ship the feature and see if people like it.
```

```markdown
# GOOD - Measurable outcomes
## Success Criteria
| Criterion | Measurement | Target |
|-----------|-------------|--------|
| User adoption | % teams using feature | 50% in 90 days |
| Performance | p95 latency | < 200ms |
```

### ❌ FRD Without Backlinks

```markdown
# BAD - No trace to SOI
### [REQ-FUNC-001] Document Sync
The system shall sync documents.
```

```markdown
# GOOD - Explicit trace
### [REQ-FUNC-001] Document Sync
**SOI Trace:** Addresses SOI Section 1 (Problem: "changes sync on save")
```

### ❌ FRP Without Alternatives

```markdown
# BAD - No evidence of evaluation
## Solution: Use Yjs
We'll use Yjs because it's good.
```

```markdown
# GOOD - Documented decision process
## Alternatives Considered
### Automerge
**Why Not Chosen:** Heavier runtime, less TipTap integration
### ShareDB
**Why Not Chosen:** OT-based, requires central server
```

### ❌ Implementation Drift

When code diverges from FRP without updating documents:

```markdown
# BAD - Code does something different
FRP says: "Use Y-Sweet for persistence"
Code uses: "Custom Redis-based sync"
No document update explaining why.
```

```markdown
# GOOD - Document evolution
FRP Addendum (2026-02-01):
Changed from Y-Sweet to custom Redis sync due to
Y-Sweet lacking granular permission hooks.
See ADR-0042 for decision record.
```

---

## File Organization

```
assets/documents/fdd/
├── SOI-20260117-realtime-collab.md
├── FRD-20260117-realtime-collab.md
├── FRP-20260117-realtime-collab.md
├── SOI-20260115-search-v2.md
├── FRD-20260115-search-v2.md
└── FRP-20260115-search-v2.md
```

**Naming convention:** `[TYPE]-[YYYYMMDD]-[feature-slug].md`

---

## Integration with Other Artifacts

### FDD → BDD

FRD requirements become BDD scenarios:

```gherkin
# From REQ-FUNC-001
Feature: Document Synchronization
  Scenario: Edits sync between users
    Given User A and User B are editing the same document
    When User A types "hello"
    Then User B sees "hello" within 200ms
```

### FDD → ADR

Major FRP decisions become ADRs for long-term reference:

```markdown
# ADR-0042: CRDT Library Selection

## Context
FRP-20260117-realtime-collab required a CRDT library for document sync.

## Decision
Chose Yjs over Automerge and ShareDB.

## Consequences
- TipTap integration is straightforward
- Must manage Yjs garbage collection for large documents
```

### FDD → Beads

Create beads issues for FRP implementation phases:

```bash
bd create --title="Implement Yjs + TipTap integration" \
  --type=task \
  --labels="fdd:FRP-20260117-realtime-collab,phase:1"
```

---

## Summary

| Document | Purpose | Key Question | Backlinks To |
|----------|---------|--------------|--------------|
| **SOI** | Intent | Why? | - |
| **FRD** | Requirements | What? | SOI |
| **FRP** | Solution | How? | FRD |

**Core discipline:** No document exists in isolation. Every decision traces back to intent.
