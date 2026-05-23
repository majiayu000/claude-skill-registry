---
name: interactive-requirements-gathering
description: Structured interactive questionnaire framework for gathering requirements from users. Uses A/B/C/D/E multiple choice patterns with additive vs exclusive question classification.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, AskUserQuestion]
best_practices:
  - Ask questions one at a time, never multiple at once
  - Classify each question as Additive or Exclusive before asking
  - Always include "Type your own" and "Auto-generate" options
  - Confirm understanding before moving to next question
  - Use gathered answers (not options) as source of truth for generation
error_handling: graceful
streaming: supported
---

# Interactive Requirements Gathering

Structured framework for gathering requirements through interactive questionnaires. Based on the Conductor methodology's proven human-in-the-loop patterns.

## When to Use

- Setting up new projects
- Defining product requirements
- Gathering feature specifications
- Onboarding users to new workflows
- Any task requiring structured user input

## Core Principles

### 1. Question Classification

Before asking ANY question, classify its type:

| Type          | Purpose                               | Phrasing                | Example                          |
| ------------- | ------------------------------------- | ----------------------- | -------------------------------- |
| **Additive**  | Brainstorming, multiple answers valid | "Select all that apply" | "Which features do you need?"    |
| **Exclusive** | Single choice required                | No multi-select phrase  | "Which framework should we use?" |

### 2. Question Structure

All questions MUST follow this structure:

```
[Question text]

A) [Option A - often recommended, marked with "(Recommended)"]
B) [Option B]
C) [Option C]
D) Type your own answer
E) Auto-generate and continue
```

### 3. Sequential Questioning

**CRITICAL**: Ask ONE question at a time. Wait for response before next question.

```
CORRECT:
1. Ask Question 1
2. Wait for response
3. Confirm understanding
4. Ask Question 2

INCORRECT:
1. Ask Questions 1, 2, and 3 together
```

## Questionnaire Workflow

### Step 1: Introduction

Announce the section you're working on:

```
"I'll now help you define [section name]. I'll ask a few questions to understand your needs."
```

### Step 2: Sequential Questions

For each question:

1. **Classify**: Is this Additive or Exclusive?
2. **Formulate**: Create clear question with options
3. **Present**: Show options in A/B/C/D/E format
4. **Wait**: Do NOT proceed without response
5. **Confirm**: Summarize understanding before continuing

### Step 3: Handle Special Options

**Option D (Type your own)**:

- Accept user's custom input
- Confirm the custom response
- Continue to next question

**Option E (Auto-generate)**:

- Stop asking questions for this section
- Use best judgment based on previous answers
- Generate content and present for review

### Step 4: Generate Content

**CRITICAL**: Use ONLY the user's selected answers as source of truth.

```
CORRECT:
- User selected "OAuth 2.0" -> Generate OAuth implementation details

INCORRECT:
- Include Option A, B, C text that wasn't selected
- Include question text in generated content
```

### Step 5: User Confirmation Loop

After generating content:

```
"I've drafted [document name]. Please review:"

[Content preview]

What would you like to do?
A) Approve - proceed to next step
B) Suggest Changes - tell me what to modify

Please respond with A or B.
```

Loop until approved or user provides alternative direction.

## Question Patterns

### Product Vision Questions (Additive)

```
What are the primary goals of this product? (Select all that apply)

A) Improve user productivity
B) Reduce operational costs
C) Enhance customer experience
D) Type your own answer
E) Auto-generate and continue
```

### Technology Selection Questions (Exclusive)

```
Which database should we use?

A) PostgreSQL (Recommended) - Best for relational data with complex queries
B) MongoDB - Document store for flexible schemas
C) SQLite - Lightweight for small applications
D) Type your own answer
E) Auto-generate and continue
```

### Feature Scoping Questions (Additive)

```
Which authentication methods should be supported? (Select all that apply)

A) Email/Password
B) OAuth (Google, GitHub)
C) Magic Links
D) Type your own answer
E) Auto-generate and continue
```

## Integration with AskUserQuestion Tool

When using the AskUserQuestion tool, map to this framework:

```javascript
AskUserQuestion({
  questions: [
    {
      header: 'Database',
      question: 'Which database should we use?',
      multiSelect: false, // Exclusive question
      options: [
        { label: 'PostgreSQL (Recommended)', description: 'Best for relational data' },
        { label: 'MongoDB', description: 'Document store for flexible schemas' },
        { label: 'SQLite', description: 'Lightweight for small apps' },
      ],
    },
  ],
});
```

## State Persistence

For multi-step questionnaires, save progress:

```json
{
  "last_successful_step": "2.1_product_guide",
  "answers": {
    "product_type": "SaaS",
    "target_users": ["developers", "teams"]
  }
}
```

This enables resuming interrupted workflows.

## Example Session

```
AGENT: "I'll help you define the product vision. First question:"

"Who are the primary users of this product?"

A) Developers
B) Business users
C) End consumers
D) Type your own answer
E) Auto-generate and continue

USER: A, B

AGENT: "Got it - targeting developers and business users. Next question:"

"What problem does this product solve?"

A) Streamlines workflows
B) Reduces manual work
C) Improves collaboration
D) Type your own answer
E) Auto-generate and continue

USER: D - "Automates code review feedback"

AGENT: "Understood - the product automates code review feedback for developers and business users. Let me generate the product vision..."
```

## Anti-Patterns

### Do NOT:

- Ask multiple questions at once
- Include unselected options in generated content
- Skip confirmation steps
- Assume answers without asking
- Use technical jargon in options without explanation

### Do:

- One question at a time
- Clear, concise option descriptions
- Summarize understanding frequently
- Include escape hatches (D, E options)
- Respect user's custom inputs

## Related Skills

- `project-onboarding` - Use this framework during project setup
- `context-driven-development` - Generate context artifacts from answers
- `brainstorming` - Alternative for open-ended exploration

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
