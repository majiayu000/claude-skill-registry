---
name: design-thinking-ps
description: Design thinking for ill-structured problems. Covers empathize, define, ideate, prototype, test — the iterative human-centered cycle used when the problem itself is not yet clear. Includes reframing, brainstorming, lateral thinking operators, assumption challenging, and the discipline of building to learn rather than building to ship. Use for wicked problems, product design, and any problem where "what is the question?" is the hard part.
type: skill
category: problem-solving
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/problem-solving/design-thinking-ps/SKILL.md
superseded_by: null
---
# Design Thinking

When the problem is well-defined, Polya's method works. When the problem itself is unclear — "how should we reduce food waste in our cafeteria?" "what should this product even do?" — a different approach is needed. Design thinking is the iterative, human-centered method that treats problem definition as part of the problem. It trades precision for exploration and rewards prototypes that fail fast over plans that succeed on paper.

**Agent affinity:** jonassen (ill-structured problems), bransford (anchored instruction, IDEAL), polya-ps (framing)

**Concept IDs:** prob-brainstorming, prob-lateral-thinking, prob-analogical-reasoning, prob-assumption-challenging

## The Design Thinking Cycle at a Glance

| Phase | Activity | Output |
|---|---|---|
| 1. Empathize | Learn about users, stakeholders, context | User insights, pain points, context map |
| 2. Define | Frame the problem sharply | "How might we..." statement |
| 3. Ideate | Generate many candidate solutions | Idea bank (divergent) |
| 4. Prototype | Build the cheapest thing that tests an idea | Low-fidelity artifact |
| 5. Test | Put prototype in front of real users | Evidence, revised understanding |

The cycle is iterative. Testing often reframes the problem, sending you back to Define. This is a feature, not a bug.

## Phase 1 — Empathize

**Goal:** Understand the users, stakeholders, context, and constraints well enough that the problem definition is grounded in reality rather than assumption.

**Operations:**

- **User interviews.** Open-ended questions, not leading questions. "Tell me about the last time you tried to do X."
- **Observation.** Watch users in their actual environment. What do they do, not what do they say they do?
- **Shadowing.** Follow a user through a complete task.
- **Empathy maps.** What does the user say, think, feel, do?
- **Journey mapping.** Chart the user's experience from first encounter to completion.

Empathize produces raw material. It does not produce a problem definition.

## Phase 2 — Define

**Goal:** Transform the raw empathy material into a sharp problem frame. The output is usually a "How might we..." statement.

**Pattern:** "How might we [action] [user] [goal] [context]?"

Example: "How might we help cafeteria cooks reduce end-of-day food waste without increasing portion complaints?"

A good "How might we..." statement:

- Names a specific user
- Names a specific action to enable
- Names the goal
- Names the context and major constraint
- Leaves room for many solutions

A bad "How might we..." statement:

- Names no user
- Bakes in the solution ("How might we build an app to...")
- Is too broad ("How might we fix world hunger?")
- Is too narrow ("How might we change the Tuesday menu?")

**Reframing:** If the initial frame does not produce interesting ideas in Phase 3, reframe. Move up a level ("reduce waste" → "reduce environmental impact"), move down a level ("reduce waste" → "reduce pasta waste on Tuesdays"), or move sideways ("reduce waste" → "increase diner satisfaction with leftovers").

## Phase 3 — Ideate

**Goal:** Generate many candidate solutions before evaluating any of them. Quantity first, quality second.

**Brainstorming rules (Osborn's original four, still valid):**

1. **Defer judgment.** Evaluation kills generation. Capture everything.
2. **Encourage wild ideas.** The wild ideas open new regions of the solution space.
3. **Build on others.** "Yes, and..." rather than "No, but..."
4. **Stay focused.** The "How might we..." statement is the anchor.

**Lateral thinking operators (de Bono):**

- **Challenge:** "Why does it have to be that way?" — attack an assumption.
- **Alternatives:** "What other ways could this work?" — demand multiple options.
- **Provocation (PO):** State an obviously false premise and see where it leads. "PO: the cafeteria throws away half the food before serving." This generates ideas like "plan smaller portions and offer refills."
- **Random entry:** Pick a random word and force a connection to the problem.
- **Concept extraction:** What is the underlying concept of an existing solution, and what other implementations could realize it?

**Analogical transfer:** Look at how other domains solve related problems. Hospitals have surgical inventory; could the cafeteria adopt similar tracking?

Ideation produces a bank of candidates. Scoring happens later.

## Phase 4 — Prototype

**Goal:** Build the cheapest, fastest thing that will test a candidate idea. A prototype is a question made physical.

**Principles:**

- **Low fidelity first.** Sketches, cardboard, wizard-of-oz. High fidelity wastes time before the idea is validated.
- **One question per prototype.** What are you trying to learn? "Do users notice the new menu layout?" is answerable; "is the new menu good?" is not.
- **Built to be thrown away.** If you are attached to the prototype, you will fail to learn.
- **Ready to test in days or hours, not weeks.**

Prototype types:

- **Storyboards:** Hand-drawn panels showing the user journey.
- **Paper mockups:** Fake the UI on paper.
- **Wizard of Oz:** A human behind the curtain performs what the system would do.
- **Role play:** Act out the scenario.
- **Physical mockups:** Cardboard, clay, 3D-printed parts.

## Phase 5 — Test

**Goal:** Expose the prototype to real users and collect evidence. The evidence may validate the idea, kill it, or reframe the problem.

**Operations:**

- **Observe.** What do users do, not what they say?
- **Ask open-ended questions.** "What is going through your mind right now?"
- **Record surprises.** Anything the team did not predict is high-signal.
- **Measure.** Time to complete, error rate, satisfaction.
- **Close the loop.** Did the evidence answer the question the prototype was built to answer?

**What to do with results:**

- **Validated:** proceed to higher-fidelity prototype or implementation.
- **Invalidated:** kill the idea and pick another from the ideation bank.
- **Reframed:** the test revealed that the original problem frame was wrong. Return to Phase 2.

## Worked Example — Cafeteria Food Waste

**Empathize:** Interviewed 8 cafeteria staff, 20 diners, shadowed 2 shifts. Found that cooks prepare for peak demand across all items, so low-demand items produce the most waste. Diners report that "fresh" signals quality — wilted items sit untouched.

**Define:** "How might we help cooks match preparation to real-time demand so that low-popularity items are not over-produced?"

**Ideate:** (20 ideas in 30 minutes)
- Real-time demand forecasting (wall screen)
- Small-batch cooking, refill as consumed
- Customer-facing "limited portions" display
- Shift low-demand items to mid-week
- Pre-order system (day before)
- PO: only prepare 10% of expected demand and refill aggressively
- ... etc.

**Prototype:** Storyboard the small-batch refill flow. Paper mockup of a kitchen display showing real-time consumption. One-day wizard-of-oz test where a staff member manually updates the display based on observation.

**Test:** The small-batch refill flow reduced waste by an estimated 30% in the one-day test, but diners complained about empty trays. Reframe: "How might we signal to diners that low levels mean fresh refill, not shortage?" — back to Phase 2.

## When Design Thinking Fails

- **Skipping empathy.** Designers who assume they know the user fail to discover what the real problem is.
- **Jumping to solutions.** Ideation before a sharp define phase produces unfocused ideas.
- **Prototyping at too high fidelity.** Burns time on the wrong details.
- **Testing without measurement.** "They liked it" is not evidence.
- **Treating the process as linear.** The cycle is meant to iterate; one pass is rarely enough.

## Cross-References

- **problem-comprehension** applies even to ill-structured problems, though the unknowns are different
- **strategy-selection** contributes brainstorming and lateral-thinking operators
- **collaborative-problem-solving** is the natural mode for design thinking in teams
- **metacognitive-monitoring** checks whether the current phase is producing its expected output
- **mathematical-problem-solving** is the complementary method for well-defined problems
