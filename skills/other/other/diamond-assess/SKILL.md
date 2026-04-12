---
name: diamond-assess
description: "Use to evaluate the current state of a diamond. Checks theory gates, confidence levels, and recommends next action."
---

# Diamond Assess Skill

Evaluate current diamond state and recommend next action.

## Workflow

1. **Identify the diamond**: Which diamond (ID, scale, phase) is being assessed?

2. **Gather current state**:
   - Current phase (Discover/Define/Develop/Deliver)
   - Evidence collected so far
   - Confidence score with breakdown
   - Blockers or risks

3. **Check theory gates for next transition**:
   - Reference theory-gates.md for the current transition
   - Check `product_type` from `diamonds/active.yml` -- gates conditioned on product_type include:
     - **Security Gate**: full OWASP for software/ai_tool; platform-only for content; infra-only for service
     - **Delivery Metrics Gate**: routes to product-type-appropriate metrics canvas
     - **Service Quality Gate**: Downe applies to consumption experience for all product types; Nielsen only for digital interfaces
   - Evaluate each applicable gate: Pass / Fail / Insufficient Evidence / N/A (if gate doesn't apply to this product_type)
   - Document what is missing for failed gates

4. **Check confidence threshold**:
   - Reference confidence-thresholds.yml for the current scale
   - Apply `project_type_adaptations` to compute effective threshold (see confidence-thresholds.yml)
   - Compare current confidence to the **effective** threshold
   - Identify what would increase confidence

5. **Check for anti-patterns**:
   - Reference anti-patterns.md
   - Flag any detected failure modes
   - For L1/L2 diamonds: also check for **system archetypes** (Senge) — Fixes That Fail, Shifting the Burden, Limits to Growth, Eroding Goals
   - At L3->L4 transitions: also run the **Design Completeness Check** (quality/CLAUDE.md) to verify all layers of the product design stack have evidence. Source: Mill, building on Garrett.

6. **Check corrections.md**:
   - Any relevant past mistakes to avoid?

7. **Recommend next action**:
   - If all gates pass and confidence meets threshold: recommend transition to next phase
   - If gates fail: recommend specific actions to address failures
   - If confidence is low: recommend evidence-gathering activities
   - If anti-patterns detected: recommend corrective actions
   - If regression needed: recommend which phase to return to and why

8. **Play devil's advocate**: Before recommending progression, ask:
   - What are we most likely wrong about?
   - What evidence have we dismissed?
   - Is there a simpler path we're overlooking?

## Output Format

**ALWAYS output in plain language first, then technical details.**
Use `.claude/engine/status-translations.md` for translations.

```
## Where We Are

Current focus: [plain-language description from status-translations.md]
  [1-2 sentences of context]
  Confidence: [plain word] ([number], [Gilad level]) -- [why this level, what would increase it]

## Progress

[N] of [M] diamonds complete:
  [Name]: [STATUS] -- [plain-language one-liner]
  [Name]: [STATUS] -- [plain-language one-liner]

## Theory Gate Check (for next transition)

| Gate | Status | Suggested Skill |
|------|--------|----------------|
| Evidence | Pass/Fail | /user-interview or /assumption-test |
| Four Risks | Pass/Fail | /assumption-test |
| ... | ... | ... |

## What I'd Challenge (Devil's Advocate)
- [Key assumption to question]
- [Evidence gap to flag]

## Recommended Next Step
[Plain-language recommendation with theory justification]

Suggested actions:
  - /skill-name -- [why this is relevant now]
  - /skill-name -- [why this is relevant now]
```

## Theory Citations
- Torres: Evidence-based progression
- Gilad: Confidence scoring with contextual explanation
- Cagan: Four risks assessment
- Snowden: Cynefin classification
- Shotton/Kahneman: Devil's advocate bias check
