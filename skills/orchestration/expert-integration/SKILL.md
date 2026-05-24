# Expert Integration Layer

Meta-orchestration system that connects all Agent Experts for seamless workflow execution.

---
name: expert-integration
description: |
  Cross-expert routing, handoffs, and learning propagation across the Agent Expert framework.
  Use when: tasks span multiple domains, workflows cross expert boundaries, or learning needs to propagate
  Triggers on: automatically routes based on task content - rarely called directly
---

## Expert Registry

| Expert | Domain | Primary Triggers | Score |
|--------|--------|------------------|-------|
| Goal Tracking/CVM | Pipeline metrics | "cvm-goals", "stage entry", "micro-actions" | 22.5 |
| Discovery/Sales | Sales execution | "discovery call", "38 questions", "follow-up" | 19.0 |
| HubSpot CRM | API operations | "hubspot", "association", "create deal" | 19.0 |
| Brand Scout | Lead research | "brand scout", "research", "email sequence" | 13.5 |

## Routing Logic

### Primary Router

```
IF task mentions "brand scout" OR "research [company]" OR "prospect"
  → Brand Scout Expert (lead)
  → HubSpot CRM Expert (support for record creation)

IF task mentions "discovery call" OR "38 questions" OR "proposal"
  → Discovery/Sales Expert (lead)
  → HubSpot CRM Expert (support for logging)

IF task mentions "cvm-goals" OR "pipeline health" OR "stage metrics"
  → Goal Tracking Expert (lead)
  → HubSpot CRM Expert (support for data fetch)

IF task mentions "hubspot" OR "create deal" OR "association"
  → HubSpot CRM Expert (lead)
  → Others as needed for context

IF task spans multiple domains
  → Determine primary domain from user intent
  → Load primary expert as lead
  → Reference supporting experts for handoffs
```

### Workflow Patterns

#### Pattern 1: Lead Generation → Outreach

```
Brand Scout Expert → HubSpot CRM Expert → Discovery/Sales Expert → Goal Tracking Expert
     ↓                    ↓                      ↓                      ↓
 Research           Create records          Send emails           Track metrics
     ↓                    ↓                      ↓                      ↓
 9-section        Company+Contact+Lead     5-email sequence     new_leads count
  report           with associations        personalized         updates
```

#### Pattern 2: Discovery → Close

```
Discovery/Sales Expert → HubSpot CRM Expert → Goal Tracking Expert
        ↓                       ↓                     ↓
   38 Questions            Update deal          Track conversions
        ↓                       ↓                     ↓
   Qualification            Move stage          Stage entry metrics
```

#### Pattern 3: Goal Analysis → Action

```
Goal Tracking Expert → [Expert by stage]
        ↓                    ↓
   Identify red         Prescribe actions
      stages
        ↓                    ↓
   Stage 1 red     →    Brand Scout Expert (more leads)
   Stage 2-4 red   →    Discovery/Sales Expert (more outreach)
   Stage 5-7 red   →    Discovery/Sales Expert (implementation follow-up)
```

## Handoff Protocols

### Brand Scout → HubSpot CRM

**Trigger**: Brand Scout report complete with HIGH confidence

**Handoff Data**:
```yaml
from: brand-scout-expert
to: hubspot-crm-expert
data:
  company:
    name: "[from Section 6]"
    domain: "[from Section 6]"
    industry: "[exact HubSpot value]"
  contacts:
    - firstname, lastname, email, title
  confidence: "[HIGH/MEDIUM]"
  report_path: "[output location]"
```

**HubSpot Actions**:
1. /check-lead (verify no duplicates)
2. Create Company
3. Create Contact(s)
4. Associate Contact→Company (type 280)
5. Create Lead with PRIMARY associations (578, 580)
6. Return record IDs

### HubSpot CRM → Discovery/Sales

**Trigger**: Lead created, ready for outreach

**Handoff Data**:
```yaml
from: hubspot-crm-expert
to: discovery-sales-expert
data:
  hubspot_ids:
    company_id: "[ID]"
    contact_id: "[ID]"
    lead_id: "[ID]"
  contact:
    name: "[Full name]"
    email: "[email]"
    title: "[title]"
  research:
    pe_backing: "[if known]"
    shipping_intel: "[from Brand Scout]"
    personalization_hooks: "[list]"
```

**Discovery Actions**:
1. Generate email sequence (from Brand Scout data)
2. Schedule Email 1 (Day 1)
3. Create follow-up tasks
4. Log activities to HubSpot

### Discovery/Sales → Goal Tracking

**Trigger**: Stage transition occurs

**Handoff Data**:
```yaml
from: discovery-sales-expert
to: goal-tracking-expert
data:
  deal_id: "[ID]"
  stage_from: "[previous stage]"
  stage_to: "[new stage]"
  timestamp: "[when entered]"
```

**Goal Tracking Actions**:
1. Update stage entry counts
2. Recalculate weekly progress
3. Check goal thresholds
4. Update rubric scores

### Goal Tracking → Micro-Actions

**Trigger**: Stage shows red (below threshold)

**Handoff Data**:
```yaml
from: goal-tracking-expert
to: "[varies by stage]"
data:
  red_stage: "[stage number]"
  current_count: "[actual]"
  target_count: "[goal]"
  gap: "[difference]"
```

**Routing**:
- Stage 1 red → Brand Scout Expert
- Stage 2-4 red → Discovery/Sales Expert
- Stage 5-7 red → Discovery/Sales Expert (implementation focus)

## Learning Propagation

### Cross-Expert Learning

When one expert learns something that affects another:

```yaml
learning_event:
  source_expert: "hubspot-crm-expert"
  learning_id: "F009"
  description: "Lead object requires PRIMARY associations inline"
  affects:
    - "brand-scout-expert"  # Uses HubSpot for lead creation
    - "discovery-sales-expert"  # May create leads after discovery

propagation:
  - Update affected experts' expertise.yaml
  - Add to known_failures if relevant
  - Increment version numbers
```

### Pattern Recognition Across Experts

```yaml
cross_expert_patterns:
  - pattern: "Zone-skipping math resonates with DTC brands"
    learned_by: brand-scout-expert
    useful_for: discovery-sales-expert
    context: "Use in discovery call questions about shipping costs"

  - pattern: "Day 4 value-add email outperforms Day 1"
    learned_by: brand-scout-expert
    useful_for: discovery-sales-expert
    context: "Apply same pattern to proposal follow-ups"

  - pattern: "Task audit trail requires NOT_STARTED then COMPLETED"
    learned_by: hubspot-crm-expert
    useful_for: goal-tracking-expert
    context: "Task completion counting uses hs_task_completion_date"
```

## Integration Points Summary

| From | To | Trigger | Data Passed |
|------|-----|---------|-------------|
| Brand Scout | HubSpot CRM | Report complete | Company/contact data |
| Brand Scout | Discovery/Sales | Email sequence needed | Personalization hooks |
| HubSpot CRM | Discovery/Sales | Lead created | Record IDs, contact info |
| HubSpot CRM | Goal Tracking | Stage change | Entry timestamps |
| Discovery/Sales | HubSpot CRM | Activity logging | Notes, tasks |
| Discovery/Sales | Goal Tracking | Stage advancement | Conversion data |
| Goal Tracking | Brand Scout | Stage 1 red | Need more leads |
| Goal Tracking | Discovery/Sales | Stage 2-7 red | Need more outreach |

## Reference Files

| File | Purpose |
|------|---------|
| `00-routing-rules.md` | Complete IF-THEN routing logic |
| `01-handoff-protocols.md` | Data structures for handoffs |
| `02-learning-propagation.md` | Cross-expert learning system |
| `03-workflow-templates.md` | Common multi-expert workflows |

## Usage

This integration layer is typically invisible - experts route automatically based on task content. However, you can explicitly invoke integration:

```
"Route this task to the appropriate expert"
"This workflow spans Brand Scout to Discovery - coordinate handoffs"
"Propagate this learning to all affected experts"
```

## Version

**Created**: 2025-12-16
**Updated**: 2025-12-16
**Experts Connected**: 4 (Goal Tracking, Discovery/Sales, HubSpot CRM, Brand Scout)
**Reference Files**: 4 (routing, handoffs, learning propagation, workflow templates)
**Framework**: The Nebuchadnezzar v3.4
