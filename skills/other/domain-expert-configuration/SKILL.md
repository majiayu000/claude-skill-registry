---
name: domain-expert-configuration
description: Configuration UIs for domain experts — users who understand their field deeply but are not software developers — require domain language, sensible defaults, and grouping by professional concept rather than technical parameter. Use when designing settings panels, solver or algorithm configuration, constraint editors, or any UI where the user needs to tune the behaviour of a complex system without understanding its internals.
metadata:
  priority: 6
  pathPatterns:
    - "components/**"
    - "src/components/**"
    - "**/*.tsx"
    - "**/*.jsx"
    - "app/**"
    - "pages/**"
  promptSignals:
    phrases:
      - "configuration"
      - "settings panel"
      - "parameters"
      - "constraints"
      - "algorithm settings"
      - "solver"
      - "optimisation"
      - "optimization"
      - "tune"
      - "configure"
      - "expert settings"
      - "advanced settings"
retrieval:
  aliases:
    - configuration UI
    - settings panel
    - algorithm configuration
    - solver settings
    - constraint editor
    - domain expert settings
    - advanced configuration
    - parameter tuning
  intents:
    - design a configuration panel for domain experts
    - expose algorithm parameters to non-technical users
    - design a settings UI for an optimisation tool
    - group configuration parameters by domain concept
    - design constraint editors for professional tools
  examples:
    - design a settings panel for a batch-processing tool
    - the user is a domain expert, not a developer
    - how should I expose solver parameters to a non-technical expert
    - make this configuration UI understandable to domain experts
    - group these algorithm settings by what they control
---

# Domain Expert Configuration

A domain expert configuration UI exposes the parameters of a complex system — an optimisation algorithm, a planning engine, a simulation — to users who understand the problem domain deeply but have no knowledge of the system's internals.

The challenge: the system's parameters are defined in technical terms (weights, thresholds, flags, tolerances). The user thinks in domain terms (how long to wait, when to retry, how to group results). The UI must translate between these two vocabularies — always favouring the user's language.

---

## The Core Principle: Domain Language Over Technical Language

Every parameter label, tooltip, and error message should describe what the parameter *means in the user's world*, not what it *does inside the system*.

| Technical label | Domain label |
|---|---|
| `max_concurrent_jobs` | Maximum tasks running at once |
| `enable_auto_retry` | Retry failed tasks automatically |
| `batch_allocation_threshold` | Start a new batch after (% filled) |
| `request_timeout_ms` | Maximum wait per request (seconds) |
| `enable_fuzzy_matching` | Allow approximate matches |

If you cannot write a domain label for a parameter, question whether the user should be exposed to it at all. Parameters that cannot be explained in domain terms belong in a developer configuration file, not in the user-facing UI.

---

## Grouping by Domain Concept

Parameters should be grouped by the aspect of the real-world problem they control — not by their technical category (booleans together, numbers together) and not alphabetically.

A processing tool might group as:

```
Processing limits
  └─ Maximum tasks at once
  └─ Maximum wait per request
  └─ Memory ceiling

Matching rules
  └─ Allow approximate matches
  └─ Case sensitivity
  └─ Required fields

Batching behaviour
  └─ Batch fill threshold
  └─ Maximum batches
```

Each group should have a short heading that describes *what aspect of the task it controls*, not what kind of parameter it is.

---

## Sensible Defaults

Every parameter must have a default that works correctly for the majority of cases. The user should be able to start with all defaults and get a reasonable result.

**Show the default value:** When a field is at its default, indicate this. When a user has changed a value away from the default, make it easy to reset.

```
Maximum wait per request  [___30___ s]  ← custom value
                          [↺ Reset to default (15 s)]

Batch fill threshold  [_70_ %]  (default)  ← at default
```

**Why this matters:** Domain experts often do not know what value to enter for an unfamiliar parameter. If the field is blank with no hint, they will either skip it (leaving the system in an unknown state) or enter an arbitrary value. A visible default communicates "this is what the system assumes unless you tell it otherwise."

---

## Input Types Matched to Domain Semantics

Choose the input type based on what the parameter *means*, not just its data type.

| Parameter nature | Input type | Example |
|---|---|---|
| Binary rule (on/off) | Toggle switch | "Retry automatically: [toggle]" |
| Constrained number with clear unit | Number input with unit label | "Max wait: [___] s" |
| Choice between named options | Select or radio group | "Output format: [JSON ▾]" |
| Percentage or ratio | Slider with numeric input | "Batch fill threshold: [━●━━] 70%" |
| Free text identifier | Text input | "Job reference: [___]" |

**Units are mandatory** for all numerical inputs. Never show a bare number without its unit. Place the unit label adjacent to the input (suffix preferred: `[___] cm`, not `cm [___]`).

---

## Progressive Disclosure

Not all parameters are equally important. Expose them in layers:

**Primary settings (always visible):** The parameters that control the most commonly adjusted behaviour. A domain expert should be able to accomplish 80% of their tasks by adjusting these alone.

**Advanced settings (collapsed by default):** Parameters for edge cases, fine-tuning, or less common scenarios. Behind a disclosure control ("Advanced options ▾"). Opened by users who need them, invisible to those who don't.

**Developer / system parameters:** Not shown in the user-facing UI at all. In a config file or environment variable.

Do not put everything in the advanced section as a catch-all. If a parameter is needed frequently, it belongs in the primary settings.

---

## Saved vs. Session Configuration

Many operational tools distinguish between:

- **Saved configuration:** The user's persisted preferences (their standard processing setup, their standard rules). Loaded automatically.
- **Session overrides:** One-off adjustments for a specific run that should not change the saved defaults.

Make this distinction explicit in the UI. If the user adjusts a parameter for one run, they should not have to worry about corrupting their saved defaults.

```
┌─ Configuration ────────────────────────────┐
│  Maximum wait    [30 s]   ← session only    │
│  Retry on fail   [✓]      ← saved           │
│                                             │
│  [Save as default]   [Reset to saved]       │
└─────────────────────────────────────────────┘
```

---

## Validation and Constraint Feedback

When a value is invalid or conflicts with another setting, tell the user in domain terms.

| Technical error | Domain error |
|---|---|
| `value out of range [0, 9999]` | "Wait time must be between 0 and 999 seconds" |
| `constraint conflict: retry=true, fail_fast=true` | "Retry automatically and Stop on first failure cannot both be enabled" |
| `threshold must be < 1.0` | "Batch fill threshold must be less than 100%" |

Show validation inline, adjacent to the affected field. Do not wait for the user to submit before reporting conflicts.

For settings that interact with each other, show the relationship: "When automatic retry is off, the maximum-attempts setting has no effect." This prevents the expert from wasting time tuning a parameter that isn't active.

---

## Review Checklist

- [ ] Does every parameter label use domain language, not technical language?
- [ ] Are parameters grouped by the domain concept they control, not by type or alphabetically?
- [ ] Does every parameter have a visible default value?
- [ ] Is there a "reset to default" action for individual parameters?
- [ ] Do all numerical inputs show their unit adjacent to the field?
- [ ] Are input types matched to domain semantics (toggle for binary, select for named options)?
- [ ] Are advanced parameters hidden by default behind a disclosure control?
- [ ] Is the distinction between saved configuration and session overrides explicit?
- [ ] Is validation shown inline in domain language?
- [ ] Are parameter interactions (conflicts, dependencies) explained in the UI?
