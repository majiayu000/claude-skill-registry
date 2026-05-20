---
name: brainstorming
description: Rapid ideation skill adapted from obra/superpowers to kick off cortex sessions. Use when defining scope, aligning on goals, or exploring solution space before coding.
license: MIT (obra/superpowers)
---

# `/collaboration:brainstorming`

Ported from obra/superpowers (MIT). Optimized for cortex so brainstorming outputs flow directly into Supersaiyan visuals and the Task TUI.

## When to run

- **Before touching code**: align on problem, success signals, blockers.
- **After big context shifts**: new stakeholder, major dependency change, fresh repo checkout.
- **When you feel stuck**: broaden solution space before diving back in.

## Inputs you need

- Current goal or ticket reference.
- Repo hints: relevant `modes/` (e.g., `modes/Super_Saiyan.md`) and `scenarios/` if they exist.
- Constraints (deadline, platforms, regulatory, etc.).

## Steps

1. **Set the stage**
   - Load `modes/Super_Saiyan.md` (CTRL+P → "Super Saiyan Mode") for visual/tone context.
   - Skim any `scenarios/ideation/*.md` tied to the feature.
2. **Map the landscape**
   - List known goals, success metrics, blockers, unknowns.
   - Capture existing assets (agents, rules, workflows) that might help.
3. **Generate options**
   - Expand at least three distinct approaches (different modes, agents, or workflows).
   - Note pros/cons, risk, required verification per approach.
4. **Select candidate plan**
   - Pick the best approach and flag what still needs validation.
5. **Seed Tasks**
   - Open the Task view (`T`) and add top-level tasks from the brainstorming takeaways (or run `/ctx:plan` next to formalize).

## Output format

```
### Problem / Goal
### Success Signals
### Constraints / Risks
### Existing Assets
### Options
- Option A …
- Option B …
- Option C …
### Chosen Direction & Next Checks
```

Paste the summary into the chat (or save under `scenarios/`). Then move to `/ctx:plan`.

## Resources

- See `skills/collaboration/brainstorming/resources/examples.md` for ready-made follow-up prompts.
