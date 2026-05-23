---
name: comments-as-last-resort
description: 'Use when comments are growing faster than clarity: many “what” comments, frequent drift, or code that needs explanation to be understood. Goal: encode intent in names and structure, and keep only high-value text such as contracts, why, and gotchas.'
metadata:
  short-description: Fewer, better comments
---

# Comments as Last Resort

Prefer code that explains itself through structure and naming. Use comments sparingly, only where code cannot carry the intent safely.

## Core Principle

**Write comments to preserve information that would otherwise be lost.**
If the information can live in code (names, types, structure), put it in code.

## What to Keep vs Remove

### Remove or replace these

* Comments that restate the next line or obvious behavior
* Step-by-step narration of straightforward code
* Comments that exist only because names are vague

Action: delete them, then improve naming or extract functions until the code reads cleanly.

### Keep or add these

* **Contracts**: inputs/outputs, invariants, error modes, side effects, performance expectations
* **Why**: rationale, tradeoffs, historical constraints, policy sources
* **Gotchas**: surprising behavior, mutation, concurrency, ordering, compatibility constraints
* **Public surface docs**: what callers must know to use it correctly

Action: write these as concise statements; prefer precise claims over storytelling.

## Replace Comments with Code

Use comments as a smell: if you need to explain a concept, try to name the concept.

### Techniques

* **Rename to carry intent**: functions, variables, types should express the domain meaning.
* **Extract intention-revealing units**: extract functions/classes/modules that name a step or rule.
* **Make rules explicit**: encode business rules as named predicates or policy objects instead of inline conditionals.
* **Make effects explicit**: separate pure computation from IO/mutation so behavior is obvious.

## Review Procedure

1. Scan comments and classify each as: Contract / Why / Gotcha / Public docs / “What”.
2. For every “What” comment:

   * delete it
   * make the code readable without it via renaming and extraction
3. For Contract/Why/Gotcha/Public docs:

   * keep it short
   * ensure it matches current behavior
   * place it at the closest boundary where readers need it
4. Re-check the file top-down: the code should be understandable without narration.

## Review Checklist

* No comment merely repeats the code.
* The remaining comments capture contracts, rationale, or risks.
* Naming and extraction make intent obvious.
* Public surfaces document caller-facing constraints.
* Comments and code agree; stale comments were removed or updated.
