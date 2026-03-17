---
name: directory-generate-3lens
description: Generate NGM Commons directory listings using a three-lens analytical framework (Mechanistic, Literature, KB Cross-Reference) with RALPH-style iterative quality gates.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task, WebFetch, WebSearch
user_invocable: true
argument-hint: <product_name> [--output-dir PATH] [--resume] [--dry-run] [--rerun-lens L1|L2|L3]
---

# Three-Lens Directory Generator

Generate comprehensive, clinically rigorous directory entries for the NGM Commons platform using a structured three-lens analytical framework.

## Invocation

```bash
/directory-generate-3lens <product_name> [options]
```

**Arguments:**
- `<product_name>` - Product to analyze (e.g., "Metformin", "Pendulum Glucose Control")
- `--output-dir PATH` - Custom output directory (default: content/commons/)
- `--resume` - Resume from last checkpoint if interrupted
- `--dry-run` - Show execution plan without running
- `--rerun-lens L1|L2|L3` - Force re-run specific lens

## Three-Lens Framework

This skill applies three distinct analytical lenses, executed in parallel where possible:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PARALLEL LENS EXECUTION                         │
│                                                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │     LENS 1       │  │     LENS 2       │  │     LENS 3       │  │
│  │   Mechanistic    │  │   Literature     │  │   KB Cross-Ref   │  │
│  │                  │  │                  │  │                  │  │
│  │ Claude Opus 4.5  │  │ Perplexity Deep  │  │ Local JSON       │  │
│  │ via OpenRouter   │  │ via OpenRouter   │  │ (no LLM)         │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
│           │                     │                     │            │
│           ▼                     ▼                     ▼            │
│      Quality Gate          Quality Gate          Quality Gate      │
│      (iterate)             (iterate)             (iterate)         │
└───────────┬─────────────────────┴─────────────────────┬────────────┘
            └─────────────────────┬─────────────────────┘
                                  ▼
                         ┌────────────────┐
                         │   SYNTHESIS    │
                         │ Claude Opus 4.5│
                         └───────┬────────┘
                                 ▼
                         ┌────────────────┐
                         │    ASSEMBLY    │
                         │  JSON + HTML   │
                         └────────────────┘
```

---

## Execution Flow

### Phase 0: Initialization

1. Parse product name and options
2. Create/load progress file at `.ralph-3lens/progress.txt`
3. Initialize state tracking
4. If `--resume`, load previous checkpoint

### Phase 1: Parallel Lens Execution

Execute all three lenses. Each lens iterates until its quality gate passes.

#### Lens 1: First-Principles Mechanistic Analysis

**Purpose:** Explain HOW the product works from foundational principles

**Process:**
1. Classify product type: biological | technological | service | hybrid
2. Identify primary molecular/system targets
3. Map signaling pathways (upstream → downstream)
4. Generate SVG pathway diagram
5. Create educational analogies

**Prompt:** `prompts/lens1_mechanistic.md`

**Quality Gate (5/6 to pass):**
- L1.1 `mechanism_depth`: Specific targets named
- L1.2 `pathway_accuracy`: Pathways correctly mapped
- L1.3 `cascade_completeness`: Full trigger → outcome chain
- L1.4 `analogy_quality`: Memorable analogy present
- L1.5 `diagram_validity`: SVG passes validation
- L1.6 `first_principles_not_claims`: Explains HOW, not IF

#### Lens 2: Comprehensive Literature Review

**Purpose:** Document what the peer-reviewed evidence demonstrates

**Process:**
1. Execute deep research via Perplexity (OpenRouter)
2. Extract PMIDs/DOIs from results
3. Grade evidence quality (RCT > Observational > Case > Mechanistic)
4. Document regulatory status
5. Note conflicting findings

**Prompt:** `prompts/lens2_literature.md`

**Quality Gate (5/6 to pass):**
- L2.1 `citation_validity`: PMIDs/DOIs resolve to real papers
- L2.2 `evidence_breadth`: 3+ distinct studies cited
- L2.3 `study_details`: Sample sizes and designs included
- L2.4 `conflict_documentation`: Conflicting findings noted
- L2.5 `regulatory_accuracy`: Regulatory status correct
- L2.6 `recency`: 2024+ studies included when available

#### Lens 3: Knowledge Base Cross-Referencing (MANDATORY)

**Purpose:** Connect product to NGM Signaling KB (664 intervention nodes) and extract peer-reviewed citations

**CRITICAL:** This lens must ALWAYS execute. Even if the product isn't directly in the KB, related intervention queries provide valuable citations and mechanism context.

**Process (varies by product type):**

**For Intervention Products (supplements, drugs, therapies):**
1. Direct lookup: `interventions/{slug}.json`
2. Target query: Find interventions with same mechanism targets
3. Pathway query: Find interventions in same signaling cascades
4. Indication query: Find interventions for same clinical use
5. Extract all `peer_reviewed_citations[]` from matched nodes

**For Testing/Diagnostic Products (microbiome tests, labs, devices):**
1. Identify biomarkers the test measures (e.g., butyrate, Akkermansia, SCFA)
2. Query KB for interventions that affect those biomarkers
3. Query KB for interventions the test results would inform
4. Build "Finding → KB Intervention" actionability map
5. Extract PMIDs that explain WHY those biomarkers matter

```bash
# Example for microbiome testing:
python scripts/query_kb.py --biomarker butyrate --json
python scripts/query_kb.py --biomarker akkermansia --json
python scripts/query_kb.py --indication "gut microbiome" --json
python scripts/query_kb.py --target SCFA --json
```

**Prompt:** `prompts/lens3_kb_query.md`
**Helper Script:** `scripts/query_kb.py`

**Quality Gate (5/6 to pass):**
- L3.1 `kb_search_exhaustive`: All query types attempted (direct, target, pathway, indication/biomarker)
- L3.2 `related_interventions_found`: Related nodes surfaced (minimum 3)
- L3.3 `mechanism_alignment`: KB claims align with Lens 1
- L3.4 `pmid_extraction`: At least 5 PMIDs/DOIs extracted from KB nodes
- L3.5 `citation_enrichment`: KB PMIDs incorporated into synthesis (not siloed)
- L3.6 `novel_product_handling`: If not in KB, indirect enrichment via biomarker/target queries

### Phase 2: Synthesis

**Purpose:** Integrate three lenses into coherent narrative

**Process:**
1. Resolve conflicts between lenses
2. Weight evidence appropriately
3. Generate integrated narrative
4. Compile all citations

**Prompt:** `prompts/synthesis.md`

**Conflict Resolution Rules:**
- L1 vs L2 conflict → Evidence (L2) precedence, note discrepancy
- L2 vs L3 conflict → Surface as "area of ongoing research"
- L3 has newer data → Update with KB insights

**Quality Gate (5/5 to pass):**
- S.1 `lens_integration`: All three lenses represented
- S.2 `conflict_addressed`: Discrepancies noted
- S.3 `evidence_graded`: Confidence communicated
- S.4 `clinical_utility`: Practitioner-actionable
- S.5 `vendor_neutrality`: No ranking

### Phase 3: Assembly

1. Generate `directory_content.json` with all structured data
2. Render `directory_page.html` from template
3. Update progress file with completion status

**Template:** `prompts/html_template.md`

---

## State Management

Progress tracked in `.ralph-3lens/progress.txt`:

```
=== DIRECTORY GENERATION: [Product Name] ===
Started: 2026-01-26T10:00:00Z

--- LENS 1: MECHANISTIC ---
Iteration 1: FAILED (L1.3 cascade_completeness=FALSE)
  Feedback: Missing downstream effects after AMPK activation
Iteration 2: PASSED (6/6)
  Mechanism type: biological
  Primary targets: AMPK, mTOR

--- LENS 2: LITERATURE ---
Iteration 1: PASSED (5/6)
  Citations: 8 (5 RCTs, 2 observational, 1 meta-analysis)
  Regulatory: FDA approved for Type 2 diabetes

--- LENS 3: KB CROSS-REFERENCE ---
Iteration 1: PASSED (5/6)
  KB node: metformin.json
  Related interventions: 3 (rapamycin, berberine, AICAR)

--- SYNTHESIS ---
Iteration 1: PASSED (5/5)

--- ASSEMBLY ---
Output: content/commons/metformin/

COMPLETED: 2026-01-26T10:45:00Z
```

---

## Output Schema

```json
{
  "meta": {
    "product_name": "Metformin",
    "slug": "metformin",
    "generated": "2026-01-26",
    "framework_version": "3lens-v1",
    "kb_status": "IN_KB"
  },
  "lens_1_mechanistic": {
    "mechanism_type": "biological",
    "primary_targets": ["AMPK", "Mitochondrial Complex I"],
    "first_principles_markdown": "...",
    "pathway_diagram_svg": "<svg>...</svg>",
    "analogies": ["..."]
  },
  "lens_2_literature": {
    "evidence_summary": "...",
    "key_studies": [...],
    "regulatory_status": {...}
  },
  "lens_3_kb_crossref": {
    "kb_node_found": true,
    "related_interventions": [...],
    "conflicts_detected": [...],
    "kb_citations_added": 4
  },
  "synthesis": {
    "integrated_narrative_markdown": "...",
    "conflict_notes": [...]
  },
  "sources": [...]
}
```

---

## API Configuration

All LLM calls route through OpenRouter using `OPENROUTER_API_KEY` from environment.

| Phase | Model | Purpose |
|-------|-------|---------|
| Lens 1 | `anthropic/claude-opus-4.5` | Mechanistic reasoning |
| Lens 2 | `perplexity/sonar-deep-research` | Literature review |
| Lens 3 | None (local) | KB queries |
| Synthesis | `anthropic/claude-opus-4.5` | Integration |
| Quality Gates | `anthropic/claude-opus-4.5` | Evaluation |

**Estimated cost per entry:** $0.35-0.50

---

## Key Principles

1. **Three Lenses, One Truth** - Each lens provides a unique perspective; synthesis reconciles them
2. **First Principles First** - Explain HOW before evaluating IF
3. **Evidence Hierarchy** - RCTs > Observational > Case > Mechanistic > Clinician Experience
4. **KB Enrichment is MANDATORY** - Lens 3 must always execute; the KB contains curated PMIDs that enrich output
5. **Conflicts Surfaced** - Never hide discrepancies; present both positions
6. **Vendor Neutrality** - Educate, don't rank; use "notable for" framing
7. **Elevated Scientific Listicle** - Deep, research-driven content in LLM-optimized structure
8. **AEO-First** - Structure content for AI answer engine citation

## Critical: KB Citation Policy

**The KB is a source aggregator, not a citable source.** When Lens 3 extracts data from the KB:

- **DO:** Extract PMIDs and DOIs from `peer_reviewed_citations[]` arrays and cite them directly
- **DO:** Reference the literature (e.g., "Butyrate serves as primary colonocyte fuel (Science, 2018)")
- **DON'T:** Cite "the KB" or "internal knowledge base" as a source
- **DON'T:** Reference "expert lecture" source types without peer-reviewed backing

Example transformation:
```
KB data: mechanism_claims[].peer_reviewed_citations[0].doi = "10.1126/science.aat9076"

✗ Wrong: "According to our knowledge base, butyrate fuels colonocytes"
✓ Right: "Butyrate serves as the primary energy substrate for colonocytes (Litvak et al., Science, 2018)"
```

---

## Output Format: Elevated Scientific Listicle

The output is an **elevated, highly scientific, research-driven listicle**—not a superficial "top 5" list. This format:
- Satisfies LLM extraction patterns (structured for AI citation)
- Provides genuine clinical value (substantive enough that practitioners learn)
- Positions vendors positively ("notable for" framing, no rankings)
- Goes deep (5,000-7,000 words, 400-600 words per entity)

### Why This Format (AEO Research)

- **80%** of articles cited by ChatGPT include list sections
- Content with **sequential H1>H2>H3 structure** is cited **3x more often**
- **Q&A format** content is **40% more likely** to be extracted by AI
- LLMs cite answers, not articles—structure each paragraph to answer one question

### Required Content Depth

| Section | Word Count | Key Elements |
|---------|------------|--------------|
| Quick Reference Table | N/A | 5-6 rows, 4-5 columns at page top |
| Executive Summary | 300-400 | Clinical value proposition |
| Technology | 800-1000 | H3 per methodology, comparison table, diagram |
| Evidence | 600-800 | Graded table, nuance callouts, inline Q&A |
| Each Entity | 400-600 | Quick facts, approach depth, clinical fit, evidence |
| Decision Support | 500-700 | Action pathways table, expectations |
| FAQ | 500-800 | 6-10 Q&A pairs, front-loaded answers |
| **Total** | **5,000-7,000** | Comprehensive clinical guide |

### Inline Q&A Distribution

Q&A blocks must be woven throughout—not siloed in FAQ section:
- Technology section: methodology comparisons
- Evidence section: interpretation guidance
- Decision support: actionability questions
- FAQ section: comprehensive coverage

See `context/aeo-best-practices.md` for detailed AEO requirements.

---

## CRITICAL: HTML Design System

**All directory pages MUST use the template at `templates/directory_page.html`** to ensure visual consistency across the NGM Commons platform.

### Design System Requirements

| Element | Specification |
|---------|---------------|
| **Fonts** | Google Fonts: `Inter` (sans) + `Newsreader` (serif) — NEVER use system fonts |
| **Color Palette** | Warm editorial: `--ink-900: #0A0B0C`, `--gold: #C5A572`, `--green: #5C8A6B` |
| **Layout** | `max-width: 860px`, centered, `padding: 48px 20px` |
| **Entity Cards** | `.entity-section` with `border: 1px solid`, `border-radius: 12px` |
| **Tables** | `.quick-reference` with dark header row (`--ink-900`) |
| **Breadcrumbs** | Always include navigation back to overview |
| **Framework Badge** | Fixed position bottom-right: `3lens-v1 | {category}` |

### Category Color Mapping

| Category | Primary Color | Badge Class |
|----------|---------------|-------------|
| Gut Microbiome | `--green: #5C8A6B` | `.badge-green` |
| Oral Microbiome | `--blue: #5C7A8A` | `.badge-blue` |
| Vaginal Microbiome | `--purple: #7A6C8A` | `.badge-purple` |
| SIBO Breath Testing | `--orange: #D4845C` | `.badge-orange` |
| Overview/Default | `--gold: #C5A572` | `.badge-gold` |

### Required HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Fonts - REQUIRED -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Newsreader:opsz,wght@6..72,400;6..72,500&display=swap" rel="stylesheet">
</head>
<body>
  <article>
    <nav class="breadcrumb">...</nav>
    <header>...</header>
    <section><!-- Quick Reference Table --></section>
    <section><!-- Executive Summary with .summary-box --></section>
    <div class="kb-insight"><!-- KB Citation Callout --></div>
    <div class="entity-section"><!-- Vendor 1 --></div>
    <div class="entity-section"><!-- Vendor 2 --></div>
    <!-- ... -->
    <section><!-- Clinical Decision Support --></section>
    <section><!-- FAQ --></section>
    <section class="sources"><!-- Sources with PMIDs --></section>
  </article>
  <div class="framework-badge">3lens-v1 | {category}</div>
</body>
</html>
```

### Design Consistency Quality Gate

Before page generation is complete, verify:

- [ ] **D.1** Uses Google Fonts (Inter + Newsreader), NOT system fonts
- [ ] **D.2** Uses NGM color palette (`--ink-*`, `--gold`, `--green`, etc.)
- [ ] **D.3** Includes breadcrumb navigation
- [ ] **D.4** Entity sections use `.entity-section` class with rounded borders
- [ ] **D.5** Quick reference table uses `.quick-reference` class
- [ ] **D.6** Has framework badge in bottom-right corner
- [ ] **D.7** KB insight callouts use `.kb-insight` class

**All 7 must pass** — design inconsistency is a blocking issue.

---

## Troubleshooting

**Lens 1 fails L1.5 (diagram_validity):**
- Check SVG viewBox dimensions match content
- Ensure 40px padding on all sides
- Validate text doesn't overflow containers

**Lens 2 fails L2.1 (citation_validity):**
- Some Perplexity citations may be hallucinated
- Cross-verify PMIDs via PubMed API
- Remove unverifiable citations

**Lens 3 finds no KB node:**
- Product may be new to KB
- Graceful degradation via L3.6
- Use indirect queries (target, pathway) to find related interventions

**Synthesis fails S.2 (conflict_addressed):**
- Review all three lens outputs for discrepancies
- Explicitly note where lenses disagree
- Provide characterization of conflict nature
