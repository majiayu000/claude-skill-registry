---
name: design-practice
description: Apply the 6-phase design framework (Describe, Diagnose, Delimit, Direction, Design, Develop) to understand a problem before implementing a solution.
---

Apply the 6-phase design framework to understand a problem before implementing a solution.

## Phases

Work through each phase sequentially. Do not skip phases. The goal is understanding, not artifacts.

### PHASE 1: DESCRIBE (Symptoms)

**Objective:** Capture the reality without imposing solutions.

1. **Gather signals:**
   - What symptoms are observed? (errors, complaints, metrics)
   - Where do they occur? (files, components, conditions)
   - When did they start? (commits, deployments, changes)
   - Who is affected? (users, systems, processes)

2. **Write a neutral description:**
   - Facts only, no speculation on causes
   - No mention of solutions
   - Observable behaviors, not interpretations

**Output format:**
```
## Description

### Observed Symptoms
- [Symptom 1]: [Where/When observed]
- [Symptom 2]: [Where/When observed]

### Signal Sources
- [Bug reports, logs, user complaints, metrics]

### Timeline
- [When symptoms first appeared, any patterns]
```

**Anti-patterns to avoid:**
- "The database is slow" (diagnosis, not description)
- "We need to add caching" (solution, not description)
- "Users are confused by the UI" (interpretation, not observation)

**Correct examples:**
- "Page load time exceeds 5s when user count > 100"
- "Error rate increased from 0.1% to 2.3% after deploy on Jan 15"
- "Users submit support tickets asking how to find the export button"

### PHASE 2: DIAGNOSE (Root Cause)

**Objective:** Identify the mechanism causing the symptoms.

1. **Generate multiple hypotheses:**
   - List at least 3 possible causes
   - "If I only have one hypothesis, I'm probably wrong"

2. **Test hypotheses systematically:**
   - Use logic to rule things out (negative progress)
   - Use evidence to support remaining hypotheses
   - Divide and conquer (git bisect, component isolation)

3. **Write the Problem Statement:**

**Problem Statement Template:**
```
## Problem Statement

**Current behavior:** [What happens now - factual]

**Mechanism:** [Root cause - how/why it happens]

**Evidence:**
- [Fact supporting this diagnosis]
- [Fact supporting this diagnosis]

**Ruled out:**
- [Hypothesis A]: [Why it's not this]
- [Hypothesis B]: [Why it's not this]
```

**Quality check:** The solution should feel obvious after writing the right problem statement. If it doesn't, the diagnosis is incomplete.

### PHASE 3: DELIMIT (Scope)

**Objective:** Define what's in and what's out.

1. **Set explicit boundaries:**
   - What subset of the problem will we solve?
   - What constraints do we accept?
   - What's explicitly NOT being addressed?

2. **Document non-goals:**
   - Future considerations
   - Related problems not in scope
   - Nice-to-haves deferred

**Output format:**
```
## Scope

### In Scope
- [What we will address]
- [Specific constraints we'll work within]

### Out of Scope (Non-Goals)
- [What we explicitly won't do]
- [Why it's deferred]

### Constraints
- [Technical limitations]
- [Time/resource constraints]
- [Compatibility requirements]
```

**Why this matters:** Prevents scope creep. Sets the "physics" of the project before considering solutions.

### PHASE 4: DIRECTION (Strategic Approach)

**Objective:** Select the best approach from viable alternatives.

1. **Generate multiple approaches:**
   - **Status Quo**: Always include "do nothing" as baseline
   - **Approach A**: [First viable approach]
   - **Approach B**: [Different viable approach]
   - **Approach C**: [If applicable]

2. **Build a Decision Matrix:**

**Decision Matrix Structure:**
```
## Decision Matrix

| Criterion | Status Quo | Approach A | Approach B |
|-----------|------------|------------|------------|
| [Criterion 1] | [Fact] | [Fact] | [Fact] |
| [Criterion 2] | [Fact] | [Fact] | [Fact] |
| [Criterion 3] | [Fact] | [Fact] | [Fact] |

### Criteria Definitions
- **[Criterion 1]**: [What this measures]
- **[Criterion 2]**: [What this measures]

### Assessment Key
- Green: Desirable
- Yellow: Acceptable with trade-offs
- Red: Problematic or blocking
```

**Rules for Decision Matrix:**
- Text is FACT (neutral, objective descriptions)
- Color/assessment is JUDGMENT (subjective evaluation)
- Status Quo is always the first column
- Each cell must be specific, not "good" or "bad"

3. **Select and justify:**
```
### Decision

**Selected approach:** [Approach name]

**Rationale:** [Why this approach best addresses the scoped problem]

**Trade-offs accepted:** [What we're giving up]
```

### PHASE 5: DESIGN (Tactical Plan)

**Objective:** Create detailed blueprint for implementation.

Only after Direction is selected:

1. **Define specifics:**
   - Data structures and schemas
   - API signatures and contracts
   - Component responsibilities
   - Error handling approach
   - Edge cases

2. **Write Implementation Plan:**

Use the standard implementation plan format with:
- Phases that can be independently verified
- TDD approach (tests before implementation)
- Specific file paths and changes
- Success criteria for each phase

**Hammock time:** Write the plan, then sleep on it. Read it the next day before proceeding.

### PHASE 6: DEVELOP (Execute)

**Objective:** Translate design into working code.

If Phases 1-5 were rigorous, this phase should feel mechanical:
- Follow the plan
- Write tests first
- Implement to pass tests
- Verify against success criteria

**If you're struggling in this phase:** Return to earlier phases. Struggling to code usually means the design is incomplete.

## Process Rules

1. **No phase skipping:** Each phase builds on the previous
2. **Artifacts are thinking tools:** Not bureaucracy, but aids to understanding
3. **Hammock time:** Sleep on ideas before committing to them
4. **Multiple hypotheses:** One idea is a trap; generate alternatives
5. **Incremental over iterative:** Understand → Design → Code → Value (not Code → Fail → Learn)

## When to Return to Earlier Phases

- **Can't write Problem Statement clearly** → Back to Describe (need more symptoms)
- **Solution doesn't feel obvious** → Back to Diagnose (incomplete root cause)
- **Scope keeps expanding** → Back to Delimit (boundaries not firm)
- **Can't choose between approaches** → Back to Direction (need more criteria or research)
- **Implementation keeps hitting surprises** → Back to Design (missing edge cases)
