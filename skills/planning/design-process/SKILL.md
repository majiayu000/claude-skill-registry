---
name: design-process
description: Engineering design cycle covering requirements elicitation, specifications writing, constraint identification, iterative prototyping, and design communication. Spans the full loop from problem definition through ideation, analysis, prototyping, testing, and redesign. Includes morphological charts, TRIZ, Pugh matrices, design reviews, and the distinction between functional and non-functional requirements. Use when framing engineering problems, generating design alternatives, writing specifications, or running design reviews.
type: skill
category: engineering
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/engineering/design-process/SKILL.md
superseded_by: null
---
# Engineering Design Process

Engineering is not invention by accident. It is the disciplined, iterative transformation of a human need into a working solution that satisfies constraints. The engineering design process is the backbone of every engineered artifact, from a bridge to a microprocessor. This skill covers the full design cycle with worked examples, decision tools, and integration with the college engineering concept graph.

**Agent affinity:** brunel (integrated design vision), polya-e (pedagogical scaffolding)

**Concept IDs:** engr-design-cycle, engr-problem-definition, engr-ideation-techniques, engr-design-communication

## The Design Cycle at a Glance

| Phase | Purpose | Key outputs |
|---|---|---|
| 1. Define | Identify the need, stakeholders, and success criteria | Problem statement, stakeholder map |
| 2. Research | Understand existing solutions, physics, regulations | Literature review, prior art, standards list |
| 3. Specify | Translate the need into measurable requirements | Requirements document, constraint matrix |
| 4. Ideate | Generate multiple design alternatives | Sketches, morphological chart, concept variants |
| 5. Analyze | Evaluate alternatives against requirements | Pugh matrix, trade study, feasibility assessment |
| 6. Prototype | Build a testable representation of the chosen design | Physical or digital prototype |
| 7. Test | Measure prototype performance against specifications | Test reports, data analysis |
| 8. Iterate | Refine the design based on test results | Updated design, revised specifications |
| 9. Communicate | Document and present the final design | Engineering drawings, specifications, reports |

The cycle is not linear. Phases 4 through 8 repeat until the design meets all requirements or the project constraints (budget, schedule) force a decision. The critical discipline is knowing when to iterate and when to converge.

## Phase 1 -- Define the Problem

A well-defined problem is half-solved. Engineering problem definition translates a vague need ("we need a better bridge") into a precise engineering problem statement with measurable criteria.

**Template.** Design a [system/component] that [primary function] for [stakeholders] subject to [key constraints], measured by [success criteria].

**Worked example.** *Design a pedestrian bridge that spans a 30-meter river crossing for a rural community subject to a $200K budget and 12-month timeline, measured by load capacity (minimum 500 kg/m), deflection limits (L/360), and 50-year design life.*

**Common mistake.** Jumping to solutions before defining the problem. "We need a suspension bridge" is a solution, not a problem statement. The problem statement must be solution-neutral to preserve the design space.

### Stakeholder Analysis

Every engineering project has stakeholders beyond the end user. A bridge serves pedestrians but must also satisfy regulators, maintenance crews, the funding authority, and adjacent property owners. Missing a stakeholder leads to requirements gaps that surface late, when they are expensive to fix.

Map stakeholders using: **Who uses it? Who pays for it? Who maintains it? Who regulates it? Who is affected by it?**

## Phase 2 -- Research

Before generating new designs, understand what exists. Research covers:

- **Prior art:** What solutions exist for similar problems? What worked and what failed?
- **Physics and materials:** What physical principles govern the problem domain?
- **Standards and codes:** What regulatory requirements constrain the design?
- **Failure history:** What engineering failures in this domain provide lessons?

Research is not optional. Skipping it leads to reinventing known solutions or, worse, repeating known failures. The Hyatt Regency walkway collapse (1981) resulted from a design change that no one analyzed against structural principles -- a failure of research and review, not of engineering knowledge.

## Phase 3 -- Specify Requirements

Requirements are the contract between the problem and the solution. They must be:

- **Measurable:** "Strong enough" is not a requirement. "Withstand 500 kg/m distributed load with deflection less than L/360" is.
- **Testable:** Every requirement must have a corresponding test. If you cannot test it, you cannot verify it.
- **Traceable:** Each requirement links back to a stakeholder need and forward to a design feature.
- **Prioritized:** Must-have (the design fails without it) vs. should-have (the design is degraded without it) vs. nice-to-have (improvement, not essential).

### Functional vs. Non-Functional Requirements

| Type | Definition | Example |
|---|---|---|
| Functional | What the system must do | "The bridge shall support pedestrian traffic in both directions simultaneously" |
| Non-functional | How well the system must do it | "The bridge shall have a design life of 50 years with annual maintenance cost below $5K" |

### Constraint Matrix

Constraints are non-negotiable boundaries. They differ from requirements in that they cannot be traded off -- they are binary pass/fail.

| Constraint type | Example |
|---|---|
| Physical | Maximum span: 30 meters (river width) |
| Regulatory | Must comply with AASHTO pedestrian bridge standards |
| Budget | Total project cost shall not exceed $200K |
| Schedule | Construction complete within 12 months |
| Environmental | No permanent in-water structures (fish habitat protection) |

## Phase 4 -- Ideate

Generate multiple design alternatives before committing to one. The goal is divergent thinking -- quantity of concepts, not quality.

### Brainstorming Rules

1. **No evaluation during ideation.** Criticism kills creativity. Evaluate later.
2. **Build on others' ideas.** "Yes, and..." not "No, but..."
3. **Encourage wild ideas.** They often contain seeds of practical solutions.
4. **Go for quantity.** More concepts increase the probability of finding a good one.

### Morphological Chart

A morphological chart decomposes the design into independent sub-functions and lists alternative solutions for each.

| Sub-function | Option A | Option B | Option C |
|---|---|---|---|
| Span structure | Beam | Arch | Cable-stayed |
| Deck material | Timber | Concrete | Steel grating |
| Foundation | Spread footing | Driven piles | Drilled shafts |
| Railing | Steel pipe | Cable | Timber |

Each combination of options is a candidate design. For 4 sub-functions with 3 options each, there are 81 possible combinations. The morphological chart makes the design space explicit and prevents premature convergence on a single concept.

### TRIZ

TRIZ (Theory of Inventive Problem Solving) is a systematic method for resolving design contradictions. When improving one parameter (strength) degrades another (weight), TRIZ provides 40 inventive principles for resolving the contradiction. Common principles include: segmentation, taking out, local quality, asymmetry, merging, universality, nesting, counterweight.

## Phase 5 -- Analyze and Select

Evaluate candidate designs against requirements using structured methods.

### Pugh Matrix (Controlled Convergence)

Select a baseline design (often the simplest or most conventional). Score each alternative relative to the baseline: better (+), same (S), or worse (-) on each criterion. Sum the scores. The design with the highest net score is the leading candidate.

| Criterion | Weight | Baseline | Concept A | Concept B |
|---|---|---|---|---|
| Load capacity | 5 | S | + | + |
| Cost | 4 | S | - | S |
| Constructability | 3 | S | S | + |
| Aesthetics | 2 | S | + | - |
| Maintenance | 3 | S | S | + |
| **Net score** | | **0** | **+1** | **+6** |

### Trade Study

For more rigorous evaluation, assign numerical scores (1-5 or 1-10) to each criterion for each alternative, multiply by weight, and sum. A trade study produces a defensible, documented selection rationale.

### Feasibility Assessment

Before detailed design, verify that the selected concept is physically, technically, economically, and schedule-feasible. Kill concepts early that cannot work, rather than investing months discovering infeasibility.

## Phase 6 -- Prototype

A prototype is a testable representation of the design. It need not be full-scale or full-fidelity. The purpose is to answer specific questions about the design's behavior.

### Prototype Fidelity Levels

| Level | Purpose | Example |
|---|---|---|
| Low fidelity | Test concept viability | Cardboard model of bridge shape |
| Medium fidelity | Test critical dimensions and interfaces | 3D-printed scale model with load testing |
| High fidelity | Test performance under realistic conditions | Full-scale section of bridge deck with instrumentation |

**Critical discipline.** Define what question the prototype answers before building it. A prototype without a test plan is a craft project, not engineering.

## Phase 7 -- Test

Testing verifies that the design meets its requirements. Every requirement from Phase 3 must have a corresponding test.

### Test Types

| Type | What it verifies | When used |
|---|---|---|
| Unit test | Individual component performance | After component fabrication |
| Integration test | Components work together | After assembly |
| System test | Complete system meets requirements | Before delivery |
| Acceptance test | Stakeholder agrees the system meets their need | At handover |

### Test Reports

A test report documents: test objective, test setup, procedure, raw data, analysis, pass/fail determination, and recommended actions. Test data without analysis is useless. Analysis without raw data is unverifiable.

## Phase 8 -- Iterate

If tests reveal deficiencies, return to the appropriate earlier phase. Minor issues may require only prototype refinement (Phase 6). Major issues may require revisiting requirements (Phase 3) or generating new concepts (Phase 4).

**When to stop iterating.** When all must-have requirements are met, should-have requirements are substantially met, and remaining improvements would exceed the project's budget or schedule constraints. Engineering is the art of making the best possible design within constraints, not the pursuit of perfection.

## Phase 9 -- Communicate

Engineering work that cannot be communicated is engineering work that does not exist. The final design must be documented in sufficient detail that someone else can build, maintain, and eventually retire it.

### Communication Artifacts

- **Engineering drawings:** Dimensioned, toleranced, to standard (ASME Y14.5 for mechanical, relevant standards for other disciplines)
- **Specifications:** Written requirements with acceptance criteria
- **Analysis reports:** Calculations showing the design meets requirements
- **Test reports:** Evidence that the built design meets specifications
- **Operations and maintenance manual:** How to use and maintain the system
- **Design rationale:** Why this design was chosen over alternatives

## Design Reviews

Formal design reviews are checkpoints where the design team presents work to reviewers (peers, management, customer, or an independent review board). Common review gates:

| Review | Timing | Purpose |
|---|---|---|
| System Requirements Review (SRR) | After Phase 3 | Confirm requirements are complete and correct |
| Preliminary Design Review (PDR) | After Phase 5 | Confirm the selected concept meets requirements |
| Critical Design Review (CDR) | After detailed design | Confirm the design is ready for fabrication/construction |
| Test Readiness Review (TRR) | Before Phase 7 | Confirm test plans and facilities are ready |
| Design Certification Review (DCR) | After Phase 7 | Confirm test results support design certification |

Reviews catch errors early, when they are cheap to fix. The cost of fixing an error increases roughly 10x at each subsequent phase.

## Cross-References

- **brunel agent:** Integrated design vision and design review leadership. Primary agent for full-cycle design problems.
- **roebling agent:** Structural aspects of the design cycle, particularly for civil and structural engineering problems.
- **polya-e agent:** Pedagogical scaffolding for learning the design process. "How to Solve It" adapted for engineering.
- **structural-analysis skill:** Deep dive into Phase 5 analysis for structural designs.
- **systems-engineering skill:** V-model, requirements management, and verification/validation as applied to complex systems.
- **prototyping-fabrication skill:** Phase 6 in depth -- materials, tools, and methods.
- **engineering-ethics skill:** Ethical dimensions of design decisions, especially at review gates.
- **technical-communication skill:** Phase 9 in depth -- writing, drawing, and presenting.

## References

- Pahl, G., Beitz, W., Feldhusen, J., & Grote, K.-H. (2007). *Engineering Design: A Systematic Approach*. 3rd edition. Springer.
- Dieter, G. E., & Schmidt, L. C. (2012). *Engineering Design*. 5th edition. McGraw-Hill.
- Dym, C. L., & Little, P. (2009). *Engineering Design: A Project-Based Introduction*. 3rd edition. Wiley.
- NASA. (2020). *NASA Systems Engineering Handbook*. SP-2016-6105 Rev 2. National Aeronautics and Space Administration.
- Altshuller, G. (1999). *The Innovation Algorithm: TRIZ, Systematic Innovation and Technical Creativity*. Technical Innovation Center.
- Cross, N. (2021). *Engineering Design Methods: Strategies for Product Design*. 5th edition. Wiley.
