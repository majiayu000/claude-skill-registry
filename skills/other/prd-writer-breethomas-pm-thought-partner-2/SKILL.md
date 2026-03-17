---
name: prd-writer
description: Full 5-stage PRD framework for complex features. Use for deep PRD work via /spec --deep full-prd. For quick feature specs, use /spec --feature instead.
---

# PRD Writer - AI Era Product Specifications

> **DEEP REFERENCE SKILL**
>
> For most PRD work, start with `/spec --feature` (Lite PRD flow).
> Use this skill via `/spec --deep full-prd` when you need:
> - The full 5-stage evolution (Planning → Kickoff → Solution Review → Launch Ready → Impact Review)
> - 15-25 behavior examples for AI features
> - Detailed rollout planning with gates
> - Complete quality checklists

This skill creates modern, decision-focused PRDs that work with AI prototyping tools while maintaining strategic clarity. Based on proven practices from leading tech companies including OpenAI.

## Core Philosophy

**PRDs are about decisions, not documentation.**

A great PRD in 2025:
- Makes explicit decisions at every turn
- Contains concrete examples, not vague descriptions
- Lives and evolves with the product
- Works alongside AI prototyping, not against it
- Is short, sharp, and actionable

**The fatal flaw of bad PRDs**: They say a lot without deciding anything. "Improve engagement" is a hope, not a specification.

## Why PRDs Still Matter

Even with AI prototyping tools (Cursor, Replit, v0), PRDs remain critical because prototypes don't specify:

1. **Strategic context**: How does this fit the overall strategy?
2. **Success criteria**: What metrics define success?
3. **Rollout plan**: Who gets this and when?
4. **Risk management**: What could go wrong and how do we handle it?
5. **Non-goals**: What are we explicitly NOT doing?

**Key insight**: When building fast becomes easy (thanks to AI), knowing what to build becomes even more important.

## The Modern Product Development Flow

**Old flow (linear)**: PRD → Design → Build → Test

**New flow (cyclical)**: Idea → Quick Prototype → PRD → Refined Prototype → Ship

### How PRDs and Prototypes Work Together

**Prototypes as discovery tools**:
- Use AI tools to mock up 3 different approaches in an afternoon
- Each prototype teaches something about the problem space
- PRD captures learnings and sets direction

**PRDs as prototype constraints**:
- PRD provides guardrails for prototyping
- Answers: What edge cases? What metrics? How does this fit strategy?

**The feedback loop**:
- Iterate between prototypes and PRDs multiple times
- Each prototype informs the PRD
- Each PRD update guides the next prototype

### Common Failure Modes Without PRDs

Teams that skip PRDs typically:
1. Build something fast that doesn't solve the right problem
2. Build the right thing but can't measure if it worked
3. Ship something that breaks other parts of the product

**The PRD is your insurance policy against these failures.**

## Essential PRD Components

Every great PRD must include these elements:

### 1. Opportunity Framing
- **Core Problem**: One-sentence summary of the issue
- **Working Hypothesis**: One-sentence proposed answer
- **Strategy Fit**: Which bet/initiative this unlocks now

### 2. Boundaries
- **Scope**: What's included
- **Non-Goals**: What's explicitly excluded (critical for decision-making)

### 3. Success Measurement
- **Offline Golden Set**: Test data for validation
- **Human Review**: Qualitative checks
- **Online Metrics**: Specific KPIs with thresholds (not "improve X")

### 4. Rollout Plan
- **Exposure**: Percentage of traffic or users (specific numbers)
- **Duration**: Planned test length
- **Segments & Ramp Gates**: Sequencing criteria and decision points

### 5. Risk Management
- **Detection**: How to spot failures
- **Fallback & Kill Switch**: Recovery mechanisms
- **Owners**: Who handles incidents

### 6. Ownership & Action
- **Primary Owner**: Accountable person/team
- **Decision Points**: When to revisit/adjust

## AI-Specific PRD Requirements

For AI features, add these critical elements:

### Behavior Contract with Examples
The defining characteristic of AI PRDs: **tons of concrete examples**

Include 15-25 labeled examples showing:
- **Good responses**: What the AI should do
- **Bad responses**: Common failure modes
- **Reject cases**: When AI should refuse/defer

**Format for each example**:
```
User Input: [specific query or scenario]
Good Response: [desired AI behavior]
Bad Response: [what to avoid]
Reject: [when to refuse]
```

### Principles and Instructions
- Clear guidelines for AI behavior
- Specific risks and how to avoid them
- Guardrails and safety measures

### Edge Cases and Red-Team List
- Adversarial inputs
- PII/sensitive data handling
- Performance degradation scenarios
- Code snippets, special characters, multi-language inputs

**Reference model**: OpenAI's Model Spec is the gold standard - filled with concrete examples, not abstract principles.

## The Five-Stage PRD Evolution

**Critical principle**: Don't treat PRDs as one-and-done. They evolve through the product lifecycle.

### Stage 1: Planning (Speclet)
Lightweight exploration document:
- Problem + motivating data (quantitative + 3 user quotes)
- Hypothesis + strategy fit
- Comp set & prior art research
- Open questions & owners

**Purpose**: Build shared understanding and get alignment to proceed

### Stage 2: Kickoff
Decision to build - now add structure:
- Clear in/out of scope
- Napkin mock (be ready to throw away)
- Success metrics + MDE (Minimum Detectable Effect) + guardrails
- Impact sizing model (order-of-magnitude)

**Purpose**: Set boundaries and success criteria before detailed design

### Stage 3: Solution Review
Detailed specification ready for engineering:
- Behavior contract draft + 15-25 examples
- Edge cases + red-team list
- Tracking requirements
- Rollout design v1

**Purpose**: Engineering can build to this spec

### Stage 4: Launch Readiness
Pre-ship checklist completion:
- Offline eval golden set ready
- Human review rubric ready
- Runbook + fallbacks + kill switch wired
- Legal/Security reviewed

**Purpose**: Safe, measurable launch

### Stage 5: Impact Review (Post-Ship)
Learning and iteration:
- Update PRD top with results doc link
- What surprised us? What will we change?
- Annex: add new good/bad/reject examples from real traffic
- Decision: iterate, scale, or retire

**Purpose**: Close the loop and capture learnings

## Writing Process Best Practices

### Critical Rule #1: Don't Use LLMs for First Drafts

**Why**: LLMs create verbose, decision-free documentation that says nothing

**Instead**:
- Write the first draft yourself with clear decisions
- Use LLM as copilot to improve and finesse
- Think of AI as teammate, not ghostwriter

### Critical Rule #2: Be Specific, Not Generic

**Bad** (vague): "Improve user engagement"
**Good** (specific): "P50 reply time drops ≥10% vs control group"

**Bad** (generic): "Generate helpful replies"
**Good** (actionable): "For simple questions (<10 words), respond within 2s with contextually relevant suggestions based on last 3 messages"

**Bad** (hopeful): "Reduce support tickets"
**Good** (measurable): "Decrease returns-related support tickets by 15-20% (from baseline 18% to 14.4-14.8%) measured over 30-day post-implementation window"

### Critical Rule #3: Make Decisions, Not Descriptions

Every section should answer a decision:
- **Not**: "We will test the feature" 
- **But**: "A/B test with 5% user-level randomization for 2 weeks, graduating at p<0.05 with 10%+ metric lift"

## PRD Quality Checklist

Before considering a PRD complete, verify:

**Strategic Clarity**
- [ ] Problem statement is one sentence
- [ ] Hypothesis is one sentence
- [ ] Strategy fit is explicit and current

**Measurability**
- [ ] Success metrics have specific thresholds (not "improve")
- [ ] Guardrail metrics are defined
- [ ] Graduation criteria are clear

**Actionability**
- [ ] Engineering knows exactly what to build
- [ ] Behavior is specified with examples (15-25 for AI features)
- [ ] Edge cases are enumerated

**Risk Management**
- [ ] Detection mechanisms are defined
- [ ] Fallback strategies exist
- [ ] Kill switch is specified with owner

**Rollout Precision**
- [ ] Exposure percentage is specific
- [ ] Duration is planned
- [ ] Ramp gates have criteria

**Decision Quality**
- [ ] Every "will" has a "how" and "when"
- [ ] Non-goals are explicit
- [ ] Owners are named

## Common PRD Antipatterns

### Antipattern 1: Prose Without Decisions
**Symptom**: Long paragraphs explaining context with no actionable outcomes

**Fix**: Every paragraph should end with a decision or a specific example

### Antipattern 2: Metric Theater
**Symptom**: "Improve engagement", "Increase satisfaction", "Reduce costs"

**Fix**: "P50 engagement time increases ≥15%", "NPS increases from 42 to 48+", "Server costs decrease $12K/month"

### Antipattern 3: Implementation Fantasy
**Symptom**: "Start small, then ramp" or "Three-phase approach"

**Fix**: "Week 1: 5% US users, Week 2: Graduate if p<0.05 and +10% metric, Week 3: Scale to 25%"

### Antipattern 4: Vibe-Based Behavior
**Symptom**: "Generate helpful replies" or "Provide good recommendations"

**Fix**: 25 labeled examples showing good/bad/reject cases with specific inputs and outputs

### Antipattern 5: One-and-Done Documentation
**Symptom**: PRD written once, never updated, gathering dust

**Fix**: Update PRD at each stage, link to results, annex learnings from production

## AI Prototyping Integration Checklist

When using AI tools in development, ensure:

**Before Prototyping**
- [ ] PRD speclet exists with problem/hypothesis
- [ ] Strategic fit is validated
- [ ] Success metrics are defined

**During Prototyping**
- [ ] Each prototype tests specific hypothesis from PRD
- [ ] Learnings feed back into PRD updates
- [ ] Edge cases discovered are documented

**After Prototyping**
- [ ] PRD reflects prototype learnings
- [ ] Behavior contract includes examples from prototypes
- [ ] Rollout plan accounts for prototype findings

**Before Engineering**
- [ ] PRD is specific enough to build from
- [ ] Examples cover major use cases
- [ ] Risk mitigation is planned

## Output Format Guidelines

When creating PRDs, use this structure:

### Document Header
```
Title: [Feature Name]
Owner: [Name/Team]
Status: [Planning/Kickoff/Solution Review/Launch Ready/Shipped]
Last Updated: [Date]
```

### Section Organization
1. **Executive Summary** (2-3 sentences max)
2. **Opportunity Framing** (Problem, Hypothesis, Strategy Fit)
3. **Success Measurement** (Metrics with thresholds)
4. **Scope & Non-Goals** (Explicit boundaries)
5. **Behavior Specification** (Examples for AI features)
6. **Rollout Plan** (Exposure, duration, gates)
7. **Risk Management** (Detection, fallbacks, owners)
8. **Open Questions** (What we don't know yet)

### Formatting Best Practices
- Use tables for examples and metrics
- Bold key decisions and thresholds
- Keep paragraphs to 3 sentences max
- Use bullet points for lists, not prose
- Include specific numbers, not ranges without justification

## Domain-Specific Guidance

### For Traditional Features (Non-AI)
Focus on:
- User flows and interaction patterns
- Technical dependencies and integrations
- Performance requirements with SLAs
- Migration plans if replacing existing functionality

### For AI/ML Features
Focus on:
- Behavior contract with 15-25 examples
- Model performance thresholds
- Human review rubrics
- PII and safety considerations
- Fallback to non-AI flows

### For Infrastructure/Platform
Focus on:
- SLAs and reliability targets
- Scale requirements with specific traffic projections
- Migration path and backward compatibility
- Monitoring and alerting specifications

### For Experiments/A B Tests
Focus on:
- Statistical power calculations
- Contamination prevention strategies
- Minimum detectable effects
- Graduation and rollback criteria

## Reviewing Existing PRDs

When reviewing a PRD, assess these dimensions:

### Decision Density
- Count decisions per page (aim for 5+)
- Flag vague language ("improve", "enhance", "optimize")
- Identify missing thresholds on metrics

### Example Richness (for AI features)
- Count labeled examples (need 15-25)
- Check for edge case coverage
- Verify good/bad/reject cases exist

### Strategic Grounding
- Can you trace feature to specific strategy?
- Are non-goals explicit?
- Is opportunity sizing quantified?

### Rollout Readiness
- Are exposure percentages specific?
- Do graduation criteria exist?
- Is risk mitigation planned?

### Actionability Test
Ask: "Can engineering build from this without asking questions?"
If no, the PRD needs more specificity.

## Reference Resources

For additional guidance, see:
- `references/prd-template.md` - Complete template with examples
- `references/ai-examples.md` - 50+ AI behavior examples
- `references/before-after.md` - Real PRD transformations
- `references/metrics-library.md` - Common metrics with thresholds

## Key Reminders

1. **PRDs are living documents** - Update through all five stages
2. **Decisions over documentation** - Every section should decide something
3. **Examples are mandatory** - Especially for AI features (15-25 minimum)
4. **Specificity wins** - "≥10%" not "improve"
5. **Work with prototypes** - PRDs and prototypes iterate together
6. **Don't use LLMs for first drafts** - Use them to polish your decisions
7. **Non-goals matter** - What you're NOT doing is as important as what you are
8. **Rollout is precise** - Percentages, durations, criteria - not "start small"