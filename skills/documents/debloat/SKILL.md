---
name: debloat
description: 'Compress a bloated artifact to its load-bearing density, cutting words and never a rule. Use when a document, skill, or spec has grown padded while every rule in it still binds, or the user says "debloat this", "tighten this up", or "this is too long". Every rule present before the pass is present after it. To cut whole documents and stale content from a markdown tree, use purge-slop-docs; for a code diff, use simplify.'
disable-model-invocation: true
---
# Debloat

Cut a bloated artifact to its load-bearing density. Same meaning, fewer words.

## Method

1. **Read end to end** and note in one line what each section must convey.
2. **Find the bloat, not the content.** Padding that adds length but not meaning, a qualifier the sentence holds without, a fused sentence carrying three ideas, a wall of enumeration where a rule plus a short list would do, a point restated within reach of itself, litigation-history where the rule alone suffices.
3. **Compress in place.** Cut the padding, split the fused sentence, collapse the wall, keep a repeated point once. Move nothing to another artifact and re-derive nothing. See `../clean-and-true/references/idioms.md` for edit safety.
4. **Keep every load-bearing claim.** If cutting a word would lose one, keep the word.
5. **Hand off what is not bloat.** Duplication across artifacts goes to `consolidate-to-one-home`, drift goes to `rewrite-clean-v0`. Do not force-compress them.
6. **Cut again cold.** The first pass always leaves some.

## Completion

Every load-bearing claim present before is present after; only density changed. A cold reader finds the result tighter, not amputated. Duplication and drift were handed off where they applied. A pass that finds nothing to genuinely improve changes nothing.

