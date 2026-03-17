---
name: guardrails-contracts
description: Follow these patterns when designing guardrails validation contracts in OptAIC. Use for signal bounds, dataset schemas, portfolio constraints, PIT validation, and other domain-specific validation rules. Covers the "Law vs Police" architecture where Definitions contain contracts and the Engine enforces them.
---

# Guardrails Contract Patterns

Guide for implementing validation contracts that enforce data quality, risk limits, and compliance.

## When to Use

Apply when:
- Adding validation rules for domain resources
- Implementing signal bounds, dataset schema checks
- Creating portfolio constraints (weights, leverage)
- Enforcing PIT correctness on datasets
- Building custom validators
- Embedding contracts in Definition resources

## Law vs Police Architecture

```
┌────────────────────────────────────────────────────────────┐
│           DEFINITION RESOURCE (The Law)                     │
│  ├── interface_spec        # Abstract interface             │
│  ├── input_schema          # Expected inputs                │
│  ├── output_schema         # Expected outputs               │
│  ├── compatibility_rules   # Connection rules               │
│  └── guardrail_contracts   # Validation rules               │
│      ├── signal.bounds: {min: -1, max: 1}                  │
│      ├── pit.policy: {knowledge_date_required: true}       │
│      └── dataset.schema: {columns: [...]}                  │
└────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│           GUARDRAILS ENGINE (The Police)                    │
│  Reads contracts FROM Definitions, enforces at gates:       │
│  ├── Gate 1: Instance Creation (validate config)           │
│  ├── Gate 2: Run Execution (validate inputs)               │
│  ├── Gate 3: Data Write (validate outputs in real-time)    │
│  └── Gate 4: Promotion/Merge (all must pass)               │
└────────────────────────────────────────────────────────────┘
```

**Key Insight**: Contracts live IN Definition resources. The Guardrails Engine reads and enforces them—no manual attachment needed.

## Core Concepts

**ContractRef**: Identifies contract kind + JSON schema
**ContractInstance**: Bound contract with config + enforcement hint
**ContractBundle**: Collection of contracts for a resource
**ValidationReport**: Results with issues, enforcement decision

## Implementation Workflow

### 1. Define Contract Kind

Use namespaced naming: `<domain>.<aspect>`

```
signal.bounds       # Value range [-1, 1]
signal.schema       # Arrow schema conformance
dataset.pit         # Point-in-time correctness
dataset.freshness   # Data staleness SLA
portfolio.weights   # Sum-to-one, min/max weight
portfolio.leverage  # Gross/net exposure limits
```

### 2. Create JSON Schema

Location: `optaic/guardrails/contracts/<domain>.py`

See [references/contract-schemas.md](references/contract-schemas.md).

### 3. Implement Validator

Location: `optaic/guardrails/validators/<domain>.py`

Validators must be **pure** and **deterministic**. See [references/validators.md](references/validators.md).

### 4. Register Contract

```python
ContractRegistry.register(
    kind="signal.bounds",
    schema=SIGNAL_BOUNDS_SCHEMA,
    validator=SignalBoundsValidator,
    version="1.0"
)
```

### 5. Write Tests

Test cases:
- Valid config + valid data → Pass
- Invalid config → Schema validation fail
- Valid config + invalid data → Business validation fail

## Enforcement Policy

```python
# official subspace → BLOCK on errors
# staging subspace → WARN on errors (unless elevated)

if subspace == "official":
    return EnforcementLevel.BLOCK
return EnforcementLevel.WARN
```

## Lifecycle Gates

Guardrails validate at:
- `resource.create` / `resource.update`
- `promotion.request` / `promotion.merge`
- `run.submit` / `run.start`

## Reference Files

- [Contract Schemas](references/contract-schemas.md) - JSON schema patterns
- [Validators](references/validators.md) - Validator implementation
- [Quant Contracts](references/quant-contracts.md) - Domain-specific examples
