---
name: declaration-contract-design
description: 'Use when designing or refactoring declaration contracts for callables, data shapes, or generic/type parameters using a Name+Shape view (named vs positional) so meaning stays explicit and positional order stays stable.'
metadata:
  short-description: Named vs positional
---

# Declaration Contract Design

## 1) Name and shape

A declaration is read through **Name + Shape**.

* **Name**: the semantic label (what it does / what it represents).
* **Shape**: the declared dependencies or composition as an **addressable structure**—either **grouped into named concepts** (named shape) or **arranged by position** (positional shape).

### Shape forms

* **Named shape**: elements are addressed by name (fields, named members, named arguments).
* **Positional shape**: elements are addressed by position (positional parameters, tuples).

---

## 2) Principles

### 2.1 Semantics-first

* Name should state the meaning.
* Shape should expose the dependencies/composition that meaning requires.

### 2.2 Named grouping must be modeled

Introduce a named grouping only when it forms a **semantically modeled, nameable concept**.

### 2.3 Positional stability gradient

When a declaration uses **positional shape**, order elements by:

1. **Anchor**: identifies the primary subject (target/id/path/key). Most stable.
2. **Core**: required information defining the primary variation of meaning.
3. **Policy**: optional strategy/tuning/edge behavior.
4. **Observability**: tracing/logging/diagnostics/metrics.

Order: `Anchor → Core → Policy → Observability`.

---

## 3) Apply by declaration kind

### 3.1 Data-shape declarations (types, interfaces, data classes)

* Model fields into nameable concepts; avoid generic “extra/misc/config” groupings that accumulate unrelated concerns.
* Make required vs optional fields explicit in the declared shape (not by convention).

### 3.2 Callable declarations (functions, methods, constructors)

* Use a small positional prefix for stable meaning-defining dependencies when positional addressing benefits call sites.
* Use named/optional mechanisms primarily for **Policy/Observability** when available.
* If you introduce an “options/config” grouping, it must be a modeled, nameable concept; otherwise keep dependencies explicit.
* Keep meaning-defining dependencies legible at call sites (avoid hiding them inside unmodeled containers).

### 3.3 Parameterized declarations (generics / type parameters)

* Order by semantic priority: meaning-defining parameters first; constraint/defaulted parameters later; defaults at the end.
* Name parameters to reflect their role when it improves readability at use sites.
* Prefer inference where reasonable; require explicit parameters mainly to reduce ambiguity.

---

## 4) Checklist

* **Name+Shape**: is the declaration readable as name plus an intentional shape?
* **Named grouping**: do named groupings form nameable concepts (not convenience containers)?
* **Positional order**: if positional shape is used, does order follow `Anchor → Core → Policy → Observability`?
* **Volatility placement**: are Policy/Observability concerns kept out of the stable core and placed at the tail (positional or named/optional as applicable)?
