---
name: sloptrim
description: >-
  Use when the user wants to humanize text, trim slop, de-AI or de-slop writing,
  remove AI tells, fix robotic or ChatGPT-sounding prose, or make writing sound
  human and natural. Also run before delivering a CV, cover letter, email,
  report, or essay to be sent. Removes 71 documented AI-writing patterns with a
  local detector, preserves numbers, names and citations, and rebuilds toward a
  human voice rather than a flat husk. Mode-aware, so it never fabricates voice
  on factual content.
version: 0.9.3
license: Apache-2.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: The text to trim, or a file path
---

# Sloptrim

Trims AI slop from text. Works a catalogue of 71 patterns: 62 machine-checked by `scripts/detect.py`, 9 requiring semantic judgment during the rewrite. Of the 62, 50 can move the score; the rest are reported as writing advice and count for nothing. Mode-aware so it does not invent voice on factual content. Preserves facts. Rebuilds the cleaned text toward a selectable human-voice **style profile** so it does not read as a sterile de-AI'd husk.

## Silence

This skill never talks about itself. It hands back the cleaned text and nothing else.

**Never emit:** any announcement that sloptrim ran, style/mode lines, scores or reports, drafts, self-audit notes, facts-preserved lines, change lists, preambles, closing offers.

**Emit only:**
- Text given inline: the final text. Nothing before it, nothing after it.
- A file path given: rewrite the file in place, then one line - the path. Nothing else.
- Fired as a pre-delivery pass on something you were already writing (CV, cover letter, email, report, essay): just deliver the clean text. Do not mention that a pass happened.

Every internal step still runs - detector, tiering, self-audit, character scrub. Silence means nothing is *printed*, not that anything is skipped.

Break silence only for: (a) a fact you cannot preserve, or an unusual word you cannot verify against the domain - one line, then the text; (b) the user explicitly asking for the score, the report, a style choice, or a diff - then answer in full; (c) a **high-stakes first-person deliverable** - a cover letter, personal statement, or bio the user is about to send - where after the text you may add exactly one line offering a voice switch (for example: "Voice here is plain-professional; say the word for warmer or more formal."). One line, only for these high-stakes cases, never for routine prose.

## Style, chosen silently

Never ask. Read the content and pick:

- encyclopedic / factual / technical → **2000s textbook**
- first-person / opinion → **conversational essay**
- docs, README, business prose → **plain / clear**
- news → **journalistic**

If the user names a style or pastes a writing sample, that wins (see *Matching the user's own voice*).

## Task

1. **Pick the style silently** (above). Never ask.
2. **Classify the content** (see *Content type and voice*) - conservative or drastic mode. The style profile sets the *target* rhythm and register; the mode sets how far you may push voice. They compose: e.g. 2000s textbook always stays conservative; conversational essay implies drastic mode.
3. **Run `scripts/detect.py`** and tier the pass to `_metrics.ai_tell_score`: `clean` (≤20) - character scrub and flagged spans only, do NOT rewrite (a human-first draft keeps its voice); `light tells` (21-40) - targeted edits plus rhythm repair; `mixed` and above - full rewrite toward the style profile.
4. **Identify remaining patterns** that require semantic judgment. Pattern names and category map are below. Read `references/patterns.md` when you need the precise Before/After examples for any pattern.
5. **Note critical content to preserve:** numbers, proper nouns, hyphenated technical terms, citations, units, dates. Then note the things an entity list does not hold, from *Critical content preservation* below: which claims are attributed and which are the writer's own, which are hedged, which figures belong to which nouns, every placeholder, and the input word count you may not exceed.
6. **Produce a draft rewrite** toward the chosen style profile.
7. **Anti-sterility self-audit loop** - internal, never printed: re-run `python "$DETECT"` on the draft; ask what still reads as AI, and whether it over-flattened (`length_cv` < 0.35, uniform paragraphs, `readability_uniform` true, contractions gone in drastic mode - a flat husk reads as machine-made just as fast as slop). Fix only the offending spans; cap at two loops; accept at `clean`/`light tells` and not over-flattened. Check the other direction in the same pass: count the words. Past 1.25x the input you have written new material, and no score justifies keeping it.
8. **Verify:** every fact preserved, no fabricated dates / quotes / sources, and every unusual word is correct for the domain (a real but wrong word is worse than a typo). Then re-read for the six failures in *Critical content preservation*: no attribution added or removed, no last hedge cut, no criticism reading as praise, every figure still on its own noun, every placeholder untouched, and the word count inside 1.25x.
9. **Scrub the output:** re-run `python "$DETECT"` on the final text and confirm `invisible_chars`, `nonstandard_spaces`, and `homoglyphs` are `0` (#62/#66/#67/#68 silent). Drafts from other models can carry zero-width or TAG-block characters that survive copy-paste; `python "$DETECT" --clean` strips them, normalizes spaces, folds homoglyphs, and trims stray whitespace without touching visible content.
10. **Output the final text, and only the final text** (see *Silence*).

## Style profiles

Removing AI tells is only half the job. The other half is rebuilding the text toward a voice a person would actually write in. Pick one from the content, silently (see *Style, chosen silently*). Each profile is a *positive target* - it does not change which AI tells are removed or the preservation rules; it sets the rhythm, register, punctuation, and paragraph shape the cleaned prose is rebuilt into.

**1. 2000s textbook** *(default)* - pre-LLM human academic prose (a well-edited textbook, roughly 2000-2008). Clear declarative sentences, one idea each; real length variation (a short statement, a longer development, a worked example - never metronomic); concrete examples introduced naturally; occasional first-person-plural for exposition, never first-person-singular opinion; semicolons and parentheses where a writer would use them, em-dash sparing. Forbidden: hype adjectives, signposting, hedge stacks, rule-of-three, "In today's world" openers, upbeat conclusions, emoji, bold-for-emphasis. Neutral and patient; explains, does not sell. Conservative mode.

**2. Plain / clear (Zinsser)** - tight modern nonfiction. Short words over long, cut every clutter phrase, concrete nouns and active verbs, one thought per sentence. Good for docs, READMEs, business prose. Conservative unless source is first-person.

**3. Conversational essay** - first-person, contractions, asides, real rhythm; reacts to facts rather than only reporting them; lets some mess in (tangents, half-formed thoughts). Implies drastic mode. Only for content that already carries a personal voice - never forced onto encyclopedic text.

**4. Journalistic / news** - AP style: short lede carrying the key fact first, inverted pyramid, attributed claims ("according to…"), plain verbs, no editorializing. Conservative.

If the user names a profile, rewrite toward it. Otherwise infer it per *Style, chosen silently*.

## Matching the user's own voice

When the user provides a writing sample (inline or a file path), take the target voice from it instead of a profile: measure its sentence lengths and their variation, formality, paragraph openers, punctuation habits, recurring phrases - then rebuild the cleaned text with those habits. No sample: fall back to *Content type and voice* below.

## Content type and voice

The biggest failure mode is injecting authorial voice into content that has none by design. A Wikipedia article does not get to say "I keep coming back to..." Classify first:

**Encyclopedic / factual** - third-person, dense with proper nouns, dates, statistics, citations, technical vocabulary (Wikipedia, science, news, docs, specs). → **Conservative mode.** Remove AI patterns, vary rhythm, keep tone neutral. Do not add first-person stance, opinions, or asides. Keep formal contractions (`it is`, `do not`) as-is.

**Opinion / first-person** - already uses "I" or "we"; expresses stance; has takes and asides (essays, posts, reviews). → **Drastic mode.** Remove AI patterns AND add voice. Contract where natural (`it's`, `don't`, `you've`).

**Mixed or unclear** → default to conservative.

**Classification signals:** first-person markers above ~2 % of words → opinion. Proper-noun density above ~5 %, numbers / dates / citations present → encyclopedic. Imperative voice → conservative (technical).

### Adding voice (drastic mode only)

Take positions - respond to facts instead of only stating them. Let rhythm move irregularly: a blunt sentence, then one that unwinds at its own pace; the enemy is a metronome in either direction. Acknowledge complexity, use "I" where it fits, and leave the small irregularities a person would - a digression, a parenthetical, an idea carried only as far as it needs to go. Be specific about feelings rather than generic.

## Critical content preservation

**Must survive every rewrite:** numbers and units (`0.19`, `1989`, `340 kg/m³`, `55 %`), proper nouns, hyphenated technical terms (`thin-walled`, `load-bearing`, `strength-to-weight`), citations, domain vocabulary.

**Safe to paraphrase:** hedges (`typically`, `generally`), generic passive verbs (`results from`, `consists of`), abstract property nouns when the domain term is also present, filler adverbs. *Paraphrasing* a hedge keeps the qualification and changes the wording; deleting the last one turns a qualified claim into an absolute one and is covered below.

**Never invent:** dates, statistics, quotes, named individuals, citations to sources not in the input. If specifics are missing, stay vague - do not supply plausible-sounding facts.

**Never change what a statement asserts, who it belongs to, or how much of it there is.** These are the failures that survive an entity check, because no number or name moves; every one was found in a real rewrite. Do not:

- **Turn a measurement into a claim, or a claim into a measurement.** `The bike weighs 23.2 lb` is the writer's observation. `Claimed weight is 23.2 lb` attributes it to the manufacturer and is a different sentence. Never add *claimed*, *reportedly*, *said to be* or *allegedly* to something stated plainly, and never remove them from something attributed.
- **Drop a hedge.** `there is the risk of over-diagnosis` becomes an assertion that over-diagnosis happens if `risk of` is cut. Hedge *stacking* is pattern 54 and gets fixed by removing one hedge, never the last one.
- **Invert a criticism.** `its small size makes it more of a deterrent than real theft prevention` is a complaint. Reading it as the reason the lock works reverses the writer's judgment.
- **Move a number to a different noun.** `30-hour battery life` is not `30 hours of noise cancellation`. Keep every figure attached to the thing it measured, especially in headings, subject lines and captions, where a reader sees it alone.
- **Rewrite a placeholder.** `[Name]`, `{{first_name}}` and `[Your Company]` are merge fields belonging to whatever system will fill them. Leave the token exactly as written, or leave the document alone.
- **Add material.** A rewrite fixes what is there. Anything past **1.25x the input word count** is invented, however plausible it sounds: elaboration, a new benefit, a closing argument the writer never made. Cutting is allowed; growing is not. This outranks the style profiles: where a profile asks for a pivot sentence, a worked example, a digression or a closing observation, it means *shape the material you have*, never *write more of it*. On a short document there is no room for any of them, and that is the correct outcome.

**Domain-correctness check:** every unusual word (≥ 7 letters, uncommon) in the rewrite must fit the surrounding domain vocabulary. Real-but-wrong words ("infantilization" appearing near vacuum-pressure / polymer terms) are harder to catch than typos and worse for credibility.

**Character layer (§62, §66, §67, §68 in `references/patterns.md`):** remove invisible and zero-width characters, normalize non-standard spaces to `U+0020`, trim stray trailing whitespace, fold mixed-script homoglyphs to ASCII (genuine non-Latin words untouched). Never strip legitimate `\t` / `\n` / `\r` inside the body. `scripts/detect.py --clean` applies all four deterministically.

## Pattern index

Each pattern has a full Before / After in `references/patterns.md` (read it for the precise phrasing list when working a pattern). The numbering groups patterns by function; it folds the community-documented signs together with this project's additions rather than ordering them by origin.

### Lexical tells (1-9)
1. AI vocabulary (era-variable - refresh per release)
2. Model-dialect vocabulary (fires at 2+ combined hits)
3. Promotional language
4. Hyphenated word-pair overuse (protect technical compounds)
5. "Simple yet X" cliché
6. Stacked adjective chains (4+ adjectives before one noun)
7. Rule of three (generic single-word triads only)
8. Synonym cycling
9. AI character names in fiction

### Rhetorical filler (10-26)
10. Significance inflation
11. Notability name-dropping
12. Vague attributions
13. Article-titles-as-proper-nouns
14. Conservation / ecosystem padding
15. False ranges
16. Superficial -ing tail clauses (never flag factual-consequence -ing; list in §16)
17. Negative parallelisms and tailing negations
18. "Not X, just Y" / "No X, just Y" framing
19. Filler phrases
20. Empty pivot phrases
21. Outcome speculation tails
22. Persuasive authority tropes
23. Editorial interjections
24. Self-thoroughness phrases
25. Question-answer rhetorical pattern
26. "Concrete evidence" defense phrase

### Structure and discourse (27-39)
27. Compulsive intro hooks
28. Meandering intro - semantic
29. Prompt echo (first sentence restates the prompt)
30. Diff-anchored writing (describe the thing, not the change) - regex + semantic
31. Signposting and announcements
32. Cataloguing lead-ins
33. Inline-header vertical lists
34. Mid-essay bullet injection (bullets where prose belongs)
35. Fragmented headers
36. Formulaic challenges sections
37. Transition cluster overuse (2+ per paragraph)
38. Compulsive conclusion phrases
39. Generic positive conclusions

### Rhythm and cadence (40-46)
40. Sentence-length monotony - statistical
41. Mechanical sentence-length alternation - statistical
42. Opener repetition
43. Avoidance of fragments and run-ons (drastic mode only)
44. Uniform paragraph length - statistical
45. Identical paragraph structure - semantic
46. Semicolon and parenthesis underuse (document-level statistical signal)

### Register and voice (47-55)
47. Chatbot artifacts
48. Sycophantic / servile tone
49. RLHF / helpful-assistant register - semantic
50. Knowledge-cutoff disclaimers
51. Copula avoidance
52. Passive voice and subjectless fragments
53. Two-way passive-voice drift (judge against the genre) - semantic
54. Excessive hedging (2+ in one sentence)
55. Contraction absence (only in opinion mode)

### Formatting and typography (56-61)
56. Boldface overuse
57. Emojis
58. Em-dash overuse (max one per paragraph)
59. Title case in headings
60. Curly quotation marks
61. Hyphen-for-en-dash in numeric ranges

### Machine artifacts (62-68), plus a lexical addition (69)
62. Invisible and zero-width characters (copy-paste artifacts)
63. Placeholder / Mad-Libs text - regex
64. Chatbot reference-markup leak - regex
65. AI tracking params (utm_source from chat UIs) - regex
66. Homoglyph / mixed-script confusables (folded by `--clean`) - character layer
67. Non-standard spaces (normalize, do not strip)
68. Trailing / stray whitespace (trim from output)
69. Canonical marketing-slop phrases - regex, high-precision
70. Decorative horizontal rules - 3+ standalone rules in a 25-line document
71. Degenerate repetition - over 20% of six-word spans repeated, a model in a loop

When working on a specific pattern, **read `references/patterns.md` and jump to the matching section** for the exact phrasing list and Before / After.

## Deterministic detection

**Resolve the detector path first** - `scripts/detect.py` is bundled in the skill directory, not the user's project, so a bare relative path will not resolve. Set `DETECT` once: as a plugin, `$CLAUDE_PLUGIN_ROOT/scripts/detect.py`; as a cloned skill, Glob `**/sloptrim/scripts/detect.py` (usually `~/.claude/skills/sloptrim/scripts/detect.py`). Then run it before manual review:

```bash
python "$DETECT" input.txt        # pass a path (works on all shells)
```

It emits JSON: pattern IDs with counts and samples, a `_metrics` block (rhythm statistics, contraction and passive ratios, character-layer counts), and **`ai_tell_score` (0-100)** with a band (`clean` / `light tells` / `mixed` / `heavy tells` / `pervasive tells`). The score weighs pattern diversity over raw density, floors when the character layer finds codepoints that carry no meaning in the text, and ignores copy-editing preferences. It is a triage heuristic, not a calibrated classifier.

A score describes the writing in front of it. It is not a judgement about who or what wrote a document, it cannot support one, and it must never be used to accuse a person of anything. See ETHICS.md. The 9 catalogue entries with no detector behind them (7, 9, 28, 29, 43, 45, 49, 52, 53) are worked by reading; even machine-checked ones deserve a reading pass for what the regex misses.

For the deterministic character layer, `--clean` emits the scrubbed text instead of JSON - it strips the invisible and non-printing codepoints, normalizes non-standard spaces to `U+0020`, folds mixed-script homoglyph letters back to ASCII (#66), and trims stray whitespace. Visible text is left alone. Trailing whitespace at the end of a line is not: it is removed, which will collapse a Markdown hard break if the draft used one. Only ever redirect this into a **new plain-text file**: given a `.docx`, `.epub`, `.odt` or `.ipynb` it prints the extracted text rather than a rebuilt document, so writing it back over the original would replace the document with loose text.

```bash
python "$DETECT" --clean gemini_nano_output.txt > clean.txt
```

Run it on any draft produced by another model to remove smuggled zero-width or TAG-block characters before the text ships.

## Positive style patterns

Removing AI patterns is half the job; fill the space with patterns a person writes: active specific verbs (`runs between`, `locks into` - not `serves as`, `provides`); a short pivot sentence every 3-4 sentences that reframes the next idea; em-dash for contrast at most once per paragraph; the colon as an explanation hinge; concrete subjects ("Wind turbine blades rely on balsa" beats "Balsa is used in turbines"); specific judgments ("unusually high stiffness"); a final sentence that carries weight - a fact or real observation, never a generic positive close; varied paragraph length, one-sentence paragraphs allowed.

## Reference

The catalogue folds publicly documented signs of AI writing with newer model-specific tells; all worked examples in `references/patterns.md` are original, and the lexical layer (#1) is the refresh point as model vocabularies shift. Scope is rewriting, not detection; defeating institutional integrity systems is out of scope. Version **0.9.3**.
