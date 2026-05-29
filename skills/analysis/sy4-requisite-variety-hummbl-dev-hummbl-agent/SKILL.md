---
name: sy4-requisite-variety
description: Apply SY4 Requisite Variety to match control system's complexity to system being controlled.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy4-requisite-variety","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY4 Requisite Variety

Apply the SY4 Requisite Variety transformation to match control system's complexity to system being controlled.

## What is SY4?

**SY4 (Requisite Variety)** Match control system's complexity to system being controlled.

## When to Use SY4

### Ideal Situations

- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions

- "How can we use Requisite Variety here?"
- "What changes if we apply SY4 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY4 help us surface?"

## The SY4 Process

### Step 1: Define the focus

```typescript
// Using SY4 (Requisite Variety) - Establish the focus
const focus = "Match control system's complexity to system being controlled";
```

### Step 2: Apply the model

```typescript
// Using SY4 (Requisite Variety) - Apply the transformation
const output = applyModel("SY4", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using SY4 (Requisite Variety) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY4 (Requisite Variety) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY4", "Match control system's complexity to system being controlled" );
```

## Integration with Other Transformations

- **SY4 -> P1**: Pair with P1 when sequencing matters.
- **SY4 -> DE3**: Use DE3 to validate or stress-test.
- **SY4 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY4
- [ ] Apply the model using explicit SY4 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY4 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy4-requisite-variety"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/sy4-requisite-variety
```

### Usage with Commands

```bash
/apply-transformation SY4 "Match control system's complexity to system being controlled"
```

---
*Apply SY4 to create repeatable, explicit mental model reasoning.*
