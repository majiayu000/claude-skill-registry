# Copywriting Skill

When writing or editing content for this guide, follow these guidelines.

## Terminology

Refer to the project as a "guide" rather than a "book" - it's more humble.

## Voice

From CLAUDE.md:
- **ELI5**: Simple, clear language
- **Short and direct**: No fluff
- **Concrete over abstract**: Show the situation, name the pattern, explain the move

## Section Headers

Use these standard headers in failure modes and patterns:

| Use | Avoid |
|-----|-------|
| Theory | Why This Happens |
| Symptoms | Signs / Indicators |
| Mitigation | How to Fix / Solution |

## Anthropomorphization

AVOID ANTHROPOMORPHIZING THE MODEL. Use mechanistic language instead of implying human-like cognition, desire, or agency.

| Avoid | Use Instead |
|-------|-------------|
| "decides" | "selects", "outputs" |
| "wants" | "is configured to", "attempts to" |
| "learns" | "is trained on", "patterns from training" |
| "reasons" | "processes", "evaluates" |
| "needs" | "requires" |
| "develops intuitions" | "exhibits patterns from training" |

## Succinctness

- Cut filler words: "basically", "essentially", "in order to", "actually"
- Prefer short sentences
- One idea per bullet point
- If you can say it in fewer words, do

## Tone

Describe, don't prescribe. This guide documents patterns—it doesn't tell people what to do.

| Avoid | Use Instead |
|-------|-------------|
| "You should..." | "One approach is..." |
| "Always do X" | "X is an option when..." |
| "The right way is..." | "This pattern involves..." |

Define terms neutrally. Let readers decide what works for them.

## Examples

Bad:
> This essentially happens because the AI is basically trying to optimize for context efficiency, which actually causes it to miss important information.

Good:
> The AI optimizes for context efficiency and misses important information.
