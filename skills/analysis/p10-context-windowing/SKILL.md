---
name: p10-context-windowing
description: Apply P10 Context Windowing to define explicit boundaries in time, space, and scope for analysis or action.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p10-context-windowing","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P10 Context Windowing

Apply the P10 Context Windowing transformation to define explicit boundaries in time, space, and scope for analysis or action.

## What is P10?

**P10 (Context Windowing)** Define explicit boundaries in time, space, and scope for analysis or action.

## When to Use P10

### Ideal Situations
- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions
- "How can we use Context Windowing here?"
- "What changes if we apply P10 to this product requirements review?"
- "Which assumptions does P10 help us surface?"

## The P10 Process

### Step 1: Define the focus
```typescript
// Using P10 (Context Windowing) - Establish the focus
const focus = "Define explicit boundaries in time, space, and scope for analysis or action";
```

### Step 2: Apply the model
```typescript
// Using P10 (Context Windowing) - Apply the transformation
const output = applyModel("P10", focus);
```

### Step 3: Synthesize outcomes
```typescript
// Using P10 (Context Windowing) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P10 (Context Windowing) - Example in a product requirements review
const result = applyModel("P10", "Define explicit boundaries in time, space, and scope for analysis or action" );
```

## Integration with Other Transformations

- **P10 -> DE3**: Pair with DE3 when sequencing matters.
- **P10 -> IN2**: Use IN2 to validate or stress-test.
- **P10 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P10
- [ ] Apply the model using explicit P10 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P10 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p10-context-windowing"; }
  ];
}
```

### Manual Installation
```bash
moltbot-registry install hummbl-agent/p10-context-windowing
```

### Usage with Commands
```bash
/apply-transformation P10 "Define explicit boundaries in time, space, and scope for analysis or action"
```

---
*Apply P10 to create repeatable, explicit mental model reasoning.*
