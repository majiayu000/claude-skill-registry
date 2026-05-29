---
name: sy5-systems-archetypes
description: Apply SY5 Systems Archetypes to recognize recurring dynamic patterns across different domains.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy5-systems-archetypes","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY5 Systems Archetypes

Apply the SY5 Systems Archetypes transformation to recognize recurring dynamic patterns across different domains.

## What is SY5?

**SY5 (Systems Archetypes)** Recognize recurring dynamic patterns across different domains.

## When to Use SY5

### Ideal Situations

- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions

- "How can we use Systems Archetypes here?"
- "What changes if we apply SY5 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY5 help us surface?"

## The SY5 Process

### Step 1: Define the focus

```typescript
// Using SY5 (Systems Archetypes) - Establish the focus
const focus = "Recognize recurring dynamic patterns across different domains";
```

### Step 2: Apply the model

```typescript
// Using SY5 (Systems Archetypes) - Apply the transformation
const output = applyModel("SY5", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using SY5 (Systems Archetypes) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY5 (Systems Archetypes) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY5", "Recognize recurring dynamic patterns across different domains" );
```

## Integration with Other Transformations

- **SY5 -> P1**: Pair with P1 when sequencing matters.
- **SY5 -> DE3**: Use DE3 to validate or stress-test.
- **SY5 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY5
- [ ] Apply the model using explicit SY5 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY5 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy5-systems-archetypes"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/sy5-systems-archetypes
```

### Usage with Commands

```bash
/apply-transformation SY5 "Recognize recurring dynamic patterns across different domains"
```

---
*Apply SY5 to create repeatable, explicit mental model reasoning.*
