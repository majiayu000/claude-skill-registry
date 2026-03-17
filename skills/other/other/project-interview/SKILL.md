---
name: project-interview
description: Deep interview process to define project fundamentals. Triggers on "Interview me about this project", "Interview me about the project", "Let's define the project".
globs: ["docs/project.md", "*.md"]
---

# Project Interview (Fase 0)

Transform a rough project idea into a comprehensive project definition through exhaustive interviewing.

## Triggers

- "Interview me about this project"
- "Interview me about the project"
- "Let's define the project"
- "Help me define this project"
- `/project-interview`

## Purpose

Before any feature work begins, we need crystal clear answers to:
- **What** are we building?
- **Who** is it for?
- **Why** does it need to exist?
- **How** will it work technically?
- **What** are the constraints?

## Interview Protocol

### 1. Read Existing Context

```bash
# Check if project.md exists and has content
cat docs/project.md 2>/dev/null || echo "No project.md yet"

# Check for any existing notes
ls -la docs/ 2>/dev/null
```

### 2. Interview Categories

#### A. Vision & Problem (Start here)
- "What problem are you solving? Who has this problem today?"
- "How do they solve it now? What's painful about that?"
- "In one sentence, what is this project?"
- "What does success look like in 6 months?"

#### B. Users & Personas
- "Who are the primary users? Describe them."
- "Are there secondary users or admins?"
- "What's their technical level?"
- "How will they discover and access this?"

#### C. Core Functionality
- "What are the 3-5 things a user MUST be able to do?"
- "Walk me through the main user flow step by step."
- "What's the ONE thing that makes this valuable?"

#### D. Technical Constraints
- "What's your preferred tech stack? Any hard requirements?"
- "Where will this run? (Cloud, on-prem, local)"
- "Any integrations required? (APIs, databases, services)"
- "Performance requirements? Expected scale?"
- "Security/compliance needs? (Auth, data privacy, regulations)"

#### E. Scope & Timeline
- "What's the deadline or target launch?"
- "What's explicitly OUT of scope for v1?"
- "Budget constraints? (infra, APIs, services)"
- "Solo project or team?"

#### F. Risks & Unknowns
- "What's the biggest risk to this project?"
- "What are you most uncertain about?"
- "What could kill this project?"

### 3. Interview Rules

```
INTERVIEW RULES

1. Maximum 3-4 questions per turn
   Let user think and respond fully

2. Start broad, then drill down
   Vision -> Users -> Features -> Technical -> Constraints

3. Document IMMEDIATELY
   Update docs/project.md after each response

4. Propose defaults for unknowns
   "I'd recommend X because Y. Sound good?"

5. Challenge vague answers
   "You said 'fast'. What does fast mean? <1s? <100ms?"

6. Summarize before moving on
   "So far: [summary]. Correct? Moving to technical questions."
```

### 4. Update project.md Structure

After gathering answers, structure docs/project.md with all sections filled.

### 5. Completion Check

Before ending, verify:
- [ ] Vision is crystal clear (one sentence)
- [ ] Users are defined
- [ ] MVP features are listed (3-5 max)
- [ ] Tech stack is decided
- [ ] Constraints are documented
- [ ] Out of scope is explicit
- [ ] No major unknowns remain

### 6. Handoff

When interview complete:

```
Project interview complete. docs/project.md updated.

Next steps:
1. "Help me define the architecture" -> Creates ADRs and architecture docs
2. "Define MVP features" -> Creates feature folders with /new-feature

Or run both: "Let's define architecture and MVP features"
```
