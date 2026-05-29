---
name: p4-lens-shifting
description: Apply P4 Lens Shifting to deliberately adopt different interpretive frameworks to reveal hidden aspects.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p4-lens-shifting","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P4 Lens Shifting

Apply the P4 Lens Shifting transformation to deliberately adopt different interpretive frameworks to reveal hidden aspects.

## What is P4?

**P4 (Lens Shifting)** Deliberately adopt different interpretive frameworks to reveal hidden aspects.

## When to Use P4

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Lens Shifting here?"
- "What changes if we apply P4 to this product requirements review?"
- "Which assumptions does P4 help us surface?"

## The P4 Process

### Step 1: Define the focus

```typescript
// Using P4 (Lens Shifting) - Establish the focus
const focus = "Deliberately adopt different interpretive frameworks to reveal hidden aspects";
```

### Step 2: Apply the model

```typescript
// Using P4 (Lens Shifting) - Apply the transformation
const output = applyModel("P4", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P4 (Lens Shifting) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P4 (Lens Shifting) - Example in a product requirements review
const result = applyModel("P4", "Deliberately adopt different interpretive frameworks to reveal hidden aspects" );
```

## Integration with Other Transformations

- **P4 -> DE3**: Pair with DE3 when sequencing matters.
- **P4 -> IN2**: Use IN2 to validate or stress-test.
- **P4 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P4
- [ ] Apply the model using explicit P4 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P4 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p4-lens-shifting"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p4-lens-shifting
```

### Usage with Commands

```bash
/apply-transformation P4 "Deliberately adopt different interpretive frameworks to reveal hidden aspects"
```

---
*Apply P4 to create repeatable, explicit mental model reasoning.*
