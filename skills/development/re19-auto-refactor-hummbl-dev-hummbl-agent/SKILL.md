---
name: re19-auto-refactor
description: Apply RE19 Auto-Refactor to systematically improve system structure without changing external behavior.
version: 1.0.0
metadata: {"moltbot":{"nix":{"plugin":"github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re19-auto-refactor","systems":["aarch64-darwin","x86_64-linux"]}}}
---

# RE19 Auto-Refactor

Apply the RE19 Auto-Refactor transformation to systematically improve system structure without changing external behavior.

## What is RE19?

**RE19 (Auto-Refactor)** Systematically improve system structure without changing external behavior.

## When to Use RE19

### Ideal Situations

- Iterate toward a better solution using feedback loops
- Refine a process through repeated cycles
- Scale a pattern through repetition and standardization

### Trigger Questions

- "How can we use Auto-Refactor here?"
- "What changes if we apply RE19 to this iterating a workflow over several cycles?"
- "Which assumptions does RE19 help us surface?"

## The RE19 Process

### Step 1: Define the focus

```typescript
// Using RE19 (Auto-Refactor) - Establish the focus
const focus = "Systematically improve system structure without changing external behavior";
```

### Step 2: Apply the model

```typescript
// Using RE19 (Auto-Refactor) - Apply the transformation
const output = applyModel("RE19", focus);
```

### Step 3: Synthesize outcomes

```typescript
// Using RE19 (Auto-Refactor) - Capture insights and decisions
const insights = summarize(output);
```

## Practical Example

```typescript
// Using RE19 (Auto-Refactor) - Example in a iterating a workflow over several cycles
const result = applyModel("RE19", "Systematically improve system structure without changing external behavior" );
```

## Integration with Other Transformations

- **RE19 -> CO5**: Pair with CO5 when sequencing matters.
- **RE19 -> SY8**: Use SY8 to validate or stress-test.
- **RE19 -> IN3**: Apply IN3 to compose the output.

## Implementation Checklist

- [ ] Identify the context that requires RE19
- [ ] Apply the model using explicit RE19 references
- [ ] Document assumptions and outputs
- [ ] Confirm alignment with stakeholders or owners

## Common Pitfalls

- Treating the model as a checklist instead of a lens
- Skipping documentation of assumptions or rationale
- Over-applying the model without validating impact

## Best Practices

- Use explicit RE19 references in comments and docs
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
    { source = "github:hummbl-dev/hummbl-agent?dir=skills/RE-recursion/re19-auto-refactor"; }
  ];
}
```

### Manual Installation

```bash
moltbot-registry install hummbl-agent/re19-auto-refactor
```

### Usage with Commands

```bash
/apply-transformation RE19 "Systematically improve system structure without changing external behavior"
```

---
*Apply RE19 to create repeatable, explicit mental model reasoning.*
