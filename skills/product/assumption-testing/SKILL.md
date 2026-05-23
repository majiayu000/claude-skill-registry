---
name: assumption-testing
description: Identify, prioritize, and test product assumptions systematically. Reduce risk by validating riskiest assumptions first through structured experiments.
allowed-tools: Read, Write, Glob, Grep, Task, WebSearch, WebFetch
---

# Assumption Testing

## When to Use This Skill

Use this skill when:

- **Assumption Testing tasks** - Working on identify, prioritize, and test product assumptions systematically. reduce risk by validating riskiest assumptions first through structured experiments
- **Planning or design** - Need guidance on Assumption Testing approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Every product idea rests on unvalidated assumptions. Assumption testing systematically identifies these assumptions, prioritizes by risk, and designs experiments to validate or invalidate them before significant investment.

## The DVFUE Framework

Five categories of assumptions to test:

| Category | Question | Failure Mode |
|----------|----------|--------------|
| **D**esirability | Will customers want this? | Nobody uses it |
| **V**iability | Does the business model work? | Unsustainable economics |
| **F**easibility | Can we build this? | Technical blockers |
| **U**sability | Can users figure it out? | Too confusing to use |
| **E**thical | Should we build this? | Harm to users/society |

## Assumption Identification

### Step 1: List All Assumptions

For your product/feature, brainstorm assumptions across categories:

**Desirability Assumptions**:

- Users have this problem
- The problem is painful enough to solve
- Users will pay for a solution
- Users prefer our approach over alternatives
- The timing is right

**Viability Assumptions**:

- We can acquire customers affordably
- Customers will pay our target price
- Customer lifetime value exceeds acquisition cost
- The market is large enough
- We can scale the business model

**Feasibility Assumptions**:

- We can build the core technology
- We have the required expertise
- We can deliver within time/budget constraints
- Third-party dependencies will work
- Performance requirements are achievable

**Usability Assumptions**:

- Users will understand the interface
- Users can complete key tasks
- Learning curve is acceptable
- Accessibility requirements can be met
- Users will adopt new workflows

**Ethical Assumptions**:

- The solution doesn't cause harm
- Data usage is acceptable to users
- No unintended negative consequences
- Aligns with our values
- Regulatory compliance is achievable

### Step 2: Identify Leap of Faith Assumptions

**Leap of Faith Assumptions** are the assumptions that:

1. If wrong, would sink the entire project
2. You have no data to support
3. You're taking on faith

**Prioritization Questions**:

- If this is wrong, does the project fail? → High priority
- Do we have evidence for this? → If no, higher priority
- How easily can we test this? → Easier = test sooner

## Assumption Mapping

### Risk × Certainty Matrix

```text
         High Certainty
              │
   ┌──────────┼──────────┐
   │   Known  │  Known   │
   │   Safe   │   Risk   │
   │ (Ignore) │ (Mitigate)│
Low├──────────┼──────────┤High
Risk│ Unknown │ Unknown  │Risk
   │   Safe   │   Risk   │
   │ (Defer)  │  (TEST!) │
   └──────────┼──────────┘
              │
         Low Certainty
```

**Priority Order**:

1. Unknown Risk (High risk, low certainty) → Test immediately
2. Known Risk (High risk, high certainty) → Mitigate
3. Unknown Safe (Low risk, low certainty) → Defer testing
4. Known Safe (Low risk, high certainty) → Ignore

### Assumption Card Template

```text
┌─────────────────────────────────────────────────────────────────┐
│  ASSUMPTION: [Statement of what we believe to be true]          │
├─────────────────────────────────────────────────────────────────┤
│  Category: □ Desirability □ Viability □ Feasibility             │
│            □ Usability    □ Ethical                             │
├─────────────────────────────────────────────────────────────────┤
│  Risk Level:     □ High  □ Medium  □ Low                        │
│  Certainty:      □ High  □ Medium  □ Low                        │
├─────────────────────────────────────────────────────────────────┤
│  Evidence (current):                                            │
│  [What evidence do we have? None = "Leap of Faith"]             │
├─────────────────────────────────────────────────────────────────┤
│  Test Method:    [How could we test this?]                      │
│  Success Signal: [What would validate it?]                      │
│  Failure Signal: [What would invalidate it?]                    │
└─────────────────────────────────────────────────────────────────┘
```

## Experiment Design

### Experiment Types by Category

| Category | Low-Effort Experiments | High-Effort Experiments |
|----------|------------------------|-------------------------|
| **Desirability** | Customer interviews, surveys, landing page | Concierge MVP, pilot program |
| **Viability** | Pricing surveys, market research | Pre-sales, crowdfunding |
| **Feasibility** | Technical spikes, prototypes | POC with real data |
| **Usability** | Paper prototype tests | Clickable prototype tests |
| **Ethical** | Expert review, user interviews | Pilot with monitoring |

### Experiment Card Template

```text
┌─────────────────────────────────────────────────────────────────┐
│  EXPERIMENT: [Name]                                             │
├─────────────────────────────────────────────────────────────────┤
│  Assumption Being Tested:                                       │
│  [Link to assumption]                                           │
├─────────────────────────────────────────────────────────────────┤
│  Hypothesis:                                                    │
│  We believe [specific outcome] will happen because [reason].    │
├─────────────────────────────────────────────────────────────────┤
│  Experiment Method:                                             │
│  [Detailed description of what we'll do]                        │
├─────────────────────────────────────────────────────────────────┤
│  Metrics:                                                       │
│  • Success: [Threshold for validation]                          │
│  • Failure: [Threshold for invalidation]                        │
│  • Sample Size: [Number of data points needed]                  │
├─────────────────────────────────────────────────────────────────┤
│  Duration: [Time to run experiment]                             │
│  Cost: [Resources required]                                     │
├─────────────────────────────────────────────────────────────────┤
│  Result: □ Validated □ Invalidated □ Inconclusive               │
│  Evidence: [What we learned]                                    │
│  Next Step: [Decision based on result]                          │
└─────────────────────────────────────────────────────────────────┘
```

### Writing Falsifiable Hypotheses

**Good hypotheses are falsifiable** - you can definitively prove them wrong.

✅ **Falsifiable**:

- "At least 40% of interviewed developers will mention code review as a top-3 pain point"
- "5% of landing page visitors will click 'Request Demo'"
- "Users can complete onboarding in under 5 minutes"

❌ **Not Falsifiable**:

- "Users will like our product"
- "The market wants this"
- "It will be successful"

### Sample Size Guidelines

| Experiment Type | Minimum Sample | Ideal Sample |
|-----------------|----------------|--------------|
| Qualitative interviews | 5-8 | 12-15 |
| Usability tests | 5 | 8-12 |
| Landing page tests | 100 visitors | 1000+ visitors |
| Survey validation | 50 responses | 200+ responses |
| A/B tests | Depends on effect size | Use calculator |

## Common Experiment Patterns

### 1. Customer Problem Interviews

**Tests**: Desirability (problem exists)

**Method**:

1. Recruit 5-8 target users
2. Ask about past behavior (not future intent)
3. Explore specific recent experiences
4. Listen for pain intensity

**Success Signal**: 80%+ confirm problem exists and actively seek solutions
**Failure Signal**: <50% recognize the problem as significant

### 2. Landing Page Test

**Tests**: Desirability (solution interest)

**Method**:

1. Create simple landing page describing solution
2. Include clear CTA (signup, request demo, etc.)
3. Drive traffic via ads or direct outreach
4. Measure conversion rate

**Success Signal**: 5%+ conversion to waitlist
**Failure Signal**: <1% conversion after 200+ visitors

### 3. Fake Door Test

**Tests**: Desirability (feature interest)

**Method**:

1. Add button/link for non-existent feature
2. When clicked, show "coming soon" message
3. Offer to notify when available
4. Measure click rate and signup rate

**Success Signal**: 2%+ of users click, 30%+ of clickers signup
**Failure Signal**: <0.5% click rate

### 4. Concierge MVP

**Tests**: Desirability + Viability

**Method**:

1. Manually deliver the service
2. Charge real money (or time commitment)
3. Observe customer behavior
4. Gather feedback

**Success Signal**: Customers pay, return, and refer
**Failure Signal**: Customers churn quickly or won't pay

### 5. Wizard of Oz

**Tests**: Desirability + Usability

**Method**:

1. Create realistic front-end
2. Manually process behind the scenes
3. Users don't know it's manual
4. Measure engagement and satisfaction

**Success Signal**: Users complete tasks and express satisfaction
**Failure Signal**: Users confused or abandon workflow

### 6. Technical Spike

**Tests**: Feasibility

**Method**:

1. Time-box exploration (1-3 days)
2. Build smallest possible proof of concept
3. Document unknowns discovered
4. Assess technical risk

**Success Signal**: Core mechanism works, risks understood
**Failure Signal**: Fundamental blockers discovered

### 7. Pricing Survey

**Tests**: Viability

**Method**: Van Westendorp Price Sensitivity Meter

- At what price is this too cheap (suspect quality)?
- At what price is this a bargain?
- At what price is this getting expensive?
- At what price is this too expensive?

**Success Signal**: Acceptable price range aligns with business model
**Failure Signal**: Willingness to pay below cost

### 8. Expert Review

**Tests**: Ethical + Feasibility

**Method**:

1. Engage domain experts / ethicists
2. Present product concept
3. Structured review against principles
4. Document concerns

**Success Signal**: No critical concerns, minor issues addressable
**Failure Signal**: Fundamental ethical or regulatory issues

## Experiment Prioritization

### ICE Score

Rate each experiment 1-10 on:

- **I**mpact: How much risk reduction if we learn the answer?
- **C**onfidence: How confident are we in the experiment design?
- **E**ase: How easy/cheap is the experiment to run?

ICE Score = I × C × E ÷ 3

Prioritize highest ICE scores first.

### Learning vs. Validation

| Purpose | Approach | Sample Size | Rigor |
|---------|----------|-------------|-------|
| **Learning** | Exploratory, qualitative | Small (5-8) | Lower |
| **Validation** | Confirmatory, quantitative | Larger (50+) | Higher |

Start with learning experiments, then validate promising directions.

## Results Documentation

### After Each Experiment

Document:

1. **What we tested**: Assumption + hypothesis
2. **What we did**: Experiment method
3. **What we learned**: Results + insights
4. **What we decided**: Pivot, persevere, or more testing
5. **What's next**: Follow-up actions

### Assumption Board

Track all assumptions and their status:

| Assumption | Category | Risk | Status | Evidence | Decision |
|------------|----------|------|--------|----------|----------|
| Users have problem | D | High | Validated | 8/10 interviews | Proceed |
| Will pay $50/mo | V | High | Testing | Survey live | - |
| Can build in 4 weeks | F | Med | Validated | Spike done | Proceed |
| AI accuracy 90%+ | F | High | Invalidated | POC: 75% | Pivot |

## AI-Assisted Assumption Testing

### Assumption Identification

Given a product concept:

1. Generate comprehensive assumption list (DVFUE)
2. Categorize by type
3. Estimate risk and certainty
4. Prioritize for testing

### Experiment Design

For each risky assumption:

1. Suggest appropriate experiment types
2. Draft falsifiable hypothesis
3. Define success/failure criteria
4. Estimate effort and timeline

### Results Analysis

Given experiment data:

1. Assess against success criteria
2. Determine validation status
3. Identify follow-up questions
4. Recommend next steps

## Integration Points

**Inputs from**:

- `lean-startup` skill: Leap of faith assumptions
- `opportunity-mapping` skill: Solution assumptions
- `design-sprint` skill: Prototype test results

**Outputs to**:

- Product decisions: Build/don't build
- `lean-startup` skill: Pivot/persevere recommendations
- Engineering backlog: Validated features

## References

For additional Assumption Testing resources, see:
