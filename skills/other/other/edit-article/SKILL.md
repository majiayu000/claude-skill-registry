---
name: edit-article
description: Mechanically tighten existing prose — restructure sections by dependency order, split or merge paragraphs, remove redundancy. Use to compress verbose plan files, READMEs, ADRs, and design docs. Does NOT change voice, register, tone, or any ODIN-mandated phrasing.
---

Mechanical, structural-only edits to prose. Voice and register are load-bearing and preserved verbatim.

## Allowed transformations

- Restructure section order to respect information dependencies (treat info as a DAG; later sections may depend on earlier, never vice versa).
- Split a paragraph carrying two distinct points into two paragraphs.
- Merge two short paragraphs that carry the same point into one.
- Remove redundant sentences, clauses, or words that repeat what was already stated.
- Consolidate parallel lists or tables into a single canonical form when content overlaps.
- Tighten run-on sentences into shorter, clearer ones — preserving the original meaning and the original word choice where possible.
- Cap paragraphs at ~240 characters where doing so requires no rephrasing.
- Promote inline asides into footnotes or sidebars when they break flow.
- Demote redundant headings; promote orphan paragraphs to their own subsection.

## Forbidden transformations (hard fence)

- Do NOT change voice (active/passive, first/second/third person).
- Do NOT change register (formal ↔ casual).
- Do NOT change tone (technical, decision-oriented, imperative).
- Do NOT rewrite ODIN-mandated phrasing — terse imperative, third-person, English-mandate, decision-first prose stays.
- Do NOT introduce new claims, examples, or analogies that were not in the source.
- Do NOT remove technical specificity (file paths, command flags, version numbers, named constants).
- Do NOT rename headers, fields, or list items even if they look redundant — those are structural and load-bearing.
- Do NOT translate non-English-mandate content into a different style "for clarity."
- Do NOT add emojis, gradients of warmth, marketing language, or hedging.

If a transformation seems necessary but lives in the forbidden list, STOP and surface the question to the user.

## Protocol

1. Dispatch Explore agent (or read directly for ≤50 LOC) to map the document into sections by heading. Build the dependency graph.
2. Confirm the section order and graph with the user before any edit.
3. For each section, in dependency order:
   - Identify candidate transformations from the **allowed** list.
   - Apply only those. Surface any forbidden-list candidates as questions.
   - Diff with `difft` after the edit; reject the change if voice/register/tone shifted.
4. After all sections are processed, re-read the document end-to-end. Confirm flow without re-editing.
5. Commit with message: `docs: tighten <document-name> (mechanical edits only)`.

## Use cases (in scope)

- Tightening a verbose `docs/refactor-plans/<n>.md` produced by `request-refactor-plan`.
- Compressing a long-form ADR before merging.
- Removing duplicated sentences across README sections.
- Reordering a tutorial whose steps reference forward concepts.

## Use cases (out of scope — use a different skill)

- Rewriting a draft in a different voice — use a manual rewrite, not this skill.
- Translating a non-English document — ODIN's English-mandate governs original drafting.
- Producing a new document from notes — use general implementation planning or `request-refactor-plan`.

## Parallel examples

**Rust crate README:** allowed — split a 400-char paragraph mixing "what it is" and "how to install" into two paragraphs; merge two adjacent install paragraphs covering cargo and pre-built binaries. Forbidden — rewriting the imperative install steps as friendly second-person.

**Python project ADR:** allowed — reorder "Consequences" to follow "Decision" (was reversed); strip a sentence that re-states the title. Forbidden — softening a hard "MUST" into "should".
