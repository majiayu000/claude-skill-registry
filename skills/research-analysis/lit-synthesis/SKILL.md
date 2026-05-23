---
name: lit-synthesis
description: Deep reading and synthesis of literature corpus. Theoretical mapping, thematic clustering, and debate identification using Zotero MCP for full-text access.
---

# Literature Synthesis

You help sociologists move from a corpus of papers to a deep understanding of a field. This is the analytical bridge between finding papers (lit-search) and writing about them (lit-writeup).

## The Lit Trilogy

This skill is the middle step in a three-skill workflow:

| Skill | Role | Key Output |
|-------|------|------------|
| **lit-search** | Find papers via OpenAlex | `database.json`, download checklist |
| **lit-synthesis** | Analyze & organize via Zotero | `field-synthesis.md`, `theoretical-map.md`, `debate-map.md` |
| **lit-writeup** | Draft prose | Publication-ready Theory section |

**Input**: Papers in Zotero (imported from lit-search or user's existing library)
**Output**: Organized understanding of the field ready for writing

## When to Use This Skill

Use this skill when users:
- Have a corpus of papers (from lit-search or their own collection)
- Need to understand the theoretical landscape before writing
- Want to identify debates, tensions, and competing positions
- Need to organize papers thematically or by theoretical tradition
- Want deep reading notes, not just metadata extraction

## Core Principles

1. **Read deeply, not widely**: Better to understand 15 papers thoroughly than 50 superficially.

2. **Theoretical traditions matter**: Papers exist within intellectual lineages. Map who cites whom and why.

3. **Debates are gold**: Competing positions create space for contributions. Find the tensions.

4. **Organization serves writing**: The clusters and maps you create should directly feed lit-writeup's architecture phase.

5. **Full text when possible**: Abstracts tell you *what*; full text tells you *how* and *why*.

## Zotero MCP Integration

This skill uses **Zotero MCP** for accessing your library:

### Setup

Install the Zotero MCP server:
```bash
uv tool install "git+https://github.com/54yyyu/zotero-mcp.git"
zotero-mcp setup
```

See `mcp/zotero-setup.md` for detailed configuration.

### Key Capabilities

| Tool | Purpose |
|------|---------|
| `zotero_search_items` | Find papers by keyword, author, tag |
| `zotero_semantic_search` | Conceptual similarity search |
| `zotero_get_item_metadata` | Retrieve full metadata + BibTeX |
| `zotero_get_annotations` | Extract PDF highlights and notes |
| `zotero_search_notes` | Search your reading notes |

### Workflow Integration

1. **From lit-search**: Import the BibTeX export into Zotero
2. **Acquire PDFs**: Use Zotero's "Find Available PDF" or manual download
3. **Read and annotate**: Highlight key passages, add notes
4. **lit-synthesis reads**: Access annotations via MCP for analysis

## Workflow Phases

### Phase 0: Corpus Audit
**Goal**: Assess what's in the corpus and identify gaps.

**Process**:
- Review the database from lit-search (or user's Zotero collection)
- Count papers by year, journal, author, theoretical tradition
- Identify potential gaps in coverage
- Prioritize which papers need deep reading vs. skimming

**Output**: `corpus-audit.md` with statistics and reading priorities.

> **Pause**: User confirms corpus coverage and reading priorities.

---

### Phase 1: Deep Reading
**Goal**: Close read priority papers and extract analytical insights.

**Process**:
- For each priority paper, read full text via Zotero MCP
- Extract: argument structure, theoretical framework, key concepts, methodological approach
- Note: how theory is deployed, what evidence supports claims, limitations acknowledged
- Create structured reading notes

**Output**: `reading-notes/` directory with per-paper notes.

> **Pause**: User reviews reading notes for key papers.

---

### Phase 2: Theoretical Mapping
**Goal**: Identify intellectual traditions and lineages.

**Process**:
- Identify which theoretical frameworks appear across papers
- Map citation relationships (who cites whom)
- Note foundational texts and their descendants
- Identify "camps" or schools of thought
- Document key concepts and how they're used

**Output**: `theoretical-map.md` with traditions, key theorists, and concept definitions.

> **Pause**: User reviews theoretical landscape.

---

### Phase 3: Thematic Clustering
**Goal**: Organize papers by what they study and how.

**Process**:
- Group papers by empirical focus (population, setting, phenomenon)
- Group papers by theoretical approach
- Group papers by methodological strategy
- Identify papers that bridge multiple clusters
- Note within-cluster consensus and variation

**Output**: `thematic-clusters.md` with organized paper groupings.

> **Pause**: User reviews clustering logic.

---

### Phase 4: Debate Mapping
**Goal**: Identify tensions, disagreements, and competing positions.

**Process**:
- Find explicit disagreements (papers that critique each other)
- Find implicit tensions (contradictory findings or incompatible assumptions)
- Identify unresolved questions the field is grappling with
- Note where evidence is mixed or contested
- Document the "state of the debate" for each tension

**Output**: `debate-map.md` with positions, evidence, and unresolved questions.

> **Pause**: User reviews debates and selects focus areas.

---

### Phase 5: Field Synthesis
**Goal**: Create comprehensive understanding ready for writing.

**Process**:
- Synthesize across phases into coherent field understanding
- Identify the most productive gaps for contribution
- Recommend which lit-writeup cluster (Gap-Filler, Theory-Extender, etc.) fits
- Create the handoff document for lit-writeup

**Output**: `field-synthesis.md` with integrated understanding and writing recommendations.

---

## Output Files

```
lit-synthesis/
├── corpus-audit.md           # Phase 0: What's in the corpus
├── reading-notes/            # Phase 1: Per-paper notes
│   ├── author2020-title.md
│   ├── author2019-title.md
│   └── ...
├── theoretical-map.md        # Phase 2: Traditions and lineages
├── thematic-clusters.md      # Phase 3: Paper groupings
├── debate-map.md             # Phase 4: Tensions and positions
└── field-synthesis.md        # Phase 5: Integrated understanding
```

## Reading Note Template

For each paper in Phase 1:

```markdown
# [Author Year] - [Short Title]

## Bibliographic Info
- Full citation: [from Zotero]
- DOI: [link]

## Core Argument
[1-2 sentences: What is the paper arguing?]

## Theoretical Framework
- Tradition: [e.g., Bourdieusian, institutionalist, interactionist]
- Key concepts used: [list]
- How theory is deployed: [description vs. extension vs. critique]

## Empirical Strategy
- Data: [what kind]
- Methods: [how analyzed]
- Sample: [who/what]

## Key Findings
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Contribution Claim
[What does the paper claim to contribute?]

## Limitations (as noted by authors)
- [Limitation 1]
- [Limitation 2]

## My Notes
[Your analytical observations, connections to other papers, questions raised]

## Key Quotes
> "[Quote 1]" (p. X)

> "[Quote 2]" (p. Y)

## Tags
[theoretical-tradition] [empirical-focus] [method] [relevant-to-my-project]
```

## Model Recommendations

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Phase 0**: Corpus Audit | **Sonnet** | Data processing, statistics |
| **Phase 1**: Deep Reading | **Opus** | Analytical reading, synthesis |
| **Phase 2**: Theoretical Mapping | **Opus** | Pattern recognition, intellectual history |
| **Phase 3**: Thematic Clustering | **Sonnet** | Organization, categorization |
| **Phase 4**: Debate Mapping | **Opus** | Tension identification, nuance |
| **Phase 5**: Field Synthesis | **Opus** | Integration, strategic judgment |

## Starting the Synthesis

When the user is ready to begin:

1. **Check Zotero setup**:
   > "Do you have Zotero MCP configured? If not, let's set that up first (see `mcp/zotero-setup.md`)."

2. **Identify the corpus**:
   > "Where are your papers? A Zotero collection from lit-search? An existing library folder? How many papers total?"

3. **Set priorities**:
   > "Which papers are most central to your project? We'll deep-read those first and skim the rest."

4. **Clarify goals**:
   > "What are you trying to understand about this field? Are you looking for gaps, debates, or a specific theoretical tradition?"

5. **Proceed with Phase 0** to audit the corpus.

## Key Reminders

- **Zotero is the source of truth**: All papers should be in Zotero for consistent access
- **Annotations accelerate**: If you've already highlighted papers, those annotations are accessible via MCP
- **Quality over quantity**: Deep reading 15 papers beats skimming 50
- **Debates are opportunities**: Every tension you find is a potential contribution space
- **This feeds lit-writeup**: The outputs here become inputs there—keep that handoff in mind
