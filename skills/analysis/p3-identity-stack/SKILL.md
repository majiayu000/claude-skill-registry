---
name: p3-identity-stack
description: Apply P3 Identity Stack to recognize that individuals operate from multiple nested identities simultaneously.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p3-identity-stack","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# P3 Identity Stack

Apply the P3 Identity Stack transformation to recognize that individuals operate from multiple nested identities simultaneously.

## What is P3?

**P3 (Identity Stack)** Recognize that individuals operate from multiple nested identities simultaneously.

## When to Use P3

### Ideal Situations

- Reframe a problem to uncover hidden assumptions or perspectives
- Align stakeholders around a shared understanding
- Clarify scope before choosing a solution path

### Trigger Questions

- "How can we use Identity Stack here?"
- "What changes if we apply P3 to this product requirements review?"
- "Which assumptions does P3 help us surface?"

## The P3 Process

### Step 1: Define the focus

```typescript
// Using P3 (Identity Stack) - Establish the focus
const focus = "Recognize that individuals operate from multiple nested identities simultaneously";
```

### Step 2: Apply the model

```typescript
// Using P3 (Identity Stack) - Apply the transformation
const output = applyModel("P3", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using P3 (Identity Stack) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using P3 (Identity Stack) - Example in a product requirements review
const result = applyModel("P3", "Recognize that individuals operate from multiple nested identities simultaneously" );
```

## Integration with Other Transformations

- **P3 -> DE3**: Pair with DE3 when sequencing matters.
- **P3 -> IN2**: Use IN2 to validate or stress-test.
- **P3 -> CO5**: Apply CO5 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires P3
- [ ] Apply the model using explicit P3 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit P3 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/P-perspective/p3-identity-stack"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/p3-identity-stack
```

### Usage with Commands

```bash
/apply-transformation P3 "Recognize that individuals operate from multiple nested identities simultaneously"
```

---
*Apply P3 to create repeatable, explicit mental model reasoning.*
