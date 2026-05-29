---
name: sy11-governance-patterns
description: Apply SY11 Governance Patterns to design decision rights, accountability structures, and coordination mechanisms.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy11-governance-patterns","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# SY11 Governance Patterns

Apply the SY11 Governance Patterns transformation to design decision rights, accountability structures, and coordination mechanisms.

## What is SY11?

**SY11 (Governance Patterns)** Design decision rights, accountability structures, and coordination mechanisms.

## When to Use SY11

### Ideal Situations
- Understand system-wide interactions and feedback loops
- Detect patterns that emerge across components
- Optimize for long-term system behavior, not just local gains

### Trigger Questions
- "How can we use Governance Patterns here?"
- "What changes if we apply SY11 to this analyzing coordination patterns across teams?"
- "Which assumptions does SY11 help us surface?"

## The SY11 Process

### Step 1: Define the focus
```typescript
// Using SY11 (Governance Patterns) - Establish the focus
const focus = "Design decision rights, accountability structures, and coordination mechanisms";
```

### Step 2: Apply the model
```typescript
// Using SY11 (Governance Patterns) - Apply the transformation
const output = applyModel("SY11", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using SY11 (Governance Patterns) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using SY11 (Governance Patterns) - Example in a analyzing coordination patterns across teams
const result = applyModel("SY11", "Design decision rights, accountability structures, and coordination mechanisms" );
```

## Integration with Other Transformations

- **SY11 -> P1**: Pair with P1 when sequencing matters.
- **SY11 -> DE3**: Use DE3 to validate or stress-test.
- **SY11 -> IN2**: Apply IN2 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires SY11
- [ ] Apply the model using explicit SY11 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit SY11 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/SY-systems/sy11-governance-patterns"; }
  ];
}
```

### Manual Installation
```bash
moltbot-registry install hummbl-agent/sy11-governance-patterns
```

### Usage with Commands
```bash
/apply-transformation SY11 "Design decision rights, accountability structures, and coordination mechanisms"
```

---
*Apply SY11 to create repeatable, explicit mental model reasoning.*
