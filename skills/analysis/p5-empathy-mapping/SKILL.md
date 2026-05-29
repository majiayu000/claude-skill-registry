---
name: p5-empathy-mapping
description: Apply P5 Empathy Mapping to systematically capture what stakeholders see, think, feel, and do in their context.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p5-empathy-mapping","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P5 Empathy Mapping

Apply the P5 Empathy Mapping transformation to systematically capture what stakeholders see, think, feel, and do in their context.

## What is P5?

**P5 (Empathy Mapping)** Systematically capture what stakeholders see, think, feel, and do in their context.

## When to Use P5

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Empathy Mapping here?"
- "What changes if we apply P5 to this product requirements review?"
- "Which assumptions does P5 help us surface?"

## The P5 Process

### Step 1: Define the focus

```typescript
// Using P5 (Empathy Mapping) - Establish the focus
const focus = "Systematically capture what stakeholders see, think, feel, and do in their context";
```

### Step 2: Apply the model

```typescript
// Using P5 (Empathy Mapping) - Apply the transformation
const output = applyModel("P5", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P5 (Empathy Mapping) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P5 (Empathy Mapping) - Example in a product requirements review
const result = applyModel("P5", "Systematically capture what stakeholders see, think, feel, and do in their context" );
```

## Integration with Other Transformations

- **P5 -> DE3**: Pair with DE3 when sequencing matters.
- **P5 -> IN2**: Use IN2 to validate or stress-test.
- **P5 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P5
- [ ] Apply the model using explicit P5 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P5 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p5-empathy-mapping"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p5-empathy-mapping
```

### Usage with Commands

```bash
/apply-transformation P5 "Systematically capture what stakeholders see, think, feel, and do in their context"
```

---
*Apply P5 to create repeatable, explicit mental model reasoning.*
