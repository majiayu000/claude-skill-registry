---
name: complexity-recognition
description: Diagnoses what makes code complex and why, using the three-symptom two-root-cause framework. Use when code feels harder to work with than it should but the specific problem is unclear. This skill identifies WHETHER complexity exists and WHERE it comes from. Not for scanning a checklist of known design smells (use red-flags) or evaluating a specific module's depth (use deep-modules).
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Complexity Recognition Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

> "Complexity is anything related to the structure of a software system that makes it hard to understand and modify the system." — John Ousterhout, _A Philosophy of Software Design_

Complexity is relative to the task: the same codebase can feel simple for one operation and painful for another. The writer of the code is often the worst judge of its complexity. If reviewers find it complex, it is. Diagnose it using three symptoms, two root causes, and the fundamental formula.

## When to Apply

- When code feels harder to work with than it should be
- When small changes require edits in many places
- When developers frequently introduce bugs in unfamiliar code
- During "should we refactor this?" discussions

## Core Principles

### The Complexity Formula

$$C = \sum_{p}(c_p \times t_p)$$

Each part's complexity weighted by how often developers work with it.

- Complexity in frequently-touched code matters most
- Encapsulating complexity where it won't be encountered is nearly as valuable as eliminating it

> "Complexity is more apparent to readers than writers." — John Ousterhout, _A Philosophy of Software Design_

If colleagues find your code complex, it is complex.

A gnarly subsystem that nobody modifies contributes almost nothing. A moderately messy module that every feature passes through dominates the total. A "simple" change to a high-traffic module matters more than a large refactor of something rarely touched.

### Three Symptoms

#### 1. Change Amplification

Directly measurable: count files touched for a single-concept change. Use this for refactoring prioritization.

#### 2. Cognitive Load

Fewer lines does not always mean less cognitive load. A terse framework requiring reverse-engineering its entire mental model is not simpler. The question is _how much do I need to know?_

#### 3. Unknown Unknowns

Unknown unknowns are the worst symptom because they are invisible. Change amplification is visible and cognitive load is navigable, but unknown unknowns let you finish a change feeling confident while the bug ships. The design goal that counters all three symptoms is to make the system obvious.

> "An obvious system is one where a developer can make a quick guess about what to do, without thinking very hard, and yet be confident that the guess is correct." — John Ousterhout, _A Philosophy of Software Design_

### Two Root Causes

#### Dependencies

Represent code that cannot be understood or modified in isolation. Not all are bad. The goal should always be to have fewer dependencies, and make remaining ones **obvious** rather than hidden.

#### Obscurity

Important information is not obvious. Vague names, undocumented assumptions, invisible dependencies, inconsistency.

> "The need for extensive documentation is often a red flag that the design isn't quite right." — John Ousterhout, _A Philosophy of Software Design_

These two root causes intersect in hidden dependencies, where a dependency exists without any surface representation in the code. Hidden dependencies produce the worst bugs because there is no signal to search for and no warning that information is missing.

### Complexity Is Incremental

> "Complexity isn't caused by a single catastrophic error; it accumulates in lots of small chunks." — John Ousterhout, _A Philosophy of Software Design_

Every developer can justify their small addition, but if everyone reasons this way, the total grows steadily. Discipline must be applied at the level of individual decisions, because that's the only level where complexity enters.

### Elimination vs. Encapsulation

1. **Eliminate**: Redesign so the complexity doesn't exist. Always best.
2. **Encapsulate**: Hide it in a deep module so most developers never encounter it.

> "Isolating complexity in a place where it will never be seen is almost as good as eliminating the complexity entirely." — John Ousterhout, _A Philosophy of Software Design_

## Review Process

1. **Identify hot paths**: Which code is modified most frequently?
2. **Check for change amplification**: Pick a likely change, count files touched
3. **Assess cognitive load**: What must a developer know to work here safely?
4. **Hunt unknown unknowns**: Hidden dependencies, implicit invariants, undocumented constraints?
5. **Trace root causes**: Dependency or obscurity?
6. **Recommend**: Eliminate the complexity, or encapsulate it in a deep module

Red flag signals for complexity are cataloged in **red-flags** (Repetition, Overexposure, Information Leakage, Non-obvious Code).
