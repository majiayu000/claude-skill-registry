---
name: aposd-reviewing-module-design
description: "Evaluate module design using APOSD principles with 40-item checklist. Detect complexity symptoms (change amplification, cognitive load, unknown unknowns), shallow modules, information leakage, pass-through methods, and structural anti-patterns. Produce categorized design review (Critical/Moderate/Observations/Positive). Use when reviewing code, assessing interfaces, during PR review, or evaluating 'is this too complex?' Triggers on: code review, design review, module complexity, interface assessment, PR review, structural analysis."
---

# Skill: aposd-reviewing-module-design

## STOP - Systematic Review Required

**Run the checklist.** The checklist exists because intuition misses structural problems.

**Unknown unknowns are highest severity.** If it's unclear what code/info is needed for changes, flag immediately.

---

## Evaluation Checklist

Use this systematic checklist when reviewing code:

### 1. Complexity Symptoms (Ch2)

| Symptom | Question | If Yes |
|---------|----------|--------|
| **Change Amplification** | Does a simple change require modifications in many places? | Flag dependency problem |
| **Cognitive Load** | Must developer know too much to work here? | Flag obscurity or leaky abstraction |
| **Unknown Unknowns** | Is it unclear what code/info is needed for changes? | **Highest severity** - flag immediately |

### 2. Module Depth (Ch4)

| Check | Deep (Good) | Shallow (Bad) |
|-------|-------------|---------------|
| Interface vs implementation | Interface much simpler | Interface rivals implementation |
| Method count | Few, powerful methods | Many, limited methods |
| Hidden information | High | Low |
| Common case | Simple to use | Complex to use |

**Red flag:** If understanding the interface isn't much simpler than understanding the implementation, the module is shallow.

### 3. Information Hiding (Ch5)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Information Leakage** | Same knowledge in multiple modules | High |
| **Temporal Decomposition** | Structure mirrors execution order rather than knowledge | Medium |
| **Back-Door Leakage** | Shared knowledge not visible in interfaces but both depend on it | High |
| **Overexposure** | Common use forces learning rare features | Medium |

### 4. Layer Abstraction (Ch7)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Pass-Through Method** | Method only passes arguments to another with same API | High |
| **Adjacent Similar Abstractions** | Following operation through layers, abstractions don't change | High |
| **Shallow Decorator** | Large boilerplate, small functionality gain | Medium |

**Test:** Follow a single operation through layers. Does the abstraction change with each method call? If not, there's a layer problem.

### 5. Together/Apart (Ch9)

| Red Flag | Detection | Severity |
|----------|-----------|----------|
| **Conjoined Methods** | Can't understand one method without another's implementation | High |
| **Special-General Mixture** | General mechanism contains use-case specific code | High |
| **Code Repetition** | Same code appears in multiple places | Medium |
| **Shallow Split** | Method split resulted in interface ≈ implementation | Medium |

---

## Red Flags Quick Reference

| Red Flag | Source | One-Line Detection |
|----------|--------|-------------------|
| Shallow Module | Ch4 | Interface as complex as implementation |
| Classitis | Ch4 | Many small classes, little functionality each |
| Information Leakage | Ch5 | Same knowledge in multiple modules |
| Temporal Decomposition | Ch5 | Structure follows execution order |
| Pass-Through Method | Ch7 | Method just delegates to another with same API |
| Conjoined Methods | Ch9 | Methods only understandable together |
| Special-General Mixture | Ch9 | General mechanism has use-case code |
| Code Repetition | Ch9 | Same code appears multiple places |
| Shallow Split | Ch9 | Method split resulted in interface ≈ implementation |

---

## Together/Apart Decision Procedure

When evaluating whether code should be combined or separated:

```
1. Do pieces share information?
   YES → Should probably be together

2. Would combining simplify the interface?
   YES → Should probably be together

3. Is there repeated code?
   YES → Extract shared method (if long snippet, simple signature)

4. Does module mix general-purpose with special-purpose?
   YES → Should be separated
```

**Key principle:** Depth > Length. Never sacrifice depth for length.

---

## Depth vs Length Rule

| Situation | Correct Action |
|-----------|---------------|
| Long method with clean abstraction | Keep together |
| Short method requiring another's impl to understand | Combine them |
| Method split creating conjoined pair | Undo the split |
| Long method with extractable subtask | Extract subtask only |

**Test for valid split:** Can the pieces be understood independently AND reused separately?

---

## Evaluation Output Format

When reporting findings, use:

```
## Design Review: [Component Name]

### Critical Issues (Must Address)
- [Red flag]: [Specific location] - [Why it's a problem]

### Moderate Issues (Should Address)
- [Red flag]: [Specific location] - [Why it's a problem]

### Observations (Consider)
- [Pattern noticed] - [Potential concern]

### Positive Patterns
- [What's working well]
```

---

## Before Flagging a Problem

Before reporting any red flag, validate:

1. **Steel-man check:** What's the best argument this design choice is intentional?
2. **Intentional shallowness:** Is this an adapter, facade, or decorator where thinness is the point?
3. **Testing seam:** Is this "leakage" actually a legitimate dependency injection point?
4. **Abstraction quality:** Can callers use this interface correctly without knowing implementation details?

---

## Cross-Module Analysis

Ask before concluding:

- **Are there related modules that should be reviewed together?** Classitis often hides across file boundaries.
- **Would combining these modules simplify the overall interface?** If yes, flag as potential shallow split.
- **Must callers use these modules in sequence?** If yes, possible temporal decomposition.

### Pattern Consistency Check

| Question | If Yes |
|----------|--------|
| Is there an existing pattern for this type of problem? | Compare approaches |
| Does this introduce a second way to do the same thing? | Flag unless justified |
| Would a maintainer be surprised by the difference? | Requires explicit documentation |

**Balance:** Evaluate patterns on merit, but don't create gratuitous inconsistency. The goal is maintainability, not conformance.

---

## When Principles Conflict

| Conflict | Resolution |
|----------|------------|
| Depth vs Cohesion | Prefer cohesion. A focused shallow module beats a bloated deep one. |
| Information Hiding vs Testability | Testing seams (injectable dependencies) are acceptable "leakage" |
| Simple Interface vs Configurability | Real systems need configuration; penalize only unnecessary complexity |

---

## Common Evaluation Mistakes

| Mistake | Reality |
|---------|---------|
| "It's long, so it's complex" | Length ≠ complexity. Depth matters more. |
| "Small classes are better" | Small classes are often shallow. Deep > small. |
| "More methods = better API" | Fewer powerful methods beat many limited ones. |
| "Separation is always good" | Subdivision has complexity costs. Sometimes combine. |
| "Code reuse requires extraction" | Only extract if snippet is long AND signature is simple. |
| "This is clearly good/bad" | Always run the systematic checklist. |
| "Standard pattern = automatically good" | Patterns can be misapplied. Require specific evidence. |

---

## Anti-Rationalization Table

| Rationalization | Counter |
|-----------------|---------|
| "I can see this is fine without the checklist" | **Stop.** The checklist exists because intuition misses structural problems. Run it anyway. |
| "This is too small to review systematically" | **Stop.** Small modules become core dependencies. Small doesn't mean safe. |
| "I know this codebase well" | **Stop.** Familiarity breeds blindness. Fresh eyes (the checklist) catch what you've normalized. |
| "The author is senior/experienced" | **Stop.** Experience doesn't prevent complexity. Apply same rigor regardless of author. |
| "It passes all the tests" | **Stop.** Tests check behavior, not design. Passing tests ≠ good architecture. |
| "I don't want to be nitpicky" | **Stop.** Red flags aren't nits. Complexity symptoms are real problems. Flag them. |
| "They'll push back on this feedback" | **Stop.** Your job is accurate evaluation, not social comfort. Present evidence. |
| "This matches what we already have" | **Stop.** Consistency with bad patterns spreads problems. Evaluate independently. |

---

## Quick Reference

```
SYSTEMATIC REVIEW CHECKLIST:

1. SYMPTOMS - Change amplification? Cognitive load? Unknown unknowns?
2. DEPTH - Interface simpler than implementation?
3. HIDING - Same knowledge in multiple modules?
4. LAYERS - Pass-through methods? Abstraction changes per layer?
5. STRUCTURE - Conjoined methods? Special-general mixture?

BEFORE FLAGGING:
- Steel-man check: Could this be intentional?
- Validate: Can caller use without knowing implementation?

OUTPUT:
- Critical (must fix)
- Moderate (should fix)
- Observations (consider)
- Positive patterns
```


---

## Chain

| After | Next |
|-------|------|
| Issues found | Fix or flag for /code-foundations:whiteboarding |
| No issues | Done |
