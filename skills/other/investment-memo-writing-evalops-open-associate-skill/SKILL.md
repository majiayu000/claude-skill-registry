---
name: investment-memo-writing
description: "Write an investment memo that forces a decision: explicit recommendation (no hedging), steelman against, decision log, and next steps. Use when preparing for IC or partner discussion."
license: Proprietary
compatibility: Works offline; improved with web comps and diligence evidence; optional Salesforce logging.
metadata:
  author: evalops
  version: "0.2"
---
# Investment memo writing

## When to use
Use this skill when:
- You need to brief partners / IC with a decision-ready document
- You have diligence evidence and need to turn it into a recommendation
- You want to reduce "vibes" and increase clarity

## Inputs you should request (only if missing)
- Company deck + diligence notes
- Round terms (or what's known so far)
- Firm constraints (ownership target, stage, geography)
- Comparable comps / pricing benchmarks if available

## Output you must produce
A memo that:
- **Opens with a clear recommendation in the first line (no hedging)**
- States the best argument AGAINST the deal (steelman)
- Includes a decision log (what changed since first call, and why)
- Names top risks (max 4, ranked) and evidence for each
- Proposes decision + next steps with dates

Templates:
- assets/memo-template.md
- assets/outcome-framing.md

## Writing rules
- **First line = recommendation.** "Recommend: Lead at $X" or "Recommend: Pass because Y". No "it depends."
- Adjectives are a tax. Replace them with evidence.
- **The best argument against the deal is mandatory.** Steelman it.
- If it's important, quantify it or show a proxy.
- Keep TL;DR to 5 bullets max.
- Include a decision log: what you believed at first call, what changed, why.

## Memo structure (required sections)

### 1) Recommendation (FIRST LINE, NO HEDGING)
- "Recommend: Lead $Xm at $Ym pre for Z% ownership"
- or "Recommend: Follow with $Xm"
- or "Recommend: Pass"
- One sentence. No "lean towards" or "potentially interested."

### 2) Best argument against (MANDATORY STEELMAN)
- In 3-5 sentences, make the strongest case for why this deal fails.
- This is not "risks" - it's the single most compelling reason a smart investor would pass.
- Write it as if you were advising a competitor fund to say no.

### 3) TL;DR (5 bullets max)
- 
- 
- 
- 
- 

### 4) Decision log (what changed since first call)
| Date | Belief | Evidence | Change |
|---|---|---|---|
| First call | | | Initial thesis |
| [Date] | | | Updated because... |
| [Date] | | | Updated because... |
| Today | | | Current view |

### 5) Why now + wedge

### 6) Market (buyer, budget, trigger, adoption timing)

### 7) Product (10x, hard to copy, deployment reality)

### 8) Traction (the 2-3 metrics that matter)

### 9) GTM (motion, cycle time, pricing, margin)

### 10) Competition + moat

### 11) Team (learning rate, decision rights, gaps)

### 12) Must be true (3-5 falsifiable claims)
For each claim:
- The claim
- Evidence today
- What would falsify it

### 13) Risks (MAX 4, ranked)
For each risk:
- The risk
- Evidence collected
- Mitigation / what we learned
- Residual concern

### 14) Deal + terms + ownership target

### 15) Next steps + decision date

### Appendix
- Customer quotes (especially anti-confirmation evidence)
- Diligence notes
- Competitor analysis

## Anti-confirmation section (required in appendix)
Every memo must document:
- **Churned customer / lost deal call:** What did we learn? What would have changed the outcome?
- **Competitor / alternative user call:** Why do they use something else? What would switch them?
- If these calls didn't happen, explain why and flag the gap prominently.

## Salesforce logging (recommended)
- Attach the memo as a File/Note to the Opportunity.
- Update Opportunity fields: stage, amount (if relevant), close date, next step.
- Record key "must be true" claims in a structured field if you have one; otherwise in Notes.

Use `salesforce-crm-ops` if you need API patterns.

## Edge cases
- If terms are unknown: write the memo "pending terms" and explicitly state what term ranges would change your recommendation.
- If evidence is thin: say so. Propose the smallest next diligence step that would change the decision.
- If you can't make a clear recommendation: you're not done diligencing. Go back and get the evidence you need.
