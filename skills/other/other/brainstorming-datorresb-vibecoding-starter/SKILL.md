---
name: brainstorming
description: Collaborative ideation-to-spec refinement via one-question-at-a-time dialogue. Use before implementing new features, changing behavior, or starting complex refactors. Always produces a design document.
---

# Brainstorming Ideas Into Designs

## Overview

Turn rough ideas into a validated design/spec through short, collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

> **⚠️ IMPORTANT:** This skill produces a **design document only**. Implementation is a separate step that the user decides when and how to do.

## The Process

**Understand the idea**
- Review current project state first (files, docs, recent commits, existing patterns)
- Ask **one question per message**; if a topic needs more exploration, split it across multiple turns
- Prefer multiple-choice questions when practical (faster to answer), but use open-ended when needed
- Focus on purpose, constraints, success criteria, and non-goals

### Interactive Questions with `ask_questions` Tool

MUST Use the `ask_questions` tool for a more interactive and efficient dialogue. This provides a native UI for the user to select options or input text.

#### Tool Parameters

| Parameter | Description |
|-----------|-------------|
| `header` | Short label (max 12 chars) - used as identifier |
| `question` | Full question text to display |
| `options` | Array of 0-6 options with `label` and optional `description` |
| `multiSelect` | Allow multiple selections (default: false) |
| `allowFreeformInput` | Allow free text in addition to options |
| `recommended` | Mark an option as recommended (**never use for quizzes**) |

#### Rules
- Maximum **4 questions** per call (batch related questions)
- **"Other"** option is added automatically — don't add it manually
- Use `recommended` only to suggest YOUR preferred implementation choice
- Omit `options` array for free text input

#### Example: Multiple Choice

```json
{
  "questions": [{
    "header": "Approach",
    "question": "Which architecture approach should we use?",
    "options": [
      {"label": "Monolith", "description": "Simple, single deployment"},
      {"label": "Microservices", "description": "Scalable, complex"},
      {"label": "Modular Monolith", "description": "Best of both", "recommended": true}
    ]
  }]
}
```

#### Example: Open-Ended

```json
{
  "questions": [{
    "header": "Goal",
    "question": "What is the main goal of this feature?",
    "allowFreeformInput": true
  }]
}
```

#### Example: Batched Questions

```json
{
  "questions": [
    {
      "header": "Priority",
      "question": "What's the priority for this feature?",
      "options": [
        {"label": "High - needed this sprint"},
        {"label": "Medium - next sprint"},
        {"label": "Low - backlog"}
      ]
    },
    {
      "header": "Scope",
      "question": "Should we include admin features?",
      "options": [
        {"label": "Yes, full admin panel"},
        {"label": "Yes, basic controls only"},
        {"label": "No, user-facing only", "recommended": true}
      ]
    }
  ]
}
```

### Fallback: Markdown Questions
When the tool is unavailable or for documentation, use this markdown format:

##### **Template (multiple-choice)**

    **Question: <short title>**
    <One-sentence context. **Optional**>

    **Choose one:**
    **A)** <option>
    **B)** <option>
    ...

    **Reply with:** A / B / ...

**Explore approaches**
- Propose 2-3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Keep options meaningfully different (not tiny variants)

**Present the design**
- Present in sections of ~200-300 words
- After each section, ask if it looks right so far before continuing
- Cover: architecture, components, data flow, error handling, testing, and rollout (if relevant)

## Output: Design Document (MANDATORY)

**This step is NOT optional.** Every brainstorming session MUST produce a written design document.

1. **Write the design document:**
   - Save to `docs/plans/YYYY-MM-DD-<topic>-design.md`
   - If `docs/plans/` doesn't exist, create it or ask user for preferred location
   - Include: objective, architecture, specifications from each section, success criteria

2. **Document structure:**
   ```markdown
   # <Topic> Design
   
   **Date:** YYYY-MM-DD
   **Status:** Validated
   
   ## Objective
   [What we're building and why]
   
   ## Architecture / Approach
   [Chosen approach with rationale]
   
   ## Specifications
   [Details from each design section]
   
   ## Implementation Order
   [Recommended sequence of tasks]
   
   ## Success Criteria
   - [ ] Criterion 1
   - [ ] Criterion 2
   ```

3. **Confirm with user:** "Design saved to `docs/plans/...`. Ready for implementation?"

## After the Design: Implementation (USER'S CHOICE)

**Implementation is optional and at user's discretion.** Do NOT start implementing unless explicitly asked.

When user wants to implement, recommend these approaches:

| Approach | When to use | How |
|----------|-------------|-----|
| **bd (beads)** | Task tracking, team visibility | `bd create "<task>"` for each item in Implementation Order |
| **PRD** | Complex features, stakeholder alignment | Create `docs/prd/YYYY-MM-DD-<topic>.md` with full requirements |
| **Direct tasks** | Simple, quick implementations | Use `task-delegation` skill to delegate to subagents |
| **Issues** | GitHub/GitLab workflow | Create issues from Implementation Order |

**If user asks to implement:**
1. Use ask_questions:
   ```json
   {
     "questions": [{
       "header": "Tracking",
       "question": "How would you like to track implementation?",
       "options": [
         {"label": "Create bd tasks", "description": "For task tracking and team visibility"},
         {"label": "Create GitHub issues", "description": "Standard GitHub workflow"},
         {"label": "Delegate to subagents", "description": "Quick, direct implementation"},
         {"label": "I'll handle it manually"}
       ]
     }]
   }
   ```
2. Follow their choice
3. Do NOT implement yourself unless explicitly delegated

**Before making changes:**
- If the repo uses branching/worktrees, create an isolated workspace before making changes
- Produce an implementation plan with clear, verifiable tasks and checkpoints
- Each task should have explicit success criteria that can be verified

## Key Principles

- **Use `ask_questions` tool** for interactive, efficient dialogue
- **One question at a time** (or batch up to 4 related questions)
- **Multiple choice preferred** when it doesn't reduce clarity
- **YAGNI ruthlessly** (delete unnecessary scope)
- **Explore alternatives** before committing
- **Incremental validation** (design in sections)
- **Be flexible** (backtrack and clarify when needed)
- **Always document** — no design lives only in chat
- **Never auto-implement** — design and implementation are separate concerns

