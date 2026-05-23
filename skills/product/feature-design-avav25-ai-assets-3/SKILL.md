---
name: feature-design
description: Feature design workflow — transform raw feature inputs (ideas, research, stakeholder requests, competitive analysis) into a structured PRD or feature brief. Applies product-manager role. Produces PRD, user stories, acceptance criteria, success metrics, and updates FEATURES.md. First step in the planning chain, precedes /architecture and /feature-plan.
argument-hint: [feature idea or requirement]
---

# Feature Design

Transform raw feature inputs into structured product documentation. This is the **product design phase** — no code, architecture, or engineering decisions are made here. Output feeds into `/architecture` for technical design and `/feature-plan` for implementation planning.

**Apply `Agent(product-manager)` role for all steps below.**

## 1. Receive Feature Inputs

Gather all available resources describing the feature:

- **Accepted inputs**: idea brief, user research, customer feedback, support tickets, competitive analysis, stakeholder request, verbal description, market data, analytics report
- Read every provided document thoroughly
- If the user provides a verbal description only — proceed to Step 2 to structure it through discovery

### Extract Raw Signals

From the provided inputs, extract and organize:

| Signal | Source | Notes |
|---|---|---|
| **Problem** | [what pain exists, for whom] | [evidence or assumption] |
| **Opportunity** | [what business value] | [data points] |
| **User segments** | [who needs this] | [ICP/persona indicators] |
| **Competitive context** | [how others solve it] | [differentiation angle] |
| **Constraints** | [timeline, budget, technical, regulatory] | [hard vs soft] |
| **Existing assets** | [related features, prior art, dependencies] | [links/refs] |

If critical signals are missing (no clear problem statement, no target user) — ask before proceeding. Do not invent user needs.

## 2. Discovery and Framing

### 2a. Problem Validation

Define the problem with precision:

1. **Problem statement**: One paragraph — who has the problem, what the problem is, why it matters now
2. **Evidence**: Data points supporting the problem (usage metrics, support volume, churn correlation, user quotes, competitive pressure)
3. **Impact of inaction**: What happens if we do nothing

If evidence is weak — flag this as a risk. Do not fabricate data.

### 2b. Target Users

Apply JTBD and ICP frameworks from `Agent(product-manager)`:

- **Job-to-be-Done**: When [situation], I want to [motivation], so I can [outcome]
- **ICP segments**: Which customer profiles benefit most. Include triggers, buying signals, objections
- **Personas** (if useful): Name, role, goal, frustration. Keep lightweight — max 2 personas

### 2c. Scope Decision

Based on complexity, decide the deliverable type:

| Complexity | Signals | Deliverable |
|---|---|---|
| **Small** | Single service, < 1 week effort, clear solution | Feature Brief (abbreviated PRD) |
| **Medium** | Multi-component, 1–4 weeks, some unknowns | Full PRD |
| **Large** | Multi-service, 4+ weeks, significant unknowns, new capabilities | Full PRD + Spike/Discovery tasks |
| **AI/Agent** | LLM-powered, autonomous behavior, trust/safety concerns | Full PRD + Agent Contract + Eval Strategy |

Present the scope decision to the user for confirmation before proceeding.

## 3. Requirements Definition

### 3a. Functional Requirements

List requirements prioritized using MoSCoW:

- **Must have**: Core functionality — feature is useless without these
- **Should have**: Important but not blocking launch
- **Could have**: Nice-to-have, defer if constrained
- **Won't have (this iteration)**: Explicitly excluded — prevents scope creep

Each requirement: one sentence, testable, outcome-focused. Never specify implementation — describe *what*, not *how*.

### 3b. Non-Functional Requirements

Identify relevant NFRs:

| Category | Requirement | Target |
|---|---|---|
| Performance | [e.g., response time] | [e.g., < 200ms p95] |
| Security | [e.g., auth, data protection] | [e.g., RBAC, PII encrypted] |
| Scalability | [e.g., concurrent users] | [e.g., 10K concurrent] |
| Accessibility | [e.g., WCAG level] | [e.g., WCAG 2.2 AA] |
| Compliance | [e.g., GDPR, SOC2] | [specific requirements] |

Only include categories relevant to this feature.

### 3c. Acceptance Criteria

Write acceptance criteria for every Must-have and Should-have requirement:

- Use **Given/When/Then** format for behavioral criteria
- Include **happy path**, **edge cases**, **error states**
- Include **operational criteria**: "no new errors in logs", "latency < Xms p95"
- Include **security criteria**: "unauthorized users receive 403", "PII not logged"
- Each criterion is independently testable

## 4. Success Metrics

Define how to measure feature success:

### 4a. Metric Framework

| Metric Type | Metric | Target | Measurement Method |
|---|---|---|---|
| **Primary** (North Star) | [e.g., activation rate] | [target value] | [how to measure] |
| **Leading** | [e.g., feature adoption D7] | [target value] | [how to measure] |
| **Guardrail** | [e.g., error rate, latency] | [must not exceed] | [how to measure] |

### 4b. Instrumentation Plan

- Events to track (name, properties, trigger)
- Dashboards to create or update
- Alerts to configure (guardrail breaches)

## 5. Risk Assessment

| Risk | Type | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| [description] | Technical / Business / Security / Compliance | High/Med/Low | High/Med/Low | [strategy] |

**Mandatory risk categories to evaluate:**
- Security threats (apply OWASP Top 10; add LLM Top 10 for AI features)
- Data handling risks (PII, secrets, retention)
- Backward compatibility and migration
- Dependency on external systems or teams
- User abuse scenarios

## 6. AI/Agent Addendum

**Include this section only for AI-powered or agent features.** Skip for standard features.

<agent_contract>
- **Autonomy level**: Assist (human decides) → Semi-auto (agent proposes, human approves) → Auto (agent acts independently)
- **Allowed tools and permissions**: Least privilege. List every tool/API the agent can access
- **Confirmation gates**: Which actions require human approval
- **Failure modes**: What happens when the agent fails, hallucinates, or exceeds scope
- **Cost budget**: Token/compute/API limits per operation
- **Context pipeline**: Consult `context-engineering` skill for context stack design, RAG pipeline, memory architecture, agent harness patterns, and production checklists
- **Eval strategy**: Offline eval set (fixtures, synthetic + real cases), online monitoring (drift, failure rates)
</agent_contract>

## 7. Compile Deliverable

### Full PRD

Compile all sections into a structured PRD:

```markdown
# PRD: [Feature Name]

## Problem Statement
[From Step 2a]

## Target Users
[From Step 2b — JTBD, ICP, personas]

## Scope and Non-Goals
[From Step 2c — what's in, what's explicitly out]

## Requirements
[From Step 3a — MoSCoW prioritized]

## Non-Functional Requirements
[From Step 3b]

## Acceptance Criteria
[From Step 3c]

## Success Metrics
[From Step 4]

## Risks and Mitigations
[From Step 5]

## Agent Contract
[From Step 6 — only for AI features]

## Rollout Strategy
- Phase 1: Internal / dogfood
- Phase 2: Beta (limited users, feature flag)
- Phase 3: GA (all users)
- Backward compatibility notes
- Feature flag name and config
```

### Feature Brief (for small scope)

Abbreviated format — single document:

```markdown
# Feature Brief: [Feature Name]

**Problem**: [1–2 sentences]
**Users**: [target segment]
**JTBD**: When [situation], I want to [motivation], so I can [outcome]

## Requirements
[Must-have list only — max 5 items]

## Acceptance Criteria
[Given/When/Then for each requirement]

## Success Metric
[Single primary metric + target]

## Risks
[Top 1–3 risks with mitigations]
```

Present the compiled deliverable to the user for review. Iterate until approved.

## 8. Update FEATURES.md

After the PRD/brief is approved:

1. If `FEATURES.md` does not exist — create it at the project root
2. Add or update the feature entry:
   - Name, one-line description
   - Status: `planned`
   - Link to PRD/brief in `features/` directory
3. Save the PRD/brief to `features/[feature-name].md` (kebab-case)

## 9. Handoff

Guide the next step based on feature complexity:

| Complexity | Next Step |
|---|---|
| **Small** (brief) | Run `/feature-plan` directly — architecture is implicit |
| **Medium** (PRD) | Run `/architecture` for technical design, then `/feature-plan` |
| **Large** (PRD + spikes) | Execute spikes first, then `/architecture` → `/feature-plan` |
| **AI/Agent** (PRD + contract) | Run `/architecture` with agent contract as input → `/feature-plan` |

## Integration

- **Input**: Raw feature resources (ideas, research, feedback, stakeholder requests)
- **Followed by**: `/architecture` (technical design), `/feature-plan` (work decomposition)
- **Roles**: `Agent(product-manager)` (primary — owns PRD), `Agent(solution-architect)` (consulted for feasibility)
- **Skills**: `context-engineering` skill (context pipeline design, RAG, memory, agent harness — for AI/Agent features, Step 6)
- **Updates**: `FEATURES.md`, `features/` directory
- **Enables**: Full planning chain: `/feature-design` → `/architecture` → `/feature-plan` → `/feature-dev`
