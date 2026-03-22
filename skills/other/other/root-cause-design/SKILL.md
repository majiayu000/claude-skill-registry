---
name: root-cause-design
description: "Trace data flow and find root cause BEFORE writing code. Use when: adding a field to output, enriching a result, passing a parameter through multiple functions, modifying function signatures, fixing 'data not available' issues, parameter threading, band-aid pattern, enrich output, add field, data flow analysis, where does data belong."
---

# Root-Cause Design

**Stop. Before you write a single line of code, trace the data flow.**

This skill prevents the most common agent anti-pattern: patching the symptom
instead of fixing the root cause. It applies to ANY change that adds data to
an output, modifies function signatures, or "enriches" a result.

## When to Use

- Adding a new field to a model or output
- "X is not available in the result" — you're about to calculate X somewhere
- Passing the same parameter through 3+ function signatures
- Calculating something post-hoc and attaching it to a result
- Any change where you think "I'll just add a parameter here"

## Procedure

### Step 1: Trace — Where Is the Output Constructed?

Don't start where the output is CONSUMED. Find where it is CONSTRUCTED.

```
Ask: "Where is <OutputType> first instantiated?"
Search for: <OutputType>( ... ) in the codebase
That function is your target — not the caller, not the consumer.
```

### Step 2: Search — Does the Data Already Exist?

Before creating new parameters, search the pipeline:

```
Ask: "Does this data already exist in any object that already flows through this pipeline?"

Look at:
  - Config/parameter objects that travel through the full call chain
  - State objects that persist across calls
  - Request/input models that carry user data
  - Domain entities that the pipeline already passes around
```

### Step 3: Decide — Where Does It Belong?

| Situation | Action |
|-----------|--------|
| Data describes a model that already travels the pipeline | Add field to that model (with sensible default) |
| Data is computed from pipeline inputs | Compute it where the output is constructed |
| Data is genuinely external (user input, API call) | Pass as parameter (last resort) |

### Step 4: Validate — Signature Count

After your change, count how many function signatures you modified:

| Signatures touched | Assessment |
|---------------------|------------|
| 0–1 | Good design — data found its home |
| 2–3 | Acceptable — sometimes unavoidable |
| 4+ | Smell — data probably doesn't have a home. Go back to Step 2 |

## Anti-Patterns to Catch

### Parameter Threading
```
❌ caller(x) → middle(x) → inner(x) → consumer(x)
   Same parameter threaded through 4 signatures just to reach its destination.

✅ Put x in the object that already travels through all those layers.
   0 signatures changed.
```

### Band-Aid Enrichment
```
❌ result = process(...)
   result.extra = compute_extra(result)   # patched after construction

✅ Build the field INTO the result where it's first constructed.
```

### Union Type Hack
```
❌ def process(config: dict | list[dict]):
      if isinstance(config, list): ...

✅ Use a single typed model. Each instance carries its own typed value.
```

### Optional That's Always Wanted
```
❌ def build(threshold: float | None = None):
      if threshold is not None: ...

✅ Give the field a default on the model: threshold: float = 1.0
   No conditional, no optional, always available.
```

## The Bus Principle

> "Don't create a taxi if there's already a bus on the same route."

If an object already travels through the entire pipeline:
`input → transform → process → build → output`

...and you need a new data point that DESCRIBES that object, put it on the bus.
Don't create a parallel parameter path.

### When to Break the Rule

If the model already has 10+ fields of mixed concerns (math params + display
config + thresholds + ...), it may be time to split into a separate config
object. But for 1–2 fields, the existing model is the right place (**YAGNI**).

## The "3 Whys" Check

Before writing code, ask why three times:

```
1. WHY can't the consumer see X?
   → Because X is not in the output.

2. WHY is X not in the output?
   → Because the builder function doesn't compute it.

3. WHY doesn't the builder compute it?
   → Because it doesn't have access to Y.

   → WHO has Y? → Find that object → THAT is where the fix belongs.
```

## Quick Checklist

Before writing code, answer these:

```
□ Where is the output CONSTRUCTED? (not consumed)
□ Does the data already exist in a pipeline object?
□ Am I about to thread a parameter through 3+ signatures?
□ Am I computing something post-hoc that could be built in-place?
□ How many signatures will I touch? (target: 0–1)
```

If you can't answer these, you haven't traced the data flow yet. Read more code.
