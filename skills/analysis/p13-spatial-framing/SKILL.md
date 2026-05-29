---
name: p13-spatial-framing
description: Apply P13 Spatial Framing to scale perspective from local details to global patterns and back.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p13-spatial-framing","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P13 Spatial Framing

Apply the P13 Spatial Framing transformation to scale perspective from local details to global patterns and back.

## What is P13?

**P13 (Spatial Framing)** Scale perspective from local details to global patterns and back.

## When to Use P13

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Spatial Framing here?"
- "What changes if we apply P13 to this product requirements review?"
- "Which assumptions does P13 help us surface?"

## The P13 Process

### Step 1: Define the focus

```typescript
// Using P13 (Spatial Framing) - Establish the focus
const focus = "Scale perspective from local details to global patterns and back";
```

### Step 2: Apply the model

```typescript
// Using P13 (Spatial Framing) - Apply the transformation
const output = applyModel("P13", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P13 (Spatial Framing) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P13 (Spatial Framing) - Example in a product requirements review
const result = applyModel("P13", "Scale perspective from local details to global patterns and back" );
```

## Integration with Other Transformations

- **P13 -> DE3**: Pair with DE3 when sequencing matters.
- **P13 -> IN2**: Use IN2 to validate or stress-test.
- **P13 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P13
- [ ] Apply the model using explicit P13 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P13 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p13-spatial-framing"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p13-spatial-framing
```

### Usage with Commands

```bash
/apply-transformation P13 "Scale perspective from local details to global patterns and back"
```

---
*Apply P13 to create repeatable, explicit mental model reasoning.*
