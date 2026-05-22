---
name: design-review
description: Orchestrates a structured design review by running existing skills in a diagnostic funnel, from complexity triage through structural, interface, and surface checks to a full red-flags sweep. Use when reviewing a file, module or PR for overall design quality and you want a comprehensive, prioritized assessment rather than a single-lens check. Not for applying one specific lens (use that skill directly) or for evolutionary analysis of how code changed over time (use code-evolution).
argument-hint: "[file, module, or PR to review]"
metadata:
  allowed-tools: Read, Grep
---

# Design Review Orchestrator

When invoked with $ARGUMENTS, scope the entire review to the specified target. Read the target code first, then proceed through the phases below in order. This skill orchestrates other skills from Clairvoyance (https://clairvoyance.fyi). It works best when the full collection is installed.

This skill does not replace individual lenses. It sequences them into a diagnostic funnel that moves from broad to narrow, skipping work when early phases find nothing actionable.

## Diagnostic Funnel

### Phase 1: Complexity Triage

Apply **complexity-recognition** checks against the target.

- Identify the three symptoms: change amplification, cognitive load, unknown unknowns
- Trace any symptoms to root causes: dependencies or obscurity
- Weight findings by the complexity formula: high-traffic code first

This phase determines whether the target has measurable complexity problems. If it does, subsequent phases diagnose where.

### Phase 2: Structural Review

Apply these lenses to the target's module-level architecture:

- **module-boundaries**: Are the boundaries drawn around knowledge domains or around steps in a process?
- **deep-modules**: Does each module provide powerful functionality behind a simple interface? Check for classitis, pass-through methods and shallow wrappers.
- **abstraction-quality**: Does each layer provide a genuinely different way of thinking, or do adjacent layers duplicate the same abstraction?

Focus on the modules that Phase 1 identified as highest-complexity. If Phase 1 found nothing, scan the largest or most-connected modules.

### Phase 3: Interface Review

Apply these lenses to the interfaces exposed by the modules from Phase 2:

- **information-hiding**: Does the interface leak implementation details? Check for back-door leakage (shared knowledge not in any interface).
- **general-vs-special**: Does the interface mix general-purpose mechanisms with special-case knowledge? Check for boolean parameters serving one caller.
- **pull-complexity-down**: Are callers forced to handle complexity the module could absorb? Check for exposed edge cases, required configuration and exceptions that could be defined away.
- **error-design**: Are errors defined out of existence where possible? Check for catch-and-ignore, overexposed exceptions and error handling longer than the happy path.

### Phase 4: Surface Review

Apply these lenses to naming and documentation:

- **naming-obviousness**: Do names create precise mental images? Check the isolation test: seen without context, could the name mean almost anything?
- **comments-docs**: Do comments capture what the code cannot say (intent, rationale, constraints)? Check for comments that repeat code and implementation details contaminating interface documentation.

### Phase 5: Red Flags Sweep

Run the full **red-flags** 17-flag checklist against the target. Any flag triggered in Phases 1-4 will already be marked. This phase catches flags that earlier phases may not have surfaced (especially Process flags 15-17: No Alternatives Considered, Tactical Momentum, Catch-and-Ignore).

## Early Termination

If Phase 1 finds no measurable complexity AND Phase 5 triggers zero flags, stop. Report the target as clean. Do not force findings where none exist.

## Prioritization

Rank findings in this order:

1. **Syndrome clusters**: Multiple flags pointing to the same root cause (e.g., information leakage + conjoined methods + repetition all stemming from one misplaced boundary). These indicate systemic issues. Fixing the root cause resolves all flags in the cluster.
2. **Boundary issues**: Information leakage, module boundary problems and abstraction mismatches. These compound over time and infect adjacent code.
3. **Canary flags**: Hard to Pick Name, Hard to Describe, Non-obvious Code, No Alternatives Considered. These are the cheapest signals. Catch them and the structural flags never materialize.
4. **Structural issues**: Shallow modules, pass-through methods, classitis. These require refactoring but affect a bounded area.
5. **Surface issues**: Naming and documentation problems. Important but lowest cost to fix and lowest risk if deferred.
