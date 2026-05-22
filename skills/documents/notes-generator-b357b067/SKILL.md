---
name: notes-generator
description: |
  Generate structured study notes following Bloom's Taxonomy methodology. Creates
  comprehensive notes from topic titles or reference files. Use when user asks to
  "create notes", "generate notes", "make study notes", or wants notes on a topic.
---

# Notes Generator

Generate study notes following Bloom's Taxonomy cognitive levels for effective learning.

## Workflow

1. Identify input: topic title OR reference file path
2. If reference file provided, read and extract key concepts
3. Structure notes using Bloom's Taxonomy levels
4. Save to `/notes/` directory with proper formatting

## Bloom's Taxonomy Structure

Apply these cognitive levels in order, from foundational to advanced:

### Level 1: Remember (Knowledge)
- Define key terms and concepts
- List fundamental facts
- State basic principles
- Format: bullet points, definitions

### Level 2: Understand (Comprehension)
- Explain concepts in your own words
- Describe relationships between ideas
- Summarize main points
- Provide analogies or metaphors

### Level 3: Apply (Application)
- Show practical examples
- Demonstrate use cases
- Include code snippets (if technical)
- Describe real-world scenarios

### Level 4: Analyze (Analysis)
- Break down complex concepts into parts
- Compare and contrast related ideas
- Identify patterns and relationships
- Examine cause and effect

### Level 5: Evaluate (Evaluation)
- Assess strengths and limitations
- Compare approaches or solutions
- Identify best practices
- Note common pitfalls or misconceptions

### Level 6: Create (Synthesis)
- Suggest extensions or applications
- Propose practice exercises
- Include thought-provoking questions
- Recommend further learning resources

## Note Template

```markdown
# [Topic Title]

## Overview
Brief introduction to the topic (2-3 sentences).

## Key Concepts (Remember)
- **Term 1**: Definition
- **Term 2**: Definition
- Key fact or principle

## Understanding the Concepts (Understand)
Explanation of how concepts work and relate to each other.

## Practical Applications (Apply)
### Example 1
[Concrete example with explanation]

### Example 2
[Another practical scenario]

## Deep Dive (Analyze)
### Component Breakdown
- Part A: [explanation]
- Part B: [explanation]

### Relationships
How different parts interact or depend on each other.

## Critical Assessment (Evaluate)
### Strengths
- [Advantage 1]
- [Advantage 2]

### Limitations
- [Limitation 1]
- [Limitation 2]

### Best Practices
- [Practice 1]
- [Practice 2]

## Extend Your Learning (Create)
### Practice Questions
1. [Question that requires synthesis]
2. [Question that applies knowledge]

### Further Exploration
- [Related topic or resource]
- [Advanced concept to explore]

## References
- [Source 1]
- [Source 2]
```

## Instructions

### When Given a Topic Title

1. Research the topic using available knowledge
2. Structure content following the Bloom's Taxonomy template
3. Include relevant examples and applications
4. Save to `/notes/[topic-name].md`

### When Given a Reference File

1. Read the reference file from `/lessons/` or provided path
2. Extract the source filename (without extension)
3. Extract key concepts and main ideas
4. Transform content into Bloom's Taxonomy structure
5. Enrich with examples and analysis
6. Save to `/notes/[source-filename].md` (preserving original filename for traceability)

### Naming Convention

**Priority: Use source filename for traceability**

| Input Type | Output Filename | Example |
|------------|-----------------|---------|
| File path: `lessons/lesson1.md` | `/notes/lesson1.md` | Maintains traceability |
| File path: `lessons/chapter-02.md` | `/notes/chapter-02.md` | Maintains traceability |
| Topic title: "REST APIs" | `/notes/rest-apis.md` | Derived from topic |

**Rules:**
- When file path provided: Extract filename, keep exact name (minus extension)
- When topic provided: Convert to lowercase with hyphens
- This ensures clear mapping: `lessons/X.md` → `notes/X.md`

## Quality Checklist

Before completing notes:
- [ ] All six Bloom's Taxonomy levels addressed
- [ ] Clear, professional language used
- [ ] Practical examples included
- [ ] No personal opinions (factual content only)
- [ ] Proper markdown formatting
- [ ] Saved to `/notes/` directory

## Example Output

**Example 1 - From file:**
**Input:** `lessons/lesson1.md`
**Output:** `/notes/lesson1.md`

**Example 2 - From topic:**
**Input:** "Create notes on REST APIs"
**Output:** `/notes/rest-apis.md`

```markdown
# REST APIs

## Overview
REST (Representational State Transfer) is an architectural style for
designing networked applications using HTTP protocols.

## Key Concepts (Remember)
- **REST**: Architectural style for web services
- **Endpoint**: URL where API resources are accessed
- **HTTP Methods**: GET, POST, PUT, DELETE, PATCH
- **Resource**: Any data entity exposed via API
- **Stateless**: Each request is independent

## Understanding the Concepts (Understand)
REST APIs work by mapping CRUD operations to HTTP methods...
[continues following the template]
```
