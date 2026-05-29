---
name: whiteboarding
description: "Brainstorm and plan features through codebase search, technology research, and 2-3 approach comparison before producing implementation-ready plans. Use when starting features, designing solutions, or planning complex work. Triggers on: whiteboard, let's plan, brainstorm, design this, figure out how to build. Save plans to docs/plans/ for execution via /code-foundations:building."
---

# Skill: whiteboarding

**Brainstorm → Design → Save → Handoff**

---

## Quick Reference

| Phase | Goal | Output |
|-------|------|--------|
| UNDERSTAND | **Search codebase** + clarify problem | Pattern summary + problem statement |
| EXPLORE | **Research technologies** + compare 2-3 approaches | Research summary + chosen approach |
| DETAIL | Break into implementation steps | Checklist with files/functions |
| VALIDATE | User confirms each section | Approval |
| SAVE | Write to docs/plans/ | Plan file ready for /code-foundations:building |

**Key change:** Phases 1 and 2 now SEARCH before asking/proposing. No relying on user to know patterns.

---

## Crisis Invariants - NEVER SKIP

| Check | Why Non-Negotiable |
|-------|-------------------|
| **Search codebase BEFORE questions** | Patterns exist that user may not know about |
| **Research BEFORE proposing approaches** | Uninformed proposals waste user's decision-making |
| **One question at a time** | Multiple questions = cognitive overload = shallow answers |
| **2-3 approaches before committing** | First idea is rarely best; comparison reveals trade-offs |
| **User confirms each section** | Unvalidated plans diverge from user intent |
| **Save before executing** | Plan file enables context refresh + checklist tracking |

---

## Phase 1: UNDERSTAND (Discovery + Research)

### Step 1a: Pattern Discovery (MANDATORY - Do First)

**Before asking ANY questions, search the codebase:**

```
SEARCH FOR:
1. Similar features/functionality (grep for keywords)
2. Same directory/module patterns (read nearby files)
3. Related components (how do similar things work?)
4. Naming conventions (what patterns exist?)
```

| Search | Action |
|--------|--------|
| Similar features | `grep -r "keyword"` across codebase |
| Module patterns | Read 2-3 files in target directory |
| Related components | Find how similar problems were solved |
| Conventions | Note naming, structure, error handling patterns |

**Output: Pattern Summary**
```markdown
## Existing Patterns Found
- [pattern 1]: [where found, how it works]
- [pattern 2]: [where found, how it works]

## Conventions to Follow
- Naming: [observed pattern]
- Structure: [observed pattern]
- Error handling: [observed pattern]

## Similar Implementations
- [file]: [what it does, relevance]
```

**If no patterns found:** State "No existing patterns found for [topic]. This will establish a new pattern."

**See:** [pattern-reuse-gate.md](../../references/pattern-reuse-gate.md)

---

### Step 1b: Adaptive Questioning

After pattern discovery, classify complexity:

| Signal | Complexity | Question Count |
|--------|-----------|----------------|
| Single file, clear scope | Simple | 2-3 questions |
| Multiple files, some unknowns | Medium | 4-5 questions |
| Architecture changes, many unknowns | Complex | 6-8 questions |

**State classification:** "This seems [simple/medium/complex]. Based on pattern discovery, I'll ask [N] questions."

### Question Sequence (Ask ONE at a time)

**Simple (2-3 questions):**
1. What specific outcome do you want?
2. What constraints should I know about?
3. What does "done" look like?

**Medium (add these):**
4. Who/what will use this?
5. What could go wrong?

**Complex (add these):**
6. What other systems does this touch?
7. What's the rollback plan if it fails?
8. What's the testing strategy?

**NOTE:** Questions about "existing patterns" removed - we searched instead of asking.

### Question Format

Use multiple-choice when possible:

```
Which authentication approach fits best?
- [ ] JWT tokens (stateless, scalable)
- [ ] Session cookies (simpler, server-state)
- [ ] OAuth2 (if external providers needed)
- [ ] Other (describe)
```

**IMPORTANT:** Wait for answer before next question. No question batching.

### Output: Problem Statement

After questions, summarize:

```markdown
## Problem Statement
[1-2 sentences describing what we're building]

## Constraints
- [constraint 1]
- [constraint 2]

## Success Criteria
- [criterion 1]
- [criterion 2]
```

Get user confirmation: "Does this capture what you want?"

---

## Phase 2: EXPLORE (Research + Approaches)

### Step 2a: Technology Research (Before Proposing)

**Before proposing approaches, gather data:**

#### Codebase Research
```
SEARCH FOR:
1. How similar problems are solved in this codebase
2. What libraries/patterns are already in use
3. What the codebase is NOT using (intentional omissions?)
```

| Check | Why |
|-------|-----|
| Existing dependencies | Don't propose new lib if similar exists |
| Rejected patterns | Check git history/comments for "we tried X" |
| Team conventions | Match what's already working |

#### Web Research (When technology choice is involved)

**Use WebSearch/WebFetch when:**
- Comparing libraries/frameworks
- Evaluating technology trade-offs
- Checking current best practices (your knowledge may be outdated)

```
SEARCH FOR:
1. "[technology A] vs [technology B] [current year]"
2. "[problem domain] best practices [current year]"
3. "[framework] [specific feature] implementation"
```

**Output: Research Summary**
```markdown
## Codebase Findings
- Already using: [libraries, patterns]
- Similar solutions: [where, how]

## Web Research (if applicable)
- [Technology A]: [pros, cons, current status]
- [Technology B]: [pros, cons, current status]
- Recommendation: [based on research]
```

---

### Step 2b: Generate Alternatives

**You MUST present 2-3 approaches before proceeding.**

**CRITICAL:** Approaches must be STRUCTURALLY different (different technology, pattern, or architecture). Variations of the same approach do NOT count:
- ❌ "JWT with refresh tokens" vs "JWT without refresh tokens" = same approach
- ✅ "JWT tokens" vs "Session cookies" vs "OAuth2" = different approaches

**Approaches must be informed by research.** Don't propose technologies you didn't research.

**If user mentioned a solution in their initial request** (e.g., "I'm thinking JWT"), this is exploratory input, NOT a decision. Still present 2-3 structurally different alternatives, informed by research.

| Approach | Trade-offs | Best When | Research Source |
|----------|-----------|-----------|-----------------|
| Option A | [pros/cons] | [conditions] | [codebase/web] |
| Option B | [pros/cons] | [conditions] | [codebase/web] |
| Option C | [pros/cons] | [conditions] | [codebase/web] |

### Presentation Format

```markdown
## Approach A: [Name] (Recommended)
**Idea:** [1-2 sentences]
**Pros:** [list]
**Cons:** [list]
**Effort:** [relative estimate]

## Approach B: [Name]
**Idea:** [1-2 sentences]
**Pros:** [list]
**Cons:** [list]
**Effort:** [relative estimate]

## Approach C: [Name] (if applicable)
...
```

### Decision

Ask: "Which approach do you prefer, or should I elaborate on any?"

Record chosen approach and rationale:
```markdown
## Chosen Approach: [Name]
**Rationale:** [why this over others]
```

---

## Phase 3: DETAIL (Implementation-Ready Plan)

### Break into Sections (200-300 words each)

For each section:
1. Present the section
2. Wait for user confirmation
3. Proceed to next section

### Section Template

```markdown
### Section N: [Name]

**Goal:** [what this section accomplishes]

**Files to create/modify:**
- `path/to/file.ts` - [what changes]
- `path/to/other.ts` - [what changes]

**Implementation details:**
- [specific function/class/pattern]
- [key decisions]
- [edge cases to handle]

**Dependencies:** [what must be done first]
```

### YAGNI Gate

Before each section, ask:
- Is this section actually needed?
- Could we ship without it?
- Are we building for hypothetical future needs?

If answer is "not needed now" → Remove from plan.

---

## Phase 4: VALIDATE (Confirmation Loop)

### Test Coverage Question (MANDATORY)

Before finalizing the plan, ask about test coverage:

```
How much test coverage do you want for this implementation?

1. 100% coverage (Recommended)
   Unit tests for all new code + integration tests for critical paths

2. Backend only
   Tests for server-side/API changes only

3. Backend + frontend
   Tests for both server and client layers

4. None
   Skip tests (not recommended - technical debt)

5. Ask at each phase
   Decide test scope when building each phase
```

**Record the answer in the plan file** under `## Test Coverage`.

**Inform building:** This choice affects POST-GATE behavior - reviewers will check for tests matching the chosen coverage level.

---

### Full Plan Review

Present complete plan structure:

```markdown
# Plan: [Topic]

## Sections
1. [Section 1 name] - [1 sentence]
2. [Section 2 name] - [1 sentence]
3. ...

## Test Plan
- [test 1]
- [test 2]

## Questions/Concerns
- [any remaining uncertainties]
```

Ask: "Does this plan look complete? Any sections to add, remove, or modify?"

---

## Phase 5: SAVE (Write Plan File)

### File Location

```
docs/plans/YYYY-MM-DD-<topic-slug>.md
```

### Plan File Schema

```markdown
# Plan: [Topic]

**Created:** YYYY-MM-DD
**Status:** ready

---

## Context

[Problem statement from Phase 1]

## Constraints

- [constraint 1]
- [constraint 2]

## Chosen Approach

**[Approach name]**

[Rationale from Phase 2]

---

## Implementation Checklist

### Phase 1: [Name]
- [ ] [Specific task with file path]
- [ ] [Specific task with file path]

**Files:**
- `path/to/file.ts`

**Details:**
[Implementation specifics]

---

### Phase 2: [Name]
...

---

## Test Coverage

**Level:** [100% / Backend only / Backend + frontend / None / Per-phase]

## Test Plan

- [ ] Unit: [specific tests]
- [ ] Integration: [specific tests]
- [ ] Manual: [verification steps]

---

## Notes

- [edge cases]
- [gotchas]
- [decisions made during planning]

---

## Execution Log

_To be filled during /code-foundations:building_
```

### Save Command

```bash
mkdir -p docs/plans
# Write plan file
```

---

## Phase 6: HANDOFF

### Ask User How to Proceed

After saving the plan, use `AskUserQuestion` with these options:

**Question:** "Plan saved to docs/plans/YYYY-MM-DD-<topic>.md. How would you like to proceed?"

**Options:**
1. **Clear conversation and build** (Recommended) - Fresh context for better execution
2. **Tell me what to do** - Get step-by-step instructions to execute manually

**If user selects option 1:**
Execute `/clear` command, then immediately run `/code-foundations:building docs/plans/YYYY-MM-DD-<topic>.md`

**If user selects option 2:**
Provide numbered steps the user can follow to implement the plan manually

---

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "I already know what to build" | Planning reveals unknowns you don't know you don't know |
| "This is too simple for planning" | Simple tasks have highest error rates |
| "Let's just start coding" | Code without plan = rework later |
| "One approach is obviously right" | If it's obvious, comparing takes 2 minutes |
| "User is waiting, skip questions" | Wrong solution fast < right solution slightly slower |
| "I'll figure out details during implementation" | Details in plan = checklist during execution |
| "Plan will be outdated by implementation" | Plan file tracks changes; no plan = no tracking |
| "Multiple choice is slower" | MC gets precise answers; open questions get vague ones |
| "I'll just plan in my head" | Mental plans don't persist. File = resumable artifact. Skip file = lose all planning work on context refresh. |
| "I'll batch questions to save time" | Batched questions get shallow, incomplete answers. One question = focused, complete answer. |
| "User mentioned X, so that's decided" | User-mentioned solutions are exploratory. Still compare 2-3 structurally different approaches. |
| "I'll ask user about patterns" | **Search instead.** User may not know all patterns. You have tools to find them. |
| "No need to search, I know this tech" | Your knowledge may be outdated. Search confirms current best practices. |
| "Searching takes too long" | 2 min search prevents 20 min wrong-approach rework. |
| "I'll research during implementation" | Research informs approach CHOICE. After choosing, it's too late. |
| "This codebase is new to me" | That's exactly why you search. Don't guess conventions - find them. |

---

## Pressure Testing Scenarios

### Scenario 1: User Wants to Skip Planning

**Situation:** User says "just build it" or "we don't need a plan."

**Response:** "I can build without planning, but past experience shows:
- Plans catch issues before code exists
- Plan files enable context refresh for better execution
- Checklist tracking reduces forgotten edge cases

How about a quick plan (3-4 questions, 5 minutes)? Or should I proceed without?"

### Scenario 2: Vague Requirements

**Situation:** User gives unclear or incomplete requirements.

**Response:** Ask clarifying questions ONE AT A TIME. Do NOT guess or assume. Each question should narrow scope until requirements are concrete.

### Scenario 3: User Rejects All Approaches

**Situation:** User doesn't like any of the 2-3 approaches presented.

**Response:** "What's missing from these approaches? I'll generate alternatives that address [specific concern]."

---

## Chaining

- **RECEIVES FROM:** User request, feature description, user story
- **CHAINS TO:** building (via saved plan file)
- **RELATED:** oberplan, aposd-designing-deep-modules, cc-construction-prerequisites
