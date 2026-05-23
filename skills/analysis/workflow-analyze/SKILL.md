---
name: workflow-analyze
description: Analyze issue and generate analysis.md with solution approaches. Use when starting a new task or feature to thoroughly analyze the problem and compare solution options.
disable-model-invocation: true
---

# Issue Analysis Command

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

---

## Outline

1. **Parse User Input**:
   - Extract task description from $ARGUMENTS
   - Generate task name (2-4 words, English, hyphen-separated)

2. **Define Problem**:
   - Identify current situation, problem to solve, and goals

3. **Investigate Solutions**:
   - Research 2-4 approaches
   - Analyze pros/cons of each approach
   - Evaluate based on coding principles

4. **Final Selection**:
   - Choose the most appropriate approach
   - Clarify rejection reasons

5. **Generate Questions**:
   - Select **maximum 3** unclear items only
   - Use reasonable defaults + Assumptions for the rest

6. **Write Documents** (Dual Language):
   - Create `docs/work/WORK-{task-name}/analysis.ko.md` (Korean - for user reference)
   - Create `docs/work/WORK-{task-name}/analysis.md` (English - for agent consumption)

---

## Key Rules

### 📝 Documentation Language

**CRITICAL**: You must generate **TWO versions** of all documents:

1. **Korean version** (`analysis.ko.md`): For user reference - written in Korean
2. **English version** (`analysis.md`): For agent consumption - written in English

**Both versions must contain identical structure and information**, only the language differs.

### 🎯 Balanced Analysis Principles

1. **Problem Definition**: Include concrete scenarios rather than abstract descriptions
2. **Solution Approach**: Consider both user perspective and technical feasibility
3. **Implementation Method**: Keep core changes concise, specify new dependencies
4. **Completion Criteria**: Separate feature verification and technical implementation

### 🎭 Anti-Bias Rules (CRITICAL)

**Core Principle: Be honest. Don't hide what exists, don't invent what doesn't.**

1. **Analyze First, Conclude Later**
   - Complete ALL approach analysis BEFORE making any selection

2. **Write What's True**
   - If A has 5 pros and B has 1, write exactly that (no forced balance)
   - If side effects exist, state them; if none, say so (no hiding, no inventing)
   - When rejecting an approach, acknowledge what you're giving up

3. **Neutral Language**
   - Forbidden: "simply", "obviously", "clearly", "just", "merely"
   - Use: "may", "could", "potentially"

### ✅ Must Do

- Conclusion first (Executive Summary)
- **Include concrete scenarios** (Problem Definition) - 1-4 cases depending on issue
- **Explain user impact** (Solution Approach) - How will it be used?
- **Evaluate technical feasibility** (Solution Approach) - Why is it suitable?
- Evaluate solutions based on coding principles
- Concise bullet points
- **NEEDS CLARIFICATION maximum 3**
- Use reasonable defaults

### ❌ Must Not Do

- Verbose explanations
- Duplicate content
- **Only abstract problem definitions** (without concrete examples)
- **Excessive technical details** (going into implementation level)
- **Missing user perspective** (talking only about technology)
- Solutions that conflict with coding principles
- Infinite questions
- **Listing obvious things** (e.g., React state, JSON schema)

---

## Document Template

Files to create:

- `docs/work/WORK-{task-name}/analysis.ko.md` (Korean version)
- `docs/work/WORK-{task-name}/analysis.md` (English version)

```markdown
# [Task Name] - Analysis Result

## 🎯 Conclusion (TL;DR)

**Selected Approach**: [Approach Name]
**Key Reason**: [Why this approach was chosen - 1-2 sentences]

---

## 📋 Problem Definition

**Concrete Scenarios** (as needed):

- [Case 1: What problem occurs in what situation]
- [Case 2: Another specific situation]

**Current Problem**: [What is inconvenient or impossible]
**Goal**: [What this task aims to achieve]

---

## 📦 Scope

**Included**:

- [Scope Item 1]
- [Scope Item 2]

**Excluded**:

- [What to explicitly exclude]

---

## 🔍 Solution Investigation

### Approach 1: [Name]

**Method**:

- [How to solve - including user impact and technical method]

**Pros**:

- [List ALL genuine pros]

**Cons**:

- [List ALL genuine cons]

**Side Effects/Risks** (if any):

- [What negative consequences may occur]

### Approach 2: [Name]

[Same structure]

---

## ✅ Final Selection

**Adopted**: Approach N

**Trade-offs Accepted** (if any):

- [Benefit from other approaches that won't be available]

**Known Risks** (if any):

- [What could go wrong]

**Selection Reason**:

- [Why this approach is most suitable]

**Rejected Approaches** (include what you're losing):

- Approach X: [Rejection reason] — Would have provided: [lost benefit]

---

## 🛠️ Implementation Method

**Core Changes**:

- [Change Item 1]
- [Change Item 2]

**New Dependencies**: [None / Name]

---

## 🎯 Completion Criteria

**Feature Verification**:

- [ ] [Scenario 1 verification]
- [ ] [Existing feature regression test]

**Technical Implementation**:

- [ ] [Core change implementation]
- [ ] [Unit test writing]

---

## ❓ Needs Confirmation

**Current Assumptions**:

- [Assumption 1]: [Default value]

**If Needed**:

- [Items needing additional confirmation - maximum 3]

---

## 🔍 Objectivity Self-Check

- [ ] Wrote what's true (no hiding, no inventing)
- [ ] Rejected approaches' lost benefits acknowledged
- [ ] Used neutral language ("may/could", not "will/obviously")
```

---

## Execution

Now start the task according to the guidelines above.
