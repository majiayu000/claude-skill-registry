---
name: bloom-taxonomy-and-mastery
description: Bloom's Taxonomy of Educational Objectives and mastery learning as practical instructional design tools. Covers the six cognitive levels (remember, understand, apply, analyze, evaluate, create), the revised 2001 taxonomy, the knowledge dimension, mastery learning loops, formative vs. summative assessment, and the writing of learning objectives that are both specific and verifiable. Use when designing lessons, writing objectives, building assessments, or diagnosing why a learner is stuck at one cognitive level.
type: skill
category: learning
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/learning/bloom-taxonomy-and-mastery/SKILL.md
superseded_by: null
---
# Bloom's Taxonomy and Mastery Learning

Bloom's taxonomy is the most influential classification of educational objectives ever published, and mastery learning is the instructional design pattern Bloom derived from it to close the "two-sigma gap" between tutored and classroom learners. This skill turns both into working tools: a vocabulary for what the learner should be able to do, a checklist for diagnosing where a lesson is failing, and a loop structure for keeping every student at mastery before advancing.

**Agent affinity:** bloom (classification and synthesis), ericsson (mastery loop calibration)

**Concept IDs:** learning-objectives, cognitive-levels, mastery-loops

## 1. The Original (1956) Taxonomy

The 1956 *Taxonomy of Educational Objectives, Handbook I: Cognitive Domain*, edited by Benjamin Bloom with Engelhart, Furst, Hill, and Krathwohl, organized the cognitive domain into six levels arranged from simplest to most complex.

| Level | Name | What the learner does |
|-------|------|------------------------|
| 1 | Knowledge | Recall facts, terms, dates, formulas |
| 2 | Comprehension | Explain meaning, translate, summarize |
| 3 | Application | Use knowledge in a new situation |
| 4 | Analysis | Break down into components, identify relationships |
| 5 | Synthesis | Combine elements to form a new whole |
| 6 | Evaluation | Make judgments against defensible criteria |

The levels were arranged as a cumulative hierarchy: each higher level presupposes mastery of the levels below it. A learner who cannot recall the definition of a derivative cannot apply differentiation rules to a new function, and cannot evaluate whether a numerical answer is reasonable. This ordering is not metaphysical; it is a working assumption that held up well across decades of use.

## 2. The Revised (2001) Taxonomy

In 2001, Anderson, Krathwohl, and a team that included several of Bloom's original collaborators published *A Taxonomy for Learning, Teaching, and Assessing*. The revision made four structural changes:

1. **Nouns became verbs.** "Knowledge" became "Remember"; "Comprehension" became "Understand"; and so on. This reframed the taxonomy around what learners **do**, not what they **have**.
2. **Order changed.** Synthesis and Evaluation swapped places: "Create" (formerly Synthesis) became the highest level, because producing a coherent new work is cognitively harder than judging an existing one.
3. **A knowledge dimension was added.** The original taxonomy mixed type-of-knowledge and cognitive-process into one list. The revision split them into two dimensions that intersect as a matrix.
4. **The matrix structure.** Every learning objective sits at one cell of a 4 x 6 table.

### The Knowledge Dimension

| Type | Examples |
|------|---------|
| Factual | Terminology, specific details (the date of a battle, the symbol for carbon) |
| Conceptual | Categories, principles, models, theories (how natural selection works) |
| Procedural | Algorithms, techniques, methods (how to solve a linear equation, how to titrate) |
| Metacognitive | Self-knowledge, strategy knowledge, knowledge of when to apply what |

### The Cognitive Process Dimension (revised order)

1. **Remember** — Retrieve from long-term memory: recognize, recall.
2. **Understand** — Construct meaning: interpret, exemplify, classify, summarize, infer, compare, explain.
3. **Apply** — Execute a procedure: carry out, implement.
4. **Analyze** — Break material apart and detect relationships: differentiate, organize, attribute.
5. **Evaluate** — Make judgments against criteria: check, critique.
6. **Create** — Put elements together to form a new whole: generate, plan, produce.

### The Matrix

A learning objective is placed in a cell by asking: *what kind of knowledge?* and *what does the learner do with it?*

| | Remember | Understand | Apply | Analyze | Evaluate | Create |
|---|---|---|---|---|---|---|
| **Factual** | List Newton's three laws | Summarize each in one sentence | — | — | — | — |
| **Conceptual** | — | Explain why inertia matters | — | Compare Newtonian and relativistic views | Critique a claim about force | — |
| **Procedural** | Recall F = ma | — | Use F = ma for a sliding block | Diagnose a miscalculation | — | — |
| **Metacognitive** | — | — | — | — | Judge your own confidence | Design a self-check routine |

This matrix is the single most useful one-page tool for curriculum designers working on technical subjects.

## 3. Writing Objectives That Work

A usable learning objective has three parts:

1. **Audience.** *The learner will...*
2. **Observable verb.** From the cognitive-process list above. Never "understand" as the only verb — "understand" is the category, not the measurement.
3. **Condition and criterion.** What the learner does, under what conditions, to what standard.

**Bad:** "The student will understand Newton's second law."
**Good:** "Given a diagram of a block on a frictionless incline, the student will predict the acceleration within 5 percent of the exact value."

The bad version is untestable: "understanding" is in the student's head. The good version is testable: you hand them a diagram, they compute, you compare to the answer. Bloom's taxonomy gives you the verb menu that makes this happen.

### Verbs by Level

| Level | Verbs |
|-------|-------|
| Remember | list, recall, identify, name, state, recognize |
| Understand | explain, summarize, classify, interpret, infer, compare, give examples |
| Apply | calculate, solve, demonstrate, use, execute, implement |
| Analyze | differentiate, break down, compare and contrast, organize, attribute |
| Evaluate | critique, judge, defend, justify, argue, rank |
| Create | design, compose, plan, produce, construct, invent |

Avoid verbs from one level when the intended outcome is from another. Saying "list the causes of the French Revolution" when you actually want "explain the interaction of fiscal crisis and Enlightenment ideas" pushes students into rote memorization of a wrong-level target.

## 4. Mastery Learning

Bloom's 1984 paper *The 2 Sigma Problem* reported that students tutored one-to-one scored about two standard deviations higher than classroom-taught students on the same objectives. Two sigmas means the average tutored student outperformed 98 percent of the classroom cohort. This is the largest effect size in the instructional-design literature.

Bloom spent the rest of his career searching for classroom-scale interventions that could close this gap. Mastery learning was the cornerstone.

### The Mastery Loop

```
[teach to objective] -> [formative check] -> met criterion?
                                                  |
                                       yes ------+------ no
                                        |                 |
                                   [advance]    [correctives] -> [re-check]
                                                  |                  |
                                                  +--- re-enter loop until met
```

Components:

- **Teach to a specific objective** (from Bloom matrix).
- **Formative check** immediately after. Low-stakes, diagnostic — the point is to find the gap, not grade it.
- **If mastery (typically 80-90 percent correct):** advance to the next objective.
- **If not:** administer correctives — a different explanation, more examples, a worked-example-to-problem pairing, or a remediation activity. Then re-check.

The loop repeats until the student meets the criterion. Everyone reaches mastery; the variable is time, not outcome. This flips the default classroom model, where time is fixed and outcome varies.

### Formative vs. Summative

| | Formative | Summative |
|---|---|---|
| **Purpose** | Diagnose, adjust | Judge, certify |
| **Stakes** | Low | High |
| **Frequency** | Many per unit | One or two per unit |
| **Example** | End-of-lesson quiz, exit ticket, ungraded concept map | Final exam, unit test |
| **Feedback speed** | Immediate | After the learning window closes |

Mastery learning lives in the formative zone. A summative-only course has no mastery loop — it just sorts students by who happened to get it without correctives.

## 5. Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| Objective verb too vague | Can't tell if the student met it | Swap "understand" for a level-appropriate verb |
| Ceiling-level objective with no scaffolding | Students can't get started | Add Apply-level stepping stones first |
| Formative check is really summative | Students hide confusion | Make checks ungraded or rubric-only |
| No correctives, just "re-read the chapter" | Students repeat the same error | Build at least two alternative explanations per objective |
| Mastery criterion unrealistic (95 percent on first try) | Mastery is rare, loop never closes | 80 percent on first or second pass is the practical floor |
| Objectives stack at one level | Students memorize but cannot apply | Check the matrix distribution — aim for coverage across levels |

## 6. Worked Lesson Design (Fractions)

**Topic:** Adding fractions with unlike denominators.

### Objectives

| # | Objective | Bloom cell |
|---|-----------|------------|
| 1 | Recall the definition of a common denominator | Factual, Remember |
| 2 | Explain why two fractions must share a denominator before adding | Conceptual, Understand |
| 3 | Find the least common denominator for any pair from a given list | Procedural, Apply |
| 4 | Diagnose an error in a peer's worked addition | Procedural, Analyze |
| 5 | Judge whether a sum has been simplified to lowest terms | Conceptual, Evaluate |
| 6 | Design a word problem whose solution requires adding 1/3 + 1/4 | Conceptual, Create |

### Mastery Loop for Objective 3

1. Teach LCD-finding via prime factorization. Worked example: 1/4 + 1/6 -> LCD 12.
2. Formative check: ten pairs, compute the LCD only.
3. Criterion: 8 of 10 correct.
4. Correctives for missed items:
   - Type A (prime factorization wrong): re-teach factor trees.
   - Type B (factorization right, LCD wrong): re-teach LCM as the product of each prime at its highest power.
5. Re-check with five new pairs.
6. Advance to Objective 4.

### Routing Heuristics

- *User asks "what level is this question?"* -> classify on the matrix.
- *User asks "my students bombed the quiz — now what?"* -> diagnose whether the quiz was formative or summative, build correctives for the missed objectives, re-check.
- *User asks "how do I write better objectives?"* -> apply the three-part structure and verb menu.
- *User asks "why doesn't my curriculum work?"* -> check matrix distribution; stacked-at-one-level is the most common failure.

## 7. Cross-References

- **bloom agent:** Classification of objectives and synthesis of mastery-loop designs. Primary routing target.
- **ericsson agent:** Deliberate-practice structure for correctives and drill design.
- **dweck agent:** Motivation framing for students who interpret "not yet mastered" as "I am bad at this."
- **deliberate-practice-design skill:** Inner loop of a mastery cycle when drilling a procedural skill.
- **zpd-and-scaffolding skill:** Corrective-design companion — what scaffolding should be added when a student misses.

## 8. References

- Bloom, B. S. (Ed.). (1956). *Taxonomy of Educational Objectives: Handbook I, Cognitive Domain*. Longman.
- Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy*. Longman.
- Bloom, B. S. (1968). "Learning for Mastery." *UCLA Evaluation Comment*, 1(2).
- Bloom, B. S. (1984). "The 2 Sigma Problem." *Educational Researcher*, 13(6), 4-16.
- Guskey, T. R. (2007). "Closing Achievement Gaps: Revisiting Benjamin S. Bloom's 'Learning for Mastery.'" *Journal of Advanced Academics*, 19(1), 8-31.
