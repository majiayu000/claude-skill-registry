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

Dependencies represent code that cannot be understood in isolation. Not all dependencies are bad, but the goal should always be to have fewer of them, and to make the ones that remain **obvious**.

#### Obscurity

Obscurity means important information is hidden or unclear. This shows up as vague names, undocumented assumptions, and invisible connections between parts of the code. If code needs a lot of explanation just to use it safely, the design is probably too complex.

### Hidden Dependencies Are the Worst

The root causes of complexity can intersect in hidden dependencies. A hidden dependency is a connection between two pieces of code with no visible sign in either one. Hidden dependencies produce the worst bugs because there is nothing to search for and no warning that information is missing.

### Complexity Is Incremental

Complexity rarely comes from one big mistake. It sneaks in through all the small ones. Each shortcut seems fine on its own, but they add up. By the time the system feels hard to work with, hundreds of tiny decisions got you there and can't be undone easily. That is why small choices matter just as much as big ones.

### Elimination vs. Encapsulation

When you find complexity, you have two options:

1. **Eliminate it**: Redesign so the complexity does not exist at all. This is always the best choice.
2. **Encapsulate it**: Bury it inside a module so that most code never has to deal with it. Complexity that callers never see causes almost no harm.

## Review Process

1. **Identify hot paths**: Which code is modified most frequently?
2. **Check for change amplification**: Pick a likely change, count files touched
3. **Assess cognitive load**: What must a developer know to work here safely?
4. **Hunt unknown unknowns**: Hidden dependencies, implicit invariants, undocumented constraints?
5. **Trace root causes**: Dependency or obscurity?
6. **Recommend**: Eliminate the complexity, or encapsulate it in a deep module

Red flag signals for complexity are cataloged in **red-flags** (Repetition, Overexposure, Information Leakage, Non-obvious Code).
