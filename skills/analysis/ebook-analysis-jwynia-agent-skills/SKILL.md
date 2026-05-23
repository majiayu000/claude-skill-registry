---
name: ebook-analysis
description: Parse ebooks, extract concepts and entities with citation traceability, classify by type/layer, and synthesize across book collections.
license: MIT
metadata:
  author: jwynia
  version: "2.1"
  domain: research
  cluster: media-meta-analysis
  type: orchestrator
  mode: diagnostic+generative
  maturity: working
  maturity_score: 14
---

# Ebook Analysis: Non-Fiction Knowledge Extraction

You analyze ebooks to extract knowledge with full citation traceability. This skill supports two complementary extraction modes:

1. **Concept Extraction** - Extract ideas classified by abstraction (principle → tactic)
2. **Entity Extraction** - Extract named things (studies, researchers, frameworks, anecdotes) that persist across books

## Core Principle

**Every extraction must be traceable to its exact source.** Citation traceability is non-negotiable. Extract less with full provenance rather than more without it.

---

## Two Extraction Modes

### Mode 1: Concept Extraction
For extracting IDEAS organized by abstraction level.

**Use when:** Analyzing a book for transferable ideas, building a concept taxonomy, understanding how abstract principles relate to concrete tactics.

**Output:** JSON files (analysis.json, concepts.json)

**Example:** "Spaced repetition improves retention" is a MECHANISM at Layer 2.

### Mode 2: Entity Extraction
For extracting NAMED THINGS that can be cross-referenced across books.

**Use when:** Building a knowledge base where the same study, researcher, or framework appears in multiple books. The goal is entity resolution—recognizing that "Hogarth's framework" in Range is the same as "kind/wicked environments" mentioned elsewhere.

**Output:** Markdown files in knowledge base structure

**Example:** "Kind vs Wicked Environments" is a FRAMEWORK by Robin Hogarth.

### Choosing a Mode

| If you want to... | Use Mode |
|-------------------|----------|
| Understand a book's argument structure | Concept Extraction |
| Build a reference library across books | Entity Extraction |
| Create actionable takeaways | Concept Extraction |
| Track what researchers say across sources | Entity Extraction |
| Both | Run both modes sequentially |

---

## Entity Extraction Mode (Detailed)

### Entity Types

| Type | What It Captures | Example |
|------|------------------|---------|
| **study** | Research findings, experiments, data | Flynn Effect, Marshmallow Test |
| **researcher** | People and their contributions | Anders Ericsson, Robin Hogarth |
| **framework** | Mental models, taxonomies, systems | Kind vs Wicked, Desirable Difficulties |
| **anecdote** | Stories used to illustrate points | Tiger vs Roger, Challenger Disaster |
| **concept** | Ideas that aren't frameworks | Cognitive entrenchment, Match quality |

### Extended Entity Type Guidance

Some entities don't fit cleanly into the five types. Guidelines:

| Entity Kind | Use Type | Rationale |
|-------------|----------|-----------|
| **Simulations/Games** (Superstruct, EVOKE) | anecdote | Illustrative events, even if hypothetical |
| **Institutions** (IFTF, WEF) | researcher | Organizations contribute ideas like individuals |
| **Historical events** (Challenger disaster) | anecdote | Stories that illustrate principles |
| **Hypothetical scenarios** | anecdote | Future scenarios from books like Imaginable |
| **Thought experiments** | framework | If systematic; otherwise concept |

**When uncertain:** Default to `anecdote` for narratives/events, `concept` for ideas, `framework` for systematic methods.

### Author-as-Subject Pattern

When the book's author is also a significant entity (e.g., Jane McGonigal in Imaginable):

**Create a researcher entity if:**
- Author has notable prior work or institutional affiliation
- Author appears in Wikipedia or other reference sources
- Author's background/credentials are relevant to understanding the book
- Other books in your collection might reference them

**Skip if:**
- Author is primarily known only for this book
- No external sources to verify/enrich the entity

**Template addition for author-subjects:**
```markdown
## Note
This researcher is the author of [Book] in our collection. Their frameworks and concepts are documented separately.
```

### Entity File Template

```markdown
# [Entity Name]
**Type:** study | researcher | framework | anecdote | concept
**Status:** stub | partial | solid | authoritative
**Last Updated:** YYYY-MM-DD
**Aliases:** alias1, alias2, alias3

## Summary
[2-3 sentence synthesized understanding]

## Key Findings / What It Illustrates
1. [Claim or finding with source]
   — Source: [Book], Ch.[X]

2. [Another claim]
   — Source: [Book], Ch.[X]

## Key Quotes
> "Quotable text here."

> "Another memorable quote."

## Sources in Collection
| Book | Author | How It's Used | Citation |
|------|--------|---------------|----------|
| Range | Epstein | [Role in book] | Ch.X |

## Sources NOT in Collection
- [Book that would enrich this entity]

## Related Entities
- [Other Entity](../type/other-entity.md) - Relationship description

## Open Questions
- [What we don't yet know]
```

### Knowledge Base Structure

```
/knowledge/
├── _index.md                    # Master registry
├── _entities.json               # Searchable index (generated)
│
├── nonfiction/
│   ├── _index.md                # Domain index
│   ├── _[book]-quotes.md        # Book-specific quotes file
│   ├── studies/
│   │   ├── flynn-effect.md
│   │   └── chase-simon-chunking.md
│   ├── researchers/
│   │   ├── hogarth-robin.md
│   │   └── tetlock-philip.md
│   ├── frameworks/
│   │   ├── kind-vs-wicked-environments.md
│   │   └── desirable-difficulties.md
│   ├── anecdotes/
│   │   ├── tiger-vs-roger.md
│   │   └── challenger-disaster.md
│   └── concepts/
│       ├── cognitive-entrenchment.md
│       └── match-quality.md
│
├── cooking/                     # Domain-specific structure
│   ├── techniques/
│   ├── ingredients/
│   └── equipment/
│
└── technical/
    ├── patterns/
    └── technologies/
```

### Quotes Extraction

Quotable quotes are a distinct extraction type. For each book, create a quotes file:

**File:** `_[book-slug]-quotes.md`

**Structure:**
```markdown
# Quotable Quotes from [Book Title]
**Author:** [Author]
**Last Updated:** YYYY-MM-DD

## On [Theme 1]
> "Quote text here."

> "Another quote on same theme."

## On [Theme 2]
> "Quote on different theme."
```

**What makes a good quote:**
- Memorable phrasing that captures a key insight
- Self-contained (understandable without context)
- Surprising or counterintuitive formulation
- Useful for presentations, writing, or reference

### Entity Extraction Workflow

1. **Scan book** - Read through identifying named studies, researchers, frameworks, illustrative stories
2. **Check existing entities** - Use `kb-resolve-entity.ts` to see if entity already exists
3. **Create or update** - New entity → create file; existing → add as source
4. **Add quotes** - Extract memorable quotes to quotes file
5. **Cross-link** - Add Related Entities sections
6. **Regenerate index** - Run `kb-generate-index.ts`

### Entity Extraction States (KB0-KB5)

| State | Symptoms | Intervention |
|-------|----------|--------------|
| **KB0** | No knowledge base | Create directory structure |
| **KB1** | Structure exists, no entities | Begin extraction |
| **KB2** | Extracting from book | Create entity files |
| **KB3** | Entities created, not linked | Add Related Entities |
| **KB4** | Linked, no index | Run kb-generate-index.ts |
| **KB5** | Complete for this book | Proceed to next book |

### Cross-Book Synthesis Workflow

**Triggered when:** 2+ books have been extracted to the knowledge base.

**Goals:**
1. Find entities that appear in multiple books
2. Identify conceptual connections between books
3. Surface contradictions or complementary perspectives
4. Update entity files with multi-source synthesis

**Process:**

1. **Entity overlap detection**
   ```bash
   # Find entities with 2+ sources
   grep -l "Sources in Collection" knowledge/nonfiction/**/*.md | \
     xargs grep -l "| .* | .* |" | head -20
   ```
   Or manually review entities updated with new source.

2. **Conceptual connection mapping**
   - Compare frameworks across books (e.g., Range's "wicked environments" ↔ Imaginable's "futures thinking")
   - Identify shared researchers (e.g., Tetlock appears in both Range and Imaginable)
   - Look for complementary themes (prediction failure → preparation despite uncertainty)

3. **Synthesis documentation**
   For entities appearing in 2+ books, update the Summary section:
   ```markdown
   ## Summary
   [Synthesized understanding from BOTH sources, noting agreements and differences]
   ```

4. **Cross-book insights**
   Document thematic connections in `context/insights/cross-book-{theme}.md`:
   ```markdown
   # Cross-Book Insight: [Theme]

   ## Books Contributing
   - Range (Epstein) - [perspective]
   - Imaginable (McGonigal) - [perspective]

   ## Synthesis
   [How the books complement or contradict each other]
   ```

---

## Concept Extraction Mode (Detailed)

### Concept Types (Abstract → Concrete)

| Type | Definition | Example |
|------|------------|---------|
| **Principle** | Foundational truth or axiom | "Communities form around shared identity" |
| **Mechanism** | How something works | "Reciprocity creates social bonds" |
| **Pattern** | Recurring structure or approach | "The community lifecycle pattern" |
| **Strategy** | High-level approach to achieve goals | "Build trust before asking for contribution" |
| **Tactic** | Specific actionable technique | "Send welcome emails within 24 hours" |

### Abstraction Layers

| Layer | Name | Abstraction | Example |
|-------|------|-------------|---------|
| 0 | Foundational | Universal principles | "Humans seek belonging" |
| 1 | Theoretical | Domain-specific theory | "Community requires shared purpose" |
| 2 | Strategic | Approaches and frameworks | "The funnel model of engagement" |
| 3 | Tactical | Specific methods | "Onboarding sequences" |
| 4 | Specific | Concrete implementations | "Use Discourse for forums" |

### Relationship Types

| Relationship | Meaning | When to Use |
|--------------|---------|-------------|
| **INFLUENCES** | A affects B | Causal or correlational connection |
| **SUPPORTS** | A provides evidence for B | Citation, example, validation |
| **CONTRADICTS** | A conflicts with B | Opposing claims |
| **COMPOSED_OF** | A contains B | Part-whole relationships |
| **DERIVES_FROM** | A is derived from B | Logical conclusions |

### Concept Extraction States (EA0-EA7)

| State | Symptoms | Intervention |
|-------|----------|--------------|
| **EA0** | No input file | Guide file preparation |
| **EA1** | Raw file, not parsed | Run ea-parse.ts |
| **EA2** | Parsed, not extracted | LLM extracts concepts |
| **EA3** | Extracted, not classified | Assign types and layers |
| **EA4** | Classified, not annotated | Add themes, relationships |
| **EA5** | Single book complete | Export or proceed to synthesis |
| **EA6** | Multi-book ready | Cross-book synthesis |
| **EA7** | Analysis complete | Generate reports |

### Concept Extraction Workflow

1. **Parse** - Run `ea-parse.ts` to chunk book with position tracking
2. **Extract** - Present chunks to LLM for concept identification with exact quotes
3. **Classify** - Assign type (principle→tactic) and layer (0-4)
4. **Annotate** - Add themes and functional analysis
5. **Link** - Connect related concepts
6. **Export** - Generate analysis.json, concepts.json, report.md

---

## Available Tools

### Parsing Tools

#### ea-parse.ts
Parse ebook files into chunks with metadata and position tracking.

```bash
deno run --allow-read scripts/ea-parse.ts path/to/book.txt
deno run --allow-read scripts/ea-parse.ts path/to/book.epub --format epub
deno run --allow-read scripts/ea-parse.ts book.txt --chunk-size 1500 --overlap 150
```

**Output:** JSON with metadata, chapters (if detected), and chunks with positions.

### Knowledge Base Tools

#### kb-generate-index.ts
Scan knowledge base and generate searchable entity index.

```bash
deno run --allow-read --allow-write scripts/kb-generate-index.ts /path/to/knowledge
```

**Output:** Creates `_entities.json` with all entities, aliases, and metadata.

#### kb-resolve-entity.ts
Search for existing entities before creating duplicates.

```bash
deno run --allow-read scripts/kb-resolve-entity.ts "Flynn Effect"
deno run --allow-read scripts/kb-resolve-entity.ts "Hogarth" --threshold 0.5
deno run --allow-read scripts/kb-resolve-entity.ts "kind learning" --json
```

**Options:**
- `--threshold <0-1>` - Minimum match score (default: 0.3)
- `--limit <n>` - Maximum results (default: 5)
- `--json` - Output as JSON

### Validation Tools

#### ea-validate.ts
Validate analysis output for citation accuracy and schema completeness.

```bash
deno run --allow-read scripts/ea-validate.ts analysis.json --report
```

---

## Anti-Patterns

### The Extraction Flood
**Pattern:** Extracting every potentially interesting phrase.
**Fix:** Ask "Would I cite this?" before extracting. Quality over quantity.

### The Citation Black Hole
**Pattern:** Extracting without preserving exact quotes or positions.
**Fix:** Always capture: exact quote, chapter reference, context.

### The Duplicate Entity
**Pattern:** Creating new entity without checking if it exists.
**Fix:** Always run `kb-resolve-entity.ts` first.

### The Orphan Entity
**Pattern:** Entities without Related Entities links.
**Fix:** Every entity should connect to at least 2 others.

### The Quote-Free Entity
**Pattern:** Entity captures ideas but no memorable phrasing.
**Fix:** Include Key Quotes section with author's exact words.

### The Single-Book Silo
**Pattern:** Analyzing books without cross-referencing.
**Fix:** After 2+ books, run synthesis to find connections.

---

## Example Workflows

### Full Entity Extraction (Range Example)

```
1. Scan book chapter by chapter
2. Identify all named studies, researchers, frameworks, anecdotes
3. Create inventory document listing all potential entities
4. For each entity:
   a. kb-resolve-entity.ts "[entity name]" to check existence
   b. Create markdown file in appropriate type directory
   c. Fill in template with findings and citations
   d. Add Key Quotes section
5. Create _range-quotes.md with all memorable quotes
6. Update _index.md with new entities
7. kb-generate-index.ts to rebuild _entities.json
```

### Quick Concept Scan

```
1. ea-parse.ts book.txt --chunk-size 2000
2. For each chunk, extract top 3-5 concepts
3. Classify by type and layer
4. Generate concepts.json and report.md
```

---

## Output Persistence

### Entity Extraction Output

| File | Location |
|------|----------|
| Entity files | `knowledge/{domain}/{type}/{entity-slug}.md` |
| Quotes file | `knowledge/{domain}/_[book]-quotes.md` |
| Entity index | `knowledge/_entities.json` |
| Domain index | `knowledge/{domain}/_index.md` |

### Concept Extraction Output

| File | Location |
|------|----------|
| Full analysis | `ebook-analysis/{author}-{title}/analysis.json` |
| Concepts only | `ebook-analysis/{author}-{title}/concepts.json` |
| Citations | `ebook-analysis/{author}-{title}/citations.json` |
| Report | `ebook-analysis/{author}-{title}/report.md` |

---

## Verification (Oracle)

### What This Skill Can Verify
- **Citation positions exist** - Validate quoted text appears at claimed position
- **Schema completeness** - Required fields present
- **Cross-reference integrity** - Referenced entities exist
- **Duplicate detection** - Entity doesn't already exist (via kb-resolve-entity.ts)

### What Requires Human Judgment
- **Significance** - Is this worth extracting?
- **Classification** - Is this really a "framework" vs "concept"?
- **Relationship validity** - Does A really influence B?
- **Quote quality** - Is this actually memorable?

---

## Integration Graph

### Inbound (From Other Skills)
| Source | Leads to |
|--------|----------|
| research | Multi-book synthesis ready |
| reverse-outliner | Structural data for concept extraction |

### Outbound (To Other Skills)
| From State | Leads to |
|------------|----------|
| Entity extraction complete | dna-extraction (deep functional analysis) |
| Concept extraction complete | media-meta-analysis (cross-source synthesis) |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| dna-extraction | 6-axis functional analysis for annotation |
| reverse-outliner | Structural approach for fiction |
| voice-analysis | Author style fingerprinting |
| context-network | Knowledge base maintenance |

---

## Calibration Data (from Range + Imaginable extractions)

### By Book Density
| Book Type | Expected Entities | Estimated Effort |
|-----------|-------------------|------------------|
| Dense non-fiction (Range, Thinking Fast & Slow) | 60-100 | 4-6 hours |
| Moderate non-fiction (most business books) | 30-50 | 2-3 hours |
| Light non-fiction (popular science) | 15-30 | 1-2 hours |
| Technical books | 20-40 | 2-3 hours |

### By Book Subtype
Different non-fiction subtypes yield different entity profiles:

| Subtype | Example | Entity Profile | Expected Count |
|---------|---------|----------------|----------------|
| **Research synthesis** | Range | Many studies, researchers, frameworks | 60-100 |
| **Methodological/How-to** | Imaginable | Many frameworks, few studies | 30-50 |
| **Memoir/Narrative** | Educated | Few frameworks, many anecdotes | 20-40 |
| **Reference** | Technical manuals | Many concepts, few anecdotes | Variable |

**Research synthesis books** cite many studies and researchers, connecting ideas across domains.
**Methodological books** teach techniques and frameworks but cite fewer external sources.
**Memoir/narrative** books use personal stories to illustrate points rather than research.

### Metadata Reliability Warning
Book classification metadata (Calibre tags, library categories) is often:
- **Wrong** - Fiction/non-fiction misclassified
- **Generic** - "General Fiction" or "Self-Help" applied broadly
- **Inconsistent** - Same book categorized differently across sources

Always verify classification makes sense before extraction. A "fiction" tag on a methodology book like Imaginable is a metadata error.

---

## Reasoning Requirements

### Standard Reasoning
- Single chunk concept extraction
- Type/layer classification
- Simple relationship identification
- Individual entity creation

### Extended Reasoning (ultrathink)
Use extended thinking for:
- **Multi-book synthesis** - requires holding multiple networks simultaneously
- **Contradiction detection** - semantic comparison across sources
- **Theme emergence** - identifying patterns across large sets
- **Knowledge gap identification** - reasoning about what's missing

**Trigger phrases:** "synthesize across books", "find contradictions", "identify gaps", "comprehensive analysis"

---

## What You Do NOT Do

- Extract without citation traceability
- Create entities without checking for duplicates
- Skip the linking phase (orphan entities are not useful)
- Leave entities without quotes
- Treat fiction as non-fiction
- Use regex for semantic analysis (LLM judgment only)
