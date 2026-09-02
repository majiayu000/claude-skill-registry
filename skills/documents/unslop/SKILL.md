---
name: unslop
description: 'Use when prose is drafted or edited, reviewed for AI tells, or the user asks to remove AI patterns, humanize, or add voice. Runs 20 pattern-replacement checks across prose files; dedash mode purges em-dashes by grammatical role; detool mode neutralizes incidental tool names in portable artifacts. For code debris use deslop.'
---

# Unslop

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Prose is drafted or edited, text is under review for AI tells, or the user asks to remove AI patterns, humanize, add voice, purge em-dashes by grammatical role, or neutralize incidental tool names in portable artifacts. |
| Authority | Reversible local write. Edit only the named prose file or scope; the original is recoverable from version control or the user's undo. |
| Side effect | Rewrites user-facing or internal prose files; may replace punctuation by grammatical role and remove incidental framework and tool nouns. |
| Done | The rewrite passes all 20 checks (full mode) or the focused mode's pass condition; meaning is preserved. |

## Refusals

- Code debris and dead code: use `deslop`. Unslop edits prose; deslop cuts code.
- Korean or other non-English humanization: unslop applies the same full-mode checks; where a check's example list is English-specific, judge the underlying pattern (puffery, filler, passive voice, meta-narration) in the target language rather than the literal words.
- The routing verdict: use `deslop` for code debris and `purge-slop-docs` for stale doc trees; use unslop when the answer is prose editing.
- Already clean: if the text contains no AI tell patterns, return it unchanged and report the text is already clean.

## Inputs

- Prose file, scope, or inline text (required): the file, text block, directory, glob, or pasted text to edit. When the user supplies text inline rather than a path, edit that text directly and return the result.
- Mode (optional): `full` (default: all 20 checks), `dedash` (em-dash purge by grammatical role), `detool` (incidental tool-name neutralization in portable artifacts).
- Tone guidance (optional): intended register or audience; defaults to the file's existing voice.
- Strictness (optional, dedash only): `default` replaces clear-cut cases; `strict` surfaces every occurrence as a judgment call.

## Procedure

### Full mode (default)

1. Read the prose file end to end. If the file is empty or missing, stop and report the failure. **Done when**: every paragraph has been read.
2. Scan every paragraph against the 20 checks below. **Done when**: every paragraph has a per-check verdict.
3. Rewrite the file while preserving its meaning and intended tone. **Done when**: all passing checks are reflected in the text.
4. Add voice: have opinions, vary rhythm, acknowledge complexity, use "I" when it fits, let some mess in, be specific. **Done when**: the text reads as a person wrote it.
5. Self-audit: "What makes this obviously AI-generated?" Fix remaining tells. **Done when**: no answer survives the question.
6. Verify meaning is preserved. If any edit changes the factual content or logical claim, revert that edit and rephrase. **Done when**: no edit altered meaning.

### Dedash mode

Triggered when the user asks to remove em-dashes and look-alikes from a named scope. The grammatical-role classification and leave-alone rules live in `references/dedash.md`.

1. Enumerate all files in the named scope. If the scope is empty or missing, stop and report `scope-empty`. **Done when**: the file list is complete.
2. Scan each file for em-dashes (`—`, `---`, `--`), en-dashes used as em-dashes, and Unicode em-dash variants. **Done when**: every occurrence is located.
3. Classify every occurrence by grammatical role per `references/dedash.md` and apply the replacement. **Done when**: each occurrence is replaced, skipped with a leave-alone reason, or surfaced as a judgment call.
4. Produce a report: occurrences found, replaced by role class, skipped by leave-alone class, judgment calls. **Done when**: per-file and aggregate counts are reported.

### Detool mode

Triggered when a durable artifact claims portability or tool-neutrality while carrying stack-specific nouns. The role classification and protection rules live in `references/detool.md`.

1. Read the target artifact end to end. If not found or unreadable, stop and report the miss. **Done when**: the whole artifact has been read.
2. Classify the artifact, or each section if mixed, into durable/portable, provenance/operational, or tool-subject per `references/detool.md`. **Done when**: every section has a recorded role.
3. Sweep durable-content sections for incidental coupling and replace each hit with the neutral mechanism that preserves the action. **Done when**: every hit is neutralized or kept with a recorded reason.
4. Re-read as a reader on a different stack. **Done when**: the artifact is still true, portable, and executable where it promised action.
5. Report neutralized couplings, deliberate keeps with their role, and judgment calls. **Done when**: the report is complete.

## The 20 checks

**Content**
1. Puffery and promotional language: "pivotal moment", "testament to", "evolving landscape", "nestled", "vibrant", "breathtaking", "groundbreaking". Cut; state what happened.
2. Name-dropping and vague attributions: listing media outlets without context, "Experts believe", "Industry reports suggest". Name the source or delete.
3. Superficial -ing phrases and formulaic challenges: "highlighting...", "ensuring...", "Despite challenges... continues to thrive". Delete or replace with specific facts.

**Language**
4. AI vocabulary: additionally, crucial, `delve`, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
5. Fancy copulas and forced structures: "serves as", "stands as", "boasts", "features", "Not just X, but Y", rule of three, synonym cycling, false ranges. Say it directly with the natural number of points.

**Style**
6. Em-dash overuse: do not stack several in one paragraph; replace each with the punctuation that spot needs (period, comma, colon, parentheses, or nothing). Count look-alikes (en dash, double hyphen, minus sign, horizontal bar); judge each on its own. For the full grammatical-role classification and leave-alone rules, run dedash mode or see `references/dedash.md`.
7. Colon overuse, boldface overuse, inline-header lists, title-case headings, decorative emojis, curly quotes: colons only before lists or examples; bold only when earned; convert restating bold-label-colon lines to prose; use sentence case for headings; remove decorative emojis; replace curly quotes with straight quotes.

**Communication artifacts**
8. Chatbot phrases, cutoff disclaimers, sycophantic tone: "I hope this helps!", "Let me know if...", "Of course!", "While specific details are limited...", "Great question!" Remove; respond directly.

**Filler**
9. Filler phrases, excessive hedging, generic conclusions: "In order to" becomes "To"; "Due to the fact that" becomes "Because"; delete "It is important to note that"; collapse "could potentially possibly be argued that it might" to "may"; replace "The future looks bright" with specific facts.

**Jargon**
10. Abstract metaphor nouns: substrate, wedge, vector, locus, vantage, nexus, bedrock, modality, paradigm, ratchet, evacuate (for moving code), endgame, north star, flywheel. Replace with the concrete word: "substrate" becomes "base", "wedge" becomes "add", "vector" becomes "way", "ratchet" becomes the mechanism's real name or "a limit that only tightens", "evacuate" becomes "move out", "endgame" becomes "the last phase". Ban a word only when a plainer concrete word says the same thing.

**Plain speech**
11. Name the mechanism, not the feeling: "the database stays close at hand" becomes "`.toSQL()` returns the exact string sent to the database". If the sentence could appear unchanged in another project's docs, cut it.
12. Dense sentences: if the reader has to backtrack, break the sentence in two. One idea per sentence.
13. Active voice: catch "is/are/was/were + past participle" and name the actor. Passive is fine only when the actor is unknown or genuinely doesn't matter.
14. Adverbs and weak verbs: "runs quickly" becomes "is fast" or the measured delta. An adverb propping up a weak verb means the verb is wrong.
15. Plain word preference: "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".

**Portability**
16. Incidental stack nouns: in content meant to travel (skills, rule docs, library READMEs), a tool or vendor name that is not the subject goes stale when the stack changes. "Run `pnpm test`" in a document about testing discipline means "run the project's test command". Judge each noun: load-bearing when the document is about that tool, incidental when it stands in for a mechanism. Replace incidental ones with the mechanism they mean; leave load-bearing ones alone. For the full role classification and protection rules, run detool mode or see `references/detool.md`.

**Trust and structure**
17. Fabricated voice or quotation: never invent a quote, testimonial, consensus, or attributed reaction. Quote only supplied or cited text; otherwise write the claim without quotation marks and name its evidence.
18. Previous-pointing prose: replace "as discussed above", "previously noted", and similar navigation with the fact the reader needs at that point. Keep a cross-reference only when the target is the literal source of truth the reader must inspect.
19. Mechanical symmetry: break repeated paragraph templates, forced three-part lists, and identical sentence openings. Keep repetition only when it carries a real comparison or invariant.
20. Meta-process narration: remove descriptions of drafting, analysis, response structure, and the writer's own effort unless the process is the subject. State the result, evidence, or required action directly.

## Failure and recovery

- Missing or empty source (full mode): stop; report "source file missing or empty". Do not create a file.
- scope-empty (dedash mode): no files matched the scope. Report; perform no writes.
- Artifact not found or unreadable (detool mode): stop immediately; report the miss. Do not fabricate content.
- Meaning drift: if an edit changes the factual content or logical claim, revert that edit and rephrase. If no rephrase preserves both meaning and the check, keep the original and flag the conflict.
- ambiguous-role (dedash mode): an occurrence fits neither a clear replacement class nor a leave-alone class. Surface it as a judgment call with the surrounding sentence. Do not guess.
- Ambiguous role classification (detool mode): default to durable content and flag the judgment call in the report.
- Neutral wording loses the mechanism (detool mode): keep the concrete detail as an example; note the decision in the report.
- Pattern introduction: if the rewrite introduces a new pattern from the checklist, re-run self-audit on the affected paragraph.
- Non-converged: if three rewrite passes still leave checklist violations, stop and report the remaining violations with their locations.
- partial-completion (dedash mode): if a file write fails mid-batch, stop processing that file, report the partial state, and continue with remaining files.
- Edit alters the mechanism or evidence (detool mode): abort that edit; report the conflict.

## Output

The rewritten prose file with original meaning preserved. Full mode: all 20 checks passing, or if non-converged after three passes, the remaining violations reported with their locations. Dedash and detool modes append a per-occurrence or per-hit report.

