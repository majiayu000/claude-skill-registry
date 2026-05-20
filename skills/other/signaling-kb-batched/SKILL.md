---
name: signaling-kb-batched
description: Extract all entity types (interventions, pathways, biomarkers, conflicts) from Google Drive transcript analyses using a three-stage LLM pipeline with Claude Opus 4.5 for extraction and Haiku 4.5 for intelligent merging.
allowed-tools: Read, Edit, Create, Glob, Grep, Execute, TodoWrite
user_invocable: true
argument-hint: <command> [--from-tracker] [--status] [--dry-run]
---

# Signaling KB Batched - Full Entity Extraction Pipeline

Extract **all entity types** from transcript analyses with:
- **4 entity types**: Interventions, Pathways, Biomarkers, Conflicts
- **LLM-based semantic deduplication** (Opus 4.5) - resolves aliases like "Sirolimus" = "Rapamycin"
- **LLM-based intelligent merging** (Haiku 4.5) - merges new data into existing entities
- **Google Drive sync** with processing tracker
- **Source-agnostic output** (no document titles)
- **PMID/DOI citations only** (invalid citations filtered)
- **Resume capability** via tracker

## Architecture

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
│  entity types from      entities to existing     merge new data into       │
│  transcript             KB entries (aliases)     existing JSON files       │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Sync transcripts from Google Drive (with tracking)
python3 scripts/sync_gdrive_transcripts.py \
  --folder-id 1ajmDczDiX1hbMsSAkyG2Lat6SmCN8Q5T \
  --recursive

# 2. Check status
python3 scripts/extract_kb_openrouter.py --status

# 3. Run extraction (resumes from tracker)
OPENROUTER_API_KEY=xxx python3 scripts/extract_kb_openrouter.py --from-tracker

# 4. For long-running extraction, use background mode
nohup python3 scripts/extract_kb_openrouter.py --from-tracker > extraction.log 2>&1 &
```

## Entity Types Extracted

### 1. Interventions
Compounds, peptides, biologics, modalities, and lifestyle interventions.

```json
{
  "intervention_id": "rapamycin",
  "aliases": ["sirolimus", "Rapamune"],
  "category": "small_molecule",
  "dosing_protocols": [{
    "indication": "longevity/healthspan",
    "dose": "5-6mg",
    "frequency": "weekly",
    "route": "oral",
    "peer_reviewed_citations": [{"pmid": "24566879", "title": "..."}],
    "confidence": "moderate"
  }],
  "mechanism_claims": [{
    "target": "MTORC1",
    "effect": "inhibit",
    "peer_reviewed_citations": [],
    "confidence": "high"
  }],
  "contraindications": ["active infection", "wound healing"],
  "monitoring": ["lipid panel", "CBC", "fasting glucose"]
}
```

### 2. Pathways
Signaling cascades mapped to SIGNAL-10 axes with crosstalk relationships.

```json
{
  "pathway_id": "mtor-signaling",
  "pathway_name": "mTOR signaling",
  "axis": 1,
  "axis_name": "Nutrient Sensing & Energetics",
  "description": "Master regulator of cell growth...",
  "core_nodes": ["MTOR", "RPTOR", "RICTOR", "EIF4EBP1"],
  "upstream_triggers": ["amino acids", "insulin", "IGF-1"],
  "downstream_effects": ["protein synthesis", "autophagy inhibition"],
  "interventions_targeting": [
    {"intervention_name": "rapamycin", "effect": "inhibit"}
  ],
  "crosstalk": [
    {"target_pathway": "autophagy", "relationship": "inhibits"}
  ],
  "confidence": "high"
}
```

### 3. Biomarkers
Lab values with interpretation patterns and context-specific optimal ranges.

```json
{
  "biomarker_id": "igf-1",
  "biomarker_name": "IGF-1",
  "full_name": "Insulin-like Growth Factor 1",
  "reference_range": {"low": 100, "high": 300, "unit": "ng/mL"},
  "interpretation_patterns": [{
    "pattern_id": "low-igf1-with-insulin-resistance",
    "biomarker_state": {"igf1": "low", "homa_ir": "elevated"},
    "interpretation": "Suggests GH resistance or hepatic dysfunction...",
    "differential": ["hepatic_insulin_resistance", "gh_resistance"],
    "clinical_implications": "Address insulin resistance before GH therapy",
    "confidence": "moderate"
  }],
  "optimal_ranges_by_context": [{
    "context": "longevity",
    "optimal": {"low": 150, "high": 250},
    "rationale": "Below 150 suggests GH deficiency..."
  }],
  "interventions_affecting": [
    {"intervention_name": "growth hormone", "effect": "increase"}
  ],
  "pathways_involved": ["igf1-axis"]
}
```

### 4. Conflicts
Contradictions between claims requiring clinical judgment.

```json
{
  "conflict_id": "conflict_rapa_pgc1a_001",
  "conflict_type": "mechanism_dispute",
  "entity_type": "intervention",
  "entity_name": "rapamycin",
  "claim_a": "Rapamycin inhibits PGC-1alpha",
  "claim_b": "Rapamycin has biphasic effect - acute inhibition but chronic upregulation",
  "context": "Different timeframes may explain apparent contradiction",
  "resolution_status": "unresolved"
}
```

## LLM Pipeline Details

### Stage 1: Extraction (Opus 4.5)
- Extracts all 4 entity types from transcript
- Parses embedded references (PMIDs/DOIs from References section)
- Assigns confidence levels based on evidence quality
- Cost: ~$1.50 per transcript

### Stage 2: Semantic Entity Resolution (Opus 4.5)
- Maps extracted entity names to existing KB entries
- Identifies aliases (e.g., "Sirolimus" → "rapamycin")
- Prevents duplicate entries for same entity
- Example mappings:
  - "NAD+" = "Nicotinamide adenine dinucleotide"
  - "GLP-1 agonists" = "Glucagon-like peptide-1 agonists"
  - "Vitamin D" = "Cholecalciferol" = "D3"

### Stage 3: LLM Merge (Haiku 4.5)
- Intelligently merges new data into existing entities
- Preserves existing information (never deletes)
- Deduplicates dosing protocols and mechanism claims
- Handles conflicting information by keeping both positions
- Cost: ~$0.10 per entity merge

## Cost Tracking

### API Pricing (January 2026 via OpenRouter)

| Model | Input | Output |
|-------|-------|--------|
| Claude Opus 4.5 | $5.00/M tokens | $25.00/M tokens |
| Claude Haiku 4.5 | $0.80/M tokens | $4.00/M tokens |

### Typical Costs

| Operation | Cost |
|-----------|------|
| Single transcript (all entities) | ~$1.50-2.00 |
| Full batch (224 transcripts) | ~$250-300 |
| LLM merge per entity | ~$0.05-0.15 |

### Configuration

All operations use **64,000 max_tokens** for maximum output capacity:
- Extraction: 64k tokens
- Entity resolution: 64k tokens  
- LLM merge: 64k tokens

## Source-Agnostic Output

**CRITICAL**: Output contains NO source-identifying information.

**Included:**
- Claims and mechanisms (rephrased, not verbatim)
- Citations with valid PMIDs or DOIs only
- Source type classification (`"source_type": "expert_lecture"`)
- Confidence levels

**Excluded:**
- Document titles or names
- Course/institute names
- Speaker names
- Any metadata that could bias downstream models

## Key Files

| File | Purpose |
|------|---------|
| `scripts/extract_kb_openrouter.py` | Main extraction script with 3-stage pipeline |
| `scripts/sync_gdrive_transcripts.py` | Google Drive sync with tracking |
| `scripts/monitor_extraction.sh` | Auto-restart monitor for long runs |
| `.signaling-kb/state/processing-tracker.json` | Tracks processed vs pending |
| `.signaling-kb/interventions/*.json` | Intervention entity nodes |
| `.signaling-kb/pathways/*.json` | Pathway entity nodes |
| `.signaling-kb/biomarkers/*.json` | Biomarker entity nodes |
| `.signaling-kb/conflicts/*.json` | Conflict entity nodes |

## Monitoring Long Runs

For extraction runs that may take hours:

```bash
# Start the monitor (checks every 10 minutes, auto-restarts if stopped)
nohup bash scripts/monitor_extraction.sh > monitor.log 2>&1 &

# Check monitor status
tail -f monitor.log

# Check extraction progress
python3 scripts/extract_kb_openrouter.py --status
```

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-29 | Full 4-entity extraction with LLM merge and semantic dedup |
| 0.3.0 | 2026-01-23 | Added Google Drive sync, tracking, source-agnostic output |
| 0.2.0 | 2026-01-23 | Upgraded to Claude Opus 4.5 |
| 0.1.0 | 2026-01-23 | Initial implementation (interventions only) |
