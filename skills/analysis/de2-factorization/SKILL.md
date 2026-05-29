---
name: de2-factorization
description: Apply DE2 Factorization to separate multiplicative components to understand relative contribution of each factor.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/DE-decomposition/de2-factorization","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# DE2 Factorization

Apply the DE2 Factorization transformation to separate multiplicative components to understand relative contribution of each factor.

## What is DE2?

**DE2 (Factorization)** Separate multiplicative components to understand relative contribution of each factor.

## When to Use DE2

### Ideal Situations

- Break a complex problem into manageable parts
- Separate concerns to isolate risk and effort
- Create modular workstreams for parallel progress

### Trigger Questions

- "How can we use Factorization here?"
- "What changes if we apply DE2 to this breaking down an implementation plan?"
- "Which assumptions does DE2 help us surface?"

## The DE2 Process

### Step 1: Define the focus

```typescript
// Using DE2 (Factorization) - Establish the focus
const focus = "Separate multiplicative components to understand relative contribution of each factor";
```

### Step 2: Apply the model

```typescript
// Using DE2 (Factorization) - Apply the transformation
const output = applyModel("DE2", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using DE2 (Factorization) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using DE2 (Factorization) - Example in a breaking down an implementation plan
const result = applyModel("DE2", "Separate multiplicative components to understand relative contribution of each factor" );
```

## Integration with Other Transformations

- **DE2 -> P1**: Pair with P1 when sequencing matters.
- **DE2 -> CO5**: Use CO5 to validate or stress-test.
- **DE2 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires DE2
- [ ] Apply the model using explicit DE2 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit DE2 references in comments and docs
- Keep the output focused and actionable
- Combine with adjacent transformations when needed

## Measurement and Success

- Clearer decisions and fewer unresolved assumptions
- Faster alignment across stakeholders
- Reusable artifacts for future iterations

## Installation and Usage

### Nix Installation

```nix
{
  programs.moltbot.plugins = [
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/DE-decomposition/de2-factorization"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/de2-factorization
```

### Usage with Commands

```bash
/apply-transformation DE2 "Separate multiplicative components to understand relative contribution of each factor"
```

---
*Apply DE2 to create repeatable, explicit mental model reasoning.*
