---
name: project-creator
description: "Project documentation scaffolding. Covers about.md, specs.md, architecture.md, project-context.md, and user stories. Keywords: project setup, documentation, specs, architecture, stories."
metadata:
  author: itechmeat
  version: "1.0.0"
---

# Project Creator

Guide creation and maintenance of project documentation in `.project/` folder.

## Quick Navigation

- **Templates**: `assets/` folder
- **Guides**: `references/` folder

## When to Use

- Starting a new project
- Creating/updating `.project/` documentation
- Planning user stories

## Project Structure

```
.project/
├── about.md              # Project overview, goals, target audience
├── specs.md              # Technical specifications, versions
├── architecture.md       # System architecture with diagrams
├── project-context.md    # Cumulative decisions (optional)
└── stories/
    ├── stories.md        # Master list
    └── 001-story-name.md # Individual stories
```

## Assets (Templates)

| Template | File | Purpose |
|----------|------|---------|
| About | `assets/about-template.md` | Project overview |
| Specs | `assets/specs-template.md` | Technical specs |
| Architecture | `assets/architecture-template.md` | System architecture |
| Context | `assets/project-context-template.md` | Project context |
| Stories List | `assets/stories-template.md` | Stories master list |
| Story | `assets/story-template.md` | Individual story |

## Guides (References)

| Guide | File | Purpose |
|-------|------|---------|
| About | `references/about-guide.md` | Questions & criteria |
| Specs | `references/specs-guide.md` | Questions & criteria |
| Architecture | `references/architecture-guide.md` | Questions & criteria |
| Context | `references/context-guide.md` | Questions & criteria |
| Stories | `references/stories-guide.md` | Questions & criteria |

## Document Dependencies

```
about.md → specs.md → architecture.md → project-context.md → stories/
```

---

## Workflow per Document

### Standard Flow

1. Load guide from `references/`
2. Check if document exists — read and assess if yes
3. Create/update using template from `assets/`
4. Interview user with questions from guide
5. Draft content based on responses
6. Present draft, ask for feedback
7. Iterate until user confirms
8. Move to next document

### Existing Documents

When documents already exist:
- Read and assess completion state
- Ask user: review/update or skip?
- Build on existing content — don't recreate
- Note gaps or inconsistencies

---

## Communication Style

### Always Do

- Ask one topic at a time
- Offer 2-3 formulation variants
- Explain technical concepts simply
- Summarize understanding before drafting
- Confirm before moving to next step

### Never Do

- Assume answers
- Skip confirmation steps
- Use jargon without explanation
- Move to next document without confirmation
- Write specs without verifying latest versions

---

## Example Interaction

```
Agent: Let's start with about.md. Can you describe what this project does in your own words?

User: It's an app for tracking expenses.

Agent: Great start! Here are some formulation options:

  1. "A personal finance app for tracking daily expenses"
  2. "An expense tracker that helps users manage spending"
  3. "A mobile app for recording and categorizing expenses"

  Which resonates most? Or combine elements?

User: Option 2, but for small businesses, not personal.

Agent: Updated formulation:

  "An expense tracker that helps small businesses 
  manage spending and categorize business expenses."

  Does that capture it? Should we add reporting 
  or team features?
```

---

## Critical Rules

- **NEVER** assume project details — always ask
- **ALWAYS** offer formulation variants
- **ALWAYS** validate understanding with user
- **NEVER** proceed without user confirmation
- **ALWAYS** use templates from `assets/`
- **NEVER** allow version downgrades (only upgrades)

---

## Example Questions

Questions are **examples** — adapt to each unique project:

### About.md
- Can you describe your project in one sentence?
- What frustration does this solve for users?
- If you could only build 3 features, what would they be?
- How will you know if the project is successful?
- What will this project definitely NOT do?

### Specs.md
- What devices/browsers must be supported?
- How many concurrent users do you expect?
- Is there existing infrastructure to integrate with?
- What's the team's experience with [technology]?
- Are there any compliance requirements?

### Architecture.md
- What are the main parts of the system?
- How should components communicate?
- What data flows exist?
- How will it scale?
- How is it secured?

### Stories
- What's absolutely essential for launch?
- What can wait until later?
- What's the logical order of features?
- Does feature X need feature Y first?

---

## Helping Non-Technical Users

When user lacks technical knowledge:

1. **Explain options simply**
  - "React is great for interactive UIs, Vue is simpler to learn"
  - "PostgreSQL is reliable for structured data, MongoDB for flexible schemas"

2. **Use analogies**
  - "The API is like a waiter taking orders to the kitchen"
  - "The database is like a filing cabinet"
  - "The cache is like a notepad for quick lookups"

3. **Make recommendations with reasoning**
  - "Given your expected user count, I recommend..."
  - "Since you need real-time updates, this pattern..."

4. **Explain trade-offs**
  - Performance vs. simplicity
  - Feature richness vs. learning curve
  - Cost vs. scalability
