---
name: p12-temporal-framing
description: Apply P12 Temporal Framing to organize understanding across past causes, present states, and future implications.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p12-temporal-framing","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P12 Temporal Framing

Apply the P12 Temporal Framing transformation to organize understanding across past causes, present states, and future implications.

## What is P12?

**P12 (Temporal Framing)** Organize understanding across past causes, present states, and future implications.

## When to Use P12

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Temporal Framing here?"
- "What changes if we apply P12 to this product requirements review?"
- "Which assumptions does P12 help us surface?"

## The P12 Process

### Step 1: Define the focus

```typescript
// Using P12 (Temporal Framing) - Establish the focus
const focus = "Organize understanding across past causes, present states, and future implications";
```

### Step 2: Apply the model

```typescript
// Using P12 (Temporal Framing) - Apply the transformation
const output = applyModel("P12", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P12 (Temporal Framing) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P12 (Temporal Framing) - Example in a product requirements review
const result = applyModel("P12", "Organize understanding across past causes, present states, and future implications" );
```

## Integration with Other Transformations

- **P12 -> DE3**: Pair with DE3 when sequencing matters.
- **P12 -> IN2**: Use IN2 to validate or stress-test.
- **P12 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P12
- [ ] Apply the model using explicit P12 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P12 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p12-temporal-framing"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p12-temporal-framing
```

### Usage with Commands

```bash
/apply-transformation P12 "Organize understanding across past causes, present states, and future implications"
```

---
*Apply P12 to create repeatable, explicit mental model reasoning.*
