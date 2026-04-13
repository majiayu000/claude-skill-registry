---
name: ost-builder
description: "Use to build or update an Opportunity Solution Tree from research data. Never from brainstorming."
---

# OST Builder Skill

Build and maintain Opportunity Solution Trees from research evidence.

## Workflow

### Building a New OST

1. **Define the desired outcome** at the top of the tree. This comes from the north star metric or current strategic goal.

2. **Review all research data**: Interview transcripts, behavioral data, analytics, observation notes.

3. **Extract opportunities** (unmet needs, pain points, desires):
   - Each opportunity must cite at least 2 evidence sources.
   - Phrase as user needs, not solutions: "Users need to know their payment succeeded" not "Users need a confirmation email."
   - Look for frequency across interviews, not just intensity in one.

4. **Structure hierarchically**: Group related opportunities. Identify parent-child relationships.
   - Before structuring, ensure each opportunity has been examined from **all three trio perspectives** (product, design, engineering). Product lens sees user value; design lens sees experience gaps; engineering lens sees technical constraints or enablers.
   - Classify each opportunity's **Cynefin domain** (clear/complicated/complex). Complex-domain opportunities must produce probes (experiments), not fully-designed solutions. See `engine/cynefin-routing.md`.

5. **For each leaf opportunity**, generate solution ideas:
   - Multiple solutions per opportunity.
   - Solutions can be simple experiments, not just features.
   - Include "do nothing" as an option when appropriate.

6. **For each solution leaf**, assess the Four Risks (Torres Product Trio):
   - **Value** (product lens): Is there evidence users want/need this?
   - **Usability** (design lens): Can users figure out how to use it?
   - **Feasibility** (engineering lens): Can we build it within constraints?
   - **Viability** (cross-cutting): Does it align with business/legal/ethical?
   Each risk must have its own evidence — a combined statement fails.
   Write `four_risks` per solution in `canvas/opportunities.yml`.

7. **For each solution**, identify riskiest assumptions from the Four Risks:
   - Which risk dimension has the least evidence?
   - What is the cheapest way to test that assumption?
   - Tag each assumption with its `risk_dimension` (value|usability|feasibility|viability).

### Updating an Existing OST

1. Review new research data since last update.
2. Add new opportunities with evidence citations.
3. Refine or remove opportunities that evidence no longer supports.
4. Add new solutions for validated opportunities.
5. Update confidence scores based on new evidence.
6. Prune solutions that have been invalidated.

## Rules

- Never add opportunities without evidence citations.
- Never brainstorm opportunities. Discover them.
- Every opportunity must link to at least 2 research data points.
- Solutions come after opportunities are understood, not before.
- The OST is a living document. Update weekly with new research.

## Canvas Output

**Always update `canvas/opportunities.yml`** with the OST contents after building or updating. This is the single source of truth for the opportunity space.

Also update:
- `canvas/user-needs.yml` if new needs were identified
- `canvas/jobs-to-be-done.yml` if JTBD dimensions surfaced during mapping

## Lean UX Connection

When generating solution ideas for leaf opportunities, frame each as a Lean UX hypothesis:
"We believe [outcome] for [users] if [change]." This makes the solution testable via `/assumption-test`.
Flow: Opportunity (research) -> Solution hypothesis (Lean UX) -> Assumption test (smallest viable test).

## Theory Citations
- Torres: Continuous Discovery Habits (OST methodology)
- Christensen: Competing Against Luck (JTBD informing opportunities)
- Gilad: Evidence Guided (ICE scoring for solutions)
- Gothelf: Lean UX (hypothesis-driven solution framing)
