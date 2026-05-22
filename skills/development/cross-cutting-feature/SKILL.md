---
name: cross-cutting-feature
description: "Step-by-step procedure for implementing features that cross multiple layers: models, functions, adapters, agent state, tools, config, and tests. Use when: adding a new constraint type, adding a new tool to an agent, new optimization feature, new agent capability, feature touches multiple files, implement constraint, add tool, agent feature, multi-layer change, end-to-end feature."
---

# Cross-Cutting Feature Implementation

Procedure for adding a feature that crosses the full stack:
**Model → Function → Adapter → State → Tool → Config → Tests**

## When to Use

- Adding a new feature that spans multiple layers (data model, business logic, API/tools, config)
- Adding a new tool or capability to an agent
- Any change where you ask "what files do I need to touch?"
- Features with user-facing input that flows through to domain logic

## Procedure

### Step 0: Discover the Layer Map

**If the feature adds data to an existing output or enriches a result**, load the
`root-cause-design` skill first and complete its trace procedure before proceeding.
That skill answers WHERE the data belongs; this skill answers HOW to wire it through all layers.

Before touching any code, map your codebase layers. Search for:

```
□ Models / schemas — Where are data shapes defined? (Pydantic, dataclasses, TypedDict, etc.)
□ Domain logic — Where are pure functions / business rules?
□ Adapters — Where does data format conversion happen?
□ State — Where is persistent state managed? (agent state, session, DB)
□ Tools / API — Where is the user-facing interface?
□ Config / prompts — Where is agent behavior configured? (system prompts, tool descriptions)
□ Tests — Where are unit and integration tests?
```

Read the key files in each layer before writing anything. Understand what patterns
they already follow.

### Step 1: Model

Define the data shape first. This is the contract everything else depends on.

```
□ Create the model/schema class with field-level validation
□ Add the field to the parent request/config model (with a default so existing code doesn't break)
□ Add cross-field validation (e.g., unknown references, duplicates, conflicts)
□ If the feature resolves to a simpler form: add resolution logic in the model validator
```

**Why resolve in the model?** The model validator has access to all sibling fields
(other config, parameters, etc.), so it can resolve derived values without
threading parameters. This follows the Information Expert principle.

**Key question:** Can this model be constructed directly (not just through the adapter)?
If yes, validation and resolution MUST live in the model — not in the adapter.

### Step 2: Pure Functions

If the feature requires new calculations or transformations:

```
□ Write pure functions (no side effects, no I/O, no state)
□ Keep them testable in isolation — input → output, nothing else
□ Export from the module's public API
```

### Step 3: Adapter

If there's a translation layer between external formats and internal models:

```
□ Add the new field as a parameter
□ Pass it through to the model constructor
□ Keep it simple — the adapter MAPS, it doesn't TRANSFORM
```

If the model handles resolution (Step 1), the adapter is just a pass-through.
Don't duplicate logic here.

### Step 4: State

If the feature needs to persist across calls (agent conversations, sessions):

```
□ Add the field to the state schema
□ Use the appropriate merge strategy (replace, append, etc.)
□ Import the model type from Step 1
```

### Step 5: Tools / API

This is the user-facing interface. Typically the most complex step:

```
□ Create the tool/endpoint function
□ Register it in the tool/route list
□ Wire into summary/list functions (so users can inspect current state)
□ Wire into clear/reset functions (so users can undo)
□ Wire into the run/execute function (read from state, pass to adapter)
□ Write a helpful response message — show computed equivalents when applicable
```

### Step 6: Config / Prompts

If an LLM agent needs to know the tool exists, update the system prompt:

```
□ Add tool to the tools listing with signature and description
□ Add natural language examples showing when/how to use it
□ Update any enumerations (e.g., valid types for a "clear" command)
□ Update the agent's capability description if this is a new category
```

**Without this step, the LLM will never call your tool.**

### Step 7: Tests

Two levels:

```
Unit tests:
□ Valid construction (each input variant)
□ Rejection cases (invalid inputs, edge cases)
□ Pure function correctness (roundtrips, boundary values, monotonicity)
□ Auto-completion / derived field tests (if model resolves values)

Integration tests:
□ Feature actually affects the system output
□ Feature interacts correctly with existing features
□ Edge cases (binding vs non-binding, conflicts)
```

### Step 8: Verify

```
□ Run the full test suite — no regressions
□ Count files touched (expect 7–9 for a full cross-cutting feature)
□ Count function signatures modified (target ≤ 3; if more, see root-cause-design skill)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Resolving derived values in the adapter instead of the model | Move to model validator (it has access to sibling fields and works for all construction paths) |
| Forgetting config/prompt update | LLM agents won't know the feature exists |
| Forgetting the clear/undo path | Users can't remove what they added |
| Test fixtures with unrealistic parameters | Use values where the feature is actually reachable/testable |
| Threading a parameter through 4+ signatures | Put it in the model that already travels the pipeline (see root-cause-design skill) |
| Implementing all steps before running tests | Run tests after each layer to catch issues early |
