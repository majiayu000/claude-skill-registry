---
name: cc-code-layout-and-style
description: "Review code formatting and documentation using 74-item checklist from Code Complete. Two modes: CHECKER executes checklists with evidence tables, APPLIER guides layout decisions and commenting strategy. Use when code has inconsistent formatting, poor visual structure, unclear comments, or readability issues. Triggers on: review formatting, check layout, code style review, commenting style, make readable, multiple statements per line, endline layout, comments repeat code."
---

# Skill: cc-code-layout-and-style

## STOP - The Fundamental Theorem

**Good visual layout shows the logical structure of a program.**

- One statement per line (always)
- If it's hard to comment, rewrite the code
- Consistency matters more than any specific style *within acceptable bounds*

---

## Quick Reference

| Threshold | Value | Source |
|-----------|-------|--------|
| Blank line density | 8-16% optimal | Gorla, Benander 1990 |
| Indentation depth | 2-4 spaces optimal; 6+ reduces comprehension | Miaria 1983 |
| Line length | 80 chars guideline | p.753 |
| Comment density | ~1 comment per 10 statements (ceiling, not target) | Jones 2000 |
| Statements per line | 1 (always) | p.758 |

**Key Principles:**
- Good layout shows logical structure visually
- Consistency matters more than any specific style *within acceptable bounds*
- White space is the primary tool for showing structure
- Good comments clarify intent, not repeat code
- If it's hard to comment, rewrite the code

**Consistency Boundary (Critical):**
Consistency applies WITHIN Quick Reference thresholds, not instead of them. "We consistently use 8-space indentation" is consistently wrong. If existing codebase violates thresholds: flag as tech debt, follow Quick Reference for new code, propose migration plan. Never use "consistency" to justify violating research-backed minimums.

**Evidence Limitations:**
Studies cited are from 1979-2000 (pre-modern IDEs). Core cognitive principles persist, but specific numbers are heuristics, not validated boundaries. When team standards differ from thresholds, team standards win IF they fall within reasonable ranges (e.g., 100-char lines acceptable with wide monitors).

**Definitions:**
- **Pure Blocks:** Begin-end delimiters always paired with control statement, never standalone for scoping
- **Logical paragraph:** 3-7 related statements performing one conceptual step (setup, process, cleanup)
- **Tricky code:** Code requiring domain knowledge not evident from naming, non-obvious side effects, or uncommon algorithms

## Crisis Protocol

**Genuine emergency?** (Production down, data loss imminent, security breach)

**Absolute Minimums (non-negotiable even in crisis):**
- One statement per line (debugging requires this)
- Block delimiters on all control structures (prevents scope bugs - see Apple goto fail CVE-2014-1266)
- One comment explaining WHY the fix works

**Deferrable with MANDATORY follow-up (create ticket before deploying):**
- Full CHECKER mode review (within 48 hours)
- Blank line/comment density optimization
- Consistency baseline research

**Red Flags - Fake "Emergency":**
- Same code repeatedly needs "emergency" fixes
- No follow-up review ever happens
- "Emergency" invoked for features, not outages
- Developer invokes emergency to avoid code review

If red flags present: Apply full skill. This is not an emergency.

**Crisis-10 Checklist (minimum viable review):**
- [ ] Does each line contain at most one statement?
- [ ] Are control structures using block delimiters?
- [ ] Is there at least one comment explaining the fix's intent?
- [ ] Is the code readable enough to review in 2 minutes?
- [ ] Is a follow-up ticket created for full review?

## Exclusions

**Do NOT apply this skill to:**
- Auto-generated files (headers like "DO NOT EDIT", @generated, protobuf output)
- Minified/bundled production code
- Third-party vendored code

**Language-specific overrides:**
- Go: `gofmt` enforces tabs - follow language convention over skill thresholds
- Python: PEP-8/Black conventions win for indentation
- Formatter-enforced styles: Formatter config IS your style guide for what formatters handle

## Core Patterns

### Multiple Statements Per Line -> One Per Line
```java
// BEFORE: Hard to scan, hard to step through debugger [ANTI-PATTERN]
a = b; c = d; x = y;
i++; j++; array[i] = array[j];

// AFTER: Clear, scannable, debuggable
a = b;
c = d;
x = y;

i++;
j++;
array[i] = array[j];
```

### Endline Layout -> Block Indentation
```cpp
// BEFORE: Hard to maintain, comments drift from code [ANTI-PATTERN]
x = 1;        // Default value
y = 2;        // Another value
longVarName = 3; // This misaligns everything

// AFTER: Standard indentation, comments above or in dedicated blocks
// Initialize coordinates
x = 1;
y = 2;
longVarName = 3;
```

### Misleading Whitespace -> Precedence-Aligned Spacing
```cpp
// BEFORE: Spacing contradicts precedence [ANTI-PATTERN]
result = a+b * c-d;

// AFTER: Spacing reinforces precedence
result = a + b*c - d;
```

### Comments That Repeat Code -> Comments That Explain Intent
```java
// BEFORE: Says what code already says [ANTI-PATTERN]
i = i + 1; // add one to i
// Loop through array
for (int i = 0; i < array.length; i++) {

// AFTER: Explains WHY, not WHAT
i++; // Compensate for 0-based indexing in external API
// Process transactions oldest-first to maintain audit trail
for (int i = 0; i < transactions.length; i++) {
```

## Modes

### CHECKER
Purpose: Execute layout and documentation checklists against code
Triggers:
  - "review my code formatting"
  - "check code layout"
  - "are my comments appropriate"
  - "review code style"
Non-Triggers:
  - "how should I format this" -> APPLIER
  - "what commenting style should I use" -> APPLIER
Checklist: **See [checklists.md](./checklists.md)**
Output Format:
  | Item | Status | Evidence | Location |
  |------|--------|----------|----------|
Severity:
  - VIOLATION: Fails checklist item (multiple statements/line, no structure consistency)
  - WARNING: Partial compliance (comments could clarify more, spacing inconsistent)
  - PASS: Meets requirement

### APPLIER
Purpose: Guide layout decisions, commenting strategies, and self-documenting techniques
Triggers:
  - "how should I format this code"
  - "what commenting style"
  - "make this more readable"
  - "how to document this"
Non-Triggers:
  - "review my formatting" -> CHECKER
  - "check my comments" -> CHECKER

#### Layout Decision Procedure

**Step 1: Establish Consistency Baseline**
1. Does codebase have existing style guide or dominant pattern?
   - YES, and it meets Quick Reference thresholds -> Follow existing conventions
   - YES, but it violates Quick Reference thresholds -> Flag as tech debt; for new code, follow Quick Reference; propose migration plan
   - NO -> Establish conventions using values from Quick Reference
2. Check: project style guide → 3+ recent files in same directory → parent module conventions

**Step 2: Apply Block Structure**
1. Use Pure Blocks (begin-end bound to control statement) [p.738]
2. Indent statements within blocks consistently (2-4 spaces)
3. Use blank lines to separate logical paragraphs

**Step 3: Apply Statement Formatting**
1. One statement per line
2. One declaration per line
3. Continuation lines indented standard amount or aligned to emphasize structure
4. Use whitespace around operators to match precedence

**Step 4: Format Control Structures**
1. Put `begin` at end of line (Java style) OR on own line (C# style) - be consistent
2. Always use block delimiters even for single statements [p.748]
3. Use blank line before each comment block

#### Commenting Strategy Procedure

**Step 1: Comment Classification**
For each potential comment location, determine type:
- FILE HEADER: Copyright, description, change history
- ROUTINE: Purpose, inputs, outputs, assumptions, limitations
- PARAGRAPH: Explains following block of statements
- ENDLINE: Avoid except for data declarations

**Step 2: Apply Intent Filter (Priority Cascade - First Match Wins)**
Before writing any comment, ask IN ORDER (stop at first YES):
1. Does this repeat what the code says? -> DELETE IT
2. Can I rename something to eliminate need for comment? -> RENAME INSTEAD
3. Is this documenting tricky code? -> REWRITE: try rename → extract function → restructure control flow → only then add comment
4. Does this explain WHY, not WHAT? -> KEEP IT

**Step 3: Maintain Comments**
1. Keep comments close to code they describe
2. Use styles that are easy to maintain (no fancy boxes)
3. Treat comment maintenance as seriously as code maintenance

Produces: Formatted code, commenting guidelines, layout standards
Constraints: Consistency trumps any specific choice (p.735), avoid comment density >1:10 (Jones 2000)

## Rationalization Counters
| Excuse | Reality |
|--------|---------|
| "Our team has our own style" | Fine - but only within acceptable bounds (see Consistency Boundary). Consistently violating thresholds is consistently wrong. |
| "Multiple statements per line saves space" | Screen space is cheap; debugging/reading time is expensive. One statement per line always (p.758) |
| "Endline comments keep code compact" | They're hard to maintain and drift from code; use comment blocks above (p.767) |
| "The code is obvious, no comments needed" | Good comments explain intent, not mechanics. "Why" is rarely obvious (p.797) |
| "I'll add lots of comments to explain this tricky code" | "Don't document bad code - rewrite it." [Kernighan and Plauger] (p.798) |
| "Commenting takes too much time" | If hard to comment, you don't understand it well enough - that's valuable information (KEY POINT) |
| "I prefer 6-8 space indentation for visibility" | Studies show comprehension decreases above 4 spaces [Miaria 1983]. Subjects FELT 6-space was easier despite scoring lower. |
| "The formatter handles this" | Formatters handle syntax (spacing, braces). Humans handle semantics (logical groupings, comment quality, paragraph breaks). Use both. |
| "Line breaks don't matter to the compiler" | Code is for humans first. Formatting affects comprehension 10-20% [Miaria et al 1983] |
| "The code works, why change it?" | Working ≠ maintainable. Layout quality compounds over every future read. The 4 hours you spent are sunk; the next 40 hours of maintenance are not. |
| "Reformatting risks breaking working code" | Automated formatters and tests mitigate risk. Poor layout introduces maintenance bugs from misread structure. |
| "I've done this successfully many times" | Past success doesn't exempt current code. The 74-item checklist catches what expertise blindness misses. Execute all steps regardless of track record. |
| "Production is down, no time for formatting" | See Crisis Protocol. Absolute Minimums take <30 seconds and prevent the NEXT outage. |
| "We'll clean it up later" | "Later" never comes. 70% of "temporary" code is never cleaned up. Create the cleanup ticket NOW before deploying. |
| "These studies are 35 years old" | Cognitive principles persist; specific numbers are heuristics. See Evidence Limitations. |


---

## Chain

| After | Next |
|-------|------|
| Layout/style verified | aposd-improving-code-clarity (if naming/comments need work) |
| All formatting done | Done (pre-commit gate) |

