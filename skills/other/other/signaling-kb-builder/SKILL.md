---
name: signaling-kb-builder
description: Build and maintain an entity-centric cell signaling knowledge base from lecture transcripts. Uses a three-stage LLM pipeline (Opus 4.5 extraction, Opus 4.5 semantic dedup, Haiku 4.5 intelligent merge) to create queryable intervention, pathway, biomarker, and conflict nodes.
allowed-tools: Read, Edit, Create, Glob, Grep, Execute, TodoWrite, Bash
user_invocable: true
argument-hint: <command> [--source PATH] [--status] [--from-tracker]
---

# Cell Signaling Knowledge Base Builder

Transform lecture transcripts into an entity-centric knowledge graph optimized for clinical queries (biomarker interpretation, intervention dosing, pathway mechanisms).

## Why This Skill Exists

### Problem Statement

The existing VectorShift knowledge base stores lecture analyses as document chunks. When queried:

| Query Type | Current Behavior | Desired Behavior |
|------------|------------------|------------------|
| "rapamycin dosing" | Returns chunks mentioning mTOR (wrong compound) | Returns all rapamycin dosing protocols |
| "low IGF-1 with insulin resistance" | Returns how to RAISE IGF-1 | Returns diagnostic INTERPRETATION |
| "thymosin alpha-1 dosing" | Returns unrelated peptides (TB-500, BPC-157) | Returns TA1 protocols (content exists!) |
| "AMPK autophagy" | Works well (vocabulary matches) | Works well |

**Root cause:** Semantic search matches entity mentions but doesn't understand clinical query intent. Document-centric chunking scatters related information.

### Solution

Reorganize knowledge from **lecture-centric** to **entity-centric**:

```
BEFORE: Lectures → Chunks → Semantic Search
AFTER:  Lectures → Extract → Entity Nodes → Intent-Classified Query
```

## Architecture Overview (Current Implementation)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THREE-STAGE LLM PIPELINE                                 │
│                                                                              │
│  ┌──────────────────┐   ┌─────────────────────┐   ┌──────────────────────┐  │
│  │   EXTRACTION     │──▶│ SEMANTIC DEDUP      │──▶│  LLM MERGE           │  │
│  │  Claude Opus 4.5 │   │ Claude Opus 4.5     │   │  Claude Haiku 4.5    │  │
│  │  (64k tokens)    │   │ (64k tokens)        │   │  (64k tokens)        │  │
│  └──────────────────┘   └─────────────────────┘   └──────────────────────┘  │
│                                                                              │
│  Stage 1: Extract all   Stage 2: Map extracted   Stage 3: Intelligently    │
│  4 entity types from    entities to existing     merge new data into       │
│  transcript with        KB entries ("Sirolimus"  existing JSON files       │
│  citations              → "rapamycin")           preserving all info       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key principles:**
- **Claude Opus 4.5** for structured fact extraction (all 4 entity types)
- **Claude Opus 4.5** for semantic entity resolution (alias detection)
- **Claude Haiku 4.5** for intelligent merging (semantic deduplication)
- **64,000 max_tokens** for all operations
- **Source-agnostic output** (no document titles, PMID/DOI citations only)

## Quick Commands

### Primary Workflow (Recommended)

```bash
# 1. Sync transcripts from Google Drive
python3 scripts/sync_gdrive_transcripts.py \
  --folder-id 1ajmDczDiX1hbMsSAkyG2Lat6SmCN8Q5T \
  --recursive

# 2. Check extraction status
python3 scripts/extract_kb_openrouter.py --status

# 3. Run extraction (resumes from tracker)
OPENROUTER_API_KEY=xxx python3 scripts/extract_kb_openrouter.py --from-tracker

# 4. For long runs, use background mode with monitor
nohup python3 scripts/extract_kb_openrouter.py --from-tracker > extraction.log 2>&1 &
nohup bash scripts/monitor_extraction.sh > monitor.log 2>&1 &
```

### View Results

```bash
# Count all entity files
ls .signaling-kb/interventions/*.json | wc -l  # ~580 files
ls .signaling-kb/pathways/*.json | wc -l       # ~207 files
ls .signaling-kb/biomarkers/*.json | wc -l     # ~239 files
ls .signaling-kb/conflicts/*.json | wc -l      # ~576 files

# View specific entity
cat .signaling-kb/interventions/rapamycin.json | jq .
```

### Future Commands (Not Yet Implemented)

```bash
# Query the KB (planned)
/signaling-kb-builder query "rapamycin dosing for longevity"

# Export for VectorShift upload (planned)
/signaling-kb-builder export --format vectorshift
```

## Output Structure

```
.signaling-kb/
├── interventions/
│   ├── rapamycin.json
│   ├── metformin.json
│   ├── thymosin-alpha-1.json
│   └── ...
├── pathways/
│   ├── axis-1-nutrient-sensing/
│   │   ├── mtor-signaling.json
│   │   ├── ampk-signaling.json
│   │   └── igf1-axis.json
│   ├── axis-2-proteostasis/
│   │   └── autophagy.json
│   ├── axis-3-mitochondrial/
│   │   └── biogenesis.json
│   ├── axis-4-inflammation/
│   │   └── nlrp3-inflammasome.json
│   └── ... (axes 5-10)
├── biomarkers/
│   ├── igf1-patterns.json
│   ├── homa-ir-patterns.json
│   └── ...
├── sources/
│   └── extraction-index.json
├── conflicts/
│   └── active-conflicts.json
├── state/
│   ├── processing-state.json
│   └── processing-log.json
└── exports/
    └── vectorshift-export-YYYY-MM-DD.json
```

## Node Schemas

### Intervention Node

```json
{
  "intervention_id": "rapamycin",
  "aliases": ["sirolimus", "Rapamune"],
  "category": "small_molecule",
  "primary_pathways": ["axis-1-nutrient-sensing/mtor-signaling"],
  
  "dosing_protocols": [
    {
      "protocol_id": "longevity-weekly",
      "indication": "longevity/healthspan",
      "dose": "5-6mg",
      "frequency": "weekly",
      "duration": "indefinite with monitoring",
      "context": "Pulsed dosing to avoid immunosuppression",
      "evidence_grade": "moderate",
      "source_type": "expert_lecture",
      "peer_reviewed_citations": [
        {
          "citation": "Mannick JB et al. (2014) Sci Transl Med",
          "doi": "10.1126/scitranslmed.3009892",
          "relevance": "Supports intermittent dosing for immune enhancement"
        }
      ],
      "confidence": "moderate"
    }
  ],
  
  "mechanism_claims": [
    {
      "claim_id": "rapa_mtorc1_001",
      "target": "MTORC1",
      "effect": "inhibit",
      "context": "Selective mTORC1 inhibition at low doses",
      "evidence_type": "EXPLICIT",
      "source_type": "expert_lecture",
      "confidence": "high"
    }
  ],
  
  "regulatory_status": {
    "fda": "Approved (transplant), off-label (longevity)",
    "wada": "Not prohibited",
    "notes": "Prescription required"
  },
  
  "contraindications": ["active infection", "wound healing"],
  "monitoring": ["lipid panel", "CBC", "glucose"],
  
  "conflicts": []
}
```

### Pathway Node

```json
{
  "pathway_id": "axis-1-nutrient-sensing/mtor-signaling",
  "axis": 1,
  "axis_name": "Nutrient Sensing & Energetics",
  "shift_domain": "S",
  
  "description": "Master regulator of cell growth integrating nutrient and energy signals",
  
  "core_nodes": ["MTOR", "RPTOR", "RICTOR", "EIF4EBP1", "RPS6KB1"],
  "upstream_triggers": ["amino_acids", "insulin", "growth_factors", "energy_status"],
  "downstream_effects": ["protein_synthesis", "autophagy_inhibition", "lipid_synthesis"],
  
  "crosstalk": [
    {
      "target_pathway": "axis-2-proteostasis/autophagy",
      "relationship": "inhibitory",
      "mechanism": "mTORC1 phosphorylates ULK1, inhibiting autophagy initiation"
    }
  ],
  
  "interventions_targeting": [
    {"intervention_id": "rapamycin", "effect": "inhibit", "specificity": "mTORC1 selective"},
    {"intervention_id": "metformin", "effect": "indirect_inhibit", "via": "AMPK activation"}
  ],
  
  "biomarker_relevance": [
    {"biomarker": "igf1", "relationship": "upstream_activator"},
    {"biomarker": "p70s6k_phospho", "relationship": "activity_marker"}
  ],
  
  "source_type": "expert_lecture"
}
```

### Biomarker Interpretation Node

```json
{
  "biomarker_id": "igf1",
  "full_name": "Insulin-like Growth Factor 1",
  "reference_range": {"low": 100, "high": 300, "unit": "ng/mL"},
  
  "interpretation_patterns": [
    {
      "pattern_id": "low-igf1-with-insulin-resistance",
      "biomarker_state": {"igf1": "low", "homa_ir": "elevated"},
      "interpretation": "Suggests GH resistance or hepatic dysfunction rather than simple GH deficiency. Liver may not respond to GH due to insulin resistance.",
      "differential": ["hepatic_insulin_resistance", "gh_resistance", "malnutrition"],
      "clinical_implications": "Address insulin resistance before considering GH therapy",
      "evidence_grade": "moderate",
      "source_type": "expert_lecture",
      "peer_reviewed_citations": [],
      "confidence": "moderate"
    }
  ],
  
  "optimal_ranges_by_context": [
    {
      "range_id": "longevity_40_60",
      "optimal": {"low": 150, "high": 250},
      "context": "Longevity optimization, adults 40-60",
      "rationale": "Below 150 suggests GH deficiency, above 250 may accelerate aging",
      "source_type": "expert_lecture",
      "confidence": "moderate"
    }
  ],
  
  "interventions_affecting": [
    {"intervention_id": "growth_hormone", "effect": "increase", "magnitude": "significant"},
    {"intervention_id": "carnitine_with_gh", "effect": "increase", "magnitude": "additive", "confidence": "low"}
  ],
  
  "pathways_involved": ["axis-1-nutrient-sensing/igf1-axis"],
  
  "range_conflicts": []
}
```

## Processing Pipeline (Detailed)

### Step 1: Extraction (✓ Implemented)

**Input:** Transcript analysis (Google Doc HTML export)
**Output:** Structured JSON with interventions, pathways, biomarkers

**Model:** Claude Sonnet (`claude-sonnet-4-20250514`)

**Extraction identifies:**
- Interventions (compounds, peptides, protocols)
- Dosing information (dose, frequency, indication, context)
- Mechanism claims (intervention → target → effect)
- Biomarker interpretations (pattern → meaning)
- Pathway mappings (which SIGNAL-10 axes are involved)
- Evidence type (EXPLICIT, STRONGLY_INFERRED, LOOSELY_INFERRED)
- Confidence level
- Contraindications and monitoring requirements

**Token usage:** ~20K input, ~2K output per transcript

### Step 2: Entity Resolution (Simplified)

**Current implementation:** Programmatic slugify

```python
def slugify(name: str) -> str:
    slug = str(name).lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')
```

**Trade-off:** "sirolimus" and "rapamycin" create separate files, but aliases are tracked for future consolidation.

**Future enhancement:** LLM-based semantic entity resolution.

### Step 3: Merge (✓ Implemented)

**Current implementation:** ID-based deduplication

- Dosing protocols: `{intervention}-{indication_slug}`
- Mechanism claims: `{intervention}_{target}_{effect}`

If ID exists, skip. If new, append to node.

### Step 4: Conflict Detection (Not Implemented)

**Status:** Aspirational - currently just appends all claims.

**Future:** LLM-based conflict detection between claims with different confidence levels.

### Step 5: Enrichment (Integrated with Processing)

**Input:** Each dosing protocol and mechanism claim
**Output:** Up to 5 peer-reviewed citations per claim

**Architecture (Actual Implementation):**
1. **Perplexity Deep Research** - Called for each protocol/claim with a structured query
2. **URL Parsing** - Extracts PMIDs/PMCIDs/DOIs from returned citation URLs
3. **Haiku Fallback** - If URL parsing fails, Claude Haiku extracts citations from prose

**Per-Claim Enrichment Query:**
```
Find peer-reviewed clinical studies on {intervention} dosing:
- Dose: {dose}
- Indication: {indication}

Include mechanism of action, clinical trial data, and safety information.
```

**Rate Limiting:** 2-second delay between Deep Research calls to avoid API limits.

**Citation Filtering:**
- Only peer-reviewed sources are included (PubMed, PMC, DOI-identified journals)
- Web sources are filtered out
- Deduplication by PMID/PMCID/DOI
- Capped at 5 citations per claim, 10 per research response

**Cost:** **$5.00 per Deep Research call** × ~5-10 claims per intervention = **~$25-$50 per intervention** ⚠️

### Step 6: Node Synthesis (✓ Implemented)

**Current implementation:** Programmatic merging in `merge_intervention()`:

1. Load existing node or create new with empty schema
2. Add new aliases (deduplicated)
3. Add new dosing protocols with enriched citations
4. Add new mechanism claims with enriched citations
5. Merge monitoring and contraindications arrays

**No LLM synthesis** - direct JSON manipulation.

### Step 7: Commit (✓ Implemented)

```python
with open(filepath, 'w') as f:
    json.dump(node, f, indent=2)
```

**Cost report** saved to `.signaling-kb/cost-report.json` after each batch.

## Source Attribution Policy

### What Is Stored

- **Source type** (not specific lecture name): `"expert_lecture"`, `"clinical_discussion"`, `"review_presentation"`
- **Peer-reviewed citations** (from enrichment): Full citation with DOI

### What Is NOT Stored

- Specific lecturer names
- Lecture titles
- Episode numbers
- Extraction references or internal tracking IDs that could trace back to specific sources

### Rationale

1. Peer-reviewed literature is more authoritative than lecture origin
2. Avoids bias toward specific sources
3. Citations are verifiable; lecture claims are not
4. **Fair use compliance:** Content is rephrased through SIGNAL-10 framework lens with no verbatim quotes or direct source traceability

## Conflict Handling Policy

### Principle: Surface Both, Don't Rank

When sources disagree, BOTH positions are preserved with full context.

### Example: Rapamycin Effect on PGC-1alpha

```json
{
  "conflicts": [
    {
      "conflict_id": "conflict_rapa_pgc1a_001",
      "topic": "rapamycin_effect_on_pgc1a",
      "nature": "temporal_context_difference",
      "position_a": {
        "summary": "Rapamycin inhibits PGC-1alpha",
        "detail": "mTORC1 inhibition reduces PGC-1alpha transcriptional activity",
        "evidence_type": "mechanistic_inference",
        "confidence": "moderate"
      },
      "position_b": {
        "summary": "Rapamycin has biphasic effect on PGC-1alpha",
        "detail": "Acute inhibition but chronic upregulation via enhanced mitophagy",
        "evidence_type": "clinical_observation",
        "confidence": "low"
      },
      "characterization": "These positions may be complementary rather than contradictory - they describe different timeframes",
      "resolution_status": "unresolved",
      "flagged_for_review": true
    }
  ]
}
```

### Conflict Types Detected

| Type | Example | Handling |
|------|---------|----------|
| Directional | "inhibits" vs "activates" | Both preserved, characterized |
| Numeric | "5mg weekly" vs "10mg weekly" | Both preserved as separate protocols |
| Contextual | Different optimal ranges for different ages | Both preserved with context |
| Evidence grade | "established" vs "speculative" | Both preserved, grades noted |

## State Management

### Processing State

```json
{
  "last_processed": "2025-11-20T14:30:00Z",
  "transcripts_processed": 147,
  "transcripts_pending": 12,
  "nodes_created": {
    "interventions": 89,
    "pathways": 47,
    "biomarkers": 34
  },
  "active_conflicts": 23,
  "last_enrichment_run": "2025-11-19T10:00:00Z"
}
```

### Processing Log

Each processing run is logged:

```json
{
  "run_id": "run_20251120_143000",
  "source": "Rapamycin_Protocols_Analysis.pdf",
  "started_at": "2025-11-20T14:30:00Z",
  "completed_at": "2025-11-20T14:35:22Z",
  "facts_extracted": 12,
  "entities_resolved": {
    "matched_existing": 3,
    "created_new": 2
  },
  "conflicts_detected": 1,
  "enrichment_performed": true,
  "nodes_updated": ["rapamycin", "mtor-signaling"]
}
```

## Query Interface

### Intent Classification

Before retrieval, queries are classified:

| Intent | Example Query | Retrieval Path |
|--------|---------------|----------------|
| `intervention_dosing` | "rapamycin dosing longevity" | `interventions/{id}.json` → `dosing_protocols` |
| `biomarker_interpretation` | "low IGF-1 insulin resistance" | `biomarkers/{id}.json` → `interpretation_patterns` |
| `mechanism` | "AMPK autophagy mitochondria" | `pathways/` → traverse crosstalk |
| `regulatory` | "BPC-157 FDA status" | `interventions/{id}.json` → `regulatory_status` |

### Query Processing

```
User Query
    │
    ▼
┌─────────────────┐
│ Intent Classify │  (LLM determines query type)
│     (LLM)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Entity Extract  │  (LLM identifies target entities)
│     (LLM)       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Node Lookup     │  (Direct file access)
│   (Direct)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Response Format │  (LLM synthesizes answer)
│     (LLM)       │
└─────────────────┘
```

## Integration with VectorShift

### Export Format

The skill can export nodes for VectorShift upload:

```bash
/signaling-kb-builder export --format vectorshift
```

This produces documents optimized for semantic search:
- Each intervention as a document with intervention-specific embedding
- Each pathway as a document with pathway-specific embedding
- Metadata fields for filtering (category, axis, confidence)

### Recommended VectorShift Configuration

```
Chunking: None (documents are already atomic)
Metadata fields: category, axis, confidence, source_type
Reranking: By confidence score
```

## Design Decisions & Rationale

### Why Entity-Centric Instead of Document-Centric?

**Problem:** Asking "rapamycin dosing" retrieves chunks that mention mTOR (the pathway) but not rapamycin (the intervention) because they're semantically similar.

**Solution:** Create dedicated intervention nodes. Query goes directly to `interventions/rapamycin.json`, not through semantic search.

### Why Programmatic Entity Resolution?

**Current approach:** Slugify intervention names for file-based storage. Simple and fast.

**Trade-off:** Synonyms like "sirolimus" and "rapamycin" create separate files. This is acceptable because:
1. Transcripts typically use consistent naming
2. Aliases are stored in each node for future consolidation
3. Keeps processing simple and fast

**Future enhancement:** LLM-based entity resolution for synonym merging.

### Why Preserve Both Conflicting Positions?

**Problem:** If we rank or resolve conflicts, we impose judgment on clinical decisions that should be made by the clinician.

**Solution:** Surface both positions with full context. Let the querying clinician decide based on their patient's situation.

### Why Source Type Instead of Specific Names?

**Problem:** Citing "Huberman Episode 245" doesn't help verify claims. Peer-reviewed citations do.

**Solution:** Abstract lecture origin to type ("expert_lecture"). Prioritize peer-reviewed citations from enrichment step.

## Cost Tracking

The processing script tracks API costs in real-time:

### API Pricing (as of Jan 2026)

| API | Cost |
|-----|------|
| Claude Sonnet (input) | $3.00/1M tokens |
| Claude Sonnet (output) | $15.00/1M tokens |
| Claude Haiku (input) | $0.25/1M tokens |
| Claude Haiku (output) | $1.25/1M tokens |
| **Perplexity Deep Research** | **$5.00/request** ⚠️ |

### Typical Costs

| Operation | Cost |
|-----------|------|
| Single transcript (6-10 interventions) | **~$25-$50** |
| Full SSRP batch (8 transcripts) | **~$200-$400** |
| Per Deep Research call | **$5.00** |

**⚠️ WARNING:** Deep Research is expensive. Consider using `sonar-pro` (~$0.005/request) for less critical enrichment.

### Cost Report

After each batch run, a cost report is saved to `.signaling-kb/cost-report.json`:

```json
{
  "batch_run": "2026-01-22T...",
  "transcripts_processed": 4,
  "total_deep_research_calls": 44,
  "total_cost": "$0.4033",
  "per_transcript": [...]
}
```

## Limitations & Future Work

### Current Limitations

1. **No automated VectorShift sync** - Export is manual
2. **No UI** - CLI only
3. **No query interface** - KB is file-based, no search yet

### Implemented Features ✓

1. **All 4 entity types** - Interventions, pathways, biomarkers, conflicts
2. **LLM-based semantic deduplication** - Opus 4.5 maps aliases (e.g., "Sirolimus" → "rapamycin")
3. **LLM-based intelligent merging** - Haiku 4.5 merges new data into existing entities
4. **Google Drive sync** - `sync_gdrive_transcripts.py` with tracking
5. **Resume capability** - Processing tracker enables restart after interruption
6. **Background processing** - `monitor_extraction.sh` auto-restarts stopped processes
7. **Source-agnostic output** - No document titles, PMID/DOI citations only
8. **64k token configuration** - Maximum output capacity for all operations

### Planned Enhancements

1. **VectorShift export** - Format nodes for upload
2. **Query interface** - Search the KB
3. **Entity consolidation UI** - Review and merge duplicate entities

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `signaling-kb-batched` | Primary extraction skill (this is the reference implementation) |
| `lecture-gen-iterative` | Uses KB for research during lecture generation |
| `process-ngm-lectures` | Produces the transcript analyses this skill consumes |
| `physician-feedback-agent` | Could use KB for evidence lookup |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-29 | Full 4-entity extraction with LLM merge (Haiku 4.5), semantic dedup (Opus 4.5), 64k tokens, 224 transcripts |
| 0.5.0 | 2026-01-28 | Added pathways, biomarkers, conflicts extraction |
| 0.4.0 | 2026-01-27 | Upgraded to Claude Haiku 4.5 for merge operations |
| 0.3.0 | 2026-01-22 | Full batch processing of SSRP transcripts (8 total), 49 interventions created |
| 0.2.1 | 2026-01-22 | Bug fix: contraindications/monitoring string-to-array handling |
| 0.2.0 | 2026-01-21 | Added Deep Research enrichment, cost tracking, batch processing scripts |
| 0.1.0 | 2025-01-16 | Initial architecture design |

## Batch Processing Scripts

### `scripts/run_kb_batch.py`

Orchestrates processing of all 8 SSRP Institute transcripts (Day 1 + Day 2):

```python
DOC_CONTENTS = {
    # Day 1
    "1BQLxxu...": ("Day 1 - Part 1", content),
    "1wqJHp...": ("Day 1 - Part 2", content),
    # ... Day 1 Parts 3-4, Day 2 Parts 1-4
}
asyncio.run(main(DOC_CONTENTS))
```

### `scripts/run_kb_batch_day2.py`

Day 2-only batch (created to resume after Day 1 stuck):

```python
DOC_CONTENTS = {
    "1a3WEMME...": ("Day 2 - Part 1", content),
    "19sdDr9P...": ("Day 2 - Part 2", content),
    "1h4dC5K4...": ("Day 2 - Part 3", content),
    "1oHKEnvJ...": ("Day 2 - Part 4", content),
}
```

### Key Bug Fix (0.2.1)

Fixed contraindications/monitoring arrays being split into individual characters when Claude returned a string instead of array:

```python
# Before (buggy): iterating string → individual chars
for item in extracted.get("contraindications", []):  # "pregnancy" → "p", "r", "e"...

# After (fixed): type check and wrap
contraindications_data = extracted.get("contraindications") or []
if isinstance(contraindications_data, str):
    contraindications_data = [contraindications_data] if contraindications_data.strip() else []
for item in contraindications_data:
    if item and isinstance(item, str) and len(item) > 1:  # Filter single chars
        ...
```
