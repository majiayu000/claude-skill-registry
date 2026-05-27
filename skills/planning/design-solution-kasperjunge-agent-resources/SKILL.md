---
name: design-solution
description: Converge on a single recommended solution after brainstorming options. Use when you have multiple candidate approaches and need to analyze trade-offs, select one, and define decision criteria before planning.
---

# Design Solution

Converge from multiple options to a single recommended approach.

## Position in Workflow

Step 3 of development workflow:
1. `/research` - Understand problem and constraints
2. `/brainstorm-solutions` - Explore solution space
3. `/design-solution` - Converge on a single solution (THIS)
4. Plan, code, review, ship

## Core Principle

**Decide deliberately.** Evaluate trade-offs, align to constraints, and pick the best fit.

## Input

**Default:** Use the options from the current conversation.

**If argument provided:**
- File path: Read the file for brainstorming output
- GitHub issue: Fetch with `gh issue view $ARG --comments`

## Workflow

### 1. Reconfirm Context

- Restate the problem, constraints, and success criteria.
- Identify any missing information that blocks a decision.

### 2. Evaluate Options

For each option, assess:
- **Pros:** Benefits and what it enables
- **Cons:** Risks and complexity
- **Codebase fit:** Alignment with existing patterns
- **Effort:** Low/Medium/High
- **Reversibility:** Easy/Moderate/Hard to change later

### 3. Decide

- Rank options against success criteria.
- Select a recommended option.
- State conditions that would change the decision.

### 4. Capture Open Questions

List unknowns that must be resolved before planning.

## Output Format

```
## Solution Decision

### Context Summary
[Brief restatement of problem and key constraints]

### Decision Criteria
[What matters most: performance, time, simplicity, extensibility, etc.]

---

### Option Evaluation

#### Option 1: [Name] - Recommended
[Description]

**Pros:**
- ...

**Cons:**
- ...

**Codebase fit:** [How it aligns with existing patterns]
**Effort:** [Low/Medium/High]
**Reversibility:** [Easy/Moderate/Hard]

#### Option 2: [Name]
[Same structure]

#### Option 3: [Name]
[Same structure]

---

### Recommendation
[Why the recommended option wins, and when you would choose differently]

### Open Questions
[Anything that could change the recommendation]

### Next Step
Ready to plan implementation. Enter Plan Mode or run `/plan`.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping decision criteria | State criteria before evaluating |
| Over-weighting novelty | Prefer codebase fit and simplicity |
| Ignoring reversibility | Consider how hard it is to change later |
| Decision without evidence | Call out unknowns explicitly |

## What NOT to Do

- Do NOT re-brainstorm options
- Do NOT proceed to planning without a chosen option
- Do NOT hide assumptions or uncertainties
- Do NOT ignore codebase constraints
