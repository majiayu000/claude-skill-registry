---
name: compress-prompt
description: 'Compresses prompts/skills into minimal goal-focused instructions. Trusts the model, drops what it already knows, maximizes action space. Use when asked to compress, condense, or minimize a prompt.'
---

# Compress Prompt

## Goal

Transform a prompt into the **minimal instruction** needed for the model to succeed. Not "preserve everything densely"—instead, "what's the least I need to say?"

Output: Display compressed result + stats. Optionally write to file with `--output <path>`.

## Input

`$ARGUMENTS` = prompt (file path or inline text) [--output path]

If file path: read content. If inline: use directly. If ambiguous: try as file first.

## Principles

1. **Trust capability, enforce discipline** - Models know HOW to do tasks. But they cut corners, forget context, skip verification, declare victory early. Drop capability instructions, keep discipline guardrails.

2. **Goal over process** - State WHAT to achieve, not HOW. Let the model choose its approach.

3. **Training filter** - "Would a competent person need to be told this?" If no → drop it. Models are trained on millions of examples.

4. **Maximize action space** - Fewer constraints = more freedom = better results. Each constraint should earn its place.

5. **Inline-typable brevity** - Short enough you could type it verbally to a capable colleague.

6. **Avoid arbitrary values** - "Max 4 rounds" or "2-3 examples" become rigid rules. State the principle, not the number. Constrain productively while giving flexibility.

## What to Keep vs Drop

| KEEP | DROP |
|------|------|
| Core goal/purpose | Process/phases (capability) |
| Acceptance criteria (success conditions) | Examples the model knows |
| Novel constraints (counter-intuitive rules) | Obvious constraints (model defaults) |
| Execution discipline (write before proceeding, verify before finalizing) | Edge case handling (model trained on these) |
| Output format if non-standard | Explanations and rationale |

**Execution discipline examples** (KEEP these):
- "Write findings to file BEFORE proceeding" — prevents context rot
- "Don't finalize until X confirmed" — prevents premature completion
- "Read full log before synthesis" — restores lost context

**Training-redundant examples** (DROP these):
- "Be thorough", "Handle errors gracefully", "Ask clarifying questions"
- "Consider edge cases", "Use professional tone"

## Constraints

**Create todo list** - Track: input validation, compression, verification iterations, output.

**Verify with agent** - Launch `prompt-compression-verifier` to check goal clarity, novel constraints preserved, no over-specification. Iterate until verification passes.

**Single paragraph output** - The compressed prompt must be one dense paragraph, not reformatted sections or bullets.

**Non-destructive** - Original file untouched. Display output + optional file save.

## Output Format

```
Compressed: {source}

Original: {tokens} tokens
Compressed: {tokens} tokens ({percentage}% reduction)

---
{compressed paragraph}
---

Verification: PASSED/INCOMPLETE ({iterations} iteration(s))
```

## Example

**Before** (1,247 tokens): Full code reviewer prompt with phases, edge cases, examples...

**After** (67 tokens):
```
Review code for bugs, security issues, performance problems; success = all critical issues identified with actionable fixes. Output JSON {file, line, issue, severity, fix}. Never approve code with critical issues.
```

**Kept**: Goal, acceptance criteria, output format, novel constraint (never approve with critical issues).
**Dropped**: Process phases, edge case handling, examples, obvious constraints.
