---
name: prd-v07-epic-scoping
description: Transform v0.6 specifications into context-window-sized work packages (EPICs) during PRD v0.7 Build Execution. Triggers on requests to create epics, scope work, break down implementation, or when user asks "create epics", "scope work", "break down work", "context window sizing", "what to build first?", "implementation planning", "epic breakdown". Consumes API-, DBT-, FEA-, ARC-. Outputs EPIC- entries with objectives, ID references, dependencies, and context windows. Feeds v0.7 Test Planning.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Epic Scoping

Position in workflow: v0.6 Technical Specification → **v0.7 Epic Scoping** → v0.7 Test Planning

## Consumes

This skill requires prior work from v0.6 Technical Specification:

- **API-\* endpoint contracts** (from v0.6 Technical Specification) — Endpoints define what must be built; API count signals complexity
- **DBT-\* data model specifications** (from v0.6 Technical Specification) — Data entities and relationships inform natural boundaries
- **ARC-\* architecture decisions** (from v0.6 Architecture Design) — System structure, module boundaries, and integration patterns define scoping boundaries
- **FEA-\* feature entries with MVP-SCOPE** (from v0.3 Features Value Planning) — MVP boundary determines EPIC scope; post-MVP features defer to backlog
- **Existing EPIC-\* entries** (if brownfield) — Inherited work packages constrain and sequence new EPICs

This skill assumes v0.6 Technical Specification is complete with API-/DBT- entries providing implementation contracts.

## Produces

This skill creates/updates:

- **EPIC-\* entries** (context-window-sized work packages, status-based) — Scope of work that fits in AI agent working memory with explicit dependencies, pre-load context budget, session state tracking, and acceptance criteria
- **EPIC dependency graph** — Sequencing showing which EPICs must complete before others; identifies infrastructure/foundation EPICs, critical path EPICs, and optional/secondary EPICs
- **Context capsule specification** — Pre-load checklist (SoT files, key IDs, code references) and working room estimate ensuring EPIC doesn't exceed 100k context tokens

All EPIC- entries are **work package specifications**, not confidence-based. They are:
- **Sized for context windows** (3-5 APIs, 2-4 DBT tables, 1-2 UJs, <100k pre-load tokens)
- **Fully traceable** (every EPIC references API-, DBT-, BR-, UJ-, TEST- from upstream)
- **Sequenced explicitly** (dependencies form a DAG; no circular dependencies)
- **Deliverable-focused** (measurable completion with acceptance criteria)

Example EPIC- entry (Auth Infrastructure):
```markdown
EPIC-01: User Authentication
State: Planned
Lifecycle: v0.7 Build Execution
Branch: epic/EPIC-01-auth

## 0. Context Capsule
### Resource Envelope
| Dimension | Target | Notes |
|-----------|--------|-------|
| Pre-load Context | ~40k tokens | Auth SoT + API-001–005 specs + DBT-010/011 schema |
| Working Room | ~160k tokens | Plenty of space for implementation |
| Session Goal | Checkpoint C1 | Database schema complete |

### Dependencies
| Type | Items | Status |
|------|-------|--------|
| Requires | None | First EPIC — foundation |
| External | Supabase project created | Ready |
| Enables | EPIC-02 (reports), EPIC-03 (data sources) | Blocked until auth completes |

### Pre-load Checklist
- [ ] SoT/SoT.BUSINESS_RULES.md — IDs: BR-001, BR-002 (auth rules)
- [ ] SoT/SoT.API_CONTRACTS.md — IDs: API-001–005 (auth endpoints)
- [ ] SoT/SoT.TECHNICAL_DECISIONS.md — IDs: TECH-003 (Clerk), ARC-003 (JWT strategy)

## 2. Objective & Scope
Goal: Enable users to authenticate with email/password, manage sessions, and maintain security.

Deliverables:
  - [ ] User registration with email/password (API-001)
  - [ ] Login/logout functionality (API-002, API-003)
  - [ ] Session management with refresh tokens (API-004)
  - [ ] Password reset flow (API-005)
  - [ ] Users and sessions schema (DBT-010, DBT-011)

Out of Scope: Social auth (EPIC-02), team invites (EPIC-05), admin user management (EPIC-07)

## 3. Context & IDs
| Type | IDs |
|------|-----|
| Business Rules | BR-001 (email uniqueness), BR-002 (password requirements), BR-010 (auth workflow) |
| User Journeys | UJ-000 (onboarding), UJ-010 (login) |
| APIs | API-001 to API-005 |
| Data Models | DBT-010 (users), DBT-011 (sessions) |
| Architecture | ARC-003 (JWT strategy), TECH-003 (Clerk) |
| Features | FEA-010 (signup), FEA-011 (login) — both in MVP-SCOPE |
| Tests | TEST-001 to TEST-015 (auth test suite) |

## 4. Execution Plan (5 Phases)
[Phase structure from skill as is]

Related IDs: TECH-003, ARC-003, FEA-010/011, API-001–005, DBT-010/011, BR-001/002/010
```

## Core Concept: Epic = Context Window

> An EPIC is not a "big user story." It is a **cognitive boundary**—a scope of work that fits in working memory (human or AI). The goal is to load exactly what's needed to complete a focused task without distraction.

**The question is not** "How long will this take?" but **"Can an agent complete this without needing more context than fits in a session?"**

## Sizing Rules

| Size | Characteristics | Action |
|------|-----------------|--------|
| **Right-sized** | 3-5 API endpoints, 2-4 DBT tables, 1-2 UJ flows | Good fit ✓ |
| **Too big** | >10 APIs, >5 tables, multiple unrelated features | Split by domain |
| **Too small** | Single endpoint, no meaningful deliverable | Merge with related |

**Rule of thumb**: If you can't describe the EPIC's goal in one sentence, it's too big.

## Context Budget Guidelines

EPICs are **context capsules** — work units sized for AI agent handoffs.

| Dimension | Target | Rationale |
|-----------|--------|-----------|
| **Pre-load context** | <100k tokens | SoT files + EPIC + code references |
| **Working room** | >100k tokens | Space for tool outputs, debugging, iteration |
| **Session goal** | 1 checkpoint | Clear "done" state per session |

**Context Monitoring**: Don't estimate upfront — monitor during work. If context exceeds 100k tokens mid-session, pause and checkpoint immediately.

**Splitting Signal**: If you need to load >5 SoT files or >10 code files to understand the EPIC, it's probably too big.

**Simplicity Signal**: Resist creating more EPICs "just in case." Each EPIC adds coordination overhead (context capsule, session state, branch management, dependency tracking). If the MVP has 12 APIs and 6 tables, 3-5 EPICs is almost always sufficient. The overhead of an unnecessary EPIC is higher than a slightly larger EPIC that stays within context budget.

## Branch Convention

Each EPIC gets its own branch. This creates:
- Clear ownership (one EPIC = one branch = one PR)
- Easy rollback (delete branch, EPIC never happened)
- Natural checkpoint = commit

**Naming**: `epic/EPIC-{NUMBER}-{slug}`

Examples:
- `epic/EPIC-01-auth-endpoints`
- `epic/EPIC-02-user-dashboard`
- `epic/EPIC-03-payment-integration`

**Workflow**:
1. EPIC created → `git checkout -b epic/EPIC-{NUMBER}-{slug}`
2. Work happens → Commits reference IDs in messages
3. Checkpoints → Commit with state saved in EPIC Section 1
4. EPIC complete → PR opened
5. PR merged → Branch deleted, EPIC marked Complete

## Scoping Process

1. **Inventory implementation items** from API-, DBT-, FEA-, ARC-
   - What must be built?

2. **Identify natural boundaries**
   - Feature clusters (features that work together)
   - Data domains (tables that belong together)
   - Architectural seams (module boundaries from ARC-)
   - **Surface ambiguous assignments**: When an API/DBT could logically belong to either EPIC, state the ambiguity explicitly: "API-012 could belong to EPIC-02 or EPIC-03 because it serves both UJ-005 and UJ-008." Record the reasoning for the final placement in the EPIC's Context & IDs section. Do not silently assign items to whichever EPIC you encounter first.

3. **Size each potential EPIC** against context window capacity
   - Can an agent hold all relevant IDs in one session?

4. **Sequence EPICs by dependencies**
   - What must be built first?
   - What enables other EPICs?

5. **Create EPIC- entries** with full ID references

6. **Validate**: Can an agent complete this EPIC without needing more context than fits in a session?

## Sequencing Framework

| Order | Priority | Rationale | Examples |
|-------|----------|-----------|----------|
| 1 | Infrastructure EPICs | Everything depends on these | Auth, DB setup, project scaffold |
| 2 | Core data model EPICs | Foundation for features | User, Workspace, base entities |
| 3 | Critical path EPICs | Journeys that drive KPIs | UJ- that affects KPI-001 |
| 4 | Supporting feature EPICs | Secondary features | Settings, admin, nice-to-haves |

## EPIC- Output Template

```
EPIC-XXX: [Epic Name]
State: [Planned | In Progress | Testing | Complete]
Lifecycle: v0.7 Build Execution
Branch: epic/EPIC-XXX-[slug]

## 0. Context Capsule
### Resource Envelope
| Dimension | Target | Notes |
|-----------|--------|-------|
| Pre-load Context | ~[N]k tokens | SoT files + EPIC + code |
| Working Room | ~[200-N]k tokens | Space for work |
| Session Goal | [Checkpoint target] | What "done" looks like |

### Dependencies
| Type | Items | Status |
|------|-------|--------|
| Requires | EPIC-YYY | Complete/Pending |
| External | [Setup needed] | Ready/Blocked |
| Enables | EPIC-ZZZ | Blocked until this completes |

### Pre-load Checklist
- [ ] SoT/SoT.[X].md — IDs: [key IDs]
- [ ] SoT/SoT.[Y].md — IDs: [key IDs]

## 1. Session State (The "Brain Dump")
### Current State
- **Last Action**: [What was just completed — reference IDs]
- **Stopping Point**: [File/line or test failure]
- **Next Steps**: [Exact instructions for next session]
- **Blockers**: [Any blockers — or "None"]
- **Decisions Made**: [Key decisions with rationale]

### Resume Instructions
[Exactly what the next session should do — or "N/A - EPIC Complete"]

## 2. Objective & Scope
Goal: [One sentence describing what this EPIC achieves]

Deliverables:
  - [ ] [Specific deliverable A]
  - [ ] [Specific deliverable B]
  - [ ] [Specific deliverable C]

Out of Scope: [What we are NOT doing in this EPIC]

## 3. Context & IDs
| Type | IDs |
|------|-----|
| Business Rules | BR-XXX, BR-YYY |
| User Journeys | UJ-XXX, UJ-YYY |
| APIs | API-XXX to API-ZZZ |
| Data Models | DBT-XXX, DBT-YYY |
| Architecture | ARC-XXX |
| Features | FEA-XXX, FEA-YYY |
| Tests | TEST-XXX to TEST-ZZZ |

## 4. Execution Plan (The 5 Phases)

### Phase A: Plan
- [ ] Context loaded
- [ ] Dependencies verified
- [ ] Strategy defined
- [ ] Branch created

**Checkpoint A**: Planning complete, branch exists.

### Phase B: Design
- [ ] Specs updated
- [ ] Architecture documented
- [ ] TEST- entries created

**Checkpoint B**: Specs drafted, tests defined.

### Phase C: Build (Context Windows)
Window 1: [Focus Area]
  - [ ] Task A
  - [ ] Task B
  - [ ] Verification: [How to confirm complete]

**Checkpoint C1**: [What exists when done]

Window 2: [Focus Area]
  - [ ] Task C
  - [ ] Task D

**Checkpoint C2**: [What exists when done]

### Phase D: Validate
- [ ] All TEST- entries pass
- [ ] Manual verification of UJ-
- [ ] Code has @implements tags
- [ ] SoT matches implementation

**Checkpoint D**: Tests green, verification complete.

### Phase E: Finish
- [ ] Temp cleanup
- [ ] SoT finalized
- [ ] Learning capture
- [ ] Resume Instructions = "N/A - EPIC Complete"
- [ ] PR ready

**Checkpoint E**: EPIC complete.

## 5. Acceptance Criteria
- [ ] All deliverables done
- [ ] All TEST- entries pass
- [ ] Resume Instructions = "N/A - EPIC Complete"
- [ ] No orphan ID references
- [ ] Branch merged or PR approved
```

**Example EPIC- entry:**
```
EPIC-01: User Authentication
State: Planned
Lifecycle: v0.7 Build Execution
Branch: epic/EPIC-01-auth

## 0. Context Capsule
### Resource Envelope
| Dimension | Target | Notes |
|-----------|--------|-------|
| Pre-load Context | ~40k tokens | Auth SoT + API specs + schema |
| Working Room | ~160k tokens | Plenty of space |
| Session Goal | Checkpoint C1 | Database schema complete |

### Dependencies
| Type | Items | Status |
|------|-------|--------|
| Requires | None | First EPIC |
| External | Supabase project | Ready |
| Enables | EPIC-02, EPIC-03 | Blocked until this completes |

### Pre-load Checklist
- [ ] SoT/SoT.BUSINESS_RULES.md — IDs: BR-001, BR-002
- [ ] SoT/SoT.API_CONTRACTS.md — IDs: API-001 to API-005
- [ ] SoT/SoT.TECHNICAL_DECISIONS.md — IDs: TECH-003, ARC-003

## 1. Session State (The "Brain Dump")
### Current State
- **Last Action**: N/A (not started)
- **Stopping Point**: N/A
- **Next Steps**:
  1. Create branch epic/EPIC-01-auth
  2. Begin with Phase A: Plan
  3. Load context from pre-load checklist
- **Blockers**: None
- **Decisions Made**: Using Supabase Auth per TECH-003

### Resume Instructions
> Start fresh: create branch and load context per pre-load checklist.

## 2. Objective & Scope
Goal: Enable users to sign up, log in, and manage their sessions.

Deliverables:
  - [ ] User registration with email/password
  - [ ] Login/logout functionality
  - [ ] Session management with refresh tokens
  - [ ] Password reset flow

Out of Scope: Social auth (EPIC-02), team invites (EPIC-05)

## 3. Context & IDs
| Type | IDs |
|------|-----|
| Business Rules | BR-001, BR-002 |
| User Journeys | UJ-000, UJ-010 |
| APIs | API-001 to API-005 |
| Data Models | DBT-010, DBT-011 |
| Architecture | ARC-003, TECH-003 |
| Features | FEA-010, FEA-011 |
| Tests | TEST-001 to TEST-015 |

## 4. Execution Plan

### Phase A: Plan
- [ ] Context loaded
- [ ] Dependencies verified (Supabase ready)
- [ ] Strategy: Database → API → UI
- [ ] Branch created: epic/EPIC-01-auth

**Checkpoint A**: Planning complete, branch exists.

### Phase C: Build
Window 1: Database Schema
  - [ ] Create users table with RLS
  - [ ] Create sessions table
  - [ ] Set up Supabase Auth triggers

**Checkpoint C1**: Schema deployed, migrations tested.

Window 2: API Endpoints
  - [ ] POST /auth/signup (API-001)
  - [ ] POST /auth/login (API-002)
  - [ ] POST /auth/logout (API-003)
  - [ ] POST /auth/refresh (API-004)
  - [ ] POST /auth/reset-password (API-005)

**Checkpoint C2**: All endpoints return correct responses.

Window 3: UI Integration
  - [ ] Signup form (SCR-001)
  - [ ] Login form (SCR-002)
  - [ ] Password reset flow (SCR-003)
  - [ ] Auth state management

**Checkpoint C3**: Full auth flow works E2E.

## 5. Acceptance Criteria
- [ ] All deliverables done
- [ ] TEST-001 to TEST-015 pass
- [ ] Resume Instructions = "N/A - EPIC Complete"
- [ ] UJ-000 and UJ-010 verified manually
- [ ] Branch merged
```

## EPIC Phase Structure

Each EPIC follows 5 phases:

| Phase | Purpose | Activities |
|-------|---------|------------|
| **A: Plan** | Load context | Read EPIC, load referenced IDs, verify Session State |
| **B: Design** | Update SoT | Draft/refine ID entries in SoT/ before coding |
| **C: Build** | Implement | Work through Context Windows, test-first |
| **D: Validate** | Verify | Run tests, manual checks, traceability audit |
| **E: Finish** | Clean up | Update SoT, archive temp/, mark complete |

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Epic explosion** | 20+ EPICs for MVP | Consolidate; most MVPs need 3-7 |
| **One mega-EPIC** | Everything in one EPIC | Split by architectural boundary |
| **No ID references** | EPIC without BR-, API-, DBT- links | Every EPIC must reference SoT/ |
| **Circular dependencies** | EPIC-01 needs EPIC-02 needs EPIC-01 | Identify shared foundation, extract to EPIC-00 |
| **Context overload** | Agent can't hold full EPIC context | Split into smaller Context Windows |
| **Missing sequencing** | No build order defined | Establish explicit dependency chain |
| **Vague objectives** | "Build the backend" | Specific, measurable: "Implement API-001–005" |
| **Silent scope assumptions** | EPIC assigns items without explaining boundary rationale | Every ambiguous assignment must note "API-XXX placed here because [reason]; alternative was EPIC-YYY" |

## Quality Gates

Before proceeding to Test Planning:

- [ ] All API- and DBT- entries assigned to EPICs
- [ ] No orphaned specifications (everything has an EPIC home)
- [ ] Dependencies form a DAG (no circular dependencies)
- [ ] Each EPIC has clear, measurable deliverables
- [ ] Context Windows defined for each EPIC
- [ ] Sequencing makes sense (foundations first)

## Downstream Connections

EPIC- entries feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **Test Planning** | EPIC scope defines test boundaries | TEST- entries for EPIC-01 scope |
| **Implementation Loop** | EPIC is execution unit | Work happens inside EPIC context |
| **Session Management** | Session State section tracks progress | Resume from where we left off |
| **Progress Tracking** | EPIC state shows overall progress | 3/7 EPICs complete |

## Detailed References

- **Epic scoping examples**: See `references/examples.md`
- **EPIC- entry template**: See `assets/epic.md`
- **Dependency mapping guide**: See `references/dependency-mapping.md`
