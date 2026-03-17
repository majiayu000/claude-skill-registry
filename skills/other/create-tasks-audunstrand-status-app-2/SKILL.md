---
name: create-tasks
description: Creates well-formed tasks following a template that engineers can implement. Use when creating tasks, defining work items, creating tasks from PRD, breaking down features, or converting requirements into actionable tasks.
---

# GitHub Copilot Skill: create-tasks

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Create Tasks

Creates well-formed tasks that provide large amounts of contexts so that engineers that weren't in conversations can implement the task without any prior knowledge and without asking questions.

Tasks should be created using the tools and documentation conventions in the project the skills is being applied to. If the conventions are not clear, ask the user to clarify and then document them.

## What Engineers Need

Every task must provide:
- What they're building (deliverable)
- Why it matters (context)
- Key decisions and principles they must follow
- Acceptance criteria
- Dependencies
- Related code/patterns
- How to verify it works

## Before Creating Tasks: Slice First

🚨 **NEVER create a task without validating its size first.** A PRD deliverable is NOT automatically a task—it may be an epic that needs splitting.

### Example Mapping Check

Before writing any task, mentally apply Example Mapping:

| Card | Question | Red Flag |
|------|----------|----------|
| 🟡 Story | Can you state it in one specific sentence? | Needs "and" or multiple clauses |
| 🔵 Rules | How many distinct rules/constraints? | More than 3-4 rules = too big |
| 🟢 Examples | Can you list 3-5 concrete examples? | Can't think of specific examples = unclear |
| 🔴 Questions | Are there unresolved unknowns? | Many questions = needs spike first |

### Splitting Signals (Task Too Big)

If ANY of these are true, **STOP and split**:

- ❌ Can't describe in a specific, action-oriented title
- ❌ Would take more than 1 day
- ❌ Title requires "and" or lists multiple things
- ❌ Has multiple clusters of acceptance criteria
- ❌ Cuts horizontally (all DB, then all API, then all UI)
- ❌ PRD calls it "full implementation" or "complete system"

### SPIDR Splitting Techniques

When you need to split, use these techniques:

| Technique | Split By | Example |
|-----------|----------|---------|
| **P**aths | Different user flows | "Pay with card" vs "Pay with PayPal" |
| **I**nterfaces | Different UIs/platforms | "Desktop search" vs "Mobile search" |
| **D**ata | Different data types | "Upload images" vs "Upload videos" |
| **R**ules | Different business rules | "Basic validation" vs "Premium validation" |
| **S**pikes | Unknown areas | "Research payment APIs" before "Implement payments" |

### Vertical Slices Only

Every task must be a **vertical slice**—cutting through all layers needed for ONE specific thing:

```
✅ VERTICAL (correct):
"Add search by title" → touches UI + API + DB for ONE search type

❌ HORIZONTAL (wrong):
"Build search UI" → "Build search API" → "Build search DB"
```

## Task Naming

### Formula

`[Action verb] [specific object] [outcome/constraint]`

### Good Names

- "Add price range filter to product search"
- "Implement POST /api/users endpoint with email validation"
- "Display product recommendations on home page"
- "Enable CSV export for transaction history"
- "Validate required fields on checkout form"

### Rejected Patterns

🚨 **NEVER use these—they signal an epic, not a task:**

| Pattern | Why It's Wrong |
|---------|----------------|
| "Full implementation of X" | Epic masquerading as task |
| "Build the X system" | Too vague, no specific deliverable |
| "Complete X feature" | Undefined scope |
| "Implement X" (alone) | Missing specificity |
| "X and Y" | Two tasks combined |
| "Set up X infrastructure" | Horizontal slice |

If you catch yourself writing one of these, **STOP and apply SPIDR**.

## Task Size Validation (INVEST)

Every task MUST pass INVEST before creation:

| Criterion | Question | Fail = Split |
|-----------|----------|--------------|
| **I**ndependent | Does it deliver value alone? | Depends on other incomplete tasks |
| **N**egotiable | Can scope be discussed? | Rigid, all-or-nothing |
| **V**aluable | Does user/stakeholder see benefit? | Only technical benefit |
| **E**stimable | Can you size it confidently? | "Uh... maybe 3 days?" |
| **S**mall | Fits in 1 day? | More than 1 day |
| **T**estable | Has concrete acceptance criteria? | Vague or missing criteria |

### Hard Limits

- **Max 1 day of work** — if longer, split it
- **Must be vertical** — touches all layers for ONE thing
- **Must be demoable** — when done, you can show it working

## Task Template

```markdown
## Deliverable: [What user/stakeholder sees]

### Context
[Where this came from and why it matters. PRD reference, bug report, conversation summary—whatever helps engineer understand WHY. You MUST provide the specific file path or URL for any referenced files like a PRD of bug report - don't assume the engineer knows where things are stored]

### Key Decisions and principles
- [Decision/Principle] — [rationale]

### Delivers
[Specific outcome in user terms]

### Acceptance Criteria
- [Condition] → [expected result]

### Dependencies
- [What must exist first]

### Related Code
- `path/to/file` — [what pattern/code to use]

### Verification
[Specific commands/tests that prove it works]
```

## Process

1. **Slice first** — Apply Example Mapping check. If task fails any splitting signal, use SPIDR to break it down before proceeding.
2. **Name it** — Write a specific, action-oriented title. If you can't, the task isn't clear enough.
3. **Validate size** — Must pass INVEST. Max 1 day. Must be vertical slice.
4. Gather context (from PRD, conversation, bug report, etc.)
5. Identify key decisions that affect implementation
6. Define clear acceptance criteria
7. Find related code/patterns in the codebase
8. Specify verification commands
9. Output task using template

## Checkpoint

Before finalizing any task, verify ALL of these:

| Check | Question | If No |
|-------|----------|-------|
| **Size** | Is this ≤1 day of work? | Split using SPIDR |
| **Name** | Is the title specific and action-oriented? | Rewrite using formula |
| **Vertical** | Does it cut through all layers for ONE thing? | Restructure as vertical slice |
| **INVEST** | Does it pass all 6 criteria? | Fix the failing criterion |
| **Context** | Can an engineer implement without asking questions? | Add what's missing |

🚨 **If the PRD says "full implementation" or similar, you MUST split it. Creating such a task is a critical failure.**
