---
context: fork
---

# /scenario

Create a Scenario note for what-if analysis, future-state planning, alternative architecture options, or risk mitigation strategies.

## Usage

```
/scenario <name>
/scenario "SAP Cloud Migration"
/scenario "Real-time Analytics" --type future-state
/scenario "Vendor Alternative: Google vs AWS" --type alternative-option
```

## Instructions

### Phase 1: Parse Input & Type

1. Extract scenario name
2. Ask for scenario type:
   ```
   Scenario Type:
   - current-state (baseline for comparison)
   - future-state (where we want to go)
   - alternative-option (different approach)
   - risk-mitigation (contingency plan)
   Default: future-state
   ```

### Phase 2: Baseline Architecture

```
What is the baseline architecture for this scenario?
(Choose existing Architecture note)

Search: [[Architecture - Current State HLD]]
Found: [[Architecture - Current State HLD]]

Confirm baseline? (Y/n)
> y
```

### Phase 3: What Changes?

For future-state / alternative scenarios, ask:

```
What changes from the baseline?

System Additions (comma-separated or one per line):
> SAP S/4HANA Cloud
> SAP Event Mesh

System Removals:
> SAP LegacyEngineeringSystem (legacy)

System Modifications:
> DataPlatform (add real-time event consumer)
> Snowflake (increase storage)

Integration Changes:
> Add: Event-driven SAP to DataPlatform
> Remove: Daily batch sync
> Modify: DataPlatform to Snowflake (add real-time)
```

### Phase 4: Systems Involved

```
Systems in this scenario (for quick view):
- [[System - SAP S/4HANA Cloud]]
- [[System - Event Mesh]]
- [[System - DataPlatform]]
- [[System - Snowflake]]
```

### Phase 5: Impact Analysis

Ask: "Analyse impact? (Y/n)"

If YES:
```
BUSINESS IMPACT:
Benefits:
> Real-time data enables faster decisions
> Reduced reporting lag from 24h to <1s
> Better customer experience

Risks:
> Migration disruption (1-2 week freeze)
> Higher licensing costs
> Team learning curve

TECHNICAL IMPACT:
Capabilities enabled:
> Event-driven architecture
> Real-time data pipelines
> Stream processing

Technical debt reduced:
> Legacy LegacyEngineeringSystem system (EOL'd)
> Point-to-point integrations (replaced)
> Batch workflows (replaced with streams)

COST IMPACT:
Implementation: £1,250,000
  - SAP migration: £800k
  - Integration: £300k
  - Analytics: £150k

Annual savings: £250,000 (infrastructure reduction)
Payback: 5 years

ORGANIZATIONAL IMPACT:
Resources: 27 people over 12 months
Budget: £1,250,000
Skills needed: SAP Cloud, Event-driven patterns, Kafka
Training required: 2 weeks per person
```

### Phase 6: Trade-offs & Comparison

Ask: "Compare with alternatives? (Y/n)"

If YES:
```
Alternative A: Vendor X SaaS
- Cost: Low (£300k/year)
- Timeline: 3 months
- Complexity: Low
- Flexibility: Limited

Alternative B: Keep current, add analytics tools
- Cost: £150k/year (tooling)
- Timeline: 6 months
- Complexity: Low
- Flexibility: High

Recommended: [Select which]
```

### Phase 7: Decision Framework

Ask: "Add decision criteria? (Y/n)"

If YES:
```
Go/No-Go Criteria:

GREEN LIGHT (Proceed):
- Budget secured
- Architecture approved
- Team available
- Executive sponsorship

YELLOW LIGHT (Conditions):
- Budget reduced (adjust scope)
- Timeline extended (resource constraints)
- Pilot approach (smaller initial scope)

RED LIGHT (Hold/Reject):
- SAP readiness < 40%
- Budget unavailable
- Key resources unavailable

Recommended: GREEN (full implementation)
Approval Status: Proposed
```

### Phase 8: Generate Frontmatter

```yaml
type: Scenario
title: "{{name}}"

scenarioId: "SCEN-{{name|sanitize}}-001"
scenarioType: {{type}}
version: "1.0"
createdDate: 2026-01-14
owner: "[[Person - {{user}}]]"

baselineArchitecture: "[[Architecture - {{baseline}}]]"
timeframe: {{timeframe}}

systemsAdded: [{{systems}}]
systemsRemoved: [{{systems}}]
systemsModified: [{{systems}}]

integrationsAdded: [{{integrations}}]
integrationsRemoved: [{{integrations}}]
integrationsModified: [{{integrations}}]

recommendedApproach: {{recommended}}
decisionStatus: proposed

confidence: medium
freshness: current
verified: false

created: 2026-01-14
tags: [type/scenario, {{type|lower}}]
```

### Phase 9: Generate Body Content

1. **Executive Summary**: 1-2 paragraphs
2. **Baseline Architecture**: Current state overview
3. **Proposed State**: What changes
4. **Full Scenario Architecture**: Diagram showing proposed
5. **Detailed Changes**: System-by-system walkthrough
6. **Impact Analysis**: Business, technical, cost, organizational
7. **Comparison Matrix**: Current vs Proposed vs Alternatives
8. **Risk & Mitigation**: Key risks and mitigation strategies
9. **Phased Implementation Plan**: Timeline by phase
10. **Success Metrics & KPIs**: How to measure success
11. **Go/No-Go Decision Criteria**: When to proceed
12. **Related Documentation**: Links to Architectures, ADRs

### Phase 10: Create File

**Filename**: `Scenario - {{name}}.md`

**Location**: Vault root

**Output**:
```
✅ Created: Scenario - {{name}}.md

Scenario Type: {{type}}
Status: {{status}}
Recommendation: {{recommended}}

Baseline: [[Architecture - {{baseline}}]]

Systems impacted: {{count}}
Integrations changed: {{count}}

Estimated cost: {{cost}}
Timeline: {{timeline}}

Next steps:
1. Review with stakeholders
2. Get executive approval: /decision {{scenario}}
3. Create project: /project {{scenario}}
4. Develop detailed plan: /architecture --type lld
```

## Example Interaction

```
User: /scenario "SAP Cloud Migration"

Scenario Type (default: future-state):
> future-state

Baseline Architecture:
> [[Architecture - Current State HLD]]

Systems being added:
> SAP S/4HANA Cloud
> SAP Event Mesh

Systems being removed:
> SAP LegacyEngineeringSystem (legacy)

Integration changes:
> Add event-driven SAP Cloud → DataPlatform
> Remove batch SAP → DataPlatform

Impact Analysis? (Y/n)
> y

Business Impact:
Benefits:
> Real-time data, faster decisions, reduced reporting lag

Risks:
> Migration disruption, higher costs, learning curve

Cost Impact:
Implementation: 1,250,000
Annual Savings: 250,000

Timeline? (Y/n)
> y

Phase 1 (Q1 2026): Planning (3 months)
Phase 2 (Q2 2026): SAP Cloud migration (3 months)
Phase 3 (Q3-Q4 2026): Integration modernization (4 months)

Compare with alternatives? (Y/n)
> y

Alternative A: Keep current, add tools (£150k, 6 months)
Alternative B: Vendor X SaaS (£300k, 3 months)

✅ Created: Scenario - SAP Cloud Migration.md

Status: Proposed
Recommendation: Proceed (GREEN light)

Next: Review with stakeholders and get approval
```
