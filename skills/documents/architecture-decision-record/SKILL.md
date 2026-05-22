---
name: architecture-decision-record
description: Use this skill when documenting significant architectural decisions. Provides ADR templates following the Nygard format with sections for context, decision, consequences, and alternatives. Use when writing ADRs, recording decisions, or evaluating options.
version: 2.0.0
author: AI Agent Hub
tags: [architecture, documentation, decision-making, backend]
context: fork
agent: backend-system-architect
user-invocable: false
---

# Architecture Decision Records
Architecture Decision Records (ADRs) are lightweight documents that capture important architectural decisions along with their context and consequences. This skill provides templates, examples, and best practices for creating and maintaining ADRs in your projects.

## Overview
- Making significant technology choices (databases, frameworks, cloud providers)
- Designing system architecture or major components
- Establishing patterns or conventions for the team
- Evaluating trade-offs between multiple approaches
- Documenting decisions that will impact future development

## Why ADRs Matter

ADRs serve as architectural memory for your team:
- **Context Preservation**: Capture why decisions were made, not just what was decided
- **Onboarding**: Help new team members understand architectural rationale
- **Prevent Revisiting**: Avoid endless debates about settled decisions
- **Track Evolution**: See how architecture evolved over time
- **Accountability**: Clear ownership and decision timeline

## ADR Format (Nygard Template)

Each ADR should follow this structure:

### 1. Title
Format: `ADR-####: [Decision Title]`
Example: `ADR-0001: Adopt Microservices Architecture`

### 2. Status
Current state of the decision:
- **Proposed**: Under consideration
- **Accepted**: Decision approved and being implemented
- **Superseded**: Replaced by a later decision (reference ADR number)
- **Deprecated**: No longer recommended but not yet replaced
- **Rejected**: Considered but not adopted (document why)

### 3. Context
**What to include:**
- Problem statement or opportunity
- Business/technical constraints
- Stakeholder requirements
- Current state of the system
- Forces at play (conflicting concerns)

### 4. Decision
**What to include:**
- The choice being made
- Key principles or patterns to follow
- What will change as a result
- Who is responsible for implementation

**Be specific and actionable:**
- ✅ "We will adopt microservices architecture using Node.js with Express"
- ❌ "We will consider using microservices"

### 5. Consequences
**What to include:**
- Positive outcomes (benefits)
- Negative outcomes (costs, risks, trade-offs)
- Neutral outcomes (things that change but aren't clearly better/worse)

### 6. Alternatives Considered
**Document at least 2 alternatives:**

**For each alternative, explain:**
- What it was
- Why it was considered
- Why it was not chosen

### 7. References (Optional)
Links to relevant resources:
- Meeting notes or discussion threads
- Related ADRs
- External research or articles
- Proof of concept implementations

## ADR Lifecycle

```
Proposed → Accepted → [Implemented] → (Eventually) Superseded/Deprecated
          ↓
      Rejected
```

## Best Practices

### 1. **Keep ADRs Immutable**
Once accepted, don't edit ADRs. Create new ADRs that supersede old ones.
- ✅ Create ADR-0015 that supersedes ADR-0003
- ❌ Update ADR-0003 with new decisions

### 2. **Write in Present Tense**
ADRs are historical records written as if the decision is being made now.
- ✅ "We will adopt microservices"
- ❌ "We adopted microservices"

### 3. **Focus on 'Why', Not 'How'**
ADRs capture decisions, not implementation details.
- ✅ "We chose PostgreSQL for relational consistency"
- ❌ "Configure PostgreSQL with these specific settings..."

### 4. **Review ADRs as Team**
Get input from relevant stakeholders before accepting.
- Architects: Technical viability
- Developers: Implementation feasibility
- Product: Business alignment
- DevOps: Operational concerns

### 5. **Number Sequentially**
Use 4-digit zero-padded numbers: ADR-0001, ADR-0002, etc.
Maintain a single sequence even with multiple projects.

### 6. **Store in Git**
Keep ADRs in version control alongside code:
- **Location**: `/docs/adr/` or `/architecture/decisions/`
- **Format**: Markdown for easy reading
- **Branch**: Same branch as implementation

## Quick Start Checklist

- [ ] Copy ADR template from `/templates/adr-template.md`
- [ ] Assign next sequential number (check existing ADRs)
- [ ] Fill in Context: problem, constraints, requirements
- [ ] Document Decision: what, why, how, who
- [ ] List Consequences: positive, negative, neutral
- [ ] Describe at least 2 Alternatives: what, pros/cons, why not chosen
- [ ] Add References: discussions, research, related ADRs
- [ ] Set Status to "Proposed"
- [ ] Review with team
- [ ] Update Status to "Accepted" after approval
- [ ] Link ADR in implementation PR
- [ ] Update Status to "Implemented" after deployment

## Common Pitfalls to Avoid

❌ **Too Technical**: "We'll use Kubernetes with these 50 YAML configs..."
✅ **Right Level**: "We'll use Kubernetes for container orchestration because..."

❌ **Too Vague**: "We'll use a better database"
✅ **Specific**: "We'll use PostgreSQL 15+ for transactional data because..."

❌ **No Alternatives**: Only documenting the chosen solution
✅ **Comparative**: Document why alternatives weren't chosen

❌ **Missing Consequences**: Only listing benefits
✅ **Balanced**: Honest about costs and trade-offs

❌ **No Context**: "We decided to use Redis"
✅ **Contextual**: "Given our 1M+ concurrent users and sub-50ms latency requirement..."

## Related Skills

- **api-design-framework**: Use when designing APIs referenced in ADRs
- **database-schema-designer**: Use when ADR involves database choices
- **security-checklist**: Consult when ADR has security implications

---

**Skill Version**: 2.0.0
**Last Updated**: 2026-01-08
**Maintained by**: AI Agent Hub Team

## Capability Details

### adr-creation
**Keywords:** adr, architecture decision, decision record, document decision
**Solves:**
- How do I document an architectural decision?
- Create an ADR
- Architecture decision template

### adr-best-practices
**Keywords:** when to write adr, adr lifecycle, adr workflow, adr process, adr review, quantify impact
**Solves:**
- When should I write an ADR?
- How do I manage ADR lifecycle?
- What's the ADR review process?
- How to quantify decision impact?
- ADR anti-patterns to avoid
- Link related ADRs

### tradeoff-analysis
**Keywords:** tradeoff, pros cons, alternatives, comparison, evaluate options
**Solves:**
- How do I analyze tradeoffs?
- Compare architectural options
- Document alternatives considered

### consequences
**Keywords:** consequence, impact, risk, benefit, outcome
**Solves:**
- What are the consequences of this decision?
- Document decision impact
- Risk and benefit analysis
