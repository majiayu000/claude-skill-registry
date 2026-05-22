---
name: code-foundations
description: "Classify code tasks and execute task-specific checklists with quality gates. Route to WRITE, DEBUG, REVIEW, OPTIMIZE, REFACTOR, SIMPLIFY, or SECURE workflows, each invoking relevant CC and APOSD skills. Produce classification statement plus DONE/NOT DONE verdict with mandatory pre-commit verification. Use when writing, debugging, reviewing, fixing, implementing, optimizing, refactoring, simplifying, or securing code. Triggers on: implement, build, create, debug, fix bug, broken, error, review, audit, optimize, slow, performance, refactor, clean up, simplify, confusing, too complex, secure, vulnerability."
---

# Code Foundations

**When in doubt, load this skill. When NOT in doubt, load it anyway.**

---

## Master Checklist: Execute In Order

### Phase 1: Classification (MANDATORY - Do First)

- [ ] **1.1** Identify task type from user signals:
  | Signal | Task Type |
  |--------|-----------|
  | "implement", "write", "build", "add", "create" | → WRITE |
  | "debug", "fix bug", "failing", "broken", "error" | → DEBUG |
  | "review", "check", "audit", "is this good?" | → REVIEW |
  | "optimize", "slow", "performance", "faster" | → OPTIMIZE |
  | "refactor", "clean up", "improve structure" | → REFACTOR |
  | "simplify", "too complex", "confusing" | → SIMPLIFY |
  | "secure", "vulnerability", "validate input" | → SECURE |

- [ ] **1.2** State classification: "This is a [TASK TYPE] task"

- [ ] **1.3** If ambiguous, ask: "Are you looking for [option A], [option B], or something else?"

---

### Phase 2: Mindset Check (For WRITE, DEBUG, REFACTOR)

- [ ] **2.1** INVOKE cc-developer-character
- [ ] **2.2** Verify: Am I thinking strategically, not tactically?
- [ ] **2.3** Check for rationalization red flags (see below)

---

### Phase 2.5: Pattern Reuse Gate (For WRITE, DEBUG, REFACTOR, SECURE)

**MANDATORY: Before implementing, search the codebase.**

- [ ] **2.5.1** Search: How is this done elsewhere in this codebase?
- [ ] **2.5.2** Identify: What patterns exist for this type of work?
- [ ] **2.5.3** Decide: Follow existing pattern OR document why diverging

| If | Then |
|----|------|
| Pattern exists and is good | Follow it exactly |
| Pattern exists but mediocre | Follow anyway (consistency > perfection) |
| Pattern exists but bad | Document why diverging, consider fixing globally |
| No pattern exists | You're establishing one - be deliberate |

**See:** [pattern-reuse-gate.md](../../references/pattern-reuse-gate.md)

---

### Phase 3: Execute Task-Specific Checklist

**Go to the checklist for your task type:**

- WRITE → [Write Checklist](#write-checklist)
- DEBUG → [Debug Checklist](#debug-checklist)
- REVIEW → [Review Checklist](#review-checklist)
- OPTIMIZE → [Optimize Checklist](#optimize-checklist)
- REFACTOR → [Refactor Checklist](#refactor-checklist)
- SIMPLIFY → [Simplify Checklist](#simplify-checklist)
- SECURE → [Secure Checklist](#secure-checklist)

---

### Phase 4: Pre-Commit Gate (MANDATORY - Before "Done")

- [ ] **4.1** INVOKE aposd-verifying-correctness
- [ ] **4.2** Requirements: Each requirement mapped to code?
- [ ] **4.3** Concurrency: Shared state protected?
- [ ] **4.4** Errors: All failure points handled?
- [ ] **4.5** Resources: All acquired resources released?
- [ ] **4.6** Boundaries: Edge cases (empty, null, huge) handled?
- [ ] **4.7** Security: Untrusted input validated?
- [ ] **4.8** State verdict: DONE or NOT DONE (list blockers)

---

## WRITE Checklist

**Goal:** Create new code with good design

### Prerequisites
- [ ] INVOKE cc-developer-character (mindset)
- [ ] INVOKE cc-construction-prerequisites (architecture ready?)

### Design Phase
- [ ] INVOKE aposd-designing-deep-modules
- [ ] Sketch 2-3 radically different approaches (not just "think through")
- [ ] Compare approaches: Which has simplest interface?
- [ ] Choose approach and document rationale
- [ ] Verify depth: Interface much simpler than implementation?

### Implementation Phase
- [ ] INVOKE aposd-improving-code-clarity
- [ ] Write interface comments BEFORE implementation
- [ ] INVOKE cc-pseudocode-programming
- [ ] Write pseudocode, then translate to real code
- [ ] Names precise? (Can someone guess meaning in isolation?)
- [ ] Names consistent? (Same name = same thing everywhere?)

### Verification Phase (Parallel Subagents)

- [ ] CHECKER(cc-routine-and-class-design)
- [ ] CHECKER(cc-defensive-programming)

See [references/checker-dispatch.md](../../references/checker-dispatch.md)

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## DEBUG Checklist

**Goal:** Find and fix bug without making design worse

### Investigation Phase
- [ ] INVOKE cc-developer-character (mindset)
- [ ] INVOKE cc-quality-practices (Scientific Method)
- [ ] Stabilize error: Can you reproduce reliably?
- [ ] Locate error: Use binary search / divide-and-conquer
- [ ] Understand root cause (not just symptoms)

### Fix Phase
- [ ] INVOKE aposd-maintaining-design-quality
- [ ] Ask: "Is current design still optimal given this fix?"
- [ ] If NO: Refactor first, then fix
- [ ] If YES: Make fix within existing design
- [ ] INVOKE cc-refactoring-guidance
- [ ] Fix ONLY the bug (don't mix fix + refactor in one commit)
- [ ] Commit fix separately from any cleanup

### Verification Phase
- [ ] Verify fix actually works
- [ ] Check for similar bugs elsewhere (same pattern?)
- [ ] INVOKE cc-quality-practices: Search for similar defects

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## REVIEW Checklist

**Goal:** Detect design problems and complexity

> **CHECKER pattern:** See [references/checker-dispatch.md](../../references/checker-dispatch.md)

### Quick Checks (Inline)

**Complexity Symptoms:**
- [ ] Change amplification? (Simple change = many modifications?)
- [ ] Cognitive load? (Must know too much to work here?)
- [ ] Unknown unknowns? (Unclear what code/info is needed?) **← Worst**

**Module Depth:**
- [ ] Interface simpler than implementation?
- [ ] Few methods (not many small ones)?
- [ ] Information hidden (not leaked across modules)?

**Red Flags:**
- [ ] Shallow module (interface ≈ implementation)
- [ ] Information leakage (same knowledge in multiple places)
- [ ] Pass-through methods (just delegates to another)

### Full Checklists (Parallel Subagents)

- [ ] CHECKER(aposd-reviewing-module-design)
- [ ] CHECKER(cc-routine-and-class-design)
- [ ] CHECKER(cc-quality-practices)

### Output

- [ ] List Findings (from all agents)
- [ ] List Questions (need more context)
- [ ] Note Positive patterns

---

## OPTIMIZE Checklist

**Goal:** Improve performance based on measurement, not intuition

### Measurement Gate (MANDATORY)
- [ ] INVOKE cc-performance-tuning
- [ ] INVOKE aposd-optimizing-critical-paths
- [ ] **STOP: Have you measured?** (No measurement = no optimization)
- [ ] Profile data collected? (timing, call counts, memory)
- [ ] Specific hotspot identified? (not just "it's slow")
- [ ] Baseline established?
- [ ] Which dimension? (throughput / latency / memory / CPU)

### Fundamental Fixes (Try First)
- [ ] Can you add a cache?
- [ ] Can you use a better algorithm?
- [ ] Can you bypass layers?
- [ ] If YES to any → implement and re-measure

### Critical Path Redesign (Last Resort)
- [ ] What's minimum code for common case?
- [ ] Disregard existing structure—what's ideal?
- [ ] Define "the ideal" even if not fully achievable

### Verification
- [ ] Re-measure with same methodology
- [ ] Faster with data? → Keep
- [ ] Simpler AND at least as fast? → Keep
- [ ] Neither? → **BACK OUT changes**

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## REFACTOR Checklist

**Goal:** Improve structure without changing behavior

### Prerequisites
- [ ] INVOKE cc-developer-character (mindset)
- [ ] Code currently WORKS? (All tests pass?)
- [ ] If NO → This is FIXING, not refactoring. Go to DEBUG checklist.

### Planning
- [ ] INVOKE cc-refactoring-guidance
- [ ] INVOKE aposd-maintaining-design-quality
- [ ] Design fundamentally sound? (If NO → consider rewrite)
- [ ] Changes touch >30% of module? (If YES → consider rewrite)
- [ ] Make list of specific refactoring steps

### Execution (One At A Time)
- [ ] Save starting code (version control checkpoint)
- [ ] Do ONE refactoring
- [ ] Recompile and retest
- [ ] State: "Tests pass after [change]"
- [ ] Commit if tests pass
- [ ] Repeat for next refactoring

### Verification (Parallel Subagents)

- [ ] CHECKER(cc-control-flow-quality)
- [ ] CHECKER(cc-routine-and-class-design)

See [references/checker-dispatch.md](../../references/checker-dispatch.md)

**Quick Checks:**
- [ ] Behavior preserved? (Same tests pass)
- [ ] Design improved? (Simpler interfaces, less duplication)

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## SIMPLIFY Checklist

**Goal:** Reduce complexity, not just relocate it

### Analysis
- [ ] INVOKE aposd-simplifying-complexity
- [ ] Identify complexity symptoms present
- [ ] Identify what makes it complex (dependencies? obscurity?)

### Error Reduction Hierarchy (Apply In Order)
For each error condition:
- [ ] **Level 1 - Define out:** Can semantics eliminate this error?
- [ ] **Level 2 - Mask:** Can low-level code handle without exposing?
- [ ] **Level 3 - Aggregate:** Can multiple errors share one handler?
- [ ] **Level 4 - Crash:** Rare, unrecoverable, app-level only?
- [ ] Document which level applied and why

### Pull Complexity Down (Check All Three)
- [ ] Is complexity related to module's existing functionality?
- [ ] Will pulling down simplify code elsewhere?
- [ ] Will pulling down simplify module's interface?
- [ ] All three YES? → Pull down. Otherwise → Leave.

### Verification
- [ ] Interfaces simpler than before?
- [ ] Callers do less work than before?
- [ ] Error handling consolidated or eliminated?
- [ ] Complexity REDUCED (not just relocated)?

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## SECURE Checklist

**Goal:** Protect against malicious or malformed input

### Analysis (Parallel Subagents)

- [ ] CHECKER(cc-defensive-programming)
- [ ] INVOKE aposd-simplifying-complexity (error reduction context)

See [references/checker-dispatch.md](../../references/checker-dispatch.md)

**Identify:**
- [ ] All external input sources
- [ ] Trust boundaries

### Validation (For Each External Input)
- [ ] Input validated before use?
- [ ] No string concatenation for SQL/shell/HTML?
- [ ] Path traversal prevented?
- [ ] Secrets not logged or exposed in errors?
- [ ] Auth/authz checked BEFORE action?

### Error Handling
- [ ] No empty catch blocks?
- [ ] Error messages don't leak security info?
- [ ] Assertions used for bugs only (not expected errors)?

### Pre-Commit
- [ ] Run Phase 4 checklist

---

## Rationalization Red Flags

**If you think any of these, STOP and apply the checklist anyway:**

| Thought | Reality |
|---------|---------|
| "This is simple/trivial" | Simple tasks have HIGHEST error rates |
| "I can already see the issue" | Seeing ≠ systematic verification |
| "I already know how to do this" | Knowing ≠ executing checklist |
| "It's just config, not code" | Config that affects runtime IS code |
| "The code already works" | Your CHANGE can break what worked |
| "I'll refactor later" | Later = never |
| "Just make it work" | Tactical thinking → permanent slowdown |
| "I don't have time" | Checklist takes minutes; debugging takes hours |
| "It's just one line" | One-line changes have highest error rate |
| "Tests pass, so it's done" | Tests check behavior, not design quality |

---

## Crisis Mode (Production Down)

**You STILL must:**
1. [ ] Classify the task (5 seconds)
2. [ ] State what you're skipping and why
3. [ ] Fix ONLY—no refactoring, no cleanup
4. [ ] Verify fix works
5. [ ] Commit to returning within 24 hours for full checklist

**What you may NOT skip:**
- Input validation on external data
- Verifying fix actually works
- One sentence explaining WHY the fix works

---

## Two Skill Families

| Family | Source | Focus | Prefix |
|--------|--------|-------|--------|
| **Code Complete** | McConnell | Process rigor, metrics, checklists | `cc-*` |
| **APOSD** | Ousterhout | Design philosophy, complexity reduction | `aposd-*` |

**Use both.** CC provides tactical rigor; APOSD provides strategic philosophy.

---

## Quick Reference: All Skills

### CC Skills (Process & Metrics)
| Skill | Use For |
|-------|---------|
| cc-developer-character | Mindset check before WRITE/DEBUG/REFACTOR |
| cc-construction-prerequisites | Architecture ready before coding |
| cc-pseudocode-programming | Design-before-code |
| cc-routine-and-class-design | Cohesion, coupling, inheritance |
| cc-defensive-programming | Error handling, validation |
| cc-refactoring-guidance | Safe refactoring process |
| cc-quality-practices | Testing, debugging, reviews |
| cc-control-flow-quality | Nesting, complexity, loops |
| cc-data-organization | Variables, types, data structures |
| cc-code-layout-and-style | Formatting, visual structure |
| cc-performance-tuning | Optimization process |
| cc-integration-practices | Build, integration |

### APOSD Skills (Design Philosophy)
| Skill | Use For |
|-------|---------|
| aposd-designing-deep-modules | Interface design, design-it-twice |
| aposd-simplifying-complexity | Error reduction, pull-down technique |
| aposd-improving-code-clarity | Comments-first, naming |
| aposd-maintaining-design-quality | Strategic vs tactical mindset |
| aposd-reviewing-module-design | Complexity symptoms detection |
| aposd-optimizing-critical-paths | Measure-first optimization |
| aposd-verifying-correctness | Pre-commit verification |

---

## Shared Reference

- [aposd-foundations.md](../../references/aposd-foundations.md) - Complexity vocabulary
