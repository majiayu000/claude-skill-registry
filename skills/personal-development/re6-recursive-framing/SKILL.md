---
name: re6-recursive-framing
description: Apply RE6 Recursive Framing to apply mental models to the process of selecting mental models.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re6-recursive-framing","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# RE6 Recursive Framing

Apply the RE6 Recursive Framing transformation to apply mental models to the process of selecting mental models.

## What is RE6?

**RE6 (Recursive Framing)** Apply mental models to the process of selecting mental models.

## When to Use RE6

### Ideal Situations

- Iterate toward a better solution using feedback loops
- Refine a process through repeated cycles
- Scale a pattern through repetition and standardization

### Trigger Questions

- "How can we use Recursive Framing here?"
- "What changes if we apply RE6 to this iterating a workflow over several cycles?"
- "Which assumptions does RE6 help us surface?"

## The RE6 Process

### Step 1: Define the focus

```typescript
// Using RE6 (Recursive Framing) - Establish the focus
const focus = "Apply mental models to the process of selecting mental models";
```

### Step 2: Apply the model

```typescript
// Using RE6 (Recursive Framing) - Apply the transformation
const output = applyModel("RE6", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using RE6 (Recursive Framing) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using RE6 (Recursive Framing) - Example in a iterating a workflow over several cycles
const result = applyModel("RE6", "Apply mental models to the process of selecting mental models" );
```

## Integration with Other Transformations

- **RE6 -> CO5**: Pair with CO5 when sequencing matters.
- **RE6 -> SY8**: Use SY8 to validate or stress-test.
- **RE6 -> IN3**: Apply IN3 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires RE6
- [ ] Apply the model using explicit RE6 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit RE6 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re6-recursive-framing"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/re6-recursive-framing
```

### Usage with Commands

```bash
/apply-transformation RE6 "Apply mental models to the process of selecting mental models"
```

---
*Apply RE6 to create repeatable, explicit mental model reasoning.*
