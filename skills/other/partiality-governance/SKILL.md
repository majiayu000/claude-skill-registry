---
name: partiality-governance
description: "Use when optional values, fallbacks, defaults, or failure paths materially influence behavior and need explicit governance. Goal: optionality and failure semantics are explicit, and non-happy paths remain deliberate."
---

# Partiality Governance

Govern missing values and failures so semantics stay explicit, core logic stays readable, and non-happy paths are deliberate.

## Response Contract

- Deliverable: apply the requested changes to the target artifact.
- Chat output: no additional output beyond the deliverable.

## Partiality Model

Definitions used to classify partiality and choose representations and placement.

### Partiality Classes

- **Missing value**
  A value may be absent.

- **Expected failure**
  A caller-actionable outcome that is part of normal control flow.

- **Unexpected failure**
  An invariant violation or impossible state.

### Boundaries

- **Leaf operations**
  Parsing, I/O, RPC, persistence. The origin of many Missing value and failure signals.

- **Boundary adapters**
  The layer that translates external partiality into domain-consumable forms and hosts policy decisions.

- **Core domain**
  Business rules and domain model where behavior should be expressed with minimal plumbing.

### Representations

- **Optional**
  A representation for Missing value when absence is a valid domain state.

- **Result**
  An explicit outcome representation for normal control flow that includes success and Expected failure.

- **Crash**
  Termination of the current unit of work for Unexpected failure.

## Governance Standards

Apply these standards throughout the change. Each standard is single-sourced here and referenced elsewhere by its ID.

- **optional.semantic_only — Optional means legitimate absence**
  Use Optional only for Missing value where absence is a valid domain state. If absence is invalid for the caller, treat it as Expected failure and represent it as Result.

- **result.expected_only — Result is for expected control flow**
  Use Result for normal control flow that includes Expected failure. Do not encode Unexpected failure as Result.

- **fail.unexpected_fast — Unexpected failures crash**
  Treat invariant violations and impossible states as Unexpected failure and Crash immediately. Do not convert them into defaults, fallbacks, or Expected failure.

- **fallback.no_silent — No silent fallback**
  Defaults, fallbacks, and degraded modes must be explicit in semantics and observable. Never “pretend success”.

- **context.preserve — Preserve diagnostic context**
  Preserve the original cause and relevant parameters when propagating or translating partiality.

- **catch.no_blanket — No blanket catch as control flow**
  Do not swallow failures. Handle only known Expected failure cases or translate at a Boundary adapter without changing semantics.

- **observability.required — Policy actions are observable**
  Fallbacks and degraded modes must emit structured signals suitable for debugging and alerting.

- **propagation.normalize — Normalize partiality before core domain**
  Translate Optional and Result at Boundary adapters so Core domain logic does not need pervasive Optional checks or Result plumbing. When partiality is semantically meaningful in the domain, represent it as an explicit domain state.

- **core.totality_prefer — Prefer total core logic**
  Keep Core domain code focused on domain behavior. Prefer explicit domain states over repeated guard clauses, Optional unwrapping, and Result branching.

## Workflow

1. Enumerate partiality points and label each as Missing value, Expected failure, or Unexpected failure.
2. Choose one representation at the origin:
   - Missing value with legitimate absence: Optional
   - Expected failure: Result
   - Unexpected failure: Crash
3. Move policy decisions into Boundary adapters and remove leaf-level policy implementations. Apply `fallback.no_silent`.
4. Normalize Optional and Result at Boundary adapters so Core domain reads as domain behavior. Apply `propagation.normalize` and `core.totality_prefer`.
5. Remove silent defaults and blanket catching that hide semantics. Apply `fallback.no_silent`, `catch.no_blanket`.
6. Add diagnostics and policy visibility. Apply `context.preserve`, `observability.required`.
7. Run acceptance checks.

## Acceptance Criteria

A revision is complete only if all checks pass.

- **Response**: Output satisfies the Response Contract.
- **Standards satisfied**: `optional.semantic_only`, `result.expected_only`, `fail.unexpected_fast`, `fallback.no_silent`, `context.preserve`, `catch.no_blanket`, `observability.required`, `propagation.normalize`, `core.totality_prefer`.
