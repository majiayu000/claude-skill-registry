---
name: tech-stack-confirmation
description: "Use after completing the requirement-analysis skill and producing a PRD document. This skill guides the process of confirming the technology stack (development languages, frameworks, databases, testing tools, infrastructure) based on PRD requirements. It should be triggered when a user has a PRD and needs to make technology selection decisions, or when the user asks to 'confirm tech stack', 'select technologies', 'do technology evaluation', or 'create architecture decisions' for a project. It should NOT be used for requirements gathering (use requirement-analysis instead) or for detailed system design/implementation planning."
---

# Tech Stack Confirmation

## Overview

Transform PRD requirements into a confirmed, evidence-based technology stack through structured analysis. This skill bridges the gap between business requirements (PRD) and technical implementation by systematically evaluating technology options against PRD-derived criteria. The process produces Architecture Decision Records (ADRs), trade-off matrices, and a final confirmed tech stack document covering development, testing, and DevOps layers.

## Prerequisites

- A completed PRD document (output of the `requirement-analysis` skill)
- The PRD file path must be known (typically at `docs/requirements/YYYY-MM-DD-<topic>-prd.md`)

## Scope Boundary

This skill covers the **technology selection and confirmation** phase ONLY:
- **In scope**: NFR extraction, technology evaluation, trade-off analysis, ADR writing, POC scoping, tech stack confirmation
- **Out of scope**: Requirements gathering (use `requirement-analysis`), detailed system design, API design, database schema design, implementation planning

If the user attempts to dive into detailed system design during this process, acknowledge the input but redirect focus: "That's a valid design consideration — let's capture it as a note, but first confirm the technology stack."

## The Process

### Phase 1: NFR Extraction — Surface Hidden Technology Drivers

**Goal**: Extract all non-functional requirements from the PRD that drive technology selection, including implicit ones hidden in functional language.

**Method**: Read `references/nfr-mapping-guide.md` for the complete NFR extraction patterns and mapping tables.

**Execution rules**:
1. Read the PRD document thoroughly
2. Scan every section for NFR signals — both explicit (Section 4 "Non-Functional Requirements") and implicit (hidden in functional descriptions)
3. For each discovered NFR, quantify the threshold — if the PRD is vague, ask the user ONE question at a time to clarify
4. Map each NFR to affected technology stack layers (frontend, backend, database, infrastructure, testing)
5. Identify NFR conflicts (e.g., "maximum flexibility" vs. "strict data consistency") and present them to the user for resolution

**Phase 1 output**: An NFR summary table following the format in `references/nfr-mapping-guide.md`.

Present the NFR table to the user for confirmation before proceeding.

### Phase 2: Technology Domain Identification — Define Decision Points

**Goal**: Identify all technology domains that require a selection decision.

**Execution rules**:
1. Based on the PRD functional requirements and extracted NFRs, list all technology domains requiring decisions. Common domains include:
   - **Frontend**: Framework, state management, UI component library, build tooling
   - **Backend**: Language, framework, API style (REST/GraphQL/gRPC)
   - **Database**: Primary data store, caching layer, search engine
   - **Messaging**: Message queue, event streaming
   - **Infrastructure**: Container orchestration, CI/CD, cloud provider, IaC
   - **Testing**: Unit test framework, E2E framework, API testing, performance testing
   - **Observability**: Logging, monitoring, APM, alerting
2. For each domain, note which NFRs and PRD requirements constrain the choice
3. Classify each domain decision as:
   - **Constrained**: Only one viable option due to hard requirements or existing infrastructure
   - **Open**: Multiple viable options requiring evaluation
   - **Deferred**: Can be decided later without blocking other decisions

**Phase 2 output**: A technology domain list with classification and constraints.

Present to the user for confirmation — some domains may be pre-decided by organizational constraints (e.g., "we already use AWS" or "team only knows TypeScript").

### Phase 3: Trade-off Analysis — Quantify Decisions

**Goal**: For each "Open" domain, perform structured trade-off analysis.

**Method**: Read `references/tradeoff-matrix-template.md` for the matrix template.

**Execution rules**:
1. For each open domain, create a trade-off matrix
2. Derive evaluation criteria directly from PRD requirements and extracted NFRs — every criterion must trace back to a source
3. Assign weights collaboratively with the user — present a proposed weighting and ask for confirmation
4. Identify 2-4 candidate technologies per domain (research current ecosystem if needed)
5. **Version verification via Context7**: For each candidate technology, use Context7 MCP tools to verify the latest stable version and maintenance status. Read `references/context7-version-verification.md` for the detailed verification workflow. Record verified versions alongside each candidate in the trade-off matrix. A technology that is EOL, unmaintained, or has known critical CVEs in its latest version should be scored lower or eliminated
6. Score each candidate against criteria with explicit justification
7. Calculate weighted totals and present the result
8. Write each matrix to: `docs/architecture/tradeoff/YYYY-MM-DD-<domain>-tradeoff-matrix.md`

**Interaction model**:
- Present ONE domain at a time — do not overwhelm with all matrices simultaneously
- For each domain, present the proposed candidates and criteria first, then the scoring
- Allow the user to challenge scores and adjust weights

**Phase 3 output**: Completed trade-off matrices for all open domains.

### Phase 4: Risk Assessment — Identify POC Needs

**Goal**: Evaluate technology risks and determine if any decisions require proof-of-concept validation before commitment.

**Execution rules**:
1. For each technology decision (both constrained and selected-via-matrix), assess risk across three dimensions:

| Risk Dimension | Assessment Question |
|---------------|-------------------|
| Technical feasibility | Has the team used this technology at this scale before? |
| Integration risk | Does this technology need to integrate with unfamiliar systems? |
| Performance uncertainty | Are the performance requirements beyond typical usage patterns? |

2. Classify each decision's risk level:
   - **Low risk**: Team has experience, well-proven at required scale → proceed directly
   - **Medium risk**: Some unknowns but manageable → document mitigation strategy
   - **High risk**: Significant unknowns, critical to project success → recommend POC

3. For each high-risk item, define a POC scope:
   - **Objective**: What specific question must the POC answer?
   - **Success criteria**: What measurable result confirms feasibility?
   - **Scope**: Minimal implementation needed to answer the question
   - **PRD reference**: Which requirement(s) this validates

**Phase 4 output**: Risk assessment table with POC recommendations (if any).

Present to the user. If POCs are recommended, confirm whether to proceed with POC execution or accept the risk.

### Phase 5: ADR Documentation — Record Decisions

**Goal**: Document each significant technology decision as a formal Architecture Decision Record.

**Method**: Read `references/adr-template.md` for the ADR template.

**Execution rules**:
1. Create one ADR per technology domain decision
2. Number ADRs sequentially: ADR-001, ADR-002, etc.
3. Each ADR must include:
   - Clear link to PRD requirements driving the decision
   - All considered options (from trade-off matrix if applicable)
   - Explicit rationale for the chosen option
   - Acknowledged negative consequences and mitigations
4. Write each ADR to: `docs/architecture/adr/YYYY-MM-DD-ADR-NNN-<title>.md`
5. For constrained decisions (pre-decided), still create an ADR — record WHY it was constrained

**Phase 5 output**: Complete set of ADR documents.

### Phase 6: Confirmed Tech Stack — Final Assembly

**Goal**: Produce the final confirmed tech stack document aggregating all decisions.

**Execution rules**:
1. Create the confirmed tech stack document at: `docs/architecture/YYYY-MM-DD-<topic>-tech-stack.md`
2. **Final version verification via Context7**: Before assembling the document, re-verify ALL selected technologies using Context7 MCP tools (read `references/context7-version-verification.md`). This ensures versions have not changed since Phase 3 evaluation. Pin exact versions — never use version ranges
3. Organize by layer:

```markdown
# Confirmed Tech Stack: [Project Name]

## Document Info
| Field | Value |
|-------|-------|
| PRD Reference | [path to PRD] |
| Created | YYYY-MM-DD |
| Status | Confirmed / Pending POC |
| Versions Verified | YYYY-MM-DD (via Context7) |

## Development Stack

### Frontend
| Component | Technology | Version | ADR Reference | Rationale Summary |
|-----------|-----------|---------|---------------|-------------------|
| [Component] | [Technology] | [Pinned version] | ADR-NNN | [One-line rationale] |

### Backend
| Component | Technology | Version | ADR Reference | Rationale Summary |
|-----------|-----------|---------|---------------|-------------------|
| [Component] | [Technology] | [Pinned version] | ADR-NNN | [One-line rationale] |

### Database
| Component | Technology | Version | ADR Reference | Rationale Summary |
|-----------|-----------|---------|---------------|-------------------|
| [Component] | [Technology] | [Pinned version] | ADR-NNN | [One-line rationale] |

## Testing Stack
| Component | Technology | Version | ADR Reference | Rationale Summary |
|-----------|-----------|---------|---------------|-------------------|
| [Component] | [Technology] | [Pinned version] | ADR-NNN | [One-line rationale] |

## DevOps / Infrastructure Stack
| Component | Technology | Version | ADR Reference | Rationale Summary |
|-----------|-----------|---------|---------------|-------------------|
| [Component] | [Technology] | [Pinned version] | ADR-NNN | [One-line rationale] |

## Dependency Version Verification
| Component | Technology | Verified Version | Latest Stable | Status | Context7 Verified |
|-----------|-----------|-----------------|---------------|--------|-------------------|
| [Component] | [Technology] | [Version in stack] | [Latest from Context7] | Active / Maintenance / EOL | Yes / Unavailable |

### Compatibility Matrix
| Dependency A | Version | Dependency B | Required Version | Compatible |
|-------------|---------|-------------|-----------------|------------|
| [e.g., Spring Boot] | [3.4.x] | [Java] | [17+] | Yes |

## Pending Items
- [ ] [POC items still requiring validation]
- [ ] [Open questions requiring stakeholder input]

## Cross-Reference
| PRD Requirement | NFR | Technology Decision | ADR |
|----------------|-----|-------------------|-----|
| [PRD-F-xxx] | [NFR-xxx] | [Technology] | [ADR-NNN] |
```

4. **Cross-check**: Verify every PRD non-functional requirement is addressed by at least one technology decision
5. If gaps exist, present them to the user and loop back to Phase 3

**Phase 6 output**: Final confirmed tech stack document with pinned, verified versions.

### Phase 7: Summary Report

After all documents are complete, present a summary:

1. **NFRs extracted** — count and key highlights
2. **Technology domains evaluated** — count by classification (constrained/open/deferred)
3. **Trade-off matrices** — count and file paths
4. **ADRs written** — count and file paths
5. **POC items** — count and status
6. **Final tech stack** — file path
7. **Coverage status** — confirm PRD NFR ↔ Tech Stack alignment is complete
8. **Open questions** — any unresolved items

## Key Principles

- **One domain at a time** — never present multiple trade-off analyses simultaneously
- **Evidence over preference** — every decision must trace to a PRD requirement or NFR
- **Quantify over qualify** — use scoring matrices, not gut feelings
- **Record rationale** — the "why" matters more than the "what" for future maintainers
- **Acknowledge trade-offs** — no technology is perfect; document accepted downsides
- **Incremental validation** — present each phase output to the user before proceeding
- **No silent assumptions** — if a technology constraint is unclear, ask; never assume defaults
- **Scope discipline** — redirect detailed system design discussions back to technology selection
- **Version currency** — always verify latest stable versions via Context7 before confirming any technology; pin exact versions in the final tech stack document to prevent dependency drift
