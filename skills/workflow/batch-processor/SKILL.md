---
name: batch-processor
description: Parallel processing for validated assets. Input array of 3-5 assets → simultaneous IDF extraction, package generation, file operations. Replaces serial workflow with parallel execution.
---

# Batch-Processor Skill

## Purpose

Process multiple validated assets simultaneously. Input: array of 3-5 asset paths. Output: complete packages in parallel. Eliminates sequential bottleneck.

## Input

```json
{
  "batch_id": "batch-theatrical-specimens",
  "assets": [
    {
      "asset_id": "ASSET-3",
      "path": "/downloads/asset-3-validated.png",
      "score": 92,
      "specs": {...}
    },
    {
      "asset_id": "ASSET-4",
      "path": "/downloads/asset-4-validated.png",
      "score": 94,
      "specs": {...}
    },
    {
      "asset_id": "ASSET-6",
      "path": "/downloads/asset-6-validated.png",
      "score": 91,
      "specs": {...}
    }
  ]
}
```

## Parallel Operations

**1. IDF Extraction (Flash-Sidekick)**
```python
# Parallel calls
results = await Promise.all([
    flash_sidekick.generate_idf(asset_3_png),
    flash_sidekick.generate_idf(asset_4_png),
    flash_sidekick.generate_idf(asset_6_png)
])
# Returns in 5-8 seconds vs 15-20 serial
```

**2. Package Generation**
Template-based parallel creation:
- context.md × 3 assets
- tokens.json × 3 assets  
- usage.md × 3 assets

**3. Directory Creation**
```bash
mkdir -p /assets/ASSET-{3,4,6}-*/
```

**4. File Copy Operations**
Parallel cp commands:
```bash
cp asset-3.png /frontend/public/assets/patterns/ &
cp asset-4.png /frontend/public/assets/specimens/ &
cp asset-6.png /frontend/public/assets/specimens/ &
wait
```

**5. Single Consolidated Commit**
```bash
git add /assets/ASSET-{3,4,6}-* /frontend/public/assets/*
git commit -m "feat(assets): Add batch theatrical specimens - Assets 3,4,6"
```

## Workflow

1. Receive array of validated assets
2. Spawn parallel IDF extraction (Flash-Sidekick)
3. Generate packages using templates
4. Execute batch file operations
5. Single git commit
6. Report completion metrics

## Integration

**Flash-Sidekick:**
- `batch_file_analysis` for parallel IDF extraction
- Returns aggregated results JSON

**Asset-Packager:**
- Batch mode trigger
- Receives array instead of single asset

**Codex CLI:**
- Executes batch file operations
- Handles git operations

## Efficiency Gain

**Sequential (3 assets):**
- IDF extraction: 15 min (5 min each)
- Packaging: 45 min (15 min each)
- Total: 60 min

**Parallel (3 assets):**
- IDF extraction: 5 min (parallel)
- Packaging: 10 min (template-based)
- Total: 15 min

**Savings:** 75% time reduction for batches

## Constraints

- Max 5 assets per batch (API rate limits)
- All assets must be validated ≥90
- Requires sufficient system memory

## Usage

```python
batch_result = batch_processor.run(
    batch_id="theatrical-specimens",
    assets=[asset_3, asset_4, asset_6]
)

# Output:
# Processed: 3 assets in 15 min
# Created: 9 files across 3 directories
# Committed: 1 consolidated commit
```

---

*Parallel processing eliminates sequential bottleneck. 3 assets in 15 min vs 60 min serial.*
