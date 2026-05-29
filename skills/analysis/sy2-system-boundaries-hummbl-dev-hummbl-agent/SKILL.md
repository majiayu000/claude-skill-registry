---
name: sy2-system-boundaries
description: Apply SY2 System Boundaries to define what is inside versus outside system scope for analysis or design.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy2-system-boundaries","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY2 System Boundaries

Apply the SY2 System Boundaries transformation to define what is inside versus outside system scope for analysis or design.

## What is SY2?

**SY2 (System Boundaries)** Define what is inside versus outside system scope for analysis or design.

## When to Use SY2

### Ideal Situations
- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions
- "How can we use System Boundaries here?"
- "What changes if we apply SY2 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY2 help us surface?"

## The SY2 Process

### Step 1: Define the focus
```typescript
// Using SY2 (System Boundaries) - Establish the focus
const focus = "Define what is inside versus outside system scope for analysis or design";
```

### Step 2: Apply the model
```typescript
// Using SY2 (System Boundaries) - Apply the transformation
const output = applyModel("SY2", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using SY2 (System Boundaries) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY2 (System Boundaries) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY2", "Define what is inside versus outside system scope for analysis or design" );
```

## Integration with Other Transformations

- **SY2 -> P1**: Pair with P1 when sequencing matters.
- **SY2 -> DE3**: Use DE3 to validate or stress-test.
- **SY2 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY2
- [ ] Apply the model using explicit SY2 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY2 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy2-system-boundaries"; }
  ];
}
```

### Manual Installation
```bash
moltbot-registry install hummbl-agent/sy2-system-boundaries
```

### Usage with Commands
```bash
/apply-transformation SY2 "Define what is inside versus outside system scope for analysis or design"
```

---
*Apply SY2 to create repeatable, explicit mental model reasoning.*
