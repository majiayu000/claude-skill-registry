---
name: dev-clarify
description: "REQUIRED Phase 3 of /dev workflow. Asks targeted questions based on codebase exploration findings."
---

**Announce:** "I'm using dev-clarify (Phase 3) to resolve ambiguities."

## Contents

- [The Iron Law of Clarification](#the-iron-law-of-clarification)
- [What Clarify Does](#what-clarify-does)
- [Process](#process)
- [Question Categories](#question-categories)
- [Red Flags](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Post-Exploration Clarification

Ask targeted questions based on what exploration revealed.
**Prerequisite:** Exploration phase complete, key files read.

<EXTREMELY-IMPORTANT>
## The Iron Law of Clarification

**ASK BEFORE DESIGNING. This is not negotiable.**

After exploration, you now know:
- What exists in the codebase
- What patterns are used
- What integrations are needed

Use this knowledge to ask **informed questions** about:
- Edge cases the code will need to handle
- Integration points with existing systems
- Behavior in ambiguous scenarios

**If you catch yourself about to design without resolving ambiguities, STOP.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The pattern choice is obvious" | Multiple patterns exist for a reason | ASK which to follow |
| "I can decide edge cases myself" | Your assumptions don't match user expectations | ASK for clarification |
| "This is a small detail" | Small details cause big bugs | ASK about edge cases now |
| "I'll handle integration points during implementation" | Wrong integration breaks everything | CLARIFY integration NOW |
| "The exploration gave me enough info" | Code tells you HOW, not WHAT SHOULD happen | ASK for requirements, not just patterns |
| "I can make a reasonable assumption" | Reasonable != correct | ASK, don't assume |
| "Asking too many questions annoys users" | Building wrong thing annoys users more | ASK clarifying questions |

### Honesty Framing

**Assuming user requirements without asking is LYING about what they want.**

You explored the codebase and found patterns. But patterns show HOW things work, not WHAT the user wants. Clarification bridges this gap.

Asking costs minutes. Wrong assumptions cost hours of rework.

### No Pause After Completion

After updating `.claude/SPEC.md` with all clarified requirements, IMMEDIATELY invoke:
```
Skill(skill="workflows:dev-design")
```

DO NOT:
- Summarize what you learned
- Ask "should I proceed to design?"
- Wait for user confirmation
- Write status updates

The workflow phases are SEQUENTIAL. Complete clarify → immediately start design.

## What Clarify Does

| DO | DON'T |
|----|-------|
| Ask questions based on exploration | Ask vague/generic questions |
| Reference specific code patterns found | Repeat questions from brainstorm |
| Clarify integration points | Propose approaches (that's design) |
| Resolve edge cases | Make assumptions |
| Update SPEC.md with answers | Skip to implementation |

**Clarify answers: WHAT EXACTLY should happen in specific scenarios**
**Design answers: HOW to build it** (next phase)

## Process

### 1. Review Exploration Findings

Before asking questions, review:
- Key files you read
- Patterns discovered
- Architecture insights
- Integration points identified

### 2. Identify Ambiguities

Common areas needing clarification after exploration:

**Integration Points:**
- "The existing auth system uses JWT. Should the new feature use the same token or create a new session type?"

**Edge Cases:**
- "What happens if [condition discovered in code]?"

**Scope Boundaries:**
- "The existing feature handles X. Should the new feature also handle X or is that out of scope?"

**Behavior Choices:**
- "I found two patterns in the codebase for this. Pattern A in `file.ts:23` and Pattern B in `other.ts:45`. Which should we follow?"

### 3. Ask Questions with AskUserQuestion

Present questions with context from exploration:

```
AskUserQuestion(questions=[{
  "question": "The auth middleware at src/middleware/auth.ts:78 validates tokens synchronously. The new endpoint needs user data. Should we: validate synchronously (faster, simpler) or fetch fresh user data (slower, always current)?",
  "header": "Auth pattern",
  "options": [
    {"label": "Sync validation (Recommended)", "description": "Faster, uses cached token claims, matches existing patterns"},
    {"label": "Fresh fetch", "description": "Slower, always current, needed if user data changes frequently"}
  ],
  "multiSelect": false
}])
```

**Key principles:**
- Reference specific files/lines from exploration
- Lead with recommendation based on codebase patterns
- Explain trade-offs clearly
- One question at a time for complex topics

### 4. Update SPEC.md

After each answer, update `.claude/SPEC.md`:
- Add clarified requirements
- Document decisions made
- Note trade-offs accepted

```markdown
## Clarified Requirements

### Auth Pattern
- Decision: Sync validation
- Rationale: Matches existing patterns, user data changes infrequently
- Reference: src/middleware/auth.ts:78

### Edge Case: Expired Token
- Decision: Return 401, let client refresh
- Rationale: Consistent with other endpoints
```

## Question Categories

### Must Ask (based on exploration)
- Integration points with existing systems
- Patterns to follow (when multiple exist)
- Edge cases revealed by code reading

### Optional (if unclear)
- Performance requirements
- Error handling preferences
- Backward compatibility needs

### Don't Ask (already decided)
- What the feature does (that's brainstorm)
- Whether to build it (user already decided)
- Architecture approach (that's design)

## Red Flags - STOP If You're About To:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Ask without exploration context | Questions will be generic | Reference specific code findings |
| Propose architecture | Too early, still clarifying | Ask questions, save design for next phase |
| Make assumptions | Leads to rework | Ask and get explicit answer |
| Skip to design | Ambiguities cause bugs | Resolve all questions first |

## Output

Clarification complete when:
- All integration points clarified
- Edge cases resolved
- Pattern choices made
- `.claude/SPEC.md` updated with final requirements
- No remaining ambiguities

## Phase Complete

**REQUIRED SUB-SKILL:** After completing clarification, IMMEDIATELY invoke:
```
Skill(skill="workflows:dev-design")
```
