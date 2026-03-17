---
name: discover-assumptions
description: Use after solution concepts exist to surface and prioritize assumptions behind outcomes, opportunities, or solution ideas and design experiments to test them.
---

# Discover Assumptions and Experiments

## Overview
Surface the riskiest assumptions in an Opportunity Solution Tree and design the smallest tests that can prove or disprove them quickly.

## Position in Workflow

Step 4 of product strategy workflow:
1. `/discover-outcomes` - Define outcomes
2. `/discover-opportunities` - Identify opportunities
3. `/ideate-solutions` - Explore solution concepts
4. `/discover-assumptions` - Validate with experiments (THIS)

## Inputs (ask if missing, max 5)
- Target node(s): outcome, opportunity, or solution
- Target users/market
- Existing evidence (data, research, learnings)
- Constraints (time, budget, ethics, legal)
- Decision deadline

## Assumption Types
- **Desirability**: Users want or value it
- **Usability**: Users can use it successfully
- **Feasibility**: We can build/deliver it
- **Viability**: It supports the business model
- **Risk/Compliance/Ethics**: It is safe and allowed
- **Strategic**: It aligns with goals and positioning

## Workflow
1. **List assumptions per node**
   - Write assumptions as testable statements.
2. **Score risk**
   - Impact (low/medium/high) x uncertainty (low/medium/high).
   - Note current evidence strength (none/weak/moderate/strong).
3. **Prioritize**
   - Select top 3-5 riskiest assumptions.
4. **Design experiments**
   - Propose 2+ tests per assumption, fastest/cheapest first.
   - Define hypothesis, method, sample, success metric, and decision threshold.
5. **Sequence tests**
   - Start with tests that can invalidate assumptions quickly.

## Experiment Patterns (examples)
- Customer interviews, observation, diary studies
- Survey with behavioral intent + follow-up validation
- Smoke test or landing page
- Fake-door or click-through test
- Concierge or Wizard-of-Oz pilot
- Prototype usability test
- A/B test or pricing experiment
- Limited rollout with manual operations

## Output Format
```
## Assumption Discovery

### Context Summary
[1-3 sentences]

### Assumptions (by node)
- Node: [Outcome/Opportunity/Solution]
  - Assumption: ... (type: desirability)
  - Evidence: ... (strength: weak)
  - Risk: impact high x uncertainty high

### Top Risks
1) Assumption: ...
   - Why risky: ...

### Experiments
1) Assumption: ...
   - Hypothesis: ...
   - Method: ...
   - Sample: ...
   - Success metric: ...
   - Decision threshold: ...
   - Time/cost: ...

### Sequenced Plan
1) ...
2) ...

### Open Questions
- ...

### Next Step
If assumptions are validated, proceed to product planning.
```

## Quick Reference
- Turn beliefs into testable statements.
- Prefer tests that can disprove the assumption fast.
- Document decision thresholds before running tests.

## Common Mistakes
- Treating opinions as evidence
- Testing solutions before validating the underlying assumption
- Running expensive tests without cheap falsification attempts
- Vague hypotheses or missing thresholds
