---
name: prime
description: Use at the very start of any coding task in a repo that has sound taste rules installed (a `.claude/sound/` directory), before writing or editing code.
user-invocable: true
---

# sound:prime

If the repo has no `.claude/sound/` directory, it carries no sound taste rules — do nothing.

Otherwise: the project's taste rules live under `.claude/sound/`, grouped into topic folders (`<topic>/<rule-name>.md`). Before you write, browse the tree to see which topics bear on the surfaces you'll touch. Read a rule's file when its situation comes up, and make sure your code meets every rule that governs a surface you change.
