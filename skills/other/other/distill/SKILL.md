---
name: distill
description: Strip overspecified instructions from an artifact. Trust the model's intuition — prescribe intent, not format.
---

# Distill

You're over-specifying. The artifact tells the reader *how* to format output instead of *what* to accomplish. That scaffolding was necessary for weaker models. It constrains stronger ones.

## The Problem

When writing skills, prompts, or instructions, you default to showing exactly what the output should look like — filled-in example tables, prescribed column names, template formats. This feels helpful but it creates a ceiling. The model matches your template instead of thinking about what the specific problem needs.

## The Test

For each instruction in the artifact, ask: **is this intent or format?**

| Intent (keep) | Format (cut) |
|----------------|--------------|
| Summarize the results in a table | Use these columns: Name, Status, Duration, Owner |
| Assessments should be opinionated | Acceptable values: "ready", "blocked", "needs work" |
| Group items by category | Categories: Infrastructure, Frontend, Backend, Testing |
| Commit your changes after each step | Run `git add -A && git commit -m "step N: description"` |

## On Activation

1. **Identify the artifact** that's over-specifying.
2. **Flag every instruction** that prescribes format rather than intent.
3. **Cut or compress** — remove examples that constrain, keep descriptions that guide.
4. **Verify nothing essential was lost** — can a capable model still produce good output from what remains?

## What to Cut

Filled-in example tables, prescribed column names, lists of acceptable values, step-by-step commands for things the model knows how to do. If an instruction only exists to show "what the output should look like" — cut it. The model knows how to make tables, pick column names, and write git commands.

**Exception:** Keep format prescriptions that encode domain insight or non-obvious constraints.

## What to Keep

- Phase structure (what to do in what order)
- Anti-patterns (what not to do)
- Non-obvious constraints (things the model would get wrong without being told)
- The "why" behind each phase

## Anti-patterns

- **Cutting intent along with format** — "Present a comparison table" is intent. Don't cut it just because it mentions tables.
- **Cutting non-obvious domain knowledge** — A constraint that looks like format ("process items sequentially") may encode a real dependency. Keep it.
- **Over-distilling into vagueness** — "Do the thing" is not a skill. Each phase should still say what to accomplish.

---

The user has an artifact that over-specifies. Distill it now.
