---
name: brainstorm
description: Transform ideas into fully-formed designs through collaborative dialogue. This skill should be used when brainstorming features, exploring implementation approaches, designing system architecture, or when the user has a vague idea that needs refinement. Uses incremental validation with 200-300 word sections.
---

# Brainstorm

Transform ideas into fully-formed designs and specs through natural collaborative dialogue.

## When to Use

- User has an idea that needs refinement ("I want to add...")
- Feature requires design exploration before implementation
- Multiple valid approaches exist and trade-offs need evaluation
- Requirements are unclear or partially defined
- User explicitly asks to brainstorm, design, or spec out a feature

## The Process

### Phase 1: Context Gathering

Before asking questions, understand the current state:

```
1. Check project structure (Glob key directories)
2. Review recent commits (git log --oneline -10)
3. Read relevant existing code/docs
4. Identify patterns and conventions already in use
```

### Phase 2: Idea Refinement

**Core Principle: One question at a time.**

Ask questions to understand the idea. Prefer multiple-choice when possible:

```
Use AskUserQuestion with:
- 2-4 options per question
- Clear, mutually exclusive choices
- Your recommended option first (with reasoning)
```

**Question Categories:**

| Category | Example Questions |
|----------|-------------------|
| Purpose | What problem does this solve? Who benefits? |
| Constraints | Must integrate with X? Budget/time limits? |
| Success | How do we know it worked? Key metrics? |
| Scope | What's explicitly NOT included? |
| Prior Art | Seen similar elsewhere? What worked/didn't? |

**Exit Criteria:** Stop asking when purpose, constraints, and success criteria are clear.

### Phase 3: Approach Exploration

Present 2-3 approaches with trade-offs:

```markdown
## Approach A: [Name] (Recommended)
- **Pros**: ...
- **Cons**: ...
- **Best when**: ...

## Approach B: [Name]
- **Pros**: ...
- **Cons**: ...
- **Best when**: ...
```

**Lead with recommendation** and explain why. Ask user to confirm or discuss.

### Phase 4: Incremental Design Presentation

Once approach is selected, present the design in sections:

**CRITICAL: Each section must be 200-300 words max.**

After each section, ask:
> "Does this section look right so far? Any adjustments needed?"

**Section Order:**

1. **Overview** - Goal, scope, success metrics
2. **Architecture** - Components, data flow, boundaries
3. **Data Model** - Schema, relationships (if applicable)
4. **Error Handling** - Failure modes, recovery strategies
5. **Testing Strategy** - What to test, how to test

Only proceed to next section after user confirms current section.

**Be flexible:** If something doesn't make sense, go back and clarify. The process is not rigid.

### Phase 5: Documentation

After all sections validated:

1. Compile into single design document
2. Use `elements-of-style` skill for clarity
3. Write to `docs/plans/YYYY-MM-DD-<topic>-design.md`
4. Commit the design document to git

### Phase 6: Implementation Setup (Optional)

After documentation is complete, ask:

> "Ready to set up for implementation?"

If yes:
1. Use `using-git-worktrees` to create isolated workspace
2. Use `/plan-feature` command to create detailed implementation plan with TDD tasks

## Question Patterns

### Good Questions (Multiple Choice)

```
AskUserQuestion:
  question: "How should we handle failed API calls?"
  options:
    - label: "Retry with backoff (Recommended)"
      description: "Automatic retry 3x with exponential backoff. Best for transient failures."
    - label: "Fail immediately"
      description: "Return error to user right away. Simpler but less resilient."
    - label: "Queue for later"
      description: "Store and retry in background. Good for non-critical operations."
```

### Good Questions (Open-ended)

Use when options aren't clear-cut:

- "What existing functionality should this integrate with?"
- "Are there any similar features in other products you'd like to emulate?"
- "What's the worst-case failure scenario we need to handle?"

## YAGNI Ruthlessly

During design, actively remove unnecessary features:

| Red Flag | Question to Ask |
|----------|-----------------|
| "It might be useful to..." | "Do we need this for MVP?" |
| "We could also add..." | "Is this solving the stated problem?" |
| "Just in case..." | "What's the likelihood this is needed?" |
| "This would be nice..." | "Is this a requirement or a want?" |

**Default answer: Remove it.** Can always add later.

## Design Document Template

```markdown
# Feature: [Name]
Date: YYYY-MM-DD

## 1. Overview
**Goal**: [One sentence]
**Success Metrics**: [How we measure success]
**In Scope**: [What we're building]
**Out of Scope**: [What we're NOT building]

## 2. Architecture
[Diagram or description of components]

### Data Flow
[Step-by-step flow]

## 3. Data Model (if applicable)
[Schema changes, relationships]

## 4. Error Handling
| Scenario | Response |
|----------|----------|
| ... | ... |

## 5. Testing Strategy
| Type | Coverage | Focus |
|------|----------|-------|
| Unit | ... | ... |
| Integration | ... | ... |
| E2E | ... | ... |

## 6. Open Questions
[Any unresolved decisions]
```

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Ask 5 questions at once | One question per message |
| Present design all at once | 200-300 word sections, validate each |
| Skip context gathering | Always check project state first |
| Present only one approach | Always show 2-3 with trade-offs |
| Assume requirements | Ask until crystal clear |
| Over-engineer MVP | YAGNI - remove the unnecessary |
| Write design without validation | Get user confirmation at each step |

## Execution Flow

```
CONTEXT → REFINE → EXPLORE → PRESENT → DOCUMENT → IMPLEMENT
   │         │         │         │          │          │
 Git/Files  1 Q at   2-3 opts  200-300   docs/plans/  git-worktrees
            a time   w/recs    sections  + commit     + /plan-feature
```

---

## Integration

**Pairs with:**

- `gemini-cli` - Get alternative perspectives during approach exploration (Phase 3)
- `elements-of-style` - Apply when writing design documents (Phase 5)
- `using-git-worktrees` - Create isolated workspace for implementation (Phase 6)
- `/plan-feature` command - Create detailed TDD implementation plans (Phase 6)
