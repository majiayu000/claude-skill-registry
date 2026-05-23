---
name: war-room
description: Multi-LLM deliberation framework for strategic decisions through pressure-based expert consultation
triggers: war room, strategic decision, multi-expert, deliberation, council, convene experts, expert panel
use_when: complex decisions requiring multiple perspectives, architectural trade-offs, high-stakes choices
do_not_use_when: simple questions, routine tasks, single-path implementations
model_preference: claude-opus-4
category: strategic-planning
tags: [deliberation, multi-llm, strategy, decision-making, council]
dependencies:
  - conjure:delegation-core
  - memory-palace:strategeion
tools: [Bash, Read, Write]
complexity: advanced
estimated_tokens: 2500
progressive_loading: true
modules:
  - modules/reversibility-assessment.md
  - modules/expert-roles.md
  - modules/deliberation-protocol.md
  - modules/merkle-dag.md
version: 1.3.7
---
## Table of Contents

- [Overview](#overview)
- [Reversibility-Based Routing](#reversibility-based-routing)
- [When to Use](#when-to-use)
- [When NOT to Use](#when-not-to-use)
- [Expert Panel](#expert-panel)
- [Deliberation Protocol](#deliberation-protocol)
- [Integration](#integration)
- [Usage](#usage)
- [Output](#output)
- [Configuration](#configuration)
- [Related Skills](#related-skills)

# War Room Skill

Orchestrate multi-LLM deliberation for complex strategic decisions.

## Overview

The War Room convenes multiple AI experts to analyze problems from diverse perspectives, challenge assumptions through adversarial review, and synthesize optimal approaches under the guidance of a Supreme Commander.

### Philosophy

> "The trick is that there is no trick. The power of intelligence stems from our vast diversity, not from any single, perfect principle."
> - Marvin Minsky, Society of Mind

## Reversibility-Based Routing

Before deliberation, assess the **Reversibility Score (RS)** to determine appropriate resource allocation:

```
RS = (Reversal Cost + Time Lock-In + Blast Radius + Information Loss + Reputation Impact) / 25
```

| RS Range | Type | Mode | Resources |
|----------|------|------|-----------|
| 0.04 - 0.40 | **Type 2** | Express | 1 expert, < 2 min |
| 0.41 - 0.60 | **Type 1B** | Lightweight | 3 experts, 5-10 min |
| 0.61 - 0.80 | **Type 1A** | Full Council | 7 experts, 15-30 min |
| 0.81 - 1.00 | **Type 1A+** | Delphi | 7 experts, 30-60 min |

**Quick Heuristics:**
- Can be A/B tested? → Type 2
- Requires data migration? → Type 1
- Public commitment required? → Type 1A+

See `modules/reversibility-assessment.md` for full scoring guide.

## When to Use

- Architectural decisions with major trade-offs
- Multi-stakeholder problems requiring diverse perspectives
- High-stakes choices with significant consequences (RS > 0.60)
- Novel problems without clear precedent
- When brainstorming produces multiple strong competing approaches

## When NOT to Use

- Simple questions with obvious answers
- Routine implementation tasks
- Well-documented patterns with clear solutions
- Time-critical decisions requiring immediate action
- **Type 2 decisions** (RS ≤ 0.40) — use Express mode or skip War Room entirely

## Expert Panel

### Default (Lightweight Mode)

| Role | Model | Purpose |
|------|-------|---------|
| Supreme Commander | Claude Opus | Final synthesis, escalation decisions |
| Chief Strategist | Claude Sonnet | Approach generation, trade-off analysis |
| Red Team | Gemini Flash | Adversarial challenge, failure modes |

### Full Council (Escalated)

| Role | Model | Purpose |
|------|-------|---------|
| Supreme Commander | Claude Opus | Final synthesis |
| Chief Strategist | Claude Sonnet | Approach generation |
| Intelligence Officer | Gemini 2.5 Pro | Large context analysis (1M+) |
| Field Tactician | GLM-4.7 | Implementation feasibility |
| Scout | Qwen Turbo | Quick data gathering |
| Red Team Commander | Gemini Flash | Adversarial challenge |
| Logistics Officer | Qwen Max | Resource estimation |

## Deliberation Protocol

### Two-Round Default

```
Round 1: Generation
  - Phase 1: Intelligence Gathering (Scout, Intel Officer)
  - Phase 2: Situation Assessment (Chief Strategist)
  - Phase 3: COA Development (Multiple experts, parallel)
  - Commander Escalation Check

Round 2: Pressure Testing
  - Phase 4: Red Team Review (all COAs)
  - Phase 5: Voting + Narrowing (top 2-3)
  - Phase 6: Premortem Analysis (selected COA)
  - Phase 7: Supreme Commander Synthesis
```

### Delphi Extension (High-Stakes)

For high-stakes decisions, extend to iterative Delphi convergence:
- Multiple rounds until expert consensus
- Convergence threshold: 0.85

## Integration

### With Brainstorm

**War Room is AUTOMATICALLY INVOKED** from `Skill(attune:project-brainstorming)` after Phase 3 (Approach Generation).

The brainstorm skill passes all context to War Room:
- Problem statement and constraints
- Generated approaches with pros/cons
- Comparison matrix
- Reversibility assessment (automatically calculated)

**Bypass conditions** (only if ALL true):
- RS ≤ 0.40 (Type 2 decision - clearly reversible)
- Single obvious approach with no meaningful trade-offs
- Low complexity with well-documented pattern
- User explicitly declines after seeing RS assessment

```bash
# Automatic invocation from brainstorm (do not skip)
/attune:war-room --from-brainstorm

# Direct invocation (standalone)
/attune:war-room "Should we use microservices or monolith for this system?"
```

### With Memory Palace

Sessions persist to the **Strategeion** (War Palace):

```
~/.claude/memory-palace/strategeion/
  - war-table/      # Active sessions
  - campaign-archive/  # Historical decisions
  - doctrine/       # Learned patterns
  - armory/         # Expert configurations
```

### With Conjure

Experts are invoked via conjure delegation:
- `conjure:gemini-delegation` for Gemini models
- `conjure:qwen-delegation` for Qwen models
- Direct CLI for GLM-4.7 (`ccgd` or `claude-glm --dangerously-skip-permissions`)

## Usage

### Basic Invocation

```bash
/attune:war-room "What architecture should we use for the new payment system?"
```

### With Context

```bash
/attune:war-room "Best approach for API versioning" --files src/api/**/*.py
```

### Reversibility Assessment Only

Quick assessment without full deliberation:

```bash
/attune:war-room "Database migration to MongoDB" --assess-only
```

Output:
```
Reversibility Assessment
========================
Decision: Database migration to MongoDB

Dimensions:
  Reversal Cost:      5/5 (months of rework)
  Time Lock-In:       4/5 (migration path hardens)
  Blast Radius:       5/5 (all services affected)
  Information Loss:   4/5 (query patterns, ACID)
  Reputation Impact:  2/5 (internal unless downtime)

Reversibility Score: 0.80
Decision Type: Type 1A (One-Way Door)
Recommended Mode: Full Council

Proceed with full deliberation? [Y/n]
```

### Force Express Mode (Type 2)

Skip to rapid decision for clearly reversible choices:

```bash
/attune:war-room "Which logging library to use" --express
```

### Force Full Council

Override RS assessment for critical decisions:

```bash
/attune:war-room "Migration strategy" --full-council
```

### Delphi Mode

For highest-stakes irreversible decisions:

```bash
/attune:war-room "Long-term platform decision" --delphi
```

### Resume Session

```bash
/attune:war-room --resume war-room-20260120-153022
```

## Output

### Decision Document

The War Room produces a Supreme Commander Decision document:

```markdown
## SUPREME COMMANDER DECISION: {session_id}

### Reversibility Assessment
| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Reversal Cost | X/5 | ... |
| Time Lock-In | X/5 | ... |
| Blast Radius | X/5 | ... |
| Information Loss | X/5 | ... |
| Reputation Impact | X/5 | ... |

**RS: 0.XX | Type: [1A+/1A/1B/2] | Mode: [delphi/full_council/lightweight/express]**

### Decision
**Selected Approach**: [Name]

### Rationale
[Why this approach was selected]

### Implementation Orders
1. [ ] Immediate actions
2. [ ] Short-term actions

### Watch Points
[From Premortem - what to monitor]

### Reversal Plan (for Type 1 decisions)
[If this decision proves wrong, here's the exit strategy]

### Dissenting Views
[For the record]
```

### Session Artifacts

Saved to Strategeion:
- Intelligence reports
- Situation assessment
- All COAs (with full attribution after unsealing)
- Red Team challenges
- Premortem analysis
- Final decision

## Anonymization

Expert contributions are anonymized during deliberation using Merkle-DAG:
- Responses labeled as "Response A, B, C..." during review
- Attribution revealed only after decision is made
- Hash verification ensures integrity

See `modules/merkle-dag.md` for details.

## Escalation

### Automatic (Reversibility-Based)

Deliberation mode is automatically selected based on Reversibility Score:

| RS Score | Automatic Mode |
|----------|----------------|
| ≤ 0.40 | Express (bypass full War Room) |
| 0.41 - 0.60 | Lightweight panel |
| 0.61 - 0.80 | Full Council |
| > 0.80 | Full Council + Delphi |

### Manual Override

The Supreme Commander may override automatic classification when:
- High complexity detected (multiple architectural trade-offs)
- Significant disagreement between initial experts
- Novel problem domain requiring specialized analysis
- Precedent-setting decision (future decisions will follow pattern)
- Political/organizational sensitivity beyond technical scope

**Escalation requires written justification with RS assessment.**

### De-escalation

Equally important: identify decisions being over-deliberated:
- If RS ≤ 0.40, recommend Express mode or immediate execution
- Challenge "false irreversibility" ("we can't change this later" without evidence)
- Track de-escalation rate as team health metric

## Configuration

### User Settings

```json
{
  "war_room": {
    "default_mode": "lightweight",
    "auto_escalate": true,
    "delphi_threshold": 0.85,
    "max_delphi_rounds": 5
  }
}
```

### Hook Auto-Trigger

War Room can be auto-suggested via hook when:
- Keywords detected ("strategic decision", "trade-off", etc.)
- Complexity score exceeds threshold (0.7)
- User has opted in via settings

## Related Skills

- `Skill(attune:project-brainstorming)` - Pre-War Room ideation
- `Skill(imbue:scope-guard)` - Scope management
- `Skill(imbue:rigorous-reasoning)` - Reasoning methodology
- `Skill(conjure:delegation-core)` - Expert dispatch

## Related Commands

- `/attune:war-room` - Invoke this skill
- `/attune:brainstorm` - Pre-War Room ideation
- `/memory-palace:strategeion` - Access War Room history

## References

### Strategic Foundations
- Sun Tzu - Art of War (intelligence gathering)
- Clausewitz - On War (friction and fog)
- Robert Greene - 33 Strategies of War (unity of command)
- MDMP - U.S. Army (structured decision process)
- Gary Klein - Premortem (failure mode analysis)
- Karpathy - LLM Council (anonymized peer review)

### Reversibility Framework
- [Jeff Bezos - Type 1 vs Type 2 Decisions](https://ashikuzzaman.com/2025/03/03/amazons-type-1-vs-type-2-decisions-a-framework-for-effective-decision-making/) (Amazon shareholder letters)
- [Farnam Street - Reversible and Irreversible Decisions](https://fs.blog/reversible-irreversible-decisions/) (STOP-LOP-KNOW framework)
- [Tapan Desai - One-Way and Two-Way Door Decision-Making](https://tapandesai.com/one-way-two-way-doors-decision-making/) (practical application)
