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
- **Hypothesis** (Gothelf Lean UX format):
  "We believe that [doing this/building this feature] for [these people] will achieve [this outcome]. We will know we are right when we see [this measurable signal]."
  The fourth clause ("we will know when") is critical — it defines success criteria upfront.
  *Source: Gothelf & Seiden, Lean UX (2013, 3rd ed. 2021). The 4-part format evolved across editions.*
- **Method**: Which test type and how
- **Success looks like**: Specific, measurable outcome (e.g., ">60% of survey respondents say X")
- **Failure looks like**: What would make us abandon this assumption
- **Sample size**: How many data points needed for confidence

## Step 5: State Your Prediction (before running)

Before running the test, write down what you **expect** will happen and why. This forces scientific thinking — if you can't state a prediction, you don't understand the assumption well enough to test it.

- **I expect**: [specific outcome, e.g., "4 of 6 users will complete onboarding in under 5 minutes"]
- **Because**: [reasoning, e.g., "the flow has only 3 steps and uses familiar patterns"]
- **I'd be surprised if**: [what would challenge your mental model]

After running, compare prediction to reality. The gap between prediction and outcome IS the learning.

*Source: Rother (Toyota Kata) — stating predictions before experiments is the core scientific thinking habit.*

## Step 6: Run and Interpret

- Run the test
- Compare results to your prediction from Step 5 — note where reality differed
- Record raw results
- Update confidence level (Gilad's meter: 0.1 -> 0.9)
- Update ICE score for the solution
- If assumption validated: move to next riskiest assumption. **Update confidence** in the relevant canvas entry (opportunities.yml, diamonds/active.yml) to reflect the validated assumption — typically +0.1 to +0.15.
- If assumption invalidated: pivot the solution or explore alternatives. **Decrease confidence** by 0.1-0.2 to reflect the failed assumption.
- Log in canvas/opportunities.yml under the solution's experiments
- **Always update diamonds/active.yml** confidence to match the test outcome

## Bias Warning

Before interpreting results, run `/bias-check`:
- Confirmation bias: Are you seeing what you want to see?
- Small sample: Is n large enough to be meaningful?
- Selection bias: Did you test with representative users?
