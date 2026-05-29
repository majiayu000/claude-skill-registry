---
name: biomarker-analysis
description: Ralph-Inspired Adaptive Learning Framework for iterative, quality-gated biomarker report analysis
allowed-tools: Read, Bash, Glob, Grep
---

# Biomarker Analysis Pipeline (RALF)

Ralph-Inspired Adaptive Learning Framework for iterative, quality-gated biomarker report analysis.

## Overview

This skill runs comprehensive biomarker analysis using the RALF architecture:
- **Iterative Processing**: Each category processed independently with fresh context
- **KB Enrichment**: Per-category VectorShift KB queries inform analysis
- **Dual Validation Gates**: Structural completeness + clinical accuracy
- **Retry with Feedback**: Failed validations trigger specific revision prompts
- **State Persistence**: Resume from any point, track learnings

## Usage

### Basic Analysis

```bash
# Run from Python
from lib.biomarker_analysis.execution import run_analysis

biomarkers = [
    {"name": "A1c", "value": "5.8", "unit": "%", "ref_range": "<5.7"},
    {"name": "Fasting Glucose", "value": "98", "unit": "mg/dL", "ref_range": "70-99"},
    # ... more biomarkers
]

prd = run_analysis(
    biomarkers=biomarkers,
    user_preference_level=3,  # 1-5 scale
    patient_goals="Optimize metabolic health and longevity",
)
```

### Resume Interrupted Analysis

```bash
from lib.biomarker_analysis.execution import resume_analysis

prd = resume_analysis(output_dir=".biomarker-analysis")
```

### Generate Visual Report

```bash
from lib.biomarker_analysis.synthesis import synthesize_report
from lib.biomarker_analysis.visual import generate_visual_report
from lib.biomarker_analysis.state import StateManager

state = StateManager()
synthesis = synthesize_report(state)
html = generate_visual_report(synthesis)
```

## Architecture

```
PHASE 1: INITIALIZATION
├── Parse biomarkers from lab report
├── Categorize into 5 core categories + dynamic modules
└── Generate PRD with segment definitions

PHASE 2: ITERATIVE ANALYSIS (per category)
├── Query VectorShift KB for research context
├── Generate category analysis (Claude Haiku 4.5)
├── Validate with dual gates
├── Retry with feedback if failed (max 2 retries)
└── Mark complete or blocked

PHASE 3: SYNTHESIS
├── Generate Goal Summary + Findings Summary
├── Merge all category analyses
├── Prioritize interventions
└── Generate visual HTML report
```

## Categories

### Core Categories (Always Present)
1. **GENERAL HEALTH**: CBC, CMP, liver/kidney function
2. **METABOLIC FUNCTION**: A1c, glucose, insulin, ApoB, triglycerides
3. **INFLAMMATION**: hs-CRP, homocysteine, GGT
4. **HORMONES**: Testosterone, thyroid, estrogen, AMH
5. **NUTRIENTS**: Vitamin D, ferritin, B12, magnesium

### Dynamic Modules (Auto-detected)
- Organic acids
- Microbiome
- Genetics/Epigenetics
- Advanced lipid panels
- Urine/salivary hormones

## User Preference Levels

| Level | Description |
|-------|-------------|
| 1 | Ultra-conservative: Evidence-based medicine only |
| 2 | Conservative: Some emerging research considered |
| 3 | Balanced: Mix of conventional and alternative |
| 4 | Progressive: Experimental approaches |
| 5 | Cutting-edge: Biohacker methodologies |

## Clinical Conventions

The pipeline enforces these clinic-specific conventions:

- **Free Testosterone**: Always labeled "suboptimal" per clinic protocol
- **GLP-1 RAs**: When recommending, add creatine monohydrate 5g daily
- **NAD+**: Consider 1000mg oral daily if A1c >5.4 AND CRP <1
- **Vitamin D**: Target 60-80 ng/mL (optimal longevity range)
- **Lab Values**: Report EXACTLY as provided (no rounding)

## Output Files

State is persisted in `.biomarker-analysis/`:

```
.biomarker-analysis/
├── prd.json              # Segment definitions + status
├── progress.txt          # Iteration logs
├── context/              # Per-category KB research
├── outputs/              # Per-category analysis JSON
└── final/
    ├── synthesis.json    # Merged synthesis data
    ├── report.html       # Visual HTML report
    └── report.md         # Markdown report
```

## Validation Gates

### Gate 1: Structural Completeness
- Status paragraph ≥100 words
- Root causes paragraph ≥100 words
- Interventions paragraph ≥100 words
- All biomarkers referenced by name

### Gate 2: Clinical Accuracy
- Biomarker values match source exactly
- Units are correct
- Status classifications accurate
- Recommendations align with preference level
- Clinical conventions followed

## Cost Comparison

| Pipeline | Cost/Report |
|----------|-------------|
| VectorShift (current) | ~$1.00 |
| RALF (Haiku 4.5) | ~$0.22 |

**78% cost reduction** with maintained or improved quality.

## Module Structure

```
lib/biomarker_analysis/
├── __init__.py      # Module exports
├── types.py         # Pydantic models
├── state.py         # State persistence
├── kb_client.py     # VectorShift KB queries
├── parser.py        # Biomarker extraction
├── generation.py    # Category analysis generation
├── validation.py    # Dual quality gates
├── execution.py     # Main iteration loop
├── synthesis.py     # Cross-category synthesis
└── visual.py        # HTML report generation
```

## API Reference

### ExecutionEngine

```python
class ExecutionEngine:
    def __init__(output_dir, config, callbacks...)
    def initialize_from_biomarkers(biomarkers, user_preference_level, patient_goals, ...)
    async def run() -> AnalysisPRD
    def run_sync() -> AnalysisPRD
    async def resume() -> AnalysisPRD
    def get_status() -> Dict
    def is_complete() -> bool
```

### StateManager

```python
class StateManager:
    def load_prd() -> Optional[AnalysisPRD]
    def save_prd(prd)
    def create_prd_from_biomarkers(biomarkers, ...) -> AnalysisPRD
    def get_segment(segment_id) -> CategorySegment
    def update_segment(segment)
    def mark_segment_completed(segment_id)
    def log_iteration(segment, status, ...)
```

### KBClient

```python
class KBClient:
    async def query(queries: List[str]) -> Dict
    def generate_category_queries(segment, user_preference_level) -> List[str]
    async def get_category_research_context(segment, ...) -> Dict
```

## Error Handling

- **Validation Failures**: Automatically retry with specific feedback (up to 2 retries)
- **KB Query Failures**: Continue with empty research context
- **Blocked Segments**: Marked as blocked, analysis continues with other segments
- **Resume**: Full state persistence allows resuming from any point

## Testing

```bash
# Run tests
pytest tests/test_biomarker_analysis.py

# Test single category
python -c "
from lib.biomarker_analysis.execution import ExecutionEngine
engine = ExecutionEngine()
# Initialize and run...
"
```
