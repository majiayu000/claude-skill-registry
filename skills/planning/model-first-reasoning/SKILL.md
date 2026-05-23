---
name: model-first-reasoning
description: Apply Model-First Reasoning (MFR) to code generation tasks. Use when the user requests "model-first", "MFR", "formal modeling before coding", "model then implement", or when tasks involve complex logic, state machines, constraint systems, or any implementation requiring formal correctness guarantees. Enforces strict separation between modeling and implementation phases.
---

# Model-First Reasoning (MFR)

A rigorous methodology that REQUIRES constructing an explicit problem MODEL before any reasoning or implementation. The model becomes a frozen contract that governs all downstream work.

> Based on Kumar & Rana (2025), "Model-First Reasoning LLM Agents: Reducing Hallucinations through Explicit Problem Modeling" (arXiv:2512.14474)

## Why MFR Works

**Hallucination is not merely the generation of false statements—it is a symptom of reasoning performed without a clearly defined model of the problem space.**

Reasoning does not create structure; it operates on structure. When that structure is implicit or unstable, reasoning becomes unreliable. MFR provides "soft symbolic grounding"—enough structure to stabilize reasoning without imposing rigid formalism.

## Core Principle

**Phase 1 produces the MODEL. Phase 2 reasons/implements ONLY within the model.**

This prevents the common failure mode where reasoning introduces ad-hoc decisions, missing constraints, or invented behavior not grounded in the problem definition.

## Non-Negotiable Rules

1. **Phase 1 (Model)** produces NO code, no solution steps—only the formal model
2. **Phase 2 (Implement)** may NOT introduce new entities, state, actions, or constraints
3. If you need something not in the model: output exactly `MODEL INCOMPLETE` + what to add, then STOP
4. No invented APIs or dependencies. If not provided, either ask (unknowns) or create a stub clearly marked `STUB`

## The Model as Contract

After creating the model, run a **MODEL AUDIT** before coding:

### Audit Checks

| Check | Description |
|-------|-------------|
| **Coverage** | Every user requirement is represented in exactly one of: a constraint, the goal/acceptance criteria, or an action precondition/effect |
| **Operability** | Every operation your plan would require is present as an action |
| **Consistency** | Constraints don't contradict each other; action effects don't violate invariants |
| **Testability** | Every constraint has ≥1 test oracle |

If any audit check fails, revise the model (still Phase 1) until it passes.

## Freeze Rule

Once the audit passes, treat the model as **read-only source of truth**.

If later you discover missing info during implementation:
1. Emit a `MODEL PATCH` (minimal change)
2. Restart Phase 2 from scratch using the updated model

## Validation

After creating the model, write it to `model.json` and run the validator:

```bash
python scripts/validate-model.py model.json
```

Exit codes:
- `0` = Valid, ready for Phase 2
- `1` = Invalid structure (fix and retry)
- `2` = Valid but has unknowns (STOP after Phase 1)

## Output Format

### Phase 1: MODEL

The model may be expressed in natural language, semi-structured text, or JSON. Flexibility improves compliance—what matters is that the representation is **explicit, inspectable, and stable**.

For code generation tasks, the structured format below is recommended. Use [MODEL_TEMPLATE.json](MODEL_TEMPLATE.json) as a reference:

```json
{
  "deliverable": {
    "description": "What we're building",
    "files_expected": ["path/to/file.ts", ...]
  },
  "entities": [
    {"name": "EntityName", "description": "...", "properties": [...]}
  ],
  "state_variables": [
    {"name": "varName", "type": "...", "initial": "...", "description": "..."}
  ],
  "actions": [
    {
      "name": "actionName",
      "description": "...",
      "preconditions": ["..."],
      "effects": ["..."],
      "parameters": [...]
    }
  ],
  "constraints": [
    {"id": "C1", "statement": "...", "type": "invariant|precondition|postcondition"}
  ],
  "initial_state": ["description of starting conditions"],
  "goal": ["acceptance criteria"],
  "assumptions": ["things we assume to be true"],
  "unknowns": ["questions that must be answered before proceeding"],
  "requirement_trace": [
    {
      "requirement": "<verbatim from user>",
      "represented_as": "goal|constraint|action",
      "ref": "C1|action_name|goal_item"
    }
  ],
  "test_oracles": [
    {"id": "T1", "maps_to": ["C1"], "description": "how to verify constraint"}
  ]
}
```

**Critical**: If `unknowns` is non-empty, STOP after Phase 1. Do not implement until unknowns are resolved.

### Phase 1.5: MODEL AUDIT

Return:

```json
{
  "audit_pass": true|false,
  "issues": [
    {"type": "coverage|operability|consistency|testability", "detail": "..."}
  ]
}
```

If `audit_pass` is false, STOP and return to Phase 1 to revise the model.

### Phase 2: IMPLEMENTATION

Using ONLY the frozen model:

#### A) PLAN

Numbered steps where each step must be an instance of a defined action:

```
Step 1: [action_name]
  - Preconditions check: [list which preconditions are satisfied]
  - Effects applied: [what state changes]
  - Constraints check: [C1, C2, ...]
```

#### B) CODE

Create all files in `deliverable.files_expected`:

| Model Element | Code Translation |
|---------------|------------------|
| entities / state_variables | Types, interfaces, data models |
| actions | Functions/modules with validation + explicit failure modes |
| constraints | Runtime checks, defensive parsing, invariants |

#### C) TESTS

Implement all `test_oracles`. Every constraint must be covered by ≥1 test.

#### D) VERIFICATION MAP

For each constraint, document:
- Where it is enforced in code (file:line)
- Which tests cover it

## When to Use MFR

MFR is most valuable for:

- **Complex state machines** — where transitions must be valid
- **Business logic with invariants** — rules that must never be violated
- **Data transformations** — where input/output contracts matter
- **Multi-step workflows** — with dependencies between steps
- **Safety-critical features** — where bugs have high cost
- **Collaborative specifications** — where the model serves as documentation

**When NOT to use:** Simple, single-step tasks where the overhead of explicit modeling exceeds its benefit.

## Relationship to Other Reasoning Strategies

MFR is **complementary**, not competing:

- **With Chain-of-Thought**: Use CoT within Phase 2 for step-by-step reasoning over the model
- **With ReAct**: Treat the model as persistent state that actions operate on
- **With planning agents**: The model provides the domain specification that planners reason over

MFR provides a foundational layer that improves robustness of any reasoning strategy in constraint-heavy domains.

## Example Workflow

```
User: Build a shopping cart that enforces: max 10 items, no duplicate SKUs,
      total can't exceed $1000

You: [PHASE 1: MODEL]
{
  "entities": [
    {"name": "CartItem", "properties": ["sku", "price", "quantity"]}
  ],
  "constraints": [
    {"id": "C1", "statement": "cart.items.length <= 10", "type": "invariant"},
    {"id": "C2", "statement": "all SKUs in cart are unique", "type": "invariant"},
    {"id": "C3", "statement": "sum(items.price * items.quantity) <= 1000", "type": "invariant"}
  ],
  "actions": [
    {
      "name": "addItem",
      "preconditions": ["cart.items.length < 10", "sku not in cart", "new total <= 1000"],
      "effects": ["item added to cart"]
    }
  ],
  ...
}

[PHASE 1.5: MODEL AUDIT]
{
  "audit_pass": true,
  "issues": []
}

[PHASE 2: IMPLEMENTATION]
// Now implementing strictly from the model...
```

## Remember

The model is not overhead—it IS the specification. Most failures in complex reasoning are **representational, not inferential**: the reasoning was fine, but it operated on an incomplete or unstable understanding of the problem.

By externalizing the model, we make assumptions inspectable, constraints enforceable, and errors diagnosable. The model becomes the contract between intent and implementation.

**Model first. Then reason. Never invert this.**
