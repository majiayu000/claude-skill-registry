---
name: gist-plan
description: "GIST planning workflow. Structure goals into ideas, steps, and tasks using Gilad's evidence-guided framework."
instruction_budget: 32
---

# GIST Planning

Replace opinion-based roadmaps with evidence-guided planning. Source: Gilad (Evidence Guided).

## Workflow

### 1. Set Goals (Quarterly)
- Derive from North Star input metrics or OKRs
- Format: "Improve [metric] from [current] to [target] by [date]"
- Maximum 3 goals per quarter
- Update canvas/gist.yml goals section

### 2. Generate Ideas (Ongoing)
- Ideas are hypothetical ways to achieve goals
- Most ideas fail (>80%) -- this is expected and planned for
- Generate many, hold loosely
- Store in canvas/gist.yml idea bank with ICE scores
- Never commit to an idea until evidence supports it

### 3. Score with ICE + Confidence Meter
Use `/ice-score` to prioritize. ICE scoring (Ellis; confidence dimension added by Gilad):
- Confidence is NOT gut feel -- it maps to evidence levels
- 0.1 = opinion only | 0.5 = data supports | 0.7 = tested | 0.9 = launched
- Rescore after every experiment
> *Mycelium uses 0.0-1.0 (adapted from Gilad's 0-10 non-linear Confidence Meter). See `/ice-score` for details.*

### 4. Design Steps (per top idea)
- Steps are small, time-boxed activities that build evidence
- Each step has: hypothesis, method, success criteria, **MoSCoW priority**
- Tag each step as **Must** / **Should** / **Could** / **Won't** (DSDM):
  - **Must**: Non-negotiable. Delivery fails without this. All REVIEW checks apply.
  - **Should**: Important. Ship if time allows. All REVIEW checks apply.
  - **Could**: Nice-to-have. Cut first when timebox runs out. NUDGE checks only.
  - **Won't**: Explicitly out of scope for this cycle. Documented for future reference.
- Steps follow a confidence ladder: assessment -> exploratory experiment -> feature experiment -> launch
- Each step produces evidence that increases or decreases confidence
- If evidence is negative: pivot or kill the idea (sunk cost is irrelevant)
- For user-facing ideas, frame hypotheses in Lean UX format: "We believe [outcome] for [users] if [change]." (Gothelf)
- **When a delivery timebox is exceeded**: Flex scope using MoSCoW — cut Could/Won't before compromising Must/Should

### 5. Execute Tasks (Sprint-level)
- Tasks belong to the CURRENT step only
- Don't plan tasks for future steps
- Standard agile execution

### 6. Reprioritize (Continuous)
After each step completes:
- Update ICE scores based on new evidence
- Re-rank ideas
- Kill ideas below threshold
- Surface new ideas from discovery work

### Shape Up: Appetite Over Estimates
Instead of asking "how long will this take?", ask "how much is this worth?" (Shape Up by Basecamp). Set an **appetite** — the maximum time you're willing to invest — then design the solution to fit within it. If the solution can't fit, narrow the scope, don't extend the timebox. This connects naturally to MoSCoW: appetite defines the timebox, MoSCoW decides what fits within it.

## Anti-Pattern: The Feature Roadmap
If your GIST board looks like a feature list with dates, you're doing it wrong. Goals are outcomes, ideas are hypotheses, steps are experiments.
