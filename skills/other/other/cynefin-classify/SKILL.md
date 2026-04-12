---
name: cynefin-classify
description: "Use when facing a new problem to classify its domain (Clear, Complicated, Complex, Chaotic, Disorder) and select appropriate methods."
---

# Cynefin Classify Skill

Classify problem domain and route to appropriate methods.

## Workflow

1. **Describe the problem** in neutral terms.

2. **Ask diagnostic questions**:
   - Can we predict the outcome of actions? (Yes=Clear/Complicated, No=Complex/Chaotic)
   - Do experts agree on the approach? (Yes=Clear, Somewhat=Complicated, No=Complex)
   - Is the situation stable? (Yes=Clear/Complicated/Complex, No=Chaotic)
   - Has this been solved before? (Yes=Clear, Similar=Complicated, No=Complex)

3. **Classify** into one of five domains using cynefin-routing.md.

4. **Select methods** appropriate to the domain:
   - Clear: Best practice, checklists, automation
   - Complicated: Expert analysis, options evaluation, technical spikes
   - Complex: Safe-to-fail probes, experiments, continuous discovery
   - Chaotic: Stabilize, act, then reassess
   - Disorder: Decompose into classifiable parts

5. **Cross-reference with Wardley evolution** if strategic context is available.

6. **Output**:
   ```
   ## Cynefin Classification
   Problem: [description]
   Domain: [Clear/Complicated/Complex/Chaotic/Disorder]
   Confidence: [High/Medium/Low]

   Rationale: [why this classification]

   Recommended methods:
   - [method 1]
   - [method 2]

   Warning signs of misclassification:
   - [what would indicate we got it wrong]
   ```

## Canvas Output
Update `.claude/diamonds/active.yml` with the `cynefin_domain` field for the relevant diamond.
If Wardley mapping was referenced, update `.claude/canvas/landscape.yml` component evolution stages.

## Theory Citations
- Snowden: Cynefin framework
- Wardley: Evolution mapping
