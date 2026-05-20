---
name: design-thinking
description: The technology design process from needs assessment through iteration, covering empathy mapping, design briefs, concept development, prototyping, user testing, and iterative refinement. Integrates design thinking methodology (Stanford d.school) with engineering design process (ITEEA) and Don Norman's human-centered design principles. Use when designing technology solutions, evaluating existing designs, running design sprints, or teaching the design cycle. Distinct from art/aesthetics -- this skill focuses on functional design that solves real problems for real people.
type: skill
category: technology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/technology/design-thinking/SKILL.md
superseded_by: null
---
# Design Thinking

Design thinking is a structured approach to solving problems by understanding people, challenging assumptions, redefining problems, and creating solutions to prototype and test. It is not a linear process but a set of overlapping phases that designers move between as understanding deepens. This skill covers the full design cycle from empathy through iteration, grounded in both the Stanford d.school framework and the ITEEA engineering design process.

**Agent affinity:** norman (human-centered design, affordances, usability), berners-lee (information architecture, systems design), resnick (creative learning, low floors/wide walls)

**Concept IDs:** tech-design-brief, tech-concept-development, tech-prototyping-testing-tech, tech-design-iteration

## The Design Cycle

### Phase 1 -- Empathize

Before designing anything, understand who you are designing for and what they actually need (which may differ from what they say they want).

**Methods:**
- **Observation:** Watch people use existing solutions. Note workarounds, frustrations, and moments of delight.
- **Interviews:** Ask open-ended questions. "Tell me about the last time you..." is more revealing than "Do you like feature X?"
- **Empathy maps:** Four quadrants -- Says, Thinks, Does, Feels -- to organize observations about a user.
- **Journey maps:** Step-by-step visualization of a user's experience, highlighting pain points and opportunities.

**Common mistake:** Skipping empathy and jumping to solutions. The most frequent cause of design failure is solving the wrong problem.

### Phase 2 -- Define

Synthesize empathy findings into a clear problem statement (design brief).

**A good design brief contains:**

| Element | Purpose | Example |
|---|---|---|
| Problem statement | What needs solving | "Parents of young children cannot find safe, local playground information when traveling" |
| User description | Who the design serves | "Traveling families with children ages 2-8" |
| Constraints | Non-negotiable boundaries | "Must work offline, must be free, must not require account creation" |
| Success criteria | How to measure success | "User finds a playground within 3 taps and 10 seconds" |
| Scope | What is and is not included | "Playgrounds only -- not parks, museums, or restaurants" |

**Point-of-view (POV) statement:** "[User] needs [need] because [insight]." This single sentence drives all subsequent design work.

### Phase 3 -- Ideate

Generate multiple possible solutions before committing to one. Quantity over quality at this stage.

**Techniques:**
- **Brainstorming:** Time-boxed idea generation. Defer judgment. Build on others' ideas. Go for volume.
- **SCAMPER:** Substitute, Combine, Adapt, Modify, Put to another use, Eliminate, Reverse -- systematic prompts to transform existing concepts.
- **Crazy 8s:** Fold paper into 8 panels. Sketch 8 ideas in 8 minutes. Forces rapid, low-fidelity exploration.
- **How Might We (HMW):** Reframe constraints as opportunities. "We can't track location" becomes "How might we find nearby playgrounds without GPS?"

**The funnel:** Generate 20+ ideas, cluster by theme, evaluate against constraints and criteria, select 2-3 for prototyping.

### Phase 4 -- Prototype

Build quick, cheap representations of selected ideas to make them testable.

**Prototype fidelity spectrum:**

| Level | Medium | Time | Purpose |
|---|---|---|---|
| Paper sketch | Pencil on paper | 5 minutes | Explore layout and flow |
| Wireframe | Digital drawing tool | 30 minutes | Test information architecture |
| Mockup | Design software | 2-4 hours | Evaluate visual design and content |
| Interactive prototype | Prototyping tool or code | 1-2 days | Test interactions and usability |
| Functional prototype | Working code | 1-2 weeks | Validate technical feasibility |

**Cardinal rule:** Prototype at the lowest fidelity that answers your current question. Building a functional prototype to test a layout is wasteful; a paper sketch suffices.

### Phase 5 -- Test

Put prototypes in front of real users and observe what happens.

**Testing protocol:**
1. Give the user a task, not instructions. "Find a playground near this hotel" not "Tap the search icon."
2. Observe silently. Resist the urge to explain or help.
3. Ask "What are you thinking?" when the user pauses or looks confused.
4. Note where users succeed, struggle, or abandon the task.
5. After the session, ask open-ended reflection questions.

**Metrics that matter:**
- **Task completion rate:** What percentage of users completed the task?
- **Time on task:** How long did it take?
- **Error rate:** How many wrong turns?
- **Satisfaction:** How did the experience feel?

### Phase 6 -- Iterate

Testing reveals what works and what does not. Iteration means returning to an earlier phase with new understanding.

- Test results may reveal you misunderstood the user (return to Empathize).
- Test results may show the problem statement was too narrow (return to Define).
- Test results may invalidate the chosen concept but not the alternatives (return to Ideate).
- Test results may show the prototype needs refinement (return to Prototype).

**Iteration is not failure.** Every cycle narrows the gap between what you built and what people need. Professional designers expect 3-7 iterations before a design is ready for production.

## Don Norman's Design Principles

Don Norman's *The Design of Everyday Things* (1988, revised 2013) established the vocabulary for analyzing design quality.

### Affordances

An affordance is a relationship between a person and an object that determines how the object can be used. A flat plate on a door affords pushing. A handle affords pulling. A button affords pressing. Good design makes affordances visible; bad design hides them.

### Signifiers

Signifiers are perceivable cues that indicate what action is possible and how to perform it. A "Push" sign on a door is a signifier. A grayed-out button signifies "not available." Affordances exist whether or not people perceive them; signifiers make them perceivable.

### Mapping

Mapping is the relationship between controls and their effects. Natural mapping uses spatial correspondence: a stove with burners arranged in a square should have knobs arranged in a square. Arbitrary mapping (four knobs in a row for burners in a square) forces memorization and causes errors.

### Feedback

Every action should produce an immediate, visible, audible, or tactile response. A button that gives no feedback when pressed leaves the user uncertain. A loading spinner during a long operation prevents premature re-clicks. Absence of feedback is a design defect, not a simplification.

### Constraints

Constraints limit the possible actions, preventing errors. Physical constraints (a USB plug only fits one way) are the strongest. Logical constraints (graying out impossible menu options) are the most common in software. Cultural constraints (red means stop) rely on shared convention.

### Conceptual Models

A conceptual model is the user's understanding of how something works. A thermostat set to 90 does not heat faster -- it heats to a higher target -- but the folk model ("higher setting = more heat") persists because the interface provides no feedback about the actual mechanism. Good design aligns the user's conceptual model with the system's actual behavior.

## The Engineering Design Process (ITEEA)

The International Technology and Engineering Educators Association defines a complementary process used in K-12 technology education:

1. **Define the problem:** Identify the need, constraints, and criteria.
2. **Research the problem:** Investigate existing solutions, relevant science, and available materials.
3. **Develop possible solutions:** Brainstorm and sketch multiple approaches.
4. **Select the best solution:** Evaluate alternatives against criteria using a decision matrix.
5. **Construct a prototype:** Build the selected solution.
6. **Test and evaluate:** Measure performance against criteria.
7. **Communicate results:** Document findings, present to stakeholders.
8. **Redesign:** Improve based on test results.

This process maps directly onto the d.school phases: Define+Research = Empathize+Define, Develop+Select = Ideate, Construct = Prototype, Test+Redesign = Test+Iterate.

## Resnick's "Low Floors, High Ceilings, Wide Walls"

Mitchel Resnick's framework for learning environments applies directly to technology design:

- **Low floors:** Easy to get started. No prerequisites, no setup barriers.
- **High ceilings:** Room to grow into sophisticated use. Power users are not constrained.
- **Wide walls:** Many different paths and projects are possible. The tool does not dictate one right way.

A well-designed technology tool satisfies all three. Scratch (which Resnick created) exemplifies this: drag-and-drop blocks (low floor), Turing-complete computation (high ceiling), art/games/music/stories (wide walls).

## Cross-References

- **norman agent:** Primary agent for human-centered design, affordances, usability evaluation. Norman applies these principles.
- **berners-lee agent:** Information architecture and systems design. Berners-Lee evaluates designs from a systems perspective.
- **resnick agent:** Creative learning environments and pedagogical design. Resnick ensures designs support diverse learners.
- **human-computer-interaction skill:** The broader field within which design thinking operates.
- **responsible-innovation skill:** Ethical considerations during the design process.

## References

- Norman, D. A. (2013). *The Design of Everyday Things*. Revised edition. Basic Books.
- Brown, T. (2009). *Change by Design*. HarperBusiness.
- Resnick, M. (2017). *Lifelong Kindergarten*. MIT Press.
- ITEEA. (2020). *Standards for Technological and Engineering Literacy*. International Technology and Engineering Educators Association.
- Kelley, T. & Kelley, D. (2013). *Creative Confidence*. Crown Business.
- Stanford d.school. (2010). *An Introduction to Design Thinking: Process Guide*. Hasso Plattner Institute of Design.
