---
name: slop-detector
description: Detects AI-generated writing patterns in prose. Use when reviewing docs for slop, vague language, or identity leaks before publishing.
globs: "**/*.md"
alwaysApply: false
category: writing-quality
tags:
- ai-detection
- slop
- writing
- cleanup
- documentation
- quality
tools: []
complexity: medium
model_hint: fast
estimated_tokens: 4200
progressive_loading: true
modules:
- modules/vocabulary-patterns.md
- modules/structural-patterns.md
- modules/fiction-patterns.md
- modules/document-economy.md
- modules/identity-and-voice-leaks.md
- modules/hallucination-detection.md
- modules/stub-and-deferral.md
- modules/evidence-backed-claims.md
- modules/anti-goals.md
- modules/cleanup-workflow.md
- modules/empirical-baseline.md
- modules/structured-finding-output.md
- modules/remediation-strategies.md
- modules/language-handling.md
- modules/config-file.md
- modules/reporting.md
- modules/ci-integration.md
dependencies:
- scribe:shared
role: library
---
# AI Slop Detection

**Slop is a density problem, not a word problem.**

A single "delve" is fine. Five "delves" near a "tapestry"
and an "embark" is generated text. This skill scores
density per 100 words, marker clustering, and whether
the overall register fits the document type. It does not
ban words; it flags concentrations.

## Execution Workflow

Identify target files and classify them as technical docs,
narrative prose, or code comments. Classification feeds
context-aware scoring: tier-1 markers in marketing copy
score lower than the same markers in API reference.

### Language Detection

- Auto-detect language from text content using function word frequency
- Override with explicit `--lang` parameter (en, de, fr, es)
- Load language-specific patterns from `data/languages/{lang}.yaml`
- Fall back to English if detection confidence is low
- See `modules/language-handling.md` for cultural calibration and concrete pattern sets

### Vocabulary and Phrase Detection

Load: `@modules/vocabulary-patterns.md`

Markers fall into three confidence tiers. Tier 1 words
("delve", "multifaceted", "leverage") appear far more often
in AI text than human text. Tier 2 covers context-dependent
transitions ("moreover", "subsequently"). Tier 3 covers
vapid phrases ("In today's fast-paced world", "cannot be
overstated").

| Word | Context | Human Alternative |
|------|---------|-------------------|
| delve | "delve into" | explore, examine, look at |
| tapestry | "rich tapestry" | mix, combination, variety |
| realm | "in the realm of" | in, within, regarding |
| embark | "embark on a journey" | start, begin |
| beacon | "a beacon of" | example, model |
| spearheaded | formal attribution | led, started |
| multifaceted | describing complexity | complex, varied |
| comprehensive | describing scope | thorough, complete |
| pivotal | importance marker | key, important |
| nuanced | sophistication signal | subtle, detailed |
| meticulous/meticulously | care marker | careful, detailed |
| intricate | complexity marker | detailed, complex |
| showcasing | display verb | showing, displaying |
| leveraging | business jargon | using |
| streamline | optimization verb | simplify, improve |

### Tier 2: Medium-Confidence Markers (Score: 2 each)

Common but context-dependent:

| Category | Words |
|----------|-------|
| Transition overuse | moreover, furthermore, indeed, notably, subsequently |
| Intensity clustering | significantly, substantially, fundamentally, profoundly |
| Hedging stacks | potentially, typically, often, might, perhaps |
| Action inflation | revolutionize, transform, unlock, unleash, elevate |
| Empty emphasis | crucial, vital, essential, paramount |

### Tier 3: Phrase Patterns (Score: 2-4 each)

| Phrase | Score | Issue |
|--------|-------|-------|
| "In today's fast-paced world" | 4 | Vapid opener |
| "It's worth noting that" | 3 | Filler |
| "At its core" | 2 | Positional crutch |
| "Cannot be overstated" | 3 | Empty emphasis |
| "A testament to" | 3 | Attribution cliche |
| "Navigate the complexities" | 4 | Business speak |
| "Unlock the potential" | 4 | Marketing speak |
| "Treasure trove of" | 3 | Overused metaphor |
| "Game changer" | 3 | Buzzword |
| "Look no further" | 4 | Sales pitch |
| "Nestled in the heart of" | 4 | Travel writing cliche |
| "Embark on a journey" | 4 | Melodrama |
| "Ever-evolving landscape" | 4 | Tech cliche |
| "Hustle and bustle" | 3 | Filler |

## Step 3: Structural Pattern Detection

Load: `@modules/structural-patterns.md`

### Em Dash Overuse

The single most-cited 2026 AI tell across Wikipedia, the Field
Guide, and the Algorithmic Bridge. Detection runs in two modes:

**Audit mode** (forensic, applied to unknown prose):
- **0-1 per 1000 words**: Normal human range
- **2-4**: Elevated, review usage
- **5+**: Strong AI signal

**Prevention mode** (applied to docs the agent just generated):
- **Target zero**. Every em-dash is a finding.
- Replace with commas (asides), parentheses (tangents), colons
  (definitions), or periods (separate thoughts). See
  `modules/structural-patterns.md` § Em Dash Analysis for the
  full replacement table.

```bash
# Count em dashes in file
grep -o '—' file.md | wc -l
```

### Tricolon Detection

AI loves groups of three with alliteration:
- "fast, efficient, and reliable"
- "clear, concise, and compelling"
- "robust, reliable, and resilient"

Pattern: `adjective, adjective, and adjective` with similar sounds.

### List-to-Prose Ratio

Count bullet points vs paragraph sentences:
- **>60% bullets**: AI tendency
- **Emoji-led bullets**: Strong AI signal in technical docs

### Sentence Length Uniformity

Measure standard deviation of sentence lengths:
- **Low variance** (SD < 5 words): AI monotony
- **High variance** (SD > 10 words): Human variation

### Paragraph Symmetry

AI produces "blocky" text with uniform paragraph lengths.
Check whether paragraphs cluster around the same word count.

## Step 4: Identity & Voice Leak Sweep (P0)

Load: `@modules/identity-and-voice-leaks.md`

**Some patterns are not slop: they are direct evidence
that AI generated text leaked into a published artifact.**
A single match in this class fails review independently
of any other score.

Scan for:

1. **Identity leaks** ("As a large language model",
   "as of my training cutoff", "I cannot provide") —
   severity: critical, no exceptions.
2. **Conversational voice leaks** ("Hope this helps!",
   "Great question!", "Sure!") outside transcript blocks.
3. **Self-narration of structure** ("In this section, we
   will cover...", "Let's dive into...", "By the end of
   this guide...").
4. **Hedging seesaw** ("While X has its merits, it's not
   without its challenges").
5. **Contrastive constructions** as paragraph openers: both
   contrastive negation ("not just X, but Y", "It's not X,
   it's Y") and affirmative antithesis ("Less X, more Y",
   "Where others X, we Y"). Avoid in all but the most
   necessary cases; keep only when the contrast carries
   information that survives removal.

See the module for the full pattern catalogue and false-
positive guidance.

## Step 4.5: Sycophantic Pattern Detection

Especially relevant for conversational or instructional content
(complements Class 2 of the identity-and-voice-leaks module):

| Phrase | Issue |
|--------|-------|
| "I'd be happy to" | Servile opener |
| "Great question!" | Empty validation |
| "Absolutely!" | Over-agreement |
| "That's a wonderful point" | Flattery |
| "I'm glad you asked" | Filler |
| "You're absolutely right" | Sycophancy |

These phrases add no information and signal generated content.

## Step 4.6: Tier 5 / 2026 Patterns (Prevention-Strict)

The 2026 cross-source consensus (Wikipedia *Signs of AI
writing*, Algorithmic Bridge *10 Signs*, Ignorance.ai *Field
Guide*, Stop-Slop Claude skill, George Kao, ContentBeta,
OliviaCal) identifies a handful of shapes that dominate
post-GPT-5 / post-Claude-4.5 prose. Each is detailed in
`@modules/vocabulary-patterns.md` (lexical form) and
`@modules/structural-patterns.md` (structural form).

| Pattern | Form | Why it matters |
|---------|------|----------------|
| Em-dash overuse | — used as rhetorical pause | Most-cited single tell of 2026 |
| Plus-sign for "and" | "hooks and skills" in prose | Strong: humans have "and" |
| Spatial copula | "lives in", "sits at", "stands as", "boasts" | Inanimate subject with animate verb |
| Negative parallelism (contrastive negation) | "Not X but Y", "No X. No Y. Just Z.", "No X, no Y, no Z", "It's not X, it's Y", "Y, not X" | Rhetorical scaffold with no argument |
| Contrastive parallelism (affirmative antithesis) | "Less X, more Y", "Where others X, we Y", "Humans propose; machines dispose" | Manufactured punch; same scaffold without the "not" |
| Throat-clearing openers | "Here's the thing,", "Look,", "Let that sink in." | Discourse markers signaling nothing |
| Three-fragment burst | "Focused. Aligned. Measurable." | Rhythm without information |
| Significance cluster | "stands as a testament to", "marks a turning point" | Asserts importance without showing it |
| Smart quotes in technical prose | `"text"` / `"text"` instead of `"text"` | Word-processor paste signature |
| Loop/cascade vocab | "unpack", "surface" (verb), "a quiet shift" | 2026 systems-theory affectation |

**Prevention rule**: when the slop-detector runs on docs the
agent itself just generated (auto-invoked by `/doc-generate`,
`/doc-polish`, `/update-readme`, `/update-docs`, etc.), every
match in this table is a hard failure. Fix before write. See
`modules/remediation-strategies.md` § Tier 5 / 2026 for the
substitution tables.

## Step 5: Calculate Slop Density Score

```
slop_score = (tier1_count * 3 + tier2_count * 2 + phrase_count * avg_phrase_score) / word_count * 100
```

| Score | Rating | Action |
|-------|--------|--------|
| 0-1.0 | Clean | No action needed |
| 1.0-2.5 | Light | Spot remediation |
| 2.5-5.0 | Moderate | Section rewrite recommended |
| 5.0+ | Heavy | Full document review |

## Step 6: Document Economy Check

Load: `@modules/document-economy.md`

**Sentence cleanliness is necessary, not sufficient.** A document
can score 0 on slop density and still waste reader time by being
too long, lacking a thesis, or repeating everything except the
one message that matters.

Score the document on three checks (0-2 each):

1. **Thesis-first**: does the lead state the single takeaway?
2. **Sentence weight**: does every sentence carry, instance,
   bound, or repeat the thesis?
3. **Repetition rule**: is the thesis echoed (good) while
   ambient repetition is cut (good)?

Combine sentence-level slop score with document-economy score.
Both must pass. See `modules/document-economy.md` for the full
rubric, the reader-time budget table, and a worked example.

## Step 7: Hallucination & Stub Sweep

Load: `@modules/hallucination-detection.md` and
`@modules/stub-and-deferral.md`.

**Hallucination is not slop: it is wrongness with
confident phrasing. Always P0.**

Scan for:

1. **Phantom code references**: every backticked
   identifier, function name, or file path in prose must
   exist in the codebase.
2. **Phantom dependencies**: every recommended `pip
   install` / `cargo install` / `npm install` must
   resolve on the relevant registry (slopsquatting
   defense).
3. **Dead URLs**: every cited URL should return 200.
4. **Made-up config keys**: every config key in docs must
   be read by the code.
5. **Bare TODO/FIXME**: requires either a tracked-issue
   link or deletion.
6. **Hedging language** ("for now", "should work",
   "placeholder", "dummy"): each one is deferred work.
7. **Stub constructs** (`todo!()`, `unimplemented!()`,
   `NotImplementedError`): defects in any path reachable
   from a public API.

See modules for detection commands and severity matrix.

## Step 8: Evidence-Backed Claims (READMEs and public docs)

Load: `@modules/evidence-backed-claims.md`

**Every quality claim must point to evidence in the same
repository. No evidence, delete the claim.**

For each claim of "production-ready", "fast", "memory-
safe", "scalable", etc., verify the corresponding
evidence (CI workflow, benchmark directory, audit
markers, etc.) actually exists. The module contains the
full claim → required-evidence table and language-
specific detection commands.

This step is highest-leverage for crate/library/project
READMEs, where feature-list buzzword soup is the most
common AI-generated failure mode.

## Step 9: Apply Anti-Goals (safety check)

Load: `@modules/anti-goals.md`

**Aggressive de-slopping has its own failure modes.**

Before applying any fix surfaced by the prior steps,
verify it does not violate the anti-goals:

1. Do not strip safety comments (`// SAFETY:`,
   `// INVARIANT:`, etc.) on `unsafe`, locked, or
   contract-bearing code.
2. Do not collapse public error variants without an
   explicit major-version-bump decision.
3. Do not "simplify" typed errors to boxed/dynamic
   errors.
4. Do not inline a function that has a domain-specific
   name even if it is short.
5. Do not touch generated code, vendored code, or
   historical changelog entries.
6. Do not auto-apply `confidence: low` findings —
   surface them for human decision.

When in doubt: leave the match flagged, do not delete.

## The full multi-pass cleanup workflow

For systematic project-wide cleanup, run the multi-pass
workflow in order. See `@modules/cleanup-workflow.md` for
the full ten-pass methodology and the rationale for the
ordering. Summary:

| Pass | Focus |
|---|---|
| 0 | Pre-slop sweep: secrets, agent configs |
| 1 | Surface lint floor (formatter and linter) |
| 2 | Hallucination & stubs (modules: hallucination, stub-and-deferral) |
| 3 | Identity & voice leaks |
| 4 | Comment slop (translation, marketing, banner, deferral) |
| 5 | Prose slop (vocabulary, structural, document-economy, and evidence-backed-claims) |
| 6 | Code idiom (delegate to language-specific plugins) |
| 7 | Architecture (judgment-heavy; see anti-goals) |
| 8 | Tests (tautology, mocks, snapshots) |
| 9 | README & public docs |
| 10 | Establish guardrails (CI, lints, constitution) |

**Cardinal rules**: one pass per commit; deletion beats
rewriting; do not silently apply low-confidence fixes;
stop when a pass finds nothing.

## Empirical baseline (cite when justifying severity)

Load: `@modules/empirical-baseline.md` for the 2025-Q1
2026 research baseline that justifies the severity
weighting. Headline numbers:

- AI PRs ship 1.7x more total issues, 1.75x more
  logic/correctness issues, 2.74x more XSS, ~8x more
  excessive I/O than human-only PRs (CodeRabbit, Dec 2025).
- 92-96% of detected AI-code issues are maintainability
  ("code smell"), not correctness (Sonar, Q4 2025).
- Model-specific patterns: GPT fabricates; Claude omits.
  Calibrate the audit accordingly.

When a finding's severity is challenged in review, cite
from this module rather than asserting from authority.

## Step 10: Generate Report

For per-finding output that reviewers can accept or reject
independently, use the canonical structured format defined
in `@modules/structured-finding-output.md`. Each finding
carries `file`, `line`, `category`, `severity`,
`confidence`, `evidence`, `rationale`, `fix`, and (for
high-confidence) `diff`. Auto-apply policy is set by
confidence; never auto-apply `confidence: low`.

Summary report format (human-readable):

```markdown
## Slop Detection Report: [filename]

**Overall Score**: X.X / 10 (Rating)
**Word Count**: N words
**Markers Found**: N total

### CRITICAL (P0, must resolve before merge)
- Line 8: "As a large language model". IDENTITY LEAK
- Line 47: References `Client.connect_with_timeout(...)` —
  HALLUCINATION (method does not exist; closest match is
  `Client.connect`)
- Line 102: "production-ready" claim with no CI workflow
 . UNVERIFIED CLAIM

### High-Confidence Markers (vocabulary)
- Line 23: "delve into" -> consider: "explore"
- Line 45: "rich tapestry" -> consider: "variety"

### Structural Issues
- Em dash density: 8/1000 words (HIGH)
- Bullet ratio: 72% (ELEVATED)
- Sentence length SD: 3.2 words (LOW VARIANCE)

### Phrase Patterns
- Line 12: "In today's fast-paced world" (vapid opener)
- Line 89: "cannot be overstated" (empty emphasis)
- Line 134: "Let's dive into" (self-narration of structure)

### Tier 5 / 2026 Patterns
- Line 19: "The skill lives in `plugins/scribe/`" → "is in"
  (spatial copula, inanimate subject)
- Line 27: "hooks + skills" → "hooks and skills" (plus-sign
  conjunction in prose)
- Line 34: "It's not a tool, it's a transformation" →
  rewrite positively (negative parallelism / contrastive
  negation)
- Line 38: "Less config, more code" → state plainly
  (contrastive parallelism; keep only if load-bearing)
- Line 56: "Here's the thing," → delete (throat-clearing
  opener)
- Line 78: "Focused. Aligned. Measurable." → "Focused,
  aligned, and measurable." (three-fragment burst)
- Line 91: 3 smart quotes outside code blocks (Word-processor
  paste signature)

### Stub & Deferral
- Line 56: bare `// TODO: handle expired tokens` (no
  tracked issue link)
- Line 71: "for now, we recommend" (deferral language)

### Document Economy Score: X / 6
- Thesis-first: 1/2 (thesis present but buried in para 3)
- Sentence weight: 1/2 (~65% of sentences earn weight)
- Repetition: 2/2 (thesis echoed; ambient repetition cut)

### Recommendations
1. **CRITICAL**: delete line 8 identity leak before merge
2. **CRITICAL**: replace `Client.connect_with_timeout`
   with `Client.connect(opts)` and update example
3. **CRITICAL**: either add CI + version >= 1.0 to back
   "production-ready", or delete the claim
4. Replace [specific word] with [alternative]
5. Convert bullet list at line 34-56 to prose
6. Hoist the thesis (line 47) into the lead paragraph
7. Link bare TODOs to tracked issues or delete code path

### Confidence-low findings (require human decision)
- Line 89: bullet count of 8 may be appropriate for this
  enumeration; do not auto-flatten
- Line 156: `Manager` suffix may be domain-meaningful;
  verify before renaming
```

Per `anti-goals.md`: surface `confidence: low` findings
in a separate section. Do not silently apply them.

## Module Reference

- See `modules/fiction-patterns.md` for narrative-specific slop markers
- See `modules/remediation-strategies.md` for fix recommendations

## Integration with Remediation

After detection, invoke `Skill(scribe:doc-generator)` with
the `--remediate` flag to apply fixes, or manually edit using
the report as a guide.

## Exit Criteria

- All target files scanned
- Density scores calculated
- Report generated with specific, line-anchored fixes
- High-severity items flagged for immediate attention
