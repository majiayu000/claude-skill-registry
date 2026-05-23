---
name: in4-contra-logic
description: Apply IN4 Contra-Logic to argue the opposite position to stress-test assumptions and expose weak reasoning.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in4-contra-logic","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# IN4 Contra-Logic

Apply the IN4 Contra-Logic transformation to argue the opposite position to stress-test assumptions and expose weak reasoning.

## What is IN4?

**IN4 (Contra-Logic)** Argue the opposite position to stress-test assumptions and expose weak reasoning.

## When to Use IN4

### Ideal Situations

- Stress-test a plan by reversing assumptions
- Identify risks by imagining failure states
- Simplify outcomes by removing unnecessary elements

### Trigger Questions

- "How can we use Contra-Logic here?"
- "What changes if we apply IN4 to this risk assessment for a launch?"
- "Which assumptions does IN4 help us surface?"

## The IN4 Process

### Step 1: Define the focus

```typescript
// Using IN4 (Contra-Logic) - Establish the focus
const focus = "Argue the opposite position to stress-test assumptions and expose weak reasoning";
```

### Step 2: Apply the model

```typescript
// Using IN4 (Contra-Logic) - Apply the transformation
const output = applyModel("IN4", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using IN4 (Contra-Logic) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using IN4 (Contra-Logic) - Example in a risk assessment for a launch
const result = applyModel("IN4", "Argue the opposite position to stress-test assumptions and expose weak reasoning" );
```

## Integration with Other Transformations

- **IN4 -> P1**: Pair with P1 when sequencing matters.
- **IN4 -> DE3**: Use DE3 to validate or stress-test.
- **IN4 -> SY8**: Apply SY8 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires IN4
- [ ] Apply the model using explicit IN4 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit IN4 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/IN-inversion/in4-contra-logic"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/in4-contra-logic
```

### Usage with Commands

```bash
/apply-transformation IN4 "Argue the opposite position to stress-test assumptions and expose weak reasoning"
```

---
*Apply IN4 to create repeatable, explicit mental model reasoning.*
