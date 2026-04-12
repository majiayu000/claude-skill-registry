---
name: assumption-test
description: "Design the smallest viable test to validate or invalidate a critical assumption. Based on Torres's assumption testing framework."
---

# Assumption Testing

Every solution rests on assumptions. Test the riskiest ones first with the lightest method possible.

## Assumption Types (Torres / Cagan)

| Type | Question | Example |
|------|----------|---------|
| **Desirability** | Will users want this? | "Users will switch from current tool" |
| **Usability** | Can users figure it out? | "Users can complete onboarding in < 5 min" |
| **Feasibility** | Can we build this? | "We can process 10K requests/sec" |
| **Viability** | Should we build this? | "Unit economics work at scale" |
| **Ethical** | Should we build this? (morally) | "This doesn't exploit user vulnerabilities" |

## Step 1: Map Assumptions

For the target solution, list ALL assumptions. Be honest -- most "obvious" things are actually assumptions.

## Step 2: Prioritize (2x2 Matrix)

Plot each assumption on:
- X-axis: How much evidence do we have? (low to high)
- Y-axis: How important is this to the solution's success? (low to high)

**Test first**: High importance + Low evidence (top-left quadrant)

## Step 3: Choose the Lightest Test

| Test Type | Effort | Signal Quality | When to Use |
|-----------|--------|---------------|-------------|
| **Data mining** | Hours | Variable | You have existing behavioral data |
| **One-question survey** | Hours | Low-Medium | Quick pulse on a specific question |
| **Smoke/fake door test** | Days | Medium | Test demand before building |
| **Concierge test** | Days | High | Manually deliver the service |
| **Wizard of Oz** | Days | High | Fake the backend, real frontend |
| **Prototype test** | 1-2 weeks | High | Test usability with interactive mockup |
| **A/B test** | 2+ weeks | Very High | Test with real users at scale |

**Rule**: Always pick the LIGHTEST test that produces meaningful signal. Don't build a prototype when a survey would suffice.

## Step 4: Define Success Criteria

Before running the test, write:
- **Hypothesis** (Lean UX format, preferred for desirability/usability):
  "We believe [outcome] will be achieved for [users] if they successfully [change/action]."
  For feasibility/viability: "We believe [assumption] because [rationale]."
- **Method**: Which test type and how
- **Success looks like**: Specific, measurable outcome (e.g., ">60% of survey respondents say X")
- **Failure looks like**: What would make us abandon this assumption
- **Sample size**: How many data points needed for confidence

## Step 5: Run and Interpret

- Run the test
- Record raw results
- Update confidence level (Gilad's meter: 0.1 -> 0.9)
- Update ICE score for the solution
- If assumption validated: move to next riskiest assumption
- If assumption invalidated: pivot the solution or explore alternatives
- Log in canvas/opportunities.yml under the solution's experiments

## Bias Warning

Before interpreting results, run `/bias-check`:
- Confirmation bias: Are you seeing what you want to see?
- Small sample: Is n large enough to be meaningful?
- Selection bias: Did you test with representative users?
