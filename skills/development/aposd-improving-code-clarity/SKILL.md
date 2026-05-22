---
name: aposd-improving-code-clarity
description: "Enforce comments-first workflow for new code and improve naming/documentation for existing code. Use when writing new classes, methods, or functions; when code is 'confusing' or 'hard to understand'; when naming precision is poor; or when variable documentation lacks units, bounds, or ownership. Triggers on: new code, comments-first, naming review, documentation review, not obvious, hard to understand. Produces well-documented code with precise naming, or identifies design problems when comments/names are hard to write."
---

# Skill: aposd-improving-code-clarity

## STOP - The Obviousness Rule

**If a code reviewer says your code is not obvious, it is not obvious**—regardless of how clear it seems to you. "Obvious" exists in the reader's mind, not the writer's.

**For new code:** Write comments BEFORE implementation. Comment difficulty signals design problems—fix the design, not the comment.

---

## What Counts as "New Code"

**Comments-first applies to ALL of these:**

| Scenario | Why It's "New Code" |
|----------|---------------------|
| Writing from scratch | Obviously new |
| Copy-paste-modify | New context requires new understanding |
| Extending existing function (>5 lines) | Substantial additions need documentation |
| Refactoring that changes interfaces | Interface change = new abstraction |
| Converting prototype to production | Throwaway code becoming permanent |

**Comments-first ALSO applies to:**
- Test methods (they're methods too)
- Lambda functions with non-trivial logic (>1 expression)
- Configuration that defines behavior
- Database migrations with business logic

**Exemptions (but document why):**
- One-liner utility functions with precise names: `def square(x): return x * x`
- Trivially obvious getters/setters with no business logic
- Character-level bug fixes (`>=` to `>`)
- Debug/logging code that will be deleted within 24 hours (mark with `// TEMP:`)

---

## Comments-First Workflow

**For new classes/methods, write comments BEFORE implementation:**

```
1. Write class interface comment (what abstraction it provides)
2. Write interface comments for public methods (signatures + comments, empty bodies)
3. Iterate on comments until structure feels right
4. Write instance variable declarations with comments
5. Fill in method bodies, adding implementation comments as needed
6. New methods discovered during implementation: comment before body
7. New variables: comment at same time as declaration

Result: When code is done, comments are also done.
```

### Why Comments-First Matters

| If You Delay | What Happens |
|--------------|--------------|
| "I'll document after coding" | Documentation often never gets written |
| "Code isn't stable yet" | Delay compounds—"even more stable in a few weeks" |
| "Just one more feature first" | Backlog grows huge and unattractive |
| "I'll find time later" | There is never a convenient time |

### Comment Quality Requirements

Comments must meet these criteria or they don't count:

| Requirement | Bad Example | Good Example |
|-------------|-------------|--------------|
| **Describe abstraction** | `# Does the thing` | `# Calculates compound interest with variable rates` |
| **Include non-obvious details** | `# Process data` | `# Processes data in chunks to stay under memory limit` |
| **Different words than code** | `# Gets user` for `getUser()` | `# Fetches user from cache, falling back to DB` |
| **Precision for variables** | `# The count` | `# Number of active connections (0 to MAX_CONN)` |

**If your comment just restates the function name, you haven't done comments-first.**

---

## Comment Types

| Type | Where | Purpose | Priority |
|------|-------|---------|----------|
| **Interface** | Declarations | Define abstraction, usage info | Highest—required for every class, variable, method |
| **Implementation** | Inside methods | Help understand what code does | Lower—often unnecessary for simple methods |
| **"How We Get Here"** | Code paths | Explain conditions under which code runs | Useful for unusual situations |
| **Cross-Module** | Dependencies | Describe cross-boundary relationships | Rare but important |

### Comment Levels

| Level | Focus | Use For |
|-------|-------|---------|
| **Precision** (lower) | Exact details: units, bounds, null, ownership | Variable declarations |
| **Intuition** (higher) | Reasoning, abstract view, overall intent | Methods, code blocks |

---

## Variable Comment Checklist

For each variable, answer these questions in the comment:

- [ ] What are the units? (seconds? milliseconds? bytes?)
- [ ] Are boundaries inclusive or exclusive?
- [ ] What does null mean, if permitted?
- [ ] Who owns the resource (responsible for freeing/closing)?
- [ ] What invariants always hold?

**Goal:** Comment should be complete enough that readers never need to examine all usage sites.

---

## Naming Principles

### Two Required Properties

| Property | Requirement | Test |
|----------|-------------|------|
| **Precision** | Name clearly conveys what entity refers to | "Can someone seeing this name in isolation guess what it refers to?" |
| **Consistency** | (1) Always use this name for this purpose (2) Never use it for other purposes (3) All instances have same behavior | Check all usages |

### Naming Procedure

```
1. Name Evaluation Test:
   "If someone sees this name without declaration or context,
   how closely can they guess what it refers to?"

2. Precision Check:
   - Could this name refer to multiple things? → Too vague
   - Does this name imply narrower usage than actual? → Too specific
   - Target: name matches actual scope exactly

3. Consistency Check:
   - Is this name used everywhere for this purpose?
   - Is this name used ONLY for this purpose?
   - Do all variables with this name behave identically?
```

---

## Common Naming Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Vague status words | `blinkStatus` | `cursorVisible` (predicate showing true/false meaning) |
| Too generic | `getCount()` | `numActiveIndexlets` |
| Too specific | `delete(Range selection)` | `delete(Range range)` if method works on any range |
| Similar names for different things | `socket` vs `sock` | Distinct, descriptive names |
| Type in name | `strName` | Just `name` (IDEs show types) |
| Repeating class in variable | `File.fileBlock` | `File.block` (context is clear) |

---

## Red Flags

| Red Flag | Symptom | What It Signals |
|----------|---------|-----------------|
| **Comment Repeats Code** | Same words in comment as in entity name | Comment adds no value—rewrite with different words |
| **Hard to Describe** | Difficulty writing simple, complete comment | **Design problem**—fix the design, not the comment |
| **Hard to Pick Name** | Can't find simple name that creates clear image | **Design smell**—underlying entity lacks clean design |
| **Vague Name** | Name could refer to many things (`status`, `flag`, `data`) | Conveys little information; misuse likely |
| **Interface Describes Implementation** | Interface comment must explain internals | Class/method is shallow—abstraction is inadequate |
| **Implementation Contaminates Interface** | Interface docs include internal details | Violates separation of concerns |

---

## Interface vs Implementation Comments

| Interface Comment | Implementation Comment |
|-------------------|------------------------|
| Describes externally visible behavior | Describes internal workings |
| Defines the abstraction | Helps understand how code works |
| Required for every public entity | Optional for simple methods |
| What user needs to use it | What maintainer needs to modify it |
| **Never include implementation details** | Can reference interface concepts |

---

## Anti-Rationalization Table

### Classic Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "I'll add comments after" | Code isn't stable yet | Delay compounds; documentation never gets written |
| "The code is self-documenting" | Good names exist | Code cannot capture abstractions; comments are the only way |
| "This is obvious" | Obvious to you now | You wrote it; first-time readers didn't |
| "Comments get out of date" | Maintenance burden | Comments-first keeps them synchronized |
| "I know what good names are" | Naming feels intuitive | Intuition fails; use the evaluation test |

### Pressure-Based Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "Demo in 30 minutes" | Time pressure is real | 5 minutes for comments saves 30 minutes of explanation later |
| "Team is blocked waiting" | Social pressure | They'll be MORE blocked debugging undocumented code |
| "Senior dev said add docs later" | Authority told me | Authority doesn't override discipline; push back |

### Technical Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "The type system documents it" | Types are precise | Types show WHAT, not WHY; comments explain intent |
| "My PR description covers it" | I'll explain there | PR descriptions aren't in the code; readers won't see them |
| "Design doc covers this" | Documentation exists | Design docs drift from code; interface comments stay with code |

---

## Types vs Comments

Strong type systems are valuable but don't replace comments:

| Types Tell You | Comments Tell You |
|----------------|-------------------|
| WHAT the signature accepts | WHY this design was chosen |
| WHAT the return type is | WHAT invariants must hold |
| WHAT constraints the compiler enforces | WHAT the abstraction represents |
| Structure | Intent |

---

## Emergency Bypass Criteria

Skip comments-first ONLY when ALL of these conditions are true:

1. Production is down RIGHT NOW
2. Users are actively impacted, security breach in progress, OR data loss occurring
3. The fix is minimal (rollback or single-line change)
4. You commit to returning for documentation within 24 hours

**If bypassing:** Add TODO marker: `// TODO(YYYY-MM-DD): document - emergency fix for [issue]`

---

## Quick Reference

```
BEFORE writing any new code:

1. COMMENT FIRST - Write interface comment before implementation
2. NAME PRECISELY - Can someone guess what it is in isolation?
3. NAME CONSISTENTLY - Same name everywhere, only for this purpose

WHEN commenting existing code:

1. DON'T REPEAT - Use different words than the code
2. PRECISION for variables - Units, bounds, null, ownership, invariants
3. INTUITION for methods - Intent, reasoning, what not how
4. HARD TO DESCRIBE? - Fix the design, not the comment

DESIGN SMELL SIGNALS:
- Hard to write simple comment → design problem
- Hard to pick clear name → design problem
- Interface must describe implementation → shallow abstraction
```


---

## Chain

| After | Next |
|-------|------|
| Comments/naming done | cc-code-layout-and-style (CHECKER) |
