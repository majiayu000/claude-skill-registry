---
name: faion-writing-specifications
user-invocable: false
description: "SDD Framework: Creates spec.md through Socratic dialogue and brainstorming. Iterative refinement of ideas through questions and alternatives. Triggers on \"spec.md\", \"specification\", \"requirements\"."
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# SDD: Writing Specifications

**Communication: User's language. Docs: English.**

## Philosophy

- **Intent is source of truth** — spec is main artifact
- **Socratic dialogue** — user formulates requirements through questions
- **Brainstorming** — iterative refinement via alternatives

## Workflow

```
BRAINSTORM → RESEARCH → CLARIFY → DRAFT → REVIEW → SAVE
```

## Phase 1: Brainstorming

Start: "Tell me about the problem. Who suffers and how?"

**Five Whys** — for each answer ask "Why?":
```
"Need export" → Why? → "Managers ask" → Why? → "No access" → Real problem: UX
```

**Alternatives** — for each idea:
```markdown
**A:** {approach 1} ✅ Pros ❌ Cons
**B:** {approach 2} ✅ Pros ❌ Cons
Which is closer?
```

**Challenge assumptions:**
- "Is this needed for v1?"
- "What if we DON'T do this?"
- "What exists in codebase?"

## Phase 2: Research Codebase

Search: `Glob **/models.py`, `Grep class.*Model`, `Glob aidocs/sdd/**/spec.md`

Share findings: "Found existing export in services.py. Does this affect approach?"

## Phase 3: Clarify Details

**User stories workshop:**
```markdown
As {role}, I want {goal}, so that {benefit}.
- How often?
- What happens if can't do this?
```

**Edge cases through questions** (not assumptions):
- "What if data invalid?"
- "What if 1000+ records?"
- "What if service unavailable?"

## Phase 4: Draft Section by Section

Each section → show → validate → next:

1. Problem Statement → "Correct?"
2. User Stories with AC → "Complete?"
3. Functional Requirements → "Anything redundant?"
4. Out of Scope → "Agree with boundaries?"

## Phase 5: Review

**Checklist:**
- [ ] Problem clear
- [ ] User Stories specific
- [ ] Requirements testable
- [ ] Out of Scope defined

Call `faion-spec-reviewer-agent` agent before save.

## Phase 6: Save

**New feature:** `aidocs/sdd/{project}/features/backlog/{NN}-{feature}/spec.md`
**Active feature:** update existing spec.md

Create CLAUDE.md navigation hub in feature directory.

## Anti-patterns

- ❌ Assumptions instead of questions
- ❌ Solution before problem
- ❌ Large blocks without validation
- ❌ Ignoring "I don't know"

## Output

`spec.md` → Next: `faion-writing-design-docs`
