---
name: ubiquitous-language
description: Extract a domain glossary from the current dialogue; flag ambiguities, propose canonical terms, persist to `UBIQUITOUS_LANGUAGE.md`. Trigger when the user is hardening domain terminology, building a glossary, or fresh domain concepts surface in conversation without documented language.
disable-model-invocation: true
---

Mine the live conversation for domain-relevant nouns, verbs, and concepts; resolve synonyms and overloaded terms into a canonical, opinionated glossary. Persist the result to `UBIQUITOUS_LANGUAGE.md` so subsequent sessions inherit the same vocabulary. Re-invocation refines the file in place rather than overwriting.

When a candidate term collides with usage already present in the codebase, dispatch an Explore agent (`fd`-first discovery, `git grep`/`ast-grep` content search) to confirm the dominant naming before recommending a winner. The user supplies domain intent; the codebase supplies factual usage.

**Modality vs adjacent skills:** This skill *extracts* glossary from raw conversation when no documented domain language exists yet. *Domain-model grilling* *grills* a plan against an already-documented `CONTEXT.md`/ADRs. Pick `ubiquitous-language` when you are creating the artifact; pick the grilling workflow when you are stress-testing one. The two compose: build the glossary here, then promote stable terms into `CONTEXT.md` and let the grilling workflow defend it thereafter.

## Process

1. Scan the dialogue for domain-relevant nouns, verbs, and concepts. Skip generic programming nouns (array, function, endpoint) unless they carry domain weight.
2. Identify three failure modes: same word for different concepts (ambiguity), different words for the same concept (synonyms), vague or overloaded terms.
3. Propose canonical terms with explicit aliases-to-avoid. Be opinionated — pick one winner per concept and justify briefly.
4. Persist `UBIQUITOUS_LANGUAGE.md` to the working directory using the format in `references/UBIQUITOUS-LANGUAGE-FORMAT.md`.
5. Emit a short inline summary of additions, renames, and flagged ambiguities so the user can react in-thread.

## Rules

- One sentence per definition. Define what the term *is*, not what it *does*.
- Group terms into multiple tables when natural clusters exist (subdomain, lifecycle, actor). Force no grouping when a single cohesive table reads cleanly.
- Express relationships with bold term names and explicit cardinality where obvious (`exactly one`, `one or more`, `optional`).
- Flagged ambiguities require a recommendation, not a question. The skill resolves; the user overrides.
- Treat module and class identifiers as glossary candidates only when they carry domain meaning. Prefer abstract domain terms over implementation aliases.
- Include an example dialogue (3–5 exchanges) demonstrating the terms used precisely. The dialogue clarifies boundaries between adjacent concepts.

## Re-invocation

When invoked again in the same conversation:

1. Read the existing `UBIQUITOUS_LANGUAGE.md`.
2. Incorporate new terms surfaced since the last pass.
3. Update definitions when shared understanding has shifted; preserve the old wording in commit history rather than the file body.
4. Re-flag any new ambiguities; demote resolved ambiguities to a closed note or remove them once the glossary stabilises.
5. Refresh the example dialogue so it exercises the latest term set.

## Reference materials

- `references/UBIQUITOUS-LANGUAGE-FORMAT.md` — table layout, relationship syntax, dialogue template, flagged-ambiguities format. Language-agnostic.

## ODIN integration

**Primary:** after the glossary stabilises, promote terms into `CONTEXT.md` and hand off to `odin:domain-model` for ongoing adversarial defence.

**Tied candidates:** when two candidate canonical terms cannot be ranked from the dialogue alone, use `odin:askme` for a clarifying question rather than arbitrarily picking a winner.

**User-directed naming:** when the user wants to drive term selection, engage `odin:duet` — user as director, skill as executor capturing the choices.
