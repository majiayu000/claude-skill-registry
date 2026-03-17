---
name: discover-opportunities
description: Use after outcomes are defined to discover opportunities, unmet needs, market gaps, or JTBD insights before choosing solutions.
---

# Discover Opportunities

## Overview
Find real opportunities by reasoning from first principles and Jobs-To-Be-Done (JTBD). Focus on the user's job, context, and constraints before any solution ideas.

## Position in Workflow

Step 2 of product strategy workflow:
1. `/discover-outcomes` - Define outcomes
2. `/discover-opportunities` - Identify opportunities (THIS)
3. `/ideate-solutions` - Explore solution concepts
4. `/discover-assumptions` - Validate with experiments

## Inputs (ask if missing, max 5)
- Target user / segment
- Trigger and context (when the job arises)
- Desired outcomes (time, money, risk, effort, emotion)
- Current alternatives / workarounds
- Non-negotiable constraints (budget, regulation, tech, org)

## Workflow
1. **Frame the jobs**
   - Define the core job as verb + outcome (not a solution).
   - Include functional, emotional, and social jobs.
   - Map the job journey: before / during / after.
2. **First-principles check**
   - Identify root frictions (physics, economics, human limits).
   - Separate real constraints from assumed constraints.
3. **Generate opportunities**
   - Produce 5-10 opportunity statements using the template below.
   - For each, note frequency, severity, and current workaround.
4. **Score and rank**
   - Score 0-3: impact, urgency/frequency, underservedness, feasibility/leverage, willingness to pay.
   - Rank top 3-5.
5. **Output and validation**
   - Present top opportunities with short rationale.
   - List key assumptions and missing evidence.
   - Suggest fastest validation tests (interviews, data checks, lightweight prototypes).

## Opportunity Statement Template
```
Help [segment] achieve [job outcome] by reducing [specific friction] in [context].
```

## Output Format
```
## Opportunity Discovery

### Context Summary
[1-3 sentences]

### JTBD Map
- Functional: ...
- Emotional: ...
- Social: ...
- Journey: before / during / after

### Opportunities (ranked)
1) [Statement]
   - Scores: impact X, urgency X, underservedness X, feasibility X, WTP X
   - Evidence: frequency, severity, workaround
   - Rationale: ...

### Assumptions / Gaps
- ...

### Fast Validation Tests
- ...

### Next Step
Proceed to solution ideation. Run `/ideate-solutions`.
```

## Quick Reference
- **No solutions** until opportunities are listed.
- Use concrete outcomes and observable behaviors.
- Always include alternatives and workarounds.

## Common Mistakes
- Jumping to features instead of jobs
- Vague outcomes ("better UX")
- Ignoring current alternatives
- Mixing constraints with assumptions
- Too few opportunities (aim for 5-10)

## Example
**Input:** "Independent designers need to invoice clients. They use spreadsheets and email, but late payments are common. They want faster payment and less admin. Budget is low."

**Opportunity statement:**
Help independent designers get paid faster by reducing follow-up overhead when invoices go overdue in client email workflows.
