---
name: prototype
description: "Validate technical feasibility with minimum code before full implementation. Prove ONE atomic question ('Can I X?') through 6-phase workflow: SCOPE, CONTEXT, MINIMUM, EXECUTE, VERIFY, CAPTURE. Use when facing technical uncertainty, unsure if something is possible, or need proof before planning. Triggers on: prototype, POC, prove this works, spike, demo this, can I do X, is it possible, feasibility check. Produce prototype log in docs/prototypes/ with YES/NO/PARTIAL verdict and chain to whiteboarding."
---

# Skill: prototype

**Prove it works. Minimum code. Maximum learning.**

---

## Master Checklist - Execute In Order

**YOU MUST complete each checkbox before proceeding to the next phase.**

### Phase 1: SCOPE
- [ ] **1.1** Ask user: "What ONE thing are you trying to prove?"
- [ ] **1.2** Narrow until atomic (starts with "Can I...")
- [ ] **1.3** State the scope: "SCOPE: [single question]"

### Phase 2: CONTEXT
- [ ] **2.1** Check current branch: `git branch --show-current`
- [ ] **2.2** If on main/master → Create branch: `git checkout -b prototype/<scope-slug>`
- [ ] **2.3** Run `Skill(code-foundations:aposd-reviewing-module-design)` to survey existing code
- [ ] **2.4** State: "CONTEXT: [environment summary]"

### Phase 3: MINIMUM
- [ ] **3.1** Run `Skill(code-foundations:cc-pseudocode-programming)` - write 3-5 lines of pseudocode
- [ ] **3.2** Verify pseudocode is ONLY happy path (no error handling)
- [ ] **3.3** Verify code will be <50 lines (if not, re-scope)
- [ ] **3.4** State: "MINIMUM PATH: [pseudocode]"

### Phase 4: EXECUTE
- [ ] **4.1** Write code from pseudocode
- [ ] **4.2** Add header comment: `// PROTOTYPE: [scope] // NOT PRODUCTION`
- [ ] **4.3** Run the code
- [ ] **4.4** State: "RESULT: [what happened]"

### Phase 5: VERIFY
- [ ] **5.1** Answer: YES / NO / PARTIAL
- [ ] **5.2** If PARTIAL → identify what specifically worked/didn't

### Phase 6: CAPTURE
- [ ] **6.1** Create `docs/prototypes/` if needed
- [ ] **6.2** Write prototype log to `docs/prototypes/YYYY-MM-DD-<scope>.md`
- [ ] **6.3** Commit: `git add . && git commit -m "prototype: [scope] - [YES/NO/PARTIAL]"`

---

## Phase 1: SCOPE (One Question Only)

**YOU MUST get a single atomic question before any code.**

### Step 1.1 - Ask the Question

Ask user: **"What ONE thing are you trying to prove?"**

### Step 1.2 - Narrow Until Atomic

| Scope | Problem | Fix |
|-------|---------|-----|
| "Can I build a notification system?" | Too broad | "Can I show ONE notification?" |
| "Can I integrate with the backend?" | Too vague | "Can I call ONE endpoint?" |
| "Can I make it work?" | Undefined | "Can I [specific thing]?" |

**Keep asking:** "What's the FIRST thing that needs to work?"

### Step 1.3 - State the Scope

```
SCOPE: Can I [specific atomic thing]?
```

**GATE:** Do not proceed until scope is ONE atomic question.

---

## Phase 2: CONTEXT (Environment Check)

**YOU MUST check branch and survey existing code.**

### Step 2.1 - Branch Check

```bash
git branch --show-current
```

### Step 2.2 - Create Prototype Branch

**If on main/master, YOU MUST create a branch:**

```bash
git checkout -b prototype/<scope-slug>
```

**GATE:** Do not write code on main/master.

### Step 2.3 - Survey Existing Code (MANDATORY)

**Run this skill:**
```
Skill(code-foundations:aposd-reviewing-module-design)
```

Answer these questions:
- What modules/APIs exist that might help?
- What patterns does this codebase use?
- What's the simplest integration point?

### Step 2.4 - State Context

```
CONTEXT: [repo/scratch], [available APIs], [constraints]
```

---

## Phase 3: MINIMUM (Shortest Path)

**YOU MUST write pseudocode before any real code.**

### Step 3.1 - Write Pseudocode (MANDATORY)

**Run this skill:**
```
Skill(code-foundations:cc-pseudocode-programming)
```

Write 3-5 lines of pseudocode:
- Happy path ONLY
- NO error handling
- NO edge cases
- NO validation

### Step 3.2 - Verify Happy Path Only

Check your pseudocode:
- [ ] No try/catch or error handling?
- [ ] No input validation?
- [ ] No edge case handling?
- [ ] Hardcoded values where possible?

**If any are checked NO → Remove them. This is POC.**

### Step 3.3 - Verify Size

**If pseudocode suggests >50 lines of code → STOP and re-scope.**

### Step 3.4 - State Minimum Path

```
MINIMUM PATH:
1. [pseudocode line 1]
2. [pseudocode line 2]
3. [pseudocode line 3]
```

**GATE:** Do not write code until pseudocode is approved.

---

## Phase 4: EXECUTE (Surgical Code)

**YOU MUST translate pseudocode to code with prototype header.**

### Step 4.1 - Write Code From Pseudocode

Translate each pseudocode line to real code. **Add nothing extra.**

### Step 4.2 - Add Prototype Header (MANDATORY)

Every prototype file MUST start with:

```javascript
// PROTOTYPE: [scope question]
// NOT PRODUCTION: No error handling, hardcoded values
// DATE: YYYY-MM-DD
```

### Step 4.3 - Run the Code

Execute and observe what happens.

### Step 4.4 - State Result

```
RESULT: [exactly what happened when code ran]
```

---

## Phase 5: VERIFY (Binary Answer)

**YOU MUST give a definitive answer.**

### Step 5.1 - Answer YES / NO / PARTIAL

| Answer | Meaning | Next Action |
|--------|---------|-------------|
| **YES** | It works as expected | Proceed to CAPTURE |
| **NO** | Blocked, doesn't work | Document blocker in CAPTURE |
| **PARTIAL** | Some parts work | Identify what specifically, then CAPTURE |

### Step 5.2 - If PARTIAL, Specify

```
PARTIAL:
- WORKS: [what succeeded]
- BLOCKED: [what failed]
- UNCLEAR: [what needs more investigation]
```

---

## Phase 6: CAPTURE (Document for Production)

**YOU MUST document learnings. Undocumented prototypes are wasted.**

### Step 6.1 - Create Directory

```bash
mkdir -p docs/prototypes
```

### Step 6.2 - Write Prototype Log (MANDATORY)

**Create `docs/prototypes/YYYY-MM-DD-<scope-slug>.md`:**

```markdown
# Prototype: [Scope Question]

**Date:** YYYY-MM-DD
**Branch:** prototype/<scope-slug>
**Result:** YES / NO / PARTIAL

## What We Proved

[1-2 sentences]

## Minimum Working Code

```[language]
[the code that worked]
```

## Key Learnings

- [learning 1]
- [learning 2]

## Production Considerations

- [ ] Error handling needed for: [list]
- [ ] Edge cases: [list]
- [ ] Estimated complexity: simple / medium / complex

## Next Steps

- [ ] Proceed to `/code-foundations:whiteboarding` with these learnings
- [ ] OR: More prototyping needed for [specific question]
- [ ] OR: Blocked by [blocker], need [alternative]
```

### Step 6.3 - Commit

```bash
git add .
git commit -m "prototype: [scope] - [YES/NO/PARTIAL]"
```

---

## Crisis Invariants - NEVER SKIP

| Check | Why Non-Negotiable |
|-------|-------------------|
| **Atomic scope first** | Multiple goals = nothing proven |
| **Branch before code** | POC on main = pollution |
| **Pseudocode before code** | No pseudocode = scope creep |
| **<50 lines** | More = not a prototype |
| **Prototype log written** | Undocumented = forgotten |

---

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "I already know what to build" | Then pseudocode takes 30 seconds. Do it. |
| "Pseudocode is overkill for POC" | Pseudocode PREVENTS scope creep. Do it. |
| "I'll document after" | You won't. Write the log now. |
| "This is throwaway, skip the branch" | Prototypes on main = pollution. Branch. |
| "Let me add error handling quick" | That's production work. Happy path only. |
| "It mostly works" | PARTIAL is not YES. Be precise. |
| "I'll remember what I learned" | You won't. Write it down. |

---

## Skill Dependencies

This skill REQUIRES invoking:

1. **`Skill(code-foundations:aposd-reviewing-module-design)`** - Phase 2.3 (survey existing code)
2. **`Skill(code-foundations:cc-pseudocode-programming)`** - Phase 3.1 (write pseudocode)

These are NOT optional. They are mandatory steps in the checklist.

---

## Chaining

- **RECEIVES FROM:** User question, feature idea, technical uncertainty
- **CHAINS TO:** `/code-foundations:whiteboarding` (with prototype learnings)
- **SKILLS INVOKED:** aposd-reviewing-module-design, cc-pseudocode-programming
