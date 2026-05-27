---
name: decisions
description: Guide for recording significant architectural and design decisions in docs/decisions.md. Use this skill when clearly significant architectural decisions are made (database choices, frameworks, core design patterns) or when explicitly asked to document a decision. Be conservative - only suggest for major decisions, not minor implementation details.
license: MIT
---

# Decisions

## Overview

This skill maintains a chronological record of significant project decisions in `docs/decisions.md`. It captures important architectural and design decisions, especially those involving tradeoffs, to create a permanent record of why key choices were made.

## When to Use This Skill

**Proactive (Conservative):**
Suggest recording decisions only when there is a clearly significant architectural choice, such as:
- Choosing between database systems (e.g., SQLite vs PostgreSQL)
- Selecting major frameworks or libraries
- Deciding on core architectural patterns (e.g., monolith vs microservices, rendering approach)
- Making fundamental design choices that will shape the project long-term

**Do NOT proactively suggest for:**
- Minor implementation details
- Routine coding decisions
- Small refactoring choices
- Trivial technical choices

**Manual:**
Record decisions when explicitly requested by the user with phrases like:
- "Record this decision"
- "Document this in the decision log"
- "Add this to decisions.md"

## Recording a Decision

### Step 1: Identify the Decision

From the conversation context, identify:
- What decision was made
- Why it was needed (context)
- What alternatives were considered (if applicable)
- Key tradeoffs evaluated (if applicable)
- Rationale for the final choice

### Step 2: Determine Detail Level

Adapt the level of detail based on decision complexity:

**Brief** (simple decisions):
- Title and 1-2 sentence summary
- Example: Choosing a well-established library

**Moderate** (typical decisions):
- Decision description
- Brief context (why it was needed)
- The choice made

**Detailed** (complex decisions):
- Decision description
- Context and motivation
- Alternatives considered
- Key tradeoffs evaluated
- Rationale for final choice

### Step 3: Format the Entry

Use this format:

```markdown
## YYYY-MM-DD: [Decision Title]

[Description paragraph(s) adapted to the complexity level]
```

Example (brief):
```markdown
## 2025-10-23: Use httprouter for HTTP routing

Chose httprouter for its simplicity and performance. It's a well-established library that fits our needs without unnecessary complexity.
```

Example (detailed):
```markdown
## 2025-10-23: Choose SQLite for primary database

After evaluating PostgreSQL and SQLite, we chose SQLite for the following reasons:

Context: Need a reliable database for the application that handles moderate traffic (< 1000 concurrent users) and simple relational data.

Alternatives considered:
- PostgreSQL: More features and better for high concurrency, but adds operational complexity
- SQLite: Simpler deployment, embedded database, sufficient performance for our scale

Tradeoffs: SQLite has limitations with high write concurrency and some advanced features, but offers zero-configuration deployment and excellent read performance. Given our expected load and preference for operational simplicity, these tradeoffs favor SQLite.

Decision: Use SQLite with WAL mode enabled for improved concurrency. We can migrate to PostgreSQL later if scaling needs change.
```

### Step 4: Write to File

1. Check if `docs/` directory exists; create it if needed
2. Check if `docs/decisions.md` exists:
   - If not, create it with this header:
     ```markdown
     # Project Decisions

     This document records significant architectural and design decisions made throughout the project's development.

     ```
   - If it exists, read the current content
3. Append the new decision entry to the bottom of the file
4. Ensure proper spacing (blank line before the new entry)

### Step 5: Confirm with User

After recording the decision, briefly confirm what was recorded. For example:
- "Recorded the decision to use SQLite in docs/decisions.md"
- "Added the routing decision to the decision log"

## Proactive Suggestion Pattern

When detecting a significant architectural decision during conversation, suggest recording it:

```
This seems like a significant architectural decision. Would you like me to record it in docs/decisions.md?
```

Wait for user confirmation before recording.

## Important Notes

- Always append to the bottom (chronological order from oldest to newest)
- Use today's date (YYYY-MM-DD format) for new entries
- Maintain formatting consistency with existing entries
- Don't create duplicate entries for the same decision
- Create `docs/` directory if it doesn't exist
- Avoid recording trivial decisions that don't have long-term architectural impact
