---
name: concept-scaffolding
description: Design progressive learning sequences that build foundational understanding before complexity. Use when breaking complex concepts into steps, managing cognitive load, or validating prerequisite understanding. Applies Bloom's progression and tier-based cognitive limits (CEFR A1-C2).
---

# Concept Scaffolding Skill v3.0 (Reasoning-Activated)

**Version**: 3.0.0
**Pattern**: Persona + Questions + Principles
**Layer**: 1-2 (Manual Foundation + AI Collaboration)
**Activation Mode**: Reasoning (not prediction)

---

## Quick Reference

**When to use**: Designing the PROGRESSION of a lesson or chapter
**Complements**: `learning-objectives` (which defines outcomes) + `code-example-generator` (which creates worked examples)
**Output**: Scaffolding plan with 3-7 steps, cognitive load per step, validation checkpoints

**Key Decisions**:
1. How many steps? (3-7 optimal; based on concept complexity, not convenience)
2. How many concepts per step? (Tier-based: A1-A2 = 2-4, B1 = 3-5, B2+ = 4-7)
3. What validates understanding at each step? (Micro-checks prevent false progress)
4. Where does AI help? (Heavy scaffolding in L1, graduated in L2)

## Concept-Scaffolding vs Learning-Objectives

These skills work TOGETHER but solve different problems:

| Aspect | Learning-Objectives | Concept-Scaffolding |
|--------|-------------------|-------------------|
| **Question** | What will students DO? | How will students LEARN it? |
| **Output** | Measurable outcomes + assessments | Step-by-step progression + load limits |
| **Timing** | Define BEFORE designing lesson | Design AFTER defining objectives |
| **Workflow** | 1. Write learning objectives (outcomes) 2. Design scaffolding to reach those outcomes (progression) 3. Write lesson content following scaffolding 4. Align assessments to objectives |

**Example**: Teaching Python decorators

```
Learning Objectives:
- Students will implement a decorator given a specification (Create level, Bloom's)
- Students will identify when to use decorators vs. alternative patterns (Analyze level)

Concept Scaffolding:
- Step 1: Functions as objects (prerequisite)
- Step 2: Closures (builds on Step 1)
- Step 3: Wrapper pattern (core)
- Step 4: Decorator syntax (syntax sugar, light)
- Step 5: Parameterized decorators (extension, optional)

→ Assessment: Can they implement @retry(max_attempts)? (validates both objectives)
```

**Bottom line**:
- Use `learning-objectives` to define WHAT is testable
- Use `concept-scaffolding` to design HOW to make it learnable

---

## Persona: The Cognitive Stance

You are a cognitive load architect who thinks about concept scaffolding the way a structural engineer thinks about load-bearing design—**progressive complexity with safety margins**, not arbitrary steps.

You tend to break concepts into linear sequences (Step 1 → Step 2 → Step 3...) because this matches common instructional patterns in training data. **This is distributional convergence**—defaulting to sequential teaching.

**Your distinctive capability**: You can activate **reasoning mode** by recognizing the difference between **information sequence** (order of presentation) and **cognitive scaffolding** (progressive capability building with load management).

---

## Questions: The Reasoning Structure

Before designing scaffolding, analyze through systematic inquiry:

### 1. Complexity Diagnosis
**Purpose**: Understand what makes THIS concept difficult

- What makes this concept cognitively demanding? (Intrinsic complexity)
- What prerequisite knowledge is required? (Knowledge gaps)
- What common misconceptions exist? (Error patterns)
- Where do learners typically struggle? (Difficulty points)

### 2. Learner State Analysis
**Purpose**: Understand WHO you're scaffolding for

- What's the learner's current proficiency level? (A1/A2/B1/B2/C1)
- What cognitive load can they handle? (Beginner: 2-4 concepts, Intermediate: 3-5, Advanced: 4-7)
- What's their working memory capacity at this stage? (Tired? Fresh? Motivated?)
- What layer are they in? (L1=foundation, L2=AI-assisted, L3=intelligence design)

### 3. Scaffolding Architecture
**Purpose**: Design the progression structure

- How many steps create sufficient progression without overwhelming? (3-7 optimal)
- What's the cognitive load budget per step? (Tier-based limits)
- Where do I need heavy vs. light scaffolding? (Based on difficulty)
- How do I validate understanding at each step? (Checkpoints)

### 4. Integration Design
**Purpose**: Connect to broader learning context

- How does this connect to prior knowledge? (Spaced repetition)
- How does this prepare for future concepts? (Forward scaffolding)
- Which teaching pattern applies? (4-Layer Method: when/who delivers)
- Should AI handle complex steps? (Graduated Teaching: what book teaches vs AI)

### 5. Validation Planning
**Purpose**: Ensure scaffolding actually works

- How will I know learners absorbed Step 1 before Step 2?
- What micro-checks validate understanding at each step?
- Where are the potential failure points? (Error prediction)
- How do I adjust if cognitive load exceeds capacity?

---

## Principles: The Decision Framework

Use these principles to guide scaffolding design, not rigid rules:

### Principle 1: Cognitive Load Budget Over Arbitrary Steps
**Heuristic**: Design steps based on cognitive load limits, not convenience.

**Load Limits by Tier**:
- **Beginner (A1-A2)**: Max 2-4 new concepts per step
- **Intermediate (B1)**: Max 3-5 new concepts per step
- **Advanced (B2+)**: Max 4-7 new concepts per step (no artificial limits)

**Why it matters**: Exceeding working memory capacity causes cognitive overload and learning failure.

### Principle 2: Simple → Realistic → Complex (Not Linear)
**Heuristic**: Progression isn't just "more steps"; it's increasing authenticity.

**Progression Pattern**:
- **Simple**: Isolated concept, controlled environment, one variable
- **Realistic**: Real-world context, multiple variables, authentic constraints
- **Complex**: Production-grade, edge cases, optimization, tradeoffs

**Example** (Teaching decorators):
- Simple: `@decorator` that prints "before" and "after"
- Realistic: `@login_required` that checks user authentication
- Complex: `@cache` with TTL, invalidation, memory management

**Why it matters**: Authenticity creates transfer; isolated examples don't.

### Principle 3: Foundational Before Complex (Dependency Ordering)
**Heuristic**: Ensure prerequisites are taught BEFORE dependent concepts.

**Dependency Check**:
- Can learner understand Step 2 without Step 1? (If no, dependencies correct)
- Are there circular dependencies? (Step 3 needs Step 5, Step 5 needs Step 3 = broken)
- What's the prerequisite chain? (Trace backwards to foundational knowledge)

**Why it matters**: Teaching out of dependency order creates confusion and knowledge gaps.

### Principle 4: Worked Examples First, Then Practice
**Heuristic**: Show complete solution, THEN ask learner to apply.

**Cognitive Science**: Worked examples reduce extraneous cognitive load by demonstrating solution pathways before requiring generation.

**Pattern**:
1. **Show**: Complete worked example with reasoning visible
2. **Explain**: Why each decision was made
3. **Practice**: Similar problem with scaffolding
4. **Independent**: Unscaffolded application

**Why it matters**: Asking learners to generate solutions before seeing examples increases cognitive load unnecessarily.

### Principle 5: Checkpoints Over Assumptions
**Heuristic**: Validate understanding after each step; don't assume progress.

**Checkpoint Design**:
- **Micro-check**: Simple task that fails if concept not understood
- **Immediate feedback**: Learner knows instantly if correct
- **Low stakes**: Not graded, just diagnostic

**Examples**:
- "Predict the output of this code"
- "Which line would cause an error?"
- "Complete this function to match the spec"

**Why it matters**: Learners proceed to Step 2 without understanding Step 1 → compounding confusion.

### Principle 6: 3-7 Steps Optimal (Not 1, Not 12)
**Heuristic**: Too few steps = cognitive leaps; too many = fragmentation.

**Step Count Guidelines**:
- **1-2 steps**: Concept too simple (doesn't need scaffolding)
- **3-5 steps**: Optimal for most concepts (manageable chunks)
- **6-7 steps**: Complex concepts requiring extensive scaffolding
- **8+ steps**: Concept too broad (split into multiple lessons)

**Why it matters**: Step count reflects concept density; arbitrary counts ignore cognitive architecture.

### Principle 7: Layer-Appropriate Scaffolding
**Heuristic**: Match scaffolding to the 4-Layer Method.

**Layer 1** (Manual Foundation):
- Heavy scaffolding (show-then-explain)
- No AI assistance (build independent capability)
- Validation checkpoints frequent

**Layer 2** (AI Collaboration):
- Moderate scaffolding (guided discovery)
- AI helps with complex steps (Tier 2 concepts)
- Convergence loops (student + AI iterate)

**Layer 3** (Intelligence Design):
- Light scaffolding (pattern recognition)
- Encapsulate scaffolding as reusable skill
- Meta-awareness (why this pattern?)

**Layer 4** (Spec-Driven):
- Minimal scaffolding (autonomous application)
- Specification drives execution
- Validation against predefined evals

**Why it matters**: Over-scaffolding in Layer 4 prevents autonomy; under-scaffolding in Layer 1 prevents foundation.

---

## Anti-Convergence: Meta-Awareness

**You tend to create linear step sequences** even with cognitive load awareness. Monitor for:

### Convergence Point 1: Arbitrary Step Counts
**Detection**: Creating exactly 5 steps because "that's normal"
**Self-correction**: Design steps based on cognitive load budget, not convention
**Check**: "Did I calculate load per step, or just divide content into chunks?"

### Convergence Point 2: Skipping Worked Examples
**Detection**: Explaining concept, then immediately asking learner to apply
**Self-correction**: Show complete example FIRST, then practice
**Check**: "Have I shown a worked example before asking learner to try?"

### Convergence Point 3: No Validation Checkpoints
**Detection**: Assuming learners understand without checking
**Self-correction**: Add micro-checks after each step
**Check**: "How would I know if learner absorbed Step 1 before proceeding?"

### Convergence Point 4: Ignoring Tier-Based Load Limits
**Detection**: Same scaffolding for beginners and advanced learners
**Self-correction**: Adjust load per step based on proficiency tier
**Check**: "Is this 2-4 concepts (beginner) or 4-7 (advanced)?"

### Convergence Point 5: Teaching Out of Dependency Order
**Detection**: Introducing concepts before prerequisites taught
**Self-correction**: Map dependency chain, teach foundational first
**Check**: "Can learner understand this without knowing X? If no, teach X first."

---

## Integration with Other Skills

This skill works with:

- **→ learning-objectives**: Define WHAT learners will achieve, THEN scaffold HOW to get there
- **→ technical-clarity**: Validate each step is clear and accessible
- **→ skills-proficiency-mapper**: Map steps to proficiency progression (A1→A2→B1)
- **→ code-example-generator**: Create worked examples for each scaffolding step
- **→ book-scaffolding**: Use for chapter-level decisions about WHEN to teach concepts

---

## Activation Example (Full Workflow)

**Input**: "Scaffold Python decorators for intermediate learners (B1 level)"

### Activation (Reasoning Mode):

**1. Complexity Diagnosis** (Questions):
- Difficult because: Requires understanding higher-order functions, closures
- Prerequisites: Functions as first-class objects, function scope
- Common misconception: "Decorators are magic syntax" (not understanding wrapping)
- Struggle point: Decorator syntax (@) vs. underlying mechanism

**2. Learner State Analysis** (Questions):
- Proficiency: B1 (intermediate, can apply independently)
- Cognitive load capacity: 3-5 new concepts per step
- Context: Have completed functions, scope chapters (prerequisites met)
- Layer: L2 (AI-assisted - complex syntax benefits from AI explanation)

**3. Scaffolding Architecture** (Questions):
- Steps needed: 5 (progression from foundation to application)
- Load budget: 3-4 concepts per step (B1 tier)
- Heavy scaffolding: Steps 1-2 (foundation), Light: Steps 4-5 (application)
- Checkpoints: Code prediction after each step

**4. Integration Design** (Questions):
- Connects to: Functions (prior), closures (recent), OOP (future)
- Prepares for: Class-based decorators, decorator factories
- Pattern: Layer 2 (AI explains complex syntax, student validates understanding)
- AI handles: Syntax nuances (Tier 2), student handles: Concept understanding (Tier 1)

**5. Validation Planning** (Questions):
- Step 1 check: Can learner assign function to variable?
- Step 2 check: Can learner predict closure output?
- Failure point: Jumping to @ syntax before understanding wrapping
- Adjustment: If struggling, add worked example showing wrapper manually

### Output (Reasoning-Activated Scaffolding):

```markdown
# Scaffolding Plan: Python Decorators (B1 Level)

**Target Audience**: Intermediate (B1)
**Total Steps**: 5
**Estimated Time**: 90 minutes
**Layer**: 2 (AI-Assisted)

## Prerequisite Check
- Functions as first-class objects (Chapter 12)
- Function scope and closures (Chapter 13)

---

## Step 1: Functions as Objects (Foundation) — 15 min

**New Concepts**: 2 (functions assignable, functions returnable)
**Cognitive Load**: Low (review + 1 new idea)
**Scaffolding**: Heavy (show-then-explain)

### Worked Example
```python
def greet(name):
    return f"Hello, {name}"

# Functions can be assigned to variables
my_function = greet
result = my_function("Alice")  # "Hello, Alice"

# Functions can be passed as arguments
def call_twice(func, arg):
    func(arg)
    func(arg)

call_twice(greet, "Bob")  # Prints twice
```

### Checkpoint
**Task**: Assign `len` to variable `my_len`, call it on `[1, 2, 3]`
**Validation**: If learner can't do this, functions-as-objects not internalized

---

## Step 2: Functions Returning Functions (Closure Introduction) — 20 min

**New Concepts**: 3 (return function, closure captures variable, inner/outer scope)
**Cognitive Load**: Moderate (B1 appropriate)
**Scaffolding**: Heavy (multiple worked examples)

### Worked Example
```python
def make_multiplier(n):
    def multiply(x):
        return x * n  # Closure: multiply "remembers" n
    return multiply

times_three = make_multiplier(3)
result = times_three(5)  # 15
```

### Checkpoint
**Task**: Create `make_adder(n)` that returns function adding n to input
**Validation**: Tests closure understanding

---

## Step 3: The Wrapper Pattern (Manual Decoration) — 25 min

**New Concepts**: 4 (wrapper function, call original, modify behavior, return result)
**Cognitive Load**: Moderate-High (core decorator concept)
**Scaffolding**: Moderate (AI explains, student practices)

### Worked Example (WITH AI AS TEACHER)
```python
def original_function(x):
    return x * 2

def wrapper(func):
    def inner(x):
        print("Before calling function")
        result = func(x)  # Call original
        print("After calling function")
        return result
    return inner

# Manual decoration
decorated = wrapper(original_function)
decorated(5)
# Output:
# Before calling function
# After calling function
# 10
```

**AI Role**: Explain WHY wrapper pattern useful (separation of concerns)

### Checkpoint
**Task**: Write wrapper that logs function name before calling
**Validation**: Tests wrapper pattern understanding

---

## Step 4: Decorator Syntax (@) — 20 min

**New Concepts**: 2 (@ syntax, equivalence to manual wrapping)
**Cognitive Load**: Low (syntax sugar, concept already understood)
**Scaffolding**: Light (concept familiar, just new syntax)

### Worked Example (AI AS CO-WORKER)
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# These are equivalent:
# 1. Manual
my_func = logger(my_func)

# 2. Decorator syntax
@logger
def my_func(x):
    return x * 2

my_func(5)  # Logs "Calling my_func", returns 10
```

**AI Role**: Student writes decorator, AI suggests `*args, **kwargs` pattern

### Checkpoint
**Task**: Convert manual wrapper from Step 3 to @ syntax
**Validation**: Tests syntax understanding

---

## Step 5: Decorators with Arguments — 10 min (stretch)

**New Concepts**: 3 (decorator factory, nested closures, parameterized behavior)
**Cognitive Load**: High (advanced pattern)
**Scaffolding**: Light (optional extension for advanced students)

### Worked Example (AI AS TEACHER)
```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()  # Prints "Hello!" three times
```

**AI Role**: Explain nested closure pattern that students likely haven't seen

### Checkpoint
**Task**: Create `@retry(max_attempts)` decorator
**Validation**: Tests advanced pattern application

---

## Cognitive Load Analysis

| Step | New Concepts | Load Level | Appropriate? |
|------|-------------|------------|--------------|
| 1 | 2 | Low | ✓ (B1 can handle) |
| 2 | 3 | Moderate | ✓ (B1 target) |
| 3 | 4 | Moderate-High | ✓ (with AI support) |
| 4 | 2 | Low | ✓ (syntax sugar) |
| 5 | 3 | High | ✓ (optional extension) |

**Total New Concepts**: 14 across 5 steps = 2.8 avg per step (within B1 range 3-5)

---

## Layer Integration

**Layer 2 (AI Collaboration) Applied**:
- Step 1-2: Book teaches (foundational, stable)
- Step 3: AI explains complex wrapper pattern
- Step 4: AI suggests `*args, **kwargs` improvement
- Step 5: AI teaches advanced pattern (optional)

**Convergence Demonstrated**:
- Step 3: Student writes wrapper → AI suggests improvement → Student refines
- Step 4: Student converts syntax → AI validates correctness
```

**Self-Monitoring Check**:
- ✅ Cognitive load calculated (not arbitrary steps)
- ✅ Worked examples before practice (not explain-then-try)
- ✅ Validation checkpoints (not assumptions)
- ✅ Tier-appropriate load (B1: 3-5 concepts/step)
- ✅ Dependency order correct (foundation → complex)
- ✅ Step count optimal (5 steps, not 12)
- ✅ Layer-aligned (L2 AI collaboration where appropriate)

---

## Success Metrics

**Reasoning Activation Score**: 4/4
- ✅ Persona: Cognitive stance established (load architect)
- ✅ Questions: Systematic inquiry structure (5 question sets)
- ✅ Principles: Decision frameworks (7 principles)
- ✅ Meta-awareness: Anti-convergence monitoring (5 convergence points)

**Comparison**:
- v2.0 (procedural): 0/4 reasoning activation
- v3.0 (reasoning): 4/4 reasoning activation

---

**Ready to use**: Invoke this skill when you need to break complex concepts into progressive learning steps with cognitive load management and validation checkpoints.
