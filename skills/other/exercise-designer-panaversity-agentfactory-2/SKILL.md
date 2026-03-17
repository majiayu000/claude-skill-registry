---
name: exercise-designer
description: Designs deliberate practice exercises applying evidence-based learning strategies like retrieval practice, spaced repetition, and interleaving. Activate when educators need varied exercise types (fill-in-blank, debug-this, build-from-scratch, extend-code, AI-collaborative) targeting learning objectives with appropriate difficulty progression. Creates exercise sets that apply cognitive science principles to maximize retention and skill development. Use when designing practice activities for Python concepts, creating homework assignments, generating problem sets, or evaluating exercise quality.
---

## Purpose

The exercise-designer skill helps educators create varied, evidence-based practice exercises that target specific learning objectives and apply proven strategies from cognitive science. This skill designs exercises with appropriate difficulty progression, spaced repetition opportunities, and clear assessment criteria.

**Constitution v4.0.1 Alignment**: This skill implements evals-first exercise design—defining success criteria BEFORE creating exercises, integrating Section IIb (AI Three Roles Framework) co-learning exercise types, and aligning with Section IIa (4-Layer Method) for layer-appropriate exercises.

## When to Activate

Use this skill when:
- Educators need practice exercises for Python concepts
- Designing homework assignments or problem sets
- Creating varied exercise types beyond simple coding problems
- Applying evidence-based learning strategies (retrieval practice, spaced repetition)
- Establishing difficulty progression across exercise sequences
- Generating test cases and rubrics for exercises
- Evaluating existing exercises for pedagogical effectiveness

## Inputs

Required:
- **Learning objectives**: What learners should be able to do
- **Concept/topic**: Python concept to practice (e.g., "loops", "dictionaries")

Optional:
- **Target audience**: beginner | intermediate | advanced
- **Number of exercises**: How many to generate
- **Exercise types**: Preferred types (fill-in, debug, build-from-scratch, etc.)
- **Time constraints**: Total time available for exercises
- **Prior concepts**: Previously learned concepts for spaced repetition

## Evals-First Exercise Design (Constitution v3.1.2)

**CRITICAL WORKFLOW**:
1. **Evals First**: Review success criteria from chapter spec BEFORE designing exercises
2. **Objectives Second**: Ensure exercises target learning objectives that lead to evals
3. **Exercises Third**: Design practice activities that prepare students for eval success
4. **Validation Fourth**: Verify exercises measure progress toward defined success criteria

**Template**:
```markdown
### Exercise Design (Evals-First)

**Source**: Chapter spec at `specs/part-X/chapter-Y/spec.md`

**Success Evals from Spec**:
1. 75%+ write valid specification (measured by final exercise)
2. 80%+ identify vague requirements (measured by quiz)

**Learning Objectives** (from spec):
- LO-001: Write clear specifications
- LO-002: Identify ambiguous requirements

**Exercise Design to Achieve Objectives → Evals**:
- Ex-1: Fill-in incomplete spec (LO-001, starter difficulty)
- Ex-2: Debug vague spec (LO-002, core difficulty)
- Ex-3: Write complete spec from scratch (LO-001, stretch difficulty) → Tests Eval #1
- Ex-4: Evaluate spec clarity (LO-002, stretch difficulty) → Tests Eval #2
```

**Do NOT** create exercises without:
- ✅ Reference to approved spec with success evals
- ✅ Explicit mapping: Exercise → Objective → Eval
- ✅ Verification that exercises prepare for eval success

## Process

### Step 1: Clarify Learning Objectives and Evals

Understand what learners should achieve:
- Specific skills to demonstrate
- Depth of understanding required (recall vs. application vs. creation)
- Connection to Bloom's taxonomy levels
- **Success evals from chapter spec** (what defines mastery?)

### Step 2: Load Exercise Type Reference

Read exercise type patterns for variety:

```bash
Read reference/exercise-types.md
```

Available types:
- **Fill-in-the-blank**: Focus on specific concepts with scaffolding
- **Debug-this**: Develop error recognition skills
- **Build-from-scratch**: Test independent problem-solving
- **Extend-the-code**: Practice incremental development
- **Trace-execution**: Test mental execution model
- **Explain-code**: Promote deeper understanding
- **Refactor**: Teach code quality and Pythonic patterns
- **Parsons problems**: Focus on logic flow
- **AI-collaborative** (NEW): Practice working WITH AI as co-learning partner

### AI-Collaborative Exercise Types (Section IIb, Constitution v4.0.1)

**CRITICAL**: AI-native exercises must teach students to work WITH AI in bidirectional co-learning partnership (per Section IIb forcing functions), not just independently.

**AI-Collaborative Exercise Categories**:

**1. Spec-to-Code with AI (AI as Student)**:
```markdown
### Exercise: User Authentication

**Task**: Write a specification that produces working OAuth implementation on first try.

**Instructions**:
1. Write detailed specification for OAuth authentication
2. Provide spec to AI
3. Evaluate AI's generated code
4. Identify gaps in your spec if code doesn't match intent

**Assessment**:
- Spec clarity (5 pts): Unambiguous requirements
- Completeness (5 pts): All edge cases specified
- AI output quality (5 pts): Code matches spec without clarification
- Reflection (5 pts): What you learned about spec-writing from AI's response
```

**2. Convergence Iteration (AI as Co-Worker)**:
```markdown
### Exercise: Optimize Database Query

**Task**: Iterate with AI to improve query performance.

**Instructions**:
1. Start with provided slow query
2. Ask AI for improvement suggestions
3. Evaluate AI's suggestions (don't blindly accept)
4. Implement chosen approach
5. Document what YOU decided vs. what AI suggested

**Assessment**:
- Iteration quality (5 pts): Clear back-and-forth refinement
- Decision-making (5 pts): Strategic choices explained
- Convergence (5 pts): Better solution than either party alone
- Validation (5 pts): Verified AI's suggestions work correctly
```

**3. Pattern Learning from AI (AI as Teacher)**:
```markdown
### Exercise: Discover Pythonic Patterns

**Task**: Learn a new pattern from AI suggestion.

**Instructions**:
1. Implement solution using your current approach
2. Ask AI: "How would you improve this for Pythonicity?"
3. Analyze AI's suggestion
4. Explain what pattern AI taught you and why it's better
5. Apply pattern to 2 new problems

**Assessment**:
- Understanding (5 pts): Clearly explains AI's suggested pattern
- Application (5 pts): Successfully applies to new contexts
- Evaluation (5 pts): Identifies when pattern is/isn't appropriate
- Reflection (5 pts): What you learned that you didn't know before
```

**4. AI Output Validation (Critical Skill)**:
```markdown
### Exercise: Verify AI-Generated Code

**Task**: Validate AI-generated authentication code for security.

**Instructions**:
1. Review provided AI-generated code
2. Identify security vulnerabilities
3. Write test cases that expose issues
4. Propose fixes
5. Document validation checklist you used

**Assessment**:
- Vulnerability detection (5 pts): Found critical issues
- Test coverage (5 pts): Tests expose problems
- Fix quality (5 pts): Secure improvements
- Validation process (5 pts): Systematic approach documented
```

**5. Spec Refinement from AI Feedback (Bidirectional Learning)**:
```markdown
### Exercise: Iterative Spec Improvement

**Task**: Refine specification based on AI clarifying questions.

**Instructions**:
1. Write initial specification
2. AI asks clarifying questions (or you simulate what AI might ask)
3. Improve spec to answer questions proactively
4. Compare initial vs. final spec quality

**Assessment**:
- Initial spec (2 pts): Baseline quality
- Question anticipation (3 pts): Identified ambiguities
- Refinement quality (3 pts): Clearer final spec
- Learning (2 pts): Documented what makes specs clear
```

**Exercise Balance for AI-Native Content**:
- 50-60%: Traditional independent exercises
- 30-40%: AI-collaborative exercises (Three Roles)
- 10-20%: Validation/verification exercises

### Step 3: Load Evidence-Based Strategies

Read cognitive science strategies to apply:

```bash
Read reference/evidence-based-strategies.md
```

Key strategies:
- **Retrieval Practice**: Recall from memory strengthens learning
- **Spaced Repetition**: Distribute practice over time
- **Interleaving**: Mix exercise types and concepts
- **Elaboration**: Ask "why" and "how" questions
- **Desirable Difficulty**: Appropriate challenge level

### Step 4: Design Exercise Variety

Create 3-5 exercises using multiple types:

**Mix Exercise Types** (avoid 5 identical exercises):
```
Exercise 1: Fill-in-blank (quick warm-up)
Exercise 2: Debug-this (error recognition)
Exercise 3: Build-from-scratch (application)
Exercise 4: Explain-code (elaboration)
Exercise 5: Extend-code (integration)
```

**Apply Interleaving**: Mix new and prior concepts:
- 60% current concept
- 30% recent concepts (last 1-2 lessons)
- 10% older concepts (3+ lessons ago)

### Step 5: Establish Difficulty Progression

Load difficulty progression guide:

```bash
Read reference/difficulty-progression.md
```

Sequence exercises from easier to harder:
- **Easy**: High scaffolding, clear structure
- **Medium**: Moderate scaffolding, specification-based
- **Hard**: Minimal scaffolding, open-ended

**Bloom's Progression**:
1. Remember/Understand (trace execution, explain)
2. Apply (fill-in-blank, standard problems)
3. Analyze (debug-this, compare approaches)
4. Evaluate/Create (build-from-scratch, refactor)

### Step 6: Incorporate Spaced Repetition

Load spaced repetition patterns:

```bash
Read reference/spaced-repetition.md
```

Include prior concepts for review:
- Identify concepts from previous lessons
- Design exercises combining old + new concepts
- Tag exercises with concepts practiced (for tracking)

**Example**:
```
Lesson 5 (Current: Loops)
Exercise 1: Loop basics (new)
Exercise 2: Loops + lists (review Lesson 2)
Exercise 3: Loops + conditionals (review Lesson 3)
Exercise 4: Loops + functions (review Lesson 4)
```

### Step 7: Create Test Cases

Generate comprehensive test cases:

```bash
Read templates/exercise-template.yml
```

Include:
- **Normal cases**: Typical usage (60%)
- **Edge cases**: Empty inputs, boundaries, special cases (30%)
- **Error cases**: Invalid inputs, exceptions (10%)

Validate test coverage using script:

```bash
python .claude/skills/exercise-designer/scripts/generate-test-cases.py exercise.yml
```

The script will:
- Analyze existing test case coverage
- Suggest missing test types
- Provide concept-specific recommendations
- Check for normal/edge/error case balance

### Step 8: Define Assessment Rubric

Load rubric template:

```bash
Read templates/rubric-template.yml
```

Create rubric with criteria:
- **Correctness** (40%): Produces correct output
- **Code Quality** (30%): Readable, well-structured
- **Efficiency** (20%): Appropriate approach
- **Error Handling** (10%): Edge case consideration

Each criterion has levels: excellent, adequate, developing, insufficient

### Step 9: Add Progressive Hints

Provide 3 levels of hints:
- **Level 1** (gentle): Direction without giving answer
- **Level 2** (moderate): More specific guidance
- **Level 3** (explicit): Nearly complete solution

**Example**:
```
Exercise: Write function to find duplicates in a list

Hint 1: "Consider using a set to track items you've seen"
Hint 2: "Iterate through list, add items to set, check if item already in set"
Hint 3: "Use: seen = set(); for item in list: if item in seen..."
```

### Step 10: Validate and Refine

Check exercise quality:
- [ ] Clear learning objective stated
- [ ] Appropriate difficulty for target audience
- [ ] Complete instructions (learner knows what to do)
- [ ] Test cases provided (normal + edge + error)
- [ ] At least 2 evidence-based strategies applied
- [ ] Exercise is achievable in estimated time
- [ ] Rubric or evaluation criteria included

## Output Format

Provide exercise set as structured markdown or YAML:

```markdown
# Exercise Set: [Topic]

**Learning Objectives**:
- [Objective 1]
- [Objective 2]

**Estimated Time**: [X minutes total]
**Evidence-Based Strategies**: [List strategies applied]

---

## Exercise 1: [Title]

**Type**: [fill-in-blank | debug-this | etc.]
**Difficulty**: [easy | medium | hard]
**Time**: [X minutes]
**Strategies**: [retrieval-practice, etc.]

### Instructions

[Clear description of what to do]

### Starter Code (if applicable)

```python
[Code here]
```

### Test Cases

1. **Input**: `[example]`
   **Expected**: `[output]`
   **Tests**: Normal case

2. **Input**: `[]`
   **Expected**: `[output]`
   **Tests**: Edge case - empty input

### Hints

**Hint 1**: [Gentle guidance]
**Hint 2**: [More specific]
**Hint 3**: [Explicit approach]

### Rubric

- **Correctness** (4 pts): Passes all test cases
- **Code Quality** (3 pts): Readable with good naming
- **Efficiency** (2 pts): Reasonable approach
- **Error Handling** (1 pt): Handles edge cases

---

[Repeat for exercises 2-5]

---

## Spaced Repetition Notes

This exercise set practices:
- **New**: [Current concept]
- **Review**: [Concepts from prior lessons]

---

## Answer Key

[Solutions for all exercises with explanations]
```

## Examples

### Example 1: Design Exercises for List Methods

**Input**: "Create 5 exercises for practicing list methods (append, remove, extend) for beginners"

**Process**:
1. Identify learning objectives: Use list methods correctly, understand when to use each
2. Choose variety: fill-in-blank, debug-this, build-from-scratch, explain-code, trace-execution
3. Progress difficulty: easy → medium → medium → hard → medium
4. Apply strategies: retrieval practice (no references), interleaving (mix method types)
5. Add test cases and rubrics
6. Include hints

**Output**: 5-exercise set with variety, progression, test cases, and strategies applied

---

### Example 2: Review Existing Exercise Set

**Input**: "Evaluate these 10 loop exercises for pedagogical effectiveness"

**Process**:
1. Check variety: "All 10 are build-from-scratch—needs more variety"
2. Check progression: "Difficulty jumps too quickly from exercise 2 to 3"
3. Check strategies: "No spaced repetition—all exercises only use loops, no prior concepts"
4. Check test cases: "Only 3 exercises have test cases, edge cases missing"
5. Provide specific recommendations

**Output**: Detailed assessment with actionable improvements

---

### Example 3: Design Exercises with Spaced Repetition

**Input**: "Create exercises for dictionaries (Lesson 4) that review lists (Lesson 2) and conditionals (Lesson 3)"

**Process**:
1. Primary concept: Dictionary methods and operations
2. Secondary concepts: Lists, conditionals (for review)
3. Design exercises combining concepts:
   - Exercise 1: Dictionary basics (new)
   - Exercise 2: Dictionary + conditionals (review)
   - Exercise 3: Dictionary + lists (review)
   - Exercise 4: All three combined
4. Tag for tracking: primary=dictionaries, secondary=[lists, conditionals]

**Output**: Exercise set with explicit spaced repetition

## Common Patterns

### Pattern 1: Concept Introduction Set

```
Exercise 1: Fill-in-blank (very easy, high scaffolding)
Exercise 2: Trace-execution (understand behavior)
Exercise 3: Build-from-scratch (simple application)
Exercise 4: Debug-this (recognize errors)
Exercise 5: Extend-code (integrate with prior knowledge)
```

### Pattern 2: Mixed Review Set

```
Exercise 1: Current concept only (60%)
Exercise 2: Current + recent concept (30%)
Exercise 3: Current concept only (60%)
Exercise 4: Current + old concept (10%)
Exercise 5: Current + recent + old (integration)
```

### Pattern 3: Progressive Challenge Set

```
Exercise 1: Guided (70% code provided)
Exercise 2: Structured (50% code provided)
Exercise 3: Specification (clear requirements)
Exercise 4: Open-ended (minimal guidance)
Exercise 5: Extension (build on Exercise 3)
```

## Validation Checklist

Before finalizing exercise set:
- [ ] 3-5 exercises (not too few, not overwhelming)
- [ ] Multiple exercise types (not all identical)
- [ ] Clear difficulty progression (easier → harder)
- [ ] At least 2 evidence-based strategies explicitly applied
- [ ] Test cases for each exercise (normal + edge + error)
- [ ] Rubric or assessment criteria provided
- [ ] Spaced repetition if applicable (reviews prior concepts)
- [ ] Instructions are clear and complete
- [ ] Exercises are achievable in estimated time
- [ ] Each exercise has clear learning objective

## Acceptance Checks

- [ ] Difficulty bands present: starter (easy), core (medium), stretch (hard)
- [ ] Hints provided at three levels (gentle, moderate, explicit)
- [ ] Rubric attached with criteria and points; maps to objectives

### Difficulty bands example
```
Starter: Warm‑up fill‑in (L2‑Understand)
Core: Implement function from spec (L3‑Apply)
Stretch: Refactor for performance (L4‑Analyze/L5‑Evaluate)
```

## References

Supporting documentation (loaded as needed):
- `reference/exercise-types.md` - Fill-in, debug, build-from-scratch, etc.
- `reference/evidence-based-strategies.md` - Retrieval, spacing, interleaving, elaboration
- `reference/difficulty-progression.md` - Scaffolding, Bloom's levels, PRIME framework
- `reference/spaced-repetition.md` - Spiral curriculum, mixed sets, optimal intervals

## Error Handling

If validation fails:
1. Report specific issues (e.g., "All exercises are same type", "No test cases provided")
2. Suggest remediation (e.g., "Add debug-this and trace-execution exercises")
3. Halt and require user intervention (hard failure mode)

Examples must meet quality standards: varied types, appropriate difficulty, clear objectives, comprehensive test cases.
