---
name: generate-flashcards
description: |
  Generate flashcards focused on core terminology and vocabulary from lessons or topics.
  Creates Q&A format cards for effective memorization. Use when user asks to "create
  flashcards", "generate flashcards", "make vocabulary cards", or wants to memorize terms.
---

# Generate Flashcards

Create flashcards from lesson files or topic titles, focusing on essential terminology and vocabulary required for understanding and retention.

## Workflow

1. Identify input: lesson file path OR topic title
2. If lesson file provided, read and extract key terminology
3. Identify core concepts that require memorization
4. Generate Q&A flashcard pairs
5. Save to `/flashcard/` directory

## Flashcard Categories

Extract terminology across these categories:

### Definitions
- Key terms and their meanings
- Technical vocabulary
- Domain-specific concepts

### Acronyms & Abbreviations
- Spell out full forms
- Explain what each represents

### Relationships
- How concepts connect
- Cause and effect pairs
- Comparisons (X vs Y)

### Core Facts
- Essential facts that must be memorized
- Foundational principles
- Key formulas or rules

## Flashcard Format

Use this Q&A format (one per line, alternating):

```
Q: [Question about the term/concept]
A: [Concise, accurate answer]

Q: [Next question]
A: [Next answer]
```

### Question Types

| Type | Template | Example |
|------|----------|---------|
| Definition | What is [term]? | Q: What is AI Fluency? |
| Acronym | What does [acronym] stand for? | Q: What does REST stand for? |
| Purpose | What is the purpose of [concept]? | Q: What is the purpose of Delegation in the 4D Framework? |
| Distinction | What is the difference between [A] and [B]? | Q: What is the difference between Automation and Augmentation? |
| Component | What are the components of [concept]? | Q: What are the 4Ds in the AI Fluency Framework? |

## Quality Guidelines

### Good Flashcards
- One concept per card
- Question is specific and unambiguous
- Answer is concise (1-2 sentences max)
- Tests recall, not recognition
- Uses precise terminology

### Avoid
- Multiple concepts in one card
- Vague or overly broad questions
- Lengthy paragraph answers
- Yes/no questions
- Questions with obvious answers

## Output Template

```markdown
# [Topic] - Flashcards

## Core Terminology

Q: [Term definition question]
A: [Definition]

Q: [Next term]
A: [Definition]

## Key Concepts

Q: [Concept question]
A: [Explanation]

## Relationships & Comparisons

Q: [Comparison question]
A: [Distinction]

---
Source: [lesson file or topic]
Card count: [number]
```

## Naming Convention

**Priority: Use source filename for traceability**

| Input Type | Output Filename | Example |
|------------|-----------------|---------|
| File path: `lessons/lesson1.md` | `/flashcard/lesson1-flashcards.md` | Maintains traceability |
| File path: `lessons/chapter-02.md` | `/flashcard/chapter-02-flashcards.md` | Maintains traceability |
| Topic title: "REST APIs" | `/flashcard/rest-apis-flashcards.md` | Derived from topic |

**Rules:**
- When file path provided: Extract filename (minus extension), append `-flashcards`
- When topic provided: Convert to lowercase with hyphens, append `-flashcards`
- This ensures clear mapping: `lessons/X.md` → `flashcard/X-flashcards.md`

## Example Output

**Example 1 - From file:**
**Input:** `lessons/lesson1.md`
**Output:** `/flashcard/lesson1-flashcards.md`

**Example 2 - From topic:**
**Input:** "REST APIs"
**Output:** `/flashcard/rest-apis-flashcards.md`

```markdown
# REST APIs - Flashcards

## Core Terminology

Q: What is REST?
A: Representational State Transfer - an architectural style for designing networked applications using HTTP protocols.

Q: What is an API endpoint?
A: A URL where API resources can be accessed.

Q: What does "stateless" mean in REST?
A: Each request is independent and contains all information needed; the server doesn't store client state between requests.

## Key Concepts

Q: What are the four main HTTP methods in REST?
A: GET (retrieve), POST (create), PUT (update), DELETE (remove).

Q: What is a resource in REST?
A: Any data entity that can be accessed and manipulated through the API.

## Relationships & Comparisons

Q: What is the difference between PUT and PATCH?
A: PUT replaces the entire resource; PATCH updates only specific fields.

---
Source: lessons/rest-api.md
Card count: 6
```

## Checklist

Before completing flashcards:
- [ ] All key terms from source material included
- [ ] One concept per card
- [ ] Answers are concise and accurate
- [ ] Questions test recall (not recognition)
- [ ] Saved to `/flashcard/` directory
- [ ] Card count noted at bottom
