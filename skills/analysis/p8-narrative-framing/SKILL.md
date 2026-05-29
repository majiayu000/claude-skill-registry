---
name: p8-narrative-framing
description: Apply P8 Narrative Framing to structure information as causal stories with conflict, choice, and consequence.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p8-narrative-framing","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P8 Narrative Framing

Apply the P8 Narrative Framing transformation to structure information as causal stories with conflict, choice, and consequence.

## What is P8?

**P8 (Narrative Framing)** Structure information as causal stories with conflict, choice, and consequence.

## When to Use P8

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Narrative Framing here?"
- "What changes if we apply P8 to this product requirements review?"
- "Which assumptions does P8 help us surface?"

## The P8 Process

### Step 1: Define the focus

```typescript
// Using P8 (Narrative Framing) - Establish the focus
const focus = "Structure information as causal stories with conflict, choice, and consequence";
```

### Step 2: Apply the model

```typescript
// Using P8 (Narrative Framing) - Apply the transformation
const output = applyModel("P8", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P8 (Narrative Framing) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P8 (Narrative Framing) - Example in a product requirements review
const result = applyModel("P8", "Structure information as causal stories with conflict, choice, and consequence" );
```

## Integration with Other Transformations

- **P8 -> DE3**: Pair with DE3 when sequencing matters.
- **P8 -> IN2**: Use IN2 to validate or stress-test.
- **P8 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P8
- [ ] Apply the model using explicit P8 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P8 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p8-narrative-framing"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p8-narrative-framing
```

### Usage with Commands

```bash
/apply-transformation P8 "Structure information as causal stories with conflict, choice, and consequence"
```

---
*Apply P8 to create repeatable, explicit mental model reasoning.*
