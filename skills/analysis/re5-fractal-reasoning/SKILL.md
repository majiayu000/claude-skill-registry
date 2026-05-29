---
name: re5-fractal-reasoning
description: Apply RE5 Fractal Reasoning to recognize self-similar patterns repeating across different scales.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re5-fractal-reasoning","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# RE5 Fractal Reasoning

Apply the RE5 Fractal Reasoning transformation to recognize self-similar patterns repeating across different scales.

## What is RE5?

**RE5 (Fractal Reasoning)** Recognize self-similar patterns repeating across different scales.

## When to Use RE5

### Ideal Situations

- Iterate toward a better solution using feedback loops
- Refine a process through repeated cycles
- Scale a pattern through repetition and standardization

### Trigger Questions

- "How can we use Fractal Reasoning here?"
- "What changes if we apply RE5 to this iterating a workflow over several cycles?"
- "Which assumptions does RE5 help us surface?"

## The RE5 Process

### Step 1: Define the focus

```typescript
// Using RE5 (Fractal Reasoning) - Establish the focus
const focus = "Recognize self-similar patterns repeating across different scales";
```

### Step 2: Apply the model

```typescript
// Using RE5 (Fractal Reasoning) - Apply the transformation
const output = applyModel("RE5", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using RE5 (Fractal Reasoning) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using RE5 (Fractal Reasoning) - Example in a iterating a workflow over several cycles
const result = applyModel("RE5", "Recognize self-similar patterns repeating across different scales" );
```

## Integration with Other Transformations

- **RE5 -> CO5**: Pair with CO5 when sequencing matters.
- **RE5 -> SY8**: Use SY8 to validate or stress-test.
- **RE5 -> IN3**: Apply IN3 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires RE5
- [ ] Apply the model using explicit RE5 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit RE5 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re5-fractal-reasoning"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/re5-fractal-reasoning
```

### Usage with Commands

```bash
/apply-transformation RE5 "Recognize self-similar patterns repeating across different scales"
```

---
*Apply RE5 to create repeatable, explicit mental model reasoning.*
