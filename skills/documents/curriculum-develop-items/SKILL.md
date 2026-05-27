---
name: curriculum-develop-items
description: Author high-quality assessment items (questions, prompts, tasks) aligned to learning objectives with answer keys and rubrics. Use when creating test questions, writing assessment items, or building item banks. Activates on "write assessment items", "create test questions", "develop quiz", or "author performance tasks".
---

# Assessment Item Authoring

Create diverse, well-constructed assessment items that validly measure learning objectives with proper alignment, difficulty, and quality standards.

## When to Use

- Create test/quiz questions
- Write essay prompts
- Design performance tasks
- Build assessment item banks
- Develop practice problems

## Required Inputs

- **Assessment Blueprint**: From `/curriculum.assess-design`
- **Learning Objectives**: What to assess
- **Item Type**: MC, true/false, short answer, essay, performance task
- **Quantity**: Number of items needed
- **Educational Level**: K-5 through post-graduate

## Workflow

### 1. Load Assessment Context

Read blueprint to understand:
- Which objectives to assess
- Bloom's cognitive levels
- Item type specifications
- Success criteria

### 2. Generate Assessment Items

**Multiple Choice Items**:
```markdown
**Item ID**: MC-1.1
**Objective**: LO-1.1
**Bloom's Level**: Remember
**Difficulty**: Easy

**Stem**: Which organelle is responsible for photosynthesis in plant cells?

A. Mitochondria
B. Chloroplast **(CORRECT)**
C. Nucleus
D. Ribosome

**Rationale**:
- **B is correct**: Chloroplasts contain chlorophyll and perform photosynthesis
- **A is incorrect**: Mitochondria perform cellular respiration (common confusion)
- **C is incorrect**: Nucleus stores genetic material
- **D is incorrect**: Ribosomes synthesize proteins

**Feedback for Wrong Answers**:
- A: "Remember that mitochondria are the powerhouse for cellular respiration, not photosynthesis."
- C: "The nucleus controls the cell but doesn't perform photosynthesis."
- D: "Ribosomes make proteins, not perform photosynthesis."
```

**Short Answer Items**:
```markdown
**Item ID**: SA-1.2
**Objective**: LO-1.2
**Bloom's Level**: Understand
**Difficulty**: Medium

**Prompt**: Explain why plants appear green. Include the role of chlorophyll in your answer. (2-3 sentences)

**Answer Key**:
Plants appear green because chlorophyll, the pigment in chloroplasts, absorbs red and blue light for photosynthesis but reflects green light. Since green light is reflected rather than absorbed, that's the color we see.

**Rubric** (4 points):
- 2 pts: Mentions chlorophyll/chloroplasts
- 1 pt: Explains light absorption
- 1 pt: Explains reflection of green light

**Common Errors**:
- Students may say "plants are green because they have chlorophyll" without explaining light reflection
```

**Essay Prompts**:
```markdown
**Item ID**: ESSAY-2.1
**Objective**: LO-2.3
**Bloom's Level**: Analyze
**Difficulty**: Hard

**Prompt**:
Compare and contrast photosynthesis and cellular respiration. In your essay:
- Explain the purpose of each process
- Identify the inputs and outputs
- Describe where each occurs in the cell
- Analyze how the two processes are related

Your essay should be 300-400 words.

**Scoring Rubric**: (See full analytic rubric with 4 criteria × 4 levels)

**Sample Exemplar Response**: [Provide model answer]
```

**Performance Tasks**:
```markdown
**Item ID**: PERF-3.1
**Objective**: LO-3.1, LO-3.2, LO-3.3
**Bloom's Level**: Create
**Difficulty**: Hard

**Task**:
Design an experiment to test the effect of light color on photosynthesis rate. Your design must include:
- Research question and hypothesis
- Materials list
- Step-by-step procedure
- Data collection table
- Method for measuring photosynthesis rate
- Safety considerations

Submit your experimental design as a 2-3 page document.

**Scoring Rubric**: (See analytic rubric - 6 criteria × 4 levels)

**Assessment Time**: 1 week (out of class)
```

### 3. Item Writing Best Practices

**Multiple Choice**:
✅ Clear, focused stems
✅ Plausible distractors (wrong but tempting)
✅ Avoid "all of the above" / "none of the above"
✅ Avoid negative stems when possible
✅ Options similar length and structure
✅ No grammatical cues to correct answer

**Short Answer**:
✅ Specific, clear expectations
✅ Indicate expected length
✅ Detailed answer key with partial credit guidance
✅ Address common misconceptions

**Essay**:
✅ Clear task and success criteria
✅ Provide rubric up front
✅ Specify length/time expectations
✅ Include sample exemplar (optional)

**Performance Tasks**:
✅ Authentic, real-world context
✅ Clear requirements and constraints
✅ Detailed rubric provided
✅ Reasonable time allocation

### 4. Alignment Verification

For each item, verify:
- ✅ Matches intended Bloom's level
- ✅ Directly assesses stated objective
- ✅ Appropriate difficulty for level
- ✅ Free from bias and barriers
- ✅ Clear and unambiguous
- ✅ Has complete answer key/rubric

### 5. Item Bank Organization

```markdown
# Assessment Items: [TOPIC]

**Educational Level**: [Level]
**Total Items**: [Count by type]
**Objectives Covered**: [List]

## Items by Objective

### LO-1.1 Items (Remember Level)
- MC-1.1: [Brief description]
- MC-1.2: [Brief description]
- TF-1.1: [Brief description]

### LO-1.2 Items (Understand Level)
- SA-1.1: [Brief description]
- SA-1.2: [Brief description]

[Continue for all objectives]

## Items by Type

### Multiple Choice (10 items)
[Full items with answer keys]

### Short Answer (5 items)
[Full items with rubrics]

### Essay (2 prompts)
[Full prompts with rubrics]

### Performance Tasks (1 task)
[Full task with detailed rubric]

## Item Statistics (To be completed after use)

| Item ID | P-Value (Difficulty) | Discrimination | Status |
|---------|---------------------|----------------|--------|
| MC-1.1  | TBD | TBD | New |

---

**Artifact Metadata**:
- **Artifact Type**: Assessment Items
- **Topic**: [Topic]
- **Level**: [Level]
- **Total Items**: [Count]
- **Next Phase**: Review or Package
```

### 6. Level-Appropriate Items

**K-5**:
- Simple, concrete language
- Visual supports (images, diagrams)
- Shorter items
- Avoid complex syntax
- Focus on fundamental skills

**6-8**:
- Moderate complexity
- Begin abstract reasoning
- Age-appropriate contexts
- Scaffold complex tasks

**9-12**:
- Discipline-specific language
- Complex problem-solving
- Multi-step tasks
- College-prep rigor

**Higher Ed**:
- Professional/research contexts
- Open-ended analysis
- Synthesis required
- Discipline expertise demonstrated

### 7. CLI Interface

```bash
# Generate items from blueprint
/curriculum.develop-items --blueprint "photosynthesis-blueprint.md" --objective "LO-1.1" --type "mc" --quantity 5

# Create full item bank
/curriculum.develop-items --blueprint "quadratics-blueprint.md" --all-objectives

# Single performance task
/curriculum.develop-items --objective "LO-3.2" --type "performance-task" --duration "1 week"

# Help
/curriculum.develop-items --help
```

## Composition with Other Skills

**Input from**:
- `/curriculum.assess-design` - Blueprint and specifications
- `/curriculum.design` - Objectives to assess

**Output to**:
- `/curriculum.review-pedagogy` - Items reviewed for quality
- `/curriculum.review-bias` - Items checked for fairness
- `/curriculum.package-*` - Items packaged for delivery
- `/curriculum.grade-assist` - Answer keys used for grading

## Exit Codes

- **0**: Success - Items created
- **1**: Invalid item type
- **2**: Cannot load blueprint/objectives
- **3**: Quantity invalid
- **4**: Insufficient specifications
