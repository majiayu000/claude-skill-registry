---
name: requirements-lifecycle
description: Use when defining requirements, tracking traceability, managing requirement changes, or establishing RTM - covers elicitation, analysis, specification across CMMI Levels 2-4
---

# Requirements Lifecycle

## Overview

This skill guides the complete **requirements lifecycle** from elicitation through change management. It covers both CMMI process areas:

- **RD (Requirements Development)** - Creating requirements: elicitation, analysis, specification
- **REQM (Requirements Management)** - Maintaining requirements: traceability, change control, alignment

**Key capabilities**:
- Elicit requirements from stakeholders without gold plating
- Prioritize conflicting requirements (MoSCoW, value/effort)
- Create bidirectional traceability (requirements ↔ design ↔ tests)
- Manage requirements volatility with impact analysis
- Scale practices from Level 2 (user stories) → Level 3 (templates) → Level 4 (metrics)

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` Section 3.1 (Requirements Phase) for complete CMMI policy.

---

## When to Use This Skill

Use this skill when:

- **Requirements changing constantly** - Stakeholder keeps revising, need volatility management
- **Scope creep pressure** - "Just one more thing" additions, need change control
- **Traceability needed** - Level 3 compliance, audit preparation, creating RTM
- **Stakeholder conflicts** - Competing requirements from VPs, need resolution process
- **Documentation overhead concerns** - "How much is enough?" for Level 2 vs. Level 3
- **Creating new features** - Starting requirements gathering for major work
- **Audit preparation** - Need to establish requirements baseline and traceability

**When NOT to use this skill**:
- **Single-page prototypes or spikes** - Throwaway experiments don't need formal requirements
- **Solo developer projects** - Traceability overhead not justified for 1-person teams
- **Bug fixes within existing architecture** - Use issue tracking, not full requirements lifecycle

---

## High-Level Guidance

### RD vs. REQM: Two Process Areas, One Lifecycle

**Requirements Development (RD)** = Creating new requirements
- Elicit needs from stakeholders (interviews, workshops)
- Analyze and prioritize (MoSCoW, value/effort)
- Specify with acceptance criteria (user stories, formal specs)
- Validate with stakeholders

**Requirements Management (REQM)** = Maintaining existing requirements
- Maintain bidirectional traceability (req ↔ design ↔ tests)
- Manage changes (change requests, impact analysis, approval)
- Ensure alignment (work products match requirements)
- Communicate changes to affected parties

**Timeline**: RD happens during requirements phase. REQM is **continuous** throughout the project.

**Common mistake**: Treating them as sequential. They're concurrent - you develop new requirements while managing existing ones.

### Bidirectional Traceability: Free vs. Theater

**The Modern Approach** (Recommended):

Traceability as **workflow byproduct** using platform-native linking:

```
GitHub:
- Commit message: "Implements #123" → auto-links to requirement
- PR description: "Closes #123" → auto-links to requirement
- Test file comment: "Verifies #123" → searchable reference
- Generate RTM on-demand via API query (for audits)

Azure DevOps:
- Commit message: "AB#123" → auto-links to work item
- Built-in traceability views (work item → commits → builds)
- Query for RTM when needed
```

**Key principle**: Traceability should be **free** (part of normal workflow), not a separate manual task.

**Anti-Pattern**: Manual spreadsheet RTM that becomes stale within days.

**Level 2**: Platform linking is sufficient (GitHub Issues ↔ PRs ↔ commits)
**Level 3**: Tool-based queries to generate traceability reports
**Level 4**: Automated coverage metrics (% requirements traced, orphaned tests detected)

See `requirements-traceability.md` for GitHub/Azure DevOps implementation patterns.

### Change Impact Analysis: Template vs. Ad-Hoc

**Baseline agents said**: "Perform impact analysis" (but didn't say HOW).

**This skill provides**: Impact analysis **checklist** and **template**.

**Minimal Impact Analysis** (Level 2):
```
Change Request: Add OAuth login support
Affected Requirements: REQ-AUTH-001, REQ-AUTH-002
Impact:
  - Design: New OAuth module needed
  - Implementation: 3 days effort
  - Testing: 5 new test cases (2 days)
  - Documentation: User guide update (1 day)
  Total Effort: 6 days
  Schedule Impact: Delays Sprint 3 → Sprint 4
Approval: Product Owner (required)
```

**Formal Impact Analysis** (Level 3):
- Uses structured template (see `requirements-change-management.md`)
- Multiple approval authorities (Product Owner + Tech Lead + QA Lead)
- Traceability verification (all downstream artifacts identified)
- Risk assessment (technical, schedule, budget risks)

**Quantitative Impact Analysis** (Level 4):
- Historical data: "Similar changes averaged 8 days ± 2 days"
- Volatility impact: "Adding this increases monthly change rate from 12% → 18%"
- Predictive: "This puts us 1σ above baseline, likely to slip milestone"

See `requirements-change-management.md` for complete templates and workflows.

### Preventing Gold Plating and Scope Creep

**Two enforcement mechanisms**:

**1. MoSCoW Prioritization**

Classify every requirement:
- **Must Have** - Non-negotiable, project fails without it
- **Should Have** - Important but not critical, could defer 1 sprint
- **Could Have** - Nice to have, include if capacity available
- **Won't Have** - Out of scope, explicitly deferred

**Enforcement**: Once sprint capacity is reached (e.g., 30 story points), all new additions must be "Could Have" or "Won't Have". Product Owner can't add "Must Have" mid-sprint without removing existing "Must Have".

**2. Change Request Process**

Level 2: Lightweight - Product Owner approval, informal impact assessment
Level 3: Formal - Change request form, multi-party approval, documented impact
Level 4: Quantitative - Change metrics tracked, volatility thresholds enforced

**Red flag**: >30% requirements changed per sprint → Scope thrashing, need stakeholder stabilization meeting.

See `requirements-analysis.md` for prioritization templates and conflict resolution.

### Level 2 vs. 3 vs. 4: What Changes?

**Biggest misconception**: Level 3 requires 100-page specs and waterfall.

**Reality**:

| Aspect | Level 2 | Level 3 | Level 4 |
|--------|---------|---------|---------|
| **Format** | User stories + acceptance criteria | Organizational template | + Quality metrics |
| **Review** | Optional/informal | Peer review required | + Defect density tracking |
| **Traceability** | Spreadsheet OR platform links | Tool-based, API-generated | + Coverage metrics (>95%) |
| **Changes** | Tracked in issue history | Formal change requests, approval workflow | + Volatility metrics, SPC |
| **Effort** | 3-5% project time | 10-15% project time | 15-20% project time |

**Escalation from L2 → L3**:
- Audit/compliance requirement
- Team size >10 developers
- Regulatory industry (medical, financial, aerospace)
- Requirements volatility causing quality issues

**Escalation from L3 → L4**:
- Need quantitative quality objectives
- Safety-critical system requiring statistical control
- Process improvement requires data-driven decisions

See `level-scaling.md` for complete escalation criteria and de-escalation guidance.

### Quick Start by Scenario

**Which scenario applies to you?**

```
What's your primary need?
├─ Starting a new feature from scratch → Scenario 1
├─ Requirements changing constantly → Scenario 2
├─ Stakeholders in conflict → Scenario 3
├─ Preparing for audit, need RTM → Scenario 4
└─ Unsure how much documentation needed → Scenario 5
```

**Scenario 1: New Feature, Starting from Scratch**

1. Load `requirements-elicitation.md` - Run stakeholder workshop
2. Load `requirements-specification.md` - Document as user stories (L2) or template (L3)
3. Load `requirements-traceability.md` - Set up GitHub/Azure DevOps linking
4. Begin implementation - REQM now kicks in (continuous change management)

**Timeline**: 1-2 days for Level 2, 3-5 days for Level 3

**Scenario 2: Constant Changes, Volatility Management**

1. Load `requirements-change-management.md` - Implement change request process
2. Calculate current volatility rate: (Added + Modified + Deleted) / Total per sprint
3. If >30% → Stakeholder stabilization meeting required
4. Set threshold: Level 2 (<30%), Level 3 (<20%), Level 4 (<10%)
5. Track metrics, escalate if threshold exceeded

**Scenario 3: Stakeholder Conflict, Two VPs Want Different Things**

1. Load `requirements-analysis.md` - Conflict resolution section
2. Document both requirements objectively (no advocacy)
3. Create decision criteria matrix (business value, risk, ROI)
4. Escalate to decision authority (both VPs' common manager)
5. Cross-reference to `governance-and-risk` skill for ADR process

**Do NOT**: Make the business decision yourself, pick sides, or implement both hoping it works out.

**Scenario 4: Audit Preparation, Need RTM**

1. Load `requirements-traceability.md` - GitHub/Azure DevOps RTM patterns
2. If using GitHub: Use Projects with custom fields OR API-generated report
3. If using Azure DevOps: Use built-in traceability views
4. Verify bidirectional coverage: Requirements → Tests AND Tests → Requirements
5. Address orphaned tests (tests not linked to requirements)

**Target**: >90% coverage for Level 3, >95% for Level 4

**Scenario 5: "How much documentation?" Question**

1. Load `level-scaling.md` - Shows exactly what Level 2/3/4 require
2. Level 2 answer: User stories + acceptance criteria (2-4 pages per sprint)
3. Overhead: 3-5% project time
4. Common fear: "We'll spend all our time writing specs" → Reality: 1-2 hours per sprint

---

## Reference Sheets (On-Demand)

### 1. Requirements Elicitation (`requirements-elicitation.md`)

**When to load**: Starting requirements gathering, unclear requirements, stakeholder workshops, new project kickoff

Gather requirements from stakeholders using structured techniques:
- Interview methods (structured, semi-structured, open-ended)
- Workshop facilitation (JAD sessions, design thinking)
- Prototyping for validation (mockups, wireframes, working prototypes)
- Stakeholder analysis (power/interest matrix, RACI for requirements)
- Level 2/3/4 formality scaling (informal → facilitated → metrics-driven)

**Provides**: Interview scripts, workshop agendas, prototyping workflows, stakeholder mapping templates

**Load reference**: See `requirements-elicitation.md` for complete elicitation techniques.

---

### 2. Requirements Analysis (`requirements-analysis.md`)

**When to load**: Conflicting requirements, prioritization needed, scope management, gold plating concerns

Analyze and prioritize requirements, resolve conflicts:
- MoSCoW prioritization (Must/Should/Could/Won't Have with enforcement)
- Value/Effort matrix (ROI-based prioritization)
- Functional vs. non-functional decomposition
- Conflict resolution techniques (facilitated negotiation, escalation criteria)
- Completeness checking (are we missing requirements?)
- Level 2/3/4 depth scaling (simple → formal → quantitative)

**Provides**: MoSCoW templates, conflict analysis templates, completeness checklists, decision matrices

**Load reference**: See `requirements-analysis.md` for prioritization and conflict resolution.

---

### 3. Requirements Specification (`requirements-specification.md`)

**When to load**: Writing requirements, creating user stories, defining acceptance criteria, documentation standards

Document requirements in appropriate formats:
- User story templates (As a... I want... So that...) with acceptance criteria
- Use case format (actor, preconditions, main flow, alternatives)
- System requirements specification (SRS) structure for formal projects
- Traceability identifiers (how to assign REQ-IDs)
- Level 2/3/4 documentation rigor (minimal → standardized → metrics-tracked)

**Provides**: User story templates, use case templates, SRS outline, acceptance criteria checklist

**Load reference**: See `requirements-specification.md` for specification formats and templates.

---

### 4. Requirements Traceability (`requirements-traceability.md`)

**When to load**: Creating RTM, establishing traceability, audit preparation, compliance verification

Implement bidirectional traceability between requirements, design, and tests:
- RTM structure and patterns (spreadsheet vs. tool-based)
- GitHub traceability (issue linking, Projects, API queries)
- Azure DevOps traceability (work item linking, built-in views, OData queries)
- Bidirectional verification (forward and backward tracing)
- Orphaned tests detection (tests not linked to requirements)
- Level 2/3/4 automation (manual → tool-based → automated coverage)

**Provides**: RTM templates, GitHub/Azure DevOps linking patterns, verification queries, automation scripts

**Load reference**: See `requirements-traceability.md` for platform-specific traceability implementation.

---

### 5. Requirements Change Management (`requirements-change-management.md`)

**When to load**: Requirements changing frequently, volatility management, impact analysis, change approval

Manage requirements changes systematically:
- Change request process (lightweight → formal → quantitative)
- Impact analysis methodology (template, checklist, approval workflow)
- Change approval workflows (who approves what at each level)
- Volatility metrics (change rate, thresholds, trend analysis)
- Change communication (notifying affected stakeholders)
- Level 2/3/4 formality (tracked → formal workflow → SPC)

**Provides**: Change request forms, impact analysis templates, approval matrices, volatility tracking dashboards

**Load reference**: See `requirements-change-management.md` for change control processes.

---

### 6. Level 2→3→4 Scaling (`level-scaling.md`)

**When to load**: Choosing CMMI level, scaling practices, understanding requirements, documentation overhead concerns

Understand what changes across maturity levels:
- Level 2 practices (user stories, basic tracking, 3-5% overhead)
- Level 3 practices (templates, peer review, tool-based traceability, 10-15% overhead)
- Level 4 practices (volatility metrics, prediction models, SPC, 15-20% overhead)
- Escalation criteria (when to move from L2 → L3 → L4)
- De-escalation criteria (when level is overkill)
- Team size adaptations (2-person to 30+ person teams)

**Provides**: Level comparison tables, escalation decision trees, overhead estimates, team size guidelines

**Load reference**: See `level-scaling.md` for complete maturity level guidance.

---

## Loading Reference Sheets

**How to access**:
```
"I need detailed guidance on [topic]"
→ Load the appropriate reference sheet from the list above
```

**When you need a reference**:
- Be specific about which aspect you need ("MoSCoW prioritization" → requirements-analysis)
- References are comprehensive (250-400 lines each with templates and examples)
- Each reference is self-contained but cross-references others when practices overlap
- References include Level 2/3/4 scaling for every practice

**Cross-references**: Reference sheets link to:
- Each other (e.g., change management references traceability)
- `platform-integration` skill for tool-specific implementations
- `governance-and-risk` skill for ADR process and decision analysis
- Prescription document for CMMI compliance policy
