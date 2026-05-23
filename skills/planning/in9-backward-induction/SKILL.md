---
name: in9-backward-induction
description: Apply IN9 Backward Induction to begin with desired end state and work backward to determine necessary steps.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in9-backward-induction","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN9 Backward Induction

Apply the IN9 Backward Induction transformation to begin with desired end state and work backward to determine necessary steps.

## What is IN9?

**IN9 (Backward Induction)** Begin with desired end state and work backward to determine necessary steps.

## When to Use IN9

### Ideal Situations
- Stress-test a plan by reversing assumptions
- Identify risks by imagining failure states
- Simplify outcomes by removing unnecessary elements

### Trigger Questions
- "How can we use Backward Induction here?"
- "What changes if we apply IN9 to this risk assessment for a launch?"
- "Which assumptions does IN9 help us surface?"

## The IN9 Process

### Step 1: Define the focus
```typescript
// Using IN9 (Backward Induction) - Establish the focus
const focus = "Begin with desired end state and work backward to determine necessary steps";
```

### Step 2: Apply the model
```typescript
// Using IN9 (Backward Induction) - Apply the transformation
const output = applyModel("IN9", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using IN9 (Backward Induction) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using IN9 (Backward Induction) - Example in a risk assessment for a launch
const result = applyModel("IN9", "Begin with desired end state and work backward to determine necessary steps" );
```

## Integration with Other Transformations

- **IN9 -> P1**: Pair with P1 when sequencing matters.
- **IN9 -> DE3**: Use DE3 to validate or stress-test.
- **IN9 -> SY8**: Apply SY8 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires IN9
- [ ] Apply the model using explicit IN9 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit IN9 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in9-backward-induction"; }
  ];
}
```

### Manual Installation
```bash
clawdhub install hummbl-agent/in9-backward-induction
```

### Usage with Commands
```bash
/apply-transformation IN9 "Begin with desired end state and work backward to determine necessary steps"
```

---
*Apply IN9 to create repeatable, explicit mental model reasoning.*
