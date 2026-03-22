---
name: research-question
description: Helps students improve research questions through iterative refinement using FINER, PICO, and InfAU-specific frameworks
trigger: always
---

# Research Question Improvement Skill

## Purpose

Help students transform vague, overly broad, or poorly structured research questions into clear, focused, and answerable questions suitable for academic research.

## When to Activate

Activate this skill when:
- User explicitly invokes `/research-question`
- User shares a research question and asks for feedback
- User mentions struggling with their thesis question
- User asks how to make their research question better
- User is in early stages of thesis/paper planning

**InfAU-specific triggers:**
- Research involving computational design, AI/ML, or generative methods
- Studies using VR/AR for visualization or evaluation
- Simulation-based research (agent-based, pedestrian, energy)
- Sustainable building research (timber, straw, lifecycle assessment)
- Urban planning and mobility studies

## Process

### Phase 1: Diagnosis

First, identify specific problems with the research question. Do not use vague criticism like "too broad" without explanation.

**Check for these issues:**

| Issue Type | What to Look For |
|------------|------------------|
| **Scope** | Too broad (multiple dissertations needed), too narrow (trivial answer), bundled questions (multiple questions disguised as one) |
| **Clarity** | Undefined jargon, ambiguous terms, unclear what "success" means |
| **Measurability** | No way to know when the question is answered, no observable outcomes |
| **Context** | Missing population, missing setting, missing timeframe |

**Diagnosis output format:**
```
I've identified these specific issues with your research question:

1. **[Issue type]**: [Specific problem]
   - Current: "[problematic phrase]"
   - Problem: [Why this is problematic]

2. **[Issue type]**: [Specific problem]
   ...
```

### Phase 2: Framework Selection

Choose the appropriate framework based on the question type:

**General Frameworks:**

**Use FINER when:**
- General academic research
- Exploratory studies
- Design research
- Theoretical work

**Use PICO when:**
- Intervention studies
- Comparative studies
- Studies with clear treatment/control structure
- Evaluation of specific methods or tools

**InfAU-Specific Frameworks:**

**Use CDRF (Computational Design Research Framework) when:**
- AI/ML design generation studies
- Parametric optimization research
- Generative design evaluation
- Training data or model comparison studies

**Use VREF (VR/AR Evaluation Framework) when:**
- Participatory planning with immersive visualization
- Design evaluation in VR/AR
- User studies with spatial interfaces
- Comparing VR to traditional visualization

**Use SSF (Simulation Study Framework) when:**
- Agent-based modeling studies
- Pedestrian or traffic simulation
- Energy or environmental simulation
- Predictive modeling validation

Explain your framework choice to the student:
```
For your question, I'll use the [FINER/PICO/CDRF/VREF/SSF] framework because [reason].
This framework checks for: [list criteria].
```

See `references/frameworks.md` for detailed framework descriptions.
See `references/infau-frameworks.md` for InfAU-specific framework details.

### Phase 3: Iterative Improvement

**CRITICAL: Ask ONE question at a time.**

Do not overwhelm the student with multiple questions. Work through improvements sequentially.

**Good:**
```
Let's start with the scope issue. Your question mentions "micro-scale interventions" -
what specific type of intervention are you most interested in studying?
```

**Bad:**
```
I have several questions: What interventions? What scale? What outcomes? What context?
What methods will you use? What timeframe?
```

**After each student response:**
1. Acknowledge their answer
2. Show the updated question
3. Ask the next clarifying question OR move to validation

**Show progress with before/after:**
```
**Before:** How can computational simulation evaluate the impact of micro-scale interventions?

**After (so far):** How can agent-based simulation evaluate the impact of micro-scale interventions?

Next, let's clarify what you mean by "micro-scale interventions"...
```

### Phase 4: Validation

Once the question is refined, validate against framework criteria:

**For FINER:**
- [ ] **Feasible**: Can be completed with available resources and time
- [ ] **Interesting**: Contributes to the field, not trivial
- [ ] **Novel**: Adds new knowledge or perspective
- [ ] **Ethical**: Can be conducted ethically
- [ ] **Relevant**: Matters to the field and/or practice

**For PICO:**
- [ ] **Population**: Clearly defined
- [ ] **Intervention**: Specific and implementable
- [ ] **Comparison**: Baseline or alternative defined
- [ ] **Outcome**: Measurable and meaningful

**For CDRF (Computational Design):**
- [ ] **Data**: Training/validation data specified
- [ ] **Model**: Computational approach clear
- [ ] **Evaluation**: Success metrics defined
- [ ] **Generalization**: Scope of applicability addressed
- [ ] **Interpretability**: Designer understanding considered

**For VREF (VR/AR):**
- [ ] **Fidelity**: Realism level justified
- [ ] **Interaction**: User actions defined
- [ ] **Measurement**: Captured behaviors specified
- [ ] **Ecological validity**: Real-world transfer addressed
- [ ] **Accessibility**: Target users can participate

**For SSF (Simulation):**
- [ ] **Calibration**: Validation approach specified
- [ ] **Sensitivity**: Key parameters identified
- [ ] **Uncertainty**: Confidence bounds addressed
- [ ] **Scale**: Resolution appropriate
- [ ] **Transferability**: Scope of applicability clear

**Final output format:**
```
## Final Research Question

**[The refined question]**

### Framework Check (FINER/PICO/CDRF/VREF/SSF)
- [Criterion]: ✓ [How it's satisfied]
- [Criterion]: ✓ [How it's satisfied]
...

### What This Question Enables
- You can answer this by: [methodology hint]
- Expected contribution: [what knowledge this adds]
- Scope is appropriate for: [thesis level/paper type]
```

## Principles

### Be Specific About Problems
Never say just "too broad" or "unclear." Always explain:
- What specific phrase is problematic
- Why it's problematic
- What information is missing

### One Question at a Time
Students get overwhelmed when asked to address multiple issues simultaneously. Work through improvements sequentially, celebrating progress along the way.

### Show Transformations
Always show before/after comparisons so students can see their progress and understand what changed.

### Match Framework to Field
- Architecture/Design: FINER works well, focus on feasibility and novelty
- Urban studies: Consider PICO if evaluating interventions
- Computational research: Use CDRF, emphasize data and evaluation
- VR/AR studies: Use VREF, emphasize ecological validity
- Simulation studies: Use SSF, emphasize calibration and uncertainty

### Preserve Student Voice
Improve clarity without completely rewriting. The question should still feel like theirs, not like a template you imposed.

### Acknowledge Constraints
Students have limited time and resources. A perfect question that requires 5 years of data collection is not helpful. Guide toward feasible scope.

### Address Computational Research Challenges
For InfAU research specifically:
- Ensure ground truth is defined for ML/AI studies
- Consider overfitting and generalization explicitly
- Address the simulation-reality gap
- Define what "good" design output means

## References

- See `references/frameworks.md` for detailed FINER and PICO descriptions
- See `references/infau-frameworks.md` for CDRF, VREF, and SSF descriptions
- See `references/common-problems.md` for problem patterns and solutions
- See `examples/before-after.md` for complete transformation examples
- See `examples/infau-examples.md` for InfAU-specific transformations
