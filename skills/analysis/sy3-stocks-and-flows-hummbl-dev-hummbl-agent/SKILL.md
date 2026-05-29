---
name: sy3-stocks-and-flows
description: Apply SY3 Stocks & Flows to distinguish accumulations from rates of change affecting them.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy3-stocks-and-flows","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY3 Stocks & Flows

Apply the SY3 Stocks & Flows transformation to distinguish accumulations from rates of change affecting them.

## What is SY3?

**SY3 (Stocks & Flows)** Distinguish accumulations from rates of change affecting them.

## When to Use SY3

### Ideal Situations
- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions
- "How can we use Stocks & Flows here?"
- "What changes if we apply SY3 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY3 help us surface?"

## The SY3 Process

### Step 1: Define the focus
```typescript
// Using SY3 (Stocks & Flows) - Establish the focus
const focus = "Distinguish accumulations from rates of change affecting them";
```

### Step 2: Apply the model
```typescript
// Using SY3 (Stocks & Flows) - Apply the transformation
const output = applyModel("SY3", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using SY3 (Stocks & Flows) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY3 (Stocks & Flows) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY3", "Distinguish accumulations from rates of change affecting them" );
```

## Integration with Other Transformations

- **SY3 -> P1**: Pair with P1 when sequencing matters.
- **SY3 -> DE3**: Use DE3 to validate or stress-test.
- **SY3 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY3
- [ ] Apply the model using explicit SY3 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY3 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy3-stocks-and-flows"; }
  ];
}
```

### Manual Installation
```bash
moltbot-registry install hummbl-agent/sy3-stocks-and-flows
```

### Usage with Commands
```bash
/apply-transformation SY3 "Distinguish accumulations from rates of change affecting them"
```

---
*Apply SY3 to create repeatable, explicit mental model reasoning.*
