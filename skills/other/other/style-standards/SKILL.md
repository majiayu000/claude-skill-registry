---
name: style-standards
type: standard
depth: extended
description: >-
    Enforces LLM-optimized style compliance for documentation and code. Use when creating/modifying markdown (headers, lists, Dictums, separators), code
    organization (comments, dividers, naming), or validating voice (grammar, tone, imperative phrasing) and formatting against taxonomy/whitespace standards.
---

# [H1][STYLE-STANDARDS]
>**Dictum:** *Style consistency maximizes agent comprehension.*

<br>

Govern file creation and modification in monorepo.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation
2. Read [keywords.md](./references/keywords.md) — Canonical keyword list; all Markers use official terms
3. (taxonomy) Read [taxonomy.md](./references/taxonomy.md) — Lexicon, references, stati definitions
4. (voice) Read [voice.md](./references/voice.md) — Grammar, ordering, comments, constraints, naming, density
5. (formatting) Read [formatting.md](./references/formatting.md) — Structure, typeset, spacing, examples
6. Apply standards — Implement per domain Guidance and Best-Practices
7. Validate — Quality gate; see §VALIDATION

**Scope:**
- *Documentation:* Markdown structure, headers, lists, tables, Dictums, separators.
- *Code:* Comments, headers, section dividers, naming conventions, file organization.

**Domain Navigation:**
- *[TAXONOMY]* — Terms, markers, cross-references. Load for: sigils, stati, lexicon definitions.
- *[VOICE]* — Tone, grammar, comments, naming. Load for: imperative phrasing, headers, code naming.
- *[FORMATTING]* — Layout, separators, spacing. Load for: header structure, dividers, whitespace rules.

[REFERENCE]: [index.md](./index.md) — Reference file listing

---
## [1][TAXONOMY]
>**Dictum:** *Vocabulary anchors structure; Markers encode state.*

<br>

Signals intent for agent execution. Leverage terms for document traversal.

**Guidance:**<br>
- `Dictum` - Read `Dictum` + headers first—rapid file mapping.
- `Qualifier` - [ALWAYS] respect inline directives when encountered.
- `Preamble` - Signals **section-wide** imperative.
- `Terminus` - Signals **task-specific** imperative; **isolated** effect.
- `Corpus` - Read after `Preamble`/`Terminus` orientation.
- `Gate` - [CRITICAL] Finalize checklist items prior to proceeding; use `[VERIFY]` for `Gate` checklists.
- `Directive` - Lists require strict adherence; polarity set by `Modifier`.
- `Stati` - Replace emoji.

**Best-Practices:**<br>
- **Markers:** Hard limit: **10 per file**. Strategic placement maximizes compliance.
  - *Preamble/Terminus* - 0–4 markers per file maximum.

[REFERENCE]: [→taxonomy.md](./references/taxonomy.md) — Lexicon, references, stati

---
## [2][VOICE]
>**Dictum:** *Universal standards for LLM-optimized context, documentation, and agentic instructions.*

<br>

Applies to documentation and comments. Scope: tone, list semantics, ordering primacy, grammar, syntax, modals, visuals, comment standards, keywords.

**Guidance:**<br>
- `Voice` - Active voice: 56% token reduction.
- `Tone` - Mechanical, domain-specific. No hedging, no self-reference.
- `Syntax` - Simple sentences: 93.7% accuracy vs 46.8% nested.
- `Punctuation` - Attention sinks—absorb 20-40% weight despite minimal semantic content.
- `Ordering` - [CRITICAL] Primacy effects peak at 150-200 instructions; 5.79× attention for early items.
  - **Critical-First** - Highest-priority constraints at sequence start.
  - **Middle Burial** - Middle positions suffer U-shaped attention loss.
- `Comments` - Front-load architectural decisions where attention peaks.
- `Density` - Tables: >2 entities, >2 dimensions. Diagrams: >3 steps or >2 hierarchy levels.

**Best-Practices:**<br>
- **Comments** - Incorrect: 78% accuracy loss—omit if uncertain. *Why > What*: intent = signal, logic = noise.
- **Constraints** - 6+ simultaneous: <25% satisfaction. Max 3-5 per level.
- **Delimiters** - Consistency over choice. 18-29% variance per change.
- **Stopwords** - Remove `the`, `a`, `an`, `please`, `kindly`.
- **Tone** - Actions: imperative. Context/facts: declarative.
- **Naming** - Prohibited: `utils`, `helpers`, `misc`, `config`, `cfg`, `opts`, `params`, `Data`, `Info`, `Manager`, `Service`.

[REFERENCE]: [→voice.md](./references/voice.md) — Grammar, ordering, comments, constraints, naming, density

---
## [3][FORMATTING]
>**Dictum:** *Whitespace and separator rules for document structure.*

<br>

Separators encode hierarchy. Whitespace: semantic, not cosmetic. Patterns enable rapid reference.

**Guidance:**<br>
- `Dictum` - Place first after H1/H2. State WHY, not WHAT. Format: `>**Dictum:** *statement*`
- `Depth` - H1: File Truth. H2: Smallest agent read unit. H3: Nesting limit. [CRITICAL] H4+ requires new file.
- `Lists` - Use numbered `1.` for sequence/priority. Use bullet `-` for equivalence/sets.
- `Labels` - Format parent: `**Bold:**` with colon. Format child: `*Italic:*` for contrast.
- `Separators` - Use `---` for hard boundaries (H2 → H2, H3 → H3). Use `<br>` for soft transitions (H2 → H3).
- `Spacing` - Place 1 blank after header. Place none after `---`. Place none between list items.
- `Dividers` - Pad code separators `// --- [LABEL] ---` to column 80.
- `Tables` - Include `[INDEX]` first column. Format headers as `[HEADER]` sigil. Align: center index, right numeric, left prose.

**Best-Practices:**<br>
- **Separator Prohibitions** - `---` between H2 and first H3 prohibited. `<br>` between sibling H3s prohibited.
- **List Prohibitions** - Single-item lists prohibited—use prose. Bullet `-` only; `*`/`+` prohibited. Parallel grammar required.
- **Header Integrity** - Level skipping prohibited. H1 → H2 → H3 strictly sequential.
- **Thresholds** - Lists: 2-7 items. Items: <100 chars. Nesting: 2 levels max.
- **Sigils** - UPPERCASE, max 3 words, underscores for compound. Exception: `.claude/` infrastructure (skills, commands, agents) use hyphens matching file/folder name.
- **Soft Breaks** - `<br>` required after Dictum and Preamble. Groups 2-3 related definitions inline.
- **Case Taxonomy** - UPPERCASE: sigils, rubrics, keywords, section labels. Title Case: table cells. kebab-case: files.
- **Directive Ordering** - `[IMPORTANT]:` precedes `[CRITICAL]:`. Within list: `[ALWAYS]` precedes `[NEVER]`.
- **Table Styling** - First column bold for category anchoring.

[REFERENCE]: [→formatting.md](./references/formatting.md) — Structure, typeset, spacing, example

---
## [4][VALIDATION]
>**Dictum:** *Gates prevent non-compliant output.*

<br>

[VERIFY] Completion:
- [ ] Structure: Nesting ≤H3, critical constraints at sequence start.
- [ ] Voice: Active voice, no stopwords, no hedging, no self-reference.
- [ ] Formatting: Separators correct, spacing rules applied.
- [ ] Consistency: All markers use canonical keywords.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md)
