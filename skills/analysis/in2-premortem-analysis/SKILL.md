---
name: in2-premortem-analysis
description: Apply IN2 Premortem Analysis to assume failure has occurred and work backward to identify causes.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in2-premortem-analysis","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN2 Premortem Analysis

Apply the IN2 Premortem Analysis transformation to assume failure has occurred and work backward to identify causes.

## What is IN2?

**IN2 (Premortem Analysis)** Assume failure has occurred and work backward to identify causes.

## When to Use IN2

### Ideal Situations
- Stress-test a plan by reversing assumptions
- Identify risks by imagining failure states
- Simplify outcomes by removing unnecessary elements

### Trigger Questions
- "How can we use Premortem Analysis here?"
- "What changes if we apply IN2 to this risk assessment for a launch?"
- "Which assumptions does IN2 help us surface?"

## The IN2 Process

### Step 1: Define the focus
```typescript
// Using IN2 (Premortem Analysis) - Establish the focus
const focus = "Assume failure has occurred and work backward to identify causes";
```

### Step 2: Apply the model
```typescript
// Using IN2 (Premortem Analysis) - Apply the transformation
const output = applyModel("IN2", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using IN2 (Premortem Analysis) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using IN2 (Premortem Analysis) - Example in a risk assessment for a launch
const result = applyModel("IN2", "Assume failure has occurred and work backward to identify causes" );
```

## Integration with Other Transformations

- **IN2 -> P1**: Pair with P1 when sequencing matters.
- **IN2 -> DE3**: Use DE3 to validate or stress-test.
- **IN2 -> SY8**: Apply SY8 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires IN2
- [ ] Apply the model using explicit IN2 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit IN2 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in2-premortem-analysis"; }
  ];
}
```

### Manual Installation
```bash
moltbot-registry install hummbl-agent/in2-premortem-analysis
```

### Usage with Commands
```bash
/apply-transformation IN2 "Assume failure has occurred and work backward to identify causes"
```

---
*Apply IN2 to create repeatable, explicit mental model reasoning.*
