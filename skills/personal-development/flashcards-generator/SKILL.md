---
name: flashcards-generator
description: Generate comprehensive educational flashcards based on Bloom's Taxonomy methodology (Remember, Understand, Apply, Analyze, Evaluate, Create). Creates structured flashcards with difficulty ratings, detailed explanations, and practice hints. Use when user requests flashcard generation, study cards, review materials, learning flashcards, mentions Bloom's Taxonomy, or provides educational topics for flashcard creation. Activates for study topics, course materials, reference files (.md, .txt, .pdf), or educational content requiring systematic review materials.
---

# Flashcards Generator

## Purpose

This skill generates comprehensive educational flashcards systematically organized according to Bloom's Taxonomy cognitive levels. It produces structured review materials incorporating difficulty ratings, answer explanations, related concept references, and practice hints to facilitate deep learning and retention.

## Bloom's Taxonomy Cognitive Levels

The flashcards shall be organized across six hierarchical cognitive levels:

1. **Remember**: Retrieve relevant knowledge from long-term memory (recall, recognize, identify)
2. **Understand**: Construct meaning from instructional messages (interpret, exemplify, classify, summarize, infer, compare, explain)
3. **Apply**: Carry out or use a procedure in a given situation (execute, implement)
4. **Analyze**: Break material into constituent parts and determine relationships (differentiate, organize, attribute)
5. **Evaluate**: Make judgments based on criteria and standards (check, critique, judge)
6. **Create**: Put elements together to form a coherent whole; reorganize into new pattern (generate, plan, produce, design)

## Instructions

When invoked, execute the following systematic procedure:

### Phase 1: Input Acquisition and Analysis

**Step 1.1**: Determine input source

Identify whether the user has provided:
- A topic title (text-based subject specification)
- A reference file path (existing educational material)
- Both topic and supporting reference materials

**Step 1.2**: Process reference materials (if applicable)

If a reference file is provided:
- Use the Read tool to extract content from the specified file path
- Analyze the content structure, key concepts, and learning objectives
- Identify core terminology, principles, and relationships
- Extract subject domain and complexity level

**Step 1.3**: Conduct supplementary research (if necessary)

If the topic is unfamiliar or requires current information:
- Employ WebSearch tool to locate authoritative educational resources
- Use WebFetch tool to retrieve comprehensive explanatory content
- Synthesize multiple sources to ensure accuracy and depth
- Prioritize academic, educational, and authoritative domain sources

### Phase 2: Content Analysis and Concept Mapping

**Step 2.1**: Identify core concepts and learning objectives

Extract or formulate:
- Primary concepts requiring mastery
- Fundamental terminology and definitions
- Key principles, theories, or methodologies
- Practical applications and use cases
- Complex analytical relationships
- Critical evaluation criteria
- Creative synthesis opportunities

**Step 2.2**: Assess content complexity

Determine appropriate difficulty distribution:
- **Beginner**: Foundational concepts, basic terminology, simple recall
- **Intermediate**: Conceptual understanding, application, comparative analysis
- **Advanced**: Complex analysis, critical evaluation, creative synthesis

**Step 2.3**: Map concepts to Bloom's Taxonomy levels

Systematically categorize identified concepts according to cognitive complexity:
- Level 1 (Remember): Facts, definitions, terminology, basic concepts
- Level 2 (Understand): Explanations, interpretations, relationships, examples
- Level 3 (Apply): Procedures, implementations, practical applications
- Level 4 (Analyze): Component relationships, structural analysis, differentiations
- Level 5 (Evaluate): Criteria-based judgments, critiques, assessments
- Level 6 (Create): Novel solutions, designs, integrated syntheses

### Phase 3: Flashcard Generation

**Step 3.1**: Generate 5-8 flashcards per Bloom's level

For each cognitive level, create flashcards following this structure:

```markdown
### [Bloom's Level]: [Question]

**Difficulty**: [Beginner | Intermediate | Advanced]

**Answer**:
[Concise, accurate response]

**Explanation**:
[Detailed elaboration providing context, rationale, and deeper understanding]

**Related Concepts**:
- [Concept 1]: [Brief relationship description]
- [Concept 2]: [Brief relationship description]

**Practice Hint** (for Analyze, Evaluate, Create levels):
[Scaffolding guidance to approach the question systematically]
```

**Step 3.2**: Ensure cognitive alignment

Verify each flashcard employs appropriate cognitive verbs:

- **Remember**: Define, identify, list, name, recall, recognize, state
- **Understand**: Describe, explain, interpret, paraphrase, summarize, classify
- **Apply**: Apply, demonstrate, execute, implement, solve, use
- **Analyze**: Analyze, compare, contrast, differentiate, distinguish, examine
- **Evaluate**: Assess, critique, evaluate, judge, justify, recommend
- **Create**: Create, design, develop, formulate, generate, synthesize

**Step 3.3**: Distribute difficulty appropriately

Across all flashcards, maintain approximate distribution:
- 40% Beginner (foundational understanding)
- 40% Intermediate (application and analysis)
- 20% Advanced (evaluation and creation)

### Phase 4: Quality Assurance

**Step 4.1**: Verify cognitive progression

Ensure flashcards demonstrate hierarchical cognitive progression from basic recall to creative synthesis.

**Step 4.2**: Validate accuracy

Confirm all factual content is accurate, current, and appropriately sourced.

**Step 4.3**: Assess pedagogical effectiveness

Verify that:
- Questions are clear, unambiguous, and appropriately scoped
- Answers are accurate and sufficiently detailed
- Explanations provide meaningful learning value
- Related concepts enhance conceptual network
- Practice hints facilitate problem-solving approaches

### Phase 5: Output Formatting and Delivery

**Step 5.1**: Structure the flashcard document

Organize the output markdown file with the following structure:

```markdown
# Flashcards: [Topic Title]

**Generated**: [Current Date]
**Cognitive Framework**: Bloom's Taxonomy
**Total Flashcards**: [Count]

---

## Level 1: Remember (Recall Knowledge)

[Flashcards 1-8 for Remember level]

---

## Level 2: Understand (Comprehension)

[Flashcards 1-8 for Understand level]

---

## Level 3: Apply (Application)

[Flashcards 1-8 for Apply level]

---

## Level 4: Analyze (Analysis)

[Flashcards 1-8 for Analyze level]

---

## Level 5: Evaluate (Evaluation)

[Flashcards 1-8 for Evaluate level]

---

## Level 6: Create (Synthesis)

[Flashcards 1-8 for Create level]

---

## Study Recommendations

[Provide brief guidance on how to use these flashcards effectively]
```

**Step 5.2**: Generate output file

Use the Write tool to create a markdown file named:
`[topic-name]-flashcards.md`

Where `[topic-name]` is the kebab-case version of the topic title.

**Step 5.3**: Deliver completion summary

Provide the user with:
- Confirmation of successful generation
- Total flashcard count (target: 30-48 flashcards)
- File path for the generated flashcard set
- Brief usage recommendations

## Advanced Features Implementation

### Difficulty Ratings

Assign difficulty based on:
- Cognitive level (higher levels tend toward intermediate/advanced)
- Concept complexity (specialized terminology, abstract concepts)
- Required prerequisite knowledge
- Multi-step reasoning requirements

### Answer Explanations

Elaborations shall:
- Provide contextual background
- Clarify reasoning processes
- Connect to broader conceptual frameworks
- Anticipate common misconceptions
- Reference authoritative principles where applicable

### Related Concepts

Identify and reference:
- Prerequisite knowledge required
- Parallel concepts in the same domain
- Applications in different contexts
- Contrasting or complementary principles

### Practice Hints

For higher-order cognitive levels (Analyze, Evaluate, Create), provide:
- Systematic approaches to problem decomposition
- Criteria to consider in evaluation
- Frameworks for generating novel solutions
- Questions to guide thinking processes

## Error Handling

**Insufficient Input**:
If the user provides neither a clear topic nor reference file, request:
- Specific topic title or subject area
- Optional reference file path for context

**Reference File Unavailable**:
If the specified reference file cannot be read:
- Inform the user of the file access issue
- Offer to proceed with topic-based generation using web research

**Topic Unfamiliarity**:
If the topic is highly specialized or obscure:
- Conduct thorough web research using WebSearch and WebFetch
- Inform the user that research-based generation is in progress
- Request user validation of accuracy for highly technical domains

## Quality Standards

All generated flashcards shall conform to:

1. **Bloom's Taxonomy Alignment**: Each flashcard correctly categorized by cognitive level
2. **Pedagogical Soundness**: Questions facilitate genuine learning, not mere memorization
3. **Factual Accuracy**: All content verified against authoritative sources
4. **Clarity**: Questions and answers are unambiguous and well-articulated
5. **Completeness**: All four components (question, answer, explanation, related concepts) present
6. **Appropriate Complexity**: Difficulty ratings accurately reflect cognitive demands
7. **Systematic Coverage**: 5-8 flashcards per level, balanced difficulty distribution

## Example Invocation Scenarios

**Scenario 1**: Topic-based generation
```
User: "Generate flashcards for Python list comprehensions"
Agent: [Conducts web research, generates 30-48 flashcards across Bloom's levels]
```

**Scenario 2**: Reference file-based generation
```
User: "Create flashcards from my notes on machine learning at notes/ml-basics.md"
Agent: [Reads file, extracts concepts, generates structured flashcards]
```

**Scenario 3**: Combined approach
```
User: "Generate flashcards for quantum computing based on lecture-notes.pdf"
Agent: [Reads PDF, supplements with web research, generates comprehensive flashcard set]
```

## References

This skill implements pedagogical principles derived from:
- Bloom's Taxonomy of Educational Objectives (Bloom et al., 1956; Anderson & Krathwohl, 2001)
- Cognitive science principles of spaced repetition and active recall
- Evidence-based learning strategies for long-term retention
