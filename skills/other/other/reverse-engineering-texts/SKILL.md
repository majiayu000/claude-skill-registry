---
name: reverse-engineering-texts
description: Reverse-engineer texts into a reusable structural blueprint (reverse outlining, argument mining, copy teardown). Use when the user asks to analyze a text’s thesis, hook, framework (AIDA/PAS/PASTOR/BAB), argument map, rhetoric (Ethos/Pathos/Logos), or when they want to convert “text → structure/blueprint” to reuse patterns in writing, specs, prompts, or marketing.
---

# Reverse-Engineering Texts

## Goal
Turn a finished text into a **TeardownBlueprint** (a “drawing”) that is reusable: structure, argument moves, and rhetorical patterning.

## Core disciplines (FPF-aligned)
- **Strict distinction**: TextArtifact (the text) ≠ Blueprint (your description) ≠ Output (new draft/prompt).
- **Evidence first**: Every non-trivial claim in the blueprint must include a short **quote** from the text (an “evidence anchor”).
- **Parsimony**: Prefer the simplest structure/framework that explains the whole text.
- **Uncertainty**: Mark low-confidence inferences explicitly.

## What “SOTA” means here
This skill is not just “label AIDA and call it done”. State-of-the-art reverse-engineering requires:
- **Paradigm transparency**: explicitly declare the interpretive lens used (and what would count as an “error” vs a paradigm clash).
- **Meaning-in-interaction**: meaning is extracted in a dynamic local context, not “derived from rules given from above”.
- **Ambiguity handling**: do not force-collapse; maintain multiple plausible interpretations when needed.
- **Order effects awareness**: sometimes A→B ≠ B→A; record when the analysis is non-commutative.

## Method layering
- **Core (default)**: fast, evidence-anchored teardown usable for most texts.
- **Advanced (SOTA extensions)**: modes, context-first grounding, ambiguity protocol, validation, non-commutativity, conflict taxonomy.

## Quick workflow (text → blueprint)

### 0) Context-first (always)
1. **ContextCapture**: Record what you know (or must assume): `audience`, `intent`, `setting`, `speaker_role`, `genre`, `stakes`.
2. **TermGrounding**: Pick 5–10 key terms/entities in the text and define their **meaning-in-context** with quotes.
3. **ParadigmDeclaration**: Declare the lens you will use (at minimum: `descriptive_structural`; optionally: `pragmatic`, `hermeneutic`, `classical_epistemology`, etc.). Also declare what counts as:
   - **intra-paradigm error** (a contradiction/failure inside the chosen lens)
   - **inter-paradigm conflict** (a clash between lenses; not automatically an “error”)

### 1) Core teardown (default)
4. **Ingest**: Copy the raw text verbatim as `TextArtifact`.
5. **Segment**: Split into semantic blocks; name each block with a one-line intent.
6. **Spine**: Infer the thesis and macro-structure (framework hypothesis).
   - Also mark `descriptive_vs_normative`: is the thesis describing reality, prescribing norms, or mixed?
7. **Hook**: Classify the hook type + target emotion.
8. **Argument map**: For each block, extract Claim + Support/Evidence type + relation to previous block.
   - Also mark `descriptive_vs_normative` per segment when relevant.
9. **Rhetoric**: Map Ethos/Pathos/Logos and where each is used.
10. **Pattern extraction**: Capture reusable micro-patterns (openings, transitions, proof moves).
11. **Reconstruct forward outline**: Produce a forward scaffold (thesis → hook → outline → arguments).
12. **Audit**: Ensure coverage + evidence anchors + note alternatives when ambiguous.

### 2) Advanced (SOTA extensions)
Use these when the situation calls for it. “Optional” here does NOT mean “skip”: each has triggers.

#### Modes (pick one; record in output)
- **ModeA_Immanent**: analyze internal logic/structure only (no outside sources).
- **ModeB_Transcendent**: validate/criticize using external sources (when available).
- **ModeC_Hybrid**: run A then B (or B then A) and integrate.

#### Ambiguity protocol (conditional-mandatory)
1. **AmbiguityCheck (always)**: is there >=2 plausible interpretations of key elements (thesis/intent/referents/causality/value-laden terms)?
2. If yes → **ModeD_AmbiguityModel (mandatory)**:
   - produce an `interpretation_set` (>=2 interpretations)
   - each interpretation must have evidence anchors (quotes)
   - provide “collapse conditions”: which context/goal/paradigm would prefer which interpretation
   - if you choose a single “best” interpretation, record why and what you lose

#### External validation (ModeB/ModeC)
- Use >=3 independent sources when feasible; if not feasible, state constraints explicitly.
- Output: agreements, disagreements, and how they affect the blueprint confidence.

#### Non-commutativity (when order might matter)
- Run a lightweight A→B and B→A comparison on 1–2 key segments.
- If results differ, record `non_commutativity.detected: true` and summarize the divergence (contextual priming / lens effects).

#### Conflict taxonomy (always when conflicts appear)
- **intra_paradigm**: critical | significant | minor
- **inter_paradigm**: paradigm conflict (not an error; requires boundary clarification)

## Output contract
You MUST produce outputs in **two phases**:

### Mandatory execution order (hard requirement)
1. Read `references/index.md` (agent entrypoint)  
2. Select mode → `references/mode-selection.md`  
3. Read the matching template file (choose exactly one):
   - `references/teardownblueprint-v2-modeA-immanent.md`
   - `references/teardownblueprint-v2-modeB-transcendent.md`
   - `references/teardownblueprint-v2-modeC-hybrid.md`
4. Fill the template completely (do not invent new fields; keep schema)  
5. Check gates → `references/quality-gates.md`  
6. Only then (optionally) label frameworks → `references/framework-markers.md`
7. Only if you need a pattern, read one concrete example file:
   - `references/modeA-mini.md`
   - `references/modeA-scientific-mini.md`
   - `references/modeC-philosophical-ambiguity.md`

### Template availability check (hard requirement)
Do NOT claim “templates are unavailable” unless you attempted to locate and read:
- `references/index.md`
- at least one concrete template file (the mode-matching one if possible):
  - `references/teardownblueprint-v2-modeA-immanent.md`
  - `references/teardownblueprint-v2-modeB-transcendent.md`
  - `references/teardownblueprint-v2-modeC-hybrid.md`

### Deliverables
#### Deliverable A (mandatory, always): TeardownBlueprint
Produce a `TeardownBlueprint` **in the exact YAML shape** of the matching template in `references/` (one of the `teardownblueprint-v2-*.md` files).

#### Deliverable B (mandatory when user asks for a human-readable report/summary): HumanReadableReport
If the user asks for a “human-readable report/summary”, you MUST still output Deliverable A first,
then derive Deliverable B strictly from the completed blueprint.

**HumanReadableReport rules:**
- It is a reformulation of the blueprint, not a replacement for it.
- Every major claim must be traceable to either:
  - a quote inside `TeardownBlueprint` (`thesis.evidence`, `segments[*].evidence`, `rhetoric_summary.*`, etc.), OR
  - an explicit “new inference” line marked `confidence: low` (and you must explain what is missing).
- Do not add new requirements/claims that are absent from the blueprint unless explicitly marked as above.

### Minimum QA checklist
- [ ] Every major block is represented in `segments`.
- [ ] Thesis and framework claims include quotes.
- [ ] Each argument block has (claim, evidence_type, relation) + quote(s).
- [ ] At least one reusable pattern is extracted.
- [ ] Any guesswork is labeled with `confidence: low` and an alternative hypothesis is listed.

### SOTA QA checklist (recommended)
- [ ] `context` is captured (or assumptions are explicit).
- [ ] `term_grounding` exists for key terms and is quote-backed.
- [ ] `paradigm` and `mode` are explicit.
- [ ] `descriptive_vs_normative` is labeled for thesis (and segments when relevant).
- [ ] `AmbiguityCheck` is present; if triggered, `interpretation_set` is present and quote-backed.
- [ ] If external validation is claimed (ModeB/ModeC), sources and disagreement handling are documented.
- [ ] If non-commutativity is claimed, the A→B vs B→A delta is recorded.

## Acceptance criteria (definition of done)

### Core acceptance (must pass)
- **Coverage**: every semantic block in the text has a corresponding `segments[*]` entry.
- **Traceability**: thesis/framework/each segment claim has >=1 quote.
- **Parsimony**: framework label is the simplest that fits; otherwise `other`.
- **Uncertainty hygiene**: any inferred-but-not-anchored statement is marked `confidence: low` and paired with an alternative hypothesis.

### Dual-output compliance (must pass when user asks for report/summary)
- **Two-phase output**: Deliverable A (TeardownBlueprint) is present and completed, and Deliverable B is derived from it.
- **Report mapping**: each major section of the HumanReadableReport maps to one or more `segments[*].id` (explicitly or implicitly),
  and no segment-level claim appears in the report without a corresponding `segments[*]` entry.
- **No-new-claims**: the report introduces no new claims beyond the blueprint unless marked as `confidence: low` + missing evidence explained.

### Advanced acceptance (when the feature is triggered/used)
- **Context-first**: `context` is explicit; if not provided, assumptions are explicit and confidence is lowered.
- **Meaning grounding**: `term_grounding` exists for key/value terms; no “dictionary-from-above” substitutions without quotes.
- **Ambiguity**:
  - `ambiguity.check.detected=false` OR
  - `ambiguity.check.detected=true` AND `ambiguity.interpretation_set` has >=2 interpretations, each quote-backed, each with `applies_when`.
- **Validation** (ModeB/ModeC): include sources, and record how disagreements change confidence.
- **Non-commutativity** (if tested): record both orders and a concrete delta summary.
- **Conflicts**: classify as intra vs inter paradigm; do not “resolve” an inter-paradigm conflict as if it were an error.

## Next actions (optional)
- Generate a new draft *from the blueprint* (structure-first).
- Build a personal `PatternLibrary` (swipe/teardown file) from repeated blueprints.

## Additional resources
- Agent entrypoint: [references/index.md](references/index.md)
- Mode selection: [references/mode-selection.md](references/mode-selection.md)
- Quality gates: [references/quality-gates.md](references/quality-gates.md)
- Templates:
  - `references/teardownblueprint-v2-modeA-immanent.md`
  - `references/teardownblueprint-v2-modeB-transcendent.md`
  - `references/teardownblueprint-v2-modeC-hybrid.md`
- Examples:
  - `references/modeA-mini.md`
  - `references/modeA-scientific-mini.md`
  - `references/modeC-philosophical-ambiguity.md`
- Framework markers: [references/framework-markers.md](references/framework-markers.md)
