---
name: in3-problem-reversal
description: Apply IN3 Problem Reversal to solve the inverse of the stated problem to reveal insights.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in3-problem-reversal","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN3 Problem Reversal

Apply the IN3 Problem Reversal transformation to solve the inverse of the stated problem to reveal insights.

## What is IN3?

**IN3 (Problem Reversal)** Solve the inverse of the stated problem to reveal insights.

## When to Use IN3

### Ideal Situations

- Stress-test a plan by reversing assumptions
- Identify risks by imagining failure states
- Simplify outcomes by removing unnecessary elements

### Trigger Questions

- "How can we use Problem Reversal here?"
- "What changes if we apply IN3 to this risk assessment for a launch?"
- "Which assumptions does IN3 help us surface?"

## The IN3 Process

### Step 1: Define the focus

```typescript
// Using IN3 (Problem Reversal) - Establish the focus
const focus = "Solve the inverse of the stated problem to reveal insights";
```

### Step 2: Apply the model

```typescript
// Using IN3 (Problem Reversal) - Apply the transformation
const output = applyModel("IN3", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using IN3 (Problem Reversal) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using IN3 (Problem Reversal) - Example in a risk assessment for a launch
const result = applyModel("IN3", "Solve the inverse of the stated problem to reveal insights" );
```

## Integration with Other Transformations

- **IN3 -> P1**: Pair with P1 when sequencing matters.
- **IN3 -> DE3**: Use DE3 to validate or stress-test.
- **IN3 -> SY8**: Apply SY8 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires IN3
- [ ] Apply the model using explicit IN3 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit IN3 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in3-problem-reversal"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/in3-problem-reversal
```

### Usage with Commands

```bash
/apply-transformation IN3 "Solve the inverse of the stated problem to reveal insights"
```

---
*Apply IN3 to create repeatable, explicit mental model reasoning.*
