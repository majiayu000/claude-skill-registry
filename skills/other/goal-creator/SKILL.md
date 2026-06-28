---
name: goal-creator
description: >
  Use when creating /goal directives, reusable testable outcome-oriented
  success standards for agentic workflows. Use whenever the user asks to
  create a goal, write a /goal directive, define what good looks like, set
  success criteria for an agent, define a reusable instruction, create a
  quality standard, write acceptance criteria for an agent workflow, or
  specify done conditions.
metadata:
  author: zebbern
  version: "1.3"
---

# `/goal` Creator

Create reusable, testable, outcome-oriented success standards that guide agents
across repeated runs. A `/goal` is not a one-off prompt - it is a durable
operating instruction that defines what good execution looks like.

## Core Workflow

Creating a `/goal` follows these steps:

1. **Define the outcome** - what does success look like in observable terms?
2. **Select category** - which workflow stage is this for? (see categories below)
3. **Apply a template** - fill in the master template or select an alternate
4. **Add constraints** - what must NOT happen? what boundaries apply?
5. **Define verification** - how will an independent checker confirm success?
6. **Run quality audit** - apply the pre-flight checklist before delivering

## What a `/goal` Is

A `/goal` directive is a **declarative, outcome-oriented specification of what
success looks like** - independent of execution path. It is:

- **Enduring** - reusable across multiple sessions, not one-off
- **Evaluable** - an independent checker can verify achievement
- **Decomposable** - can be broken into sub-goals with dependencies
- **Role-anchored** - tied to a specific agent responsibility

## What a `/goal` Is Not

| Format | What It Specifies | `/goal` Difference |
|--------|-------------------|-------------------|
| One-off prompt | A single task invocation | Durable standard, not transient |
| System instruction | How the agent should behave (identity, tone) | What the agent must achieve (outcome) |
| Checklist | Steps to execute | Success conditions to meet |
| Acceptance criteria | Verifiable conditions for one feature | Reusable standard for a class of work |
| User story | User need from product perspective | Agent responsibility from execution perspective |
| SOP | Procedural "how to" instructions | Outcome specification - "what done means" |

**Rule of thumb**: Use a `/goal` when you need a reusable success standard. Use
other formats for one-time tasks, identity definition, procedure lists, or
feature-level verification.

## Master Template

Fill every `/goal` using this template. All fields marked * are required.

```markdown
## /goal: [Short Name]

**Category**: [EXPLORE / DEFINE / PLAN / BUILD / VERIFY / DEPLOY / MONITOR / REFLECT]
**Scope**: [One-line: what this goal covers and excludes]

### Objective*
[Single declarative sentence: what success looks like in observable terms]

### Success Criteria* (verify ALL before returning)
- [Criterion 1: measurable, pass/fail verifiable condition]
- [Criterion 2: measurable, pass/fail verifiable condition]
- [Criterion 3: measurable, pass/fail verifiable condition]

### Constraints* (hard boundaries)
- MUST NOT: [forbidden action or output characteristic]
- MUST: [required characteristic every output must have]
- LIMIT: [quantified bound - time, length, count, etc.]

### Output Specification*
[Exact expected output: format, structure, required sections, naming conventions]

### Verification Method*
[How an independent checker confirms success without re-doing the work]

### Failure Modes to Prevent
- [Specific failure mode 1]: [prevention strategy]
- [Specific failure mode 2]: [prevention strategy]

### Context (optional)
[Domain assumptions, prerequisite state, related goals]

### Examples (optional)
**Good output example:** [brief illustration]
**Bad output example:** [brief illustration with why it fails]
```

## Required Fields Reference

| Field | Purpose | Quality Bar |
|-------|---------|-------------|
| Objective | North star for the agent | Observable state, not process description |
| Success Criteria | Done checklist | Each criterion is pass/fail verifiable |
| Constraints | Guardrails | Quantified where possible, MUST NOT/MUST/LIMIT format |
| Output Specification | Delivery contract | Format + structure + required elements |
| Verification Method | Independent confirmation | Method an external checker can execute |

## Category Quick Reference

Each workflow stage has a different goal category. Read the appropriate reference
file for detailed templates, examples, and stage-specific guidance.

| Category | Verb Family | Read This | Use When |
|----------|------------|-----------|----------|
| **EXPLORE** | explore, investigate, research | `references/categories.md` | Gathering information, learning, discovering |
| **DEFINE** | define, scope, frame | `references/categories.md` | Setting boundaries, specifying requirements |
| **PLAN** | plan, design, architect | `references/categories.md` | Creating blueprints, selecting approaches |
| **BUILD** | implement, build, create | `references/categories.md` | Producing artifacts, writing code/content |
| **VERIFY** | verify, validate, test | `references/categories.md` | Checking correctness, quality assurance |
| **DEPLOY** | deploy, launch, release | `references/categories.md` | Shipping to production |
| **MONITOR** | monitor, maintain, improve | `references/categories.md` | Ongoing operations, optimization |
| **REFLECT** | reflect, evaluate, learn | `references/categories.md` | Post-hoc analysis, knowledge capture |

## Gold Patterns (High-Impact)

Read `references/patterns.md` for full details with examples. The top 5:

1. **End-State-First** - Define "done" in verifiable terms before describing process
2. **Structured Output Contract** - Specify exact output format as an interface contract
3. **Constraint-First Safety** - Define what NOT to do before what to do
4. **Second-Agent Test** - A different agent can verify success from the output alone
5. **BDD-Style Verification** - Use Given/When/Then for complex multi-step goals

## Anti-Patterns (Avoid These)

Read `references/patterns.md` for the full catalog with before/after corrections.

| Anti-Pattern | Symptom | Fix |
|-------------|---------|-----|
| Vague Aspiration | "Create something good" | Add measurable criteria |
| Over-Specification | Prescribes every micro-step | Separate goal (outcome) from procedure (how) |
| Under-Specification | Missing output format | Add output contract section |
| Conflicting Signals | Multiple incompatible priorities | Explicit priority order |
| No Termination | Agent does not know when to stop | Add explicit stop conditions |
| Sycophancy Trap | Vague praise-seeking language | Replace with objective criteria |

## Workflow-Specific Guidance

Read the appropriate file when targeting a specific workflow type:

| Workflow Type | Read This File |
|---------------|---------------|
| Website building (frontend, UI/UX) | `references/workflow-guides.md` |
| Software build/CI-CD | `references/workflow-guides.md` |
| Research and analysis | `references/workflow-guides.md` |
| Product development | `references/workflow-guides.md` |

## Pre-Flight Quality Checklist

Before delivering any `/goal` directive, confirm ALL of the following.
**Any item marked [VETO] failing blocks delivery regardless of other quality.**

### A. Clarity
- [ ] Objective states an observable outcome, not a process
- [ ] Success criteria use pass/fail language (no "should" or "try to")
- [ ] Output format is specified with required sections/fields
- [ ] Constraints use MUST NOT / MUST / LIMIT format

### B. Verifiability
- [ ] Second-agent test: a different agent could verify success from output alone
- [ ] Each success criterion is independently checkable
- [ ] Verification method does not require re-doing the work

### C. Safety [VETO items - any failure blocks delivery]
- [ ] At least one MUST NOT constraint prevents harmful output
- [ ] No instruction conflicts with safety or compliance requirements
- [ ] Goal explicitly forbids fabricating data, sources, or credentials
- [ ] Stop conditions prevent infinite loops or runaway execution

### D. Completeness
- [ ] Category is assigned (EXPLORE/DEFINE/PLAN/BUILD/VERIFY/DEPLOY/MONITOR/REFLECT)
- [ ] Scope boundaries are explicit (what is included AND excluded)
- [ ] At least 2 specific failure modes are listed with prevention strategies
- [ ] Examples are provided for non-trivial goals

### E. Reusability
- [ ] Goal is parameterized (uses placeholders for context-specific values)
- [ ] No hardcoded dates, names, or one-time references
- [ ] Goal can guide multiple runs without modification

### F. Actionability
- [ ] Agent receiving this goal knows exactly what to produce
- [ ] Agent receiving this goal knows when to stop
- [ ] Agent receiving this goal knows what to avoid

**Minimum passing score: 10/12 items from sections A, B, D, E, F + ALL section C**
