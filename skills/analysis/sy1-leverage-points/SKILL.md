---
name: sy1-leverage-points
description: Apply SY1 Leverage Points to identify intervention points where small changes produce disproportionate effects.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy1-leverage-points","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY1 Leverage Points

Apply the SY1 Leverage Points transformation to identify intervention points where small changes produce disproportionate effects.

## What is SY1?

**SY1 (Leverage Points)** Identify intervention points where small changes produce disproportionate effects.

## When to Use SY1

### Ideal Situations

- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions

- "How can we use Leverage Points here?"
- "What changes if we apply SY1 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY1 help us surface?"

## The SY1 Process

### Step 1: Define the focus

```typescript
// Using SY1 (Leverage Points) - Establish the focus
const focus = "Identify intervention points where small changes produce disproportionate effects";
```

### Step 2: Apply the model

```typescript
// Using SY1 (Leverage Points) - Apply the transformation
const output = applyModel("SY1", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using SY1 (Leverage Points) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY1 (Leverage Points) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY1", "Identify intervention points where small changes produce disproportionate effects" );
```

## Integration with Other Transformations

- **SY1 -> P1**: Pair with P1 when sequencing matters.
- **SY1 -> DE3**: Use DE3 to validate or stress-test.
- **SY1 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY1
- [ ] Apply the model using explicit SY1 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY1 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy1-leverage-points"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/sy1-leverage-points
```

### Usage with Commands

```bash
/apply-transformation SY1 "Identify intervention points where small changes produce disproportionate effects"
```

---
*Apply SY1 to create repeatable, explicit mental model reasoning.*
