---
name: create-table-classifier
description: >
  Train vision classifiers for Camelot table extraction strategy prediction.
  Uses MobileNetV2 with GRPO training and Camelot execution feedback.
  Integrates with Federated Taxonomy for preset-aware predictions.
allowed-tools: Bash, Read
triggers:
  - train table classifier
  - table strategy training
  - camelot strategy model
  - extraction strategy training
  - s05 strategy predictor
metadata:
  short-description: GRPO training for table extraction strategy prediction

provides:
  - create-table-classifier
composes: [, task-monitor]
---

# Create Table Classifier

Train vision models to predict optimal Camelot extraction strategies for PDF tables.
Uses GRPO with execution feedback from actual Camelot extractions.

## Training Approaches

| Approach | Description | Use When |
|----------|-------------|----------|
| **GRPO (Recommended)** | RL with Camelot execution feedback | Production training |
| **SFT Only** | Supervised fine-tuning | Quick baseline |
| **Collect Only** | Data collection from corpus | Building dataset |

## Quick Start (GRPO with Execution Feedback)

```bash
cd .pi/skills/create-table-classifier

# 1. Setup environment
cp .env.example .env
# Edit .env with paths to corpus and extractor

# 2. Collect training data from successful extractions
./run.sh collect \
    --corpus /path/to/12tb/corpus \
    --extractor-results /path/to/s05/outputs \
    --limit 5000

# 3. Split data into train/eval
./run.sh split --input data/labels/collected.jsonl --train-ratio 0.85

# 4. Run full training pipeline (warmup -> GRPO -> eval)
./run.sh train-full \
    --train-file data/labels/train.jsonl \
    --eval-file data/labels/eval.jsonl \
    --wandb

# 5. Test inference
./run.sh infer --image data/images/test/sample.png
```

## GRPO Training Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRPO Training Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Data Collection (from S05 successful extractions)            │
│     PDF → Table Region → [Image, Strategy, Quality]              │
│                                                                  │
│  2. SFT Warmup (3 epochs)                                        │
│     Initialize policy on high-quality extractions                │
│                                                                  │
│  3. GRPO Training Loop                                           │
│     ┌───────────────────────────────────────────────────────┐   │
│     │  Image ──▶ Generate N strategies ──▶ Execute Camelot  │   │
│     │                                           │            │   │
│     │  ┌─────────────────────────────────────────┐          │   │
│     │  │ Reward = 0.5×Quality + 0.3×Speed       │          │   │
│     │  │        + 0.2×PresetMatch                │          │   │
│     │  └─────────────────────────────────────────┘          │   │
│     │                    │                                   │   │
│     │                    ▼                                   │   │
│     │  Group-relative advantage ──▶ Policy update           │   │
│     └───────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. Evaluation on Holdout                                        │
│     If fails: Retry with adjusted hyperparameters               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Reward Functions

| Reward | Weight | Source | Description |
|--------|--------|--------|-------------|
| Quality | 50% | Camelot accuracy | Table extraction accuracy score |
| Speed | 30% | Extraction time | Faster than baseline = bonus |
| PresetMatch | 20% | Federated Taxonomy | Strategy matches preset expectations |

## Federated Taxonomy Integration

The classifier predicts **preset-aware** strategies:

```json
{
  "strategy": "lattice_sensitive",
  "line_scale": 15,
  "edge_tol": 300,
  "preset_hint": "arxiv_scientific",
  "domain": "scientific",
  "confidence": 0.92
}
```

**Preset-Strategy Mapping:**

| Preset | Expected Strategy | line_scale | Notes |
|--------|------------------|------------|-------|
| arxiv_scientific | lattice_sensitive | 12-15 | Thin LaTeX borders |
| requirements_spec | lattice | 20-25 | Structured tables |
| archive_scanned | stream | 35-40 | OCR-degraded lines |

## Evaluation Thresholds

| Metric | Threshold | Description |
|--------|-----------|-------------|
| strategy_accuracy | ≥ 85% | Correct strategy selection |
| param_mae | ≤ 5 | Mean absolute error for line_scale |
| fallback_rate | ≤ 10% | Tables needing retry |
| avg_quality | ≥ 0.85 | Mean extraction quality |

## Architecture

```
Table Region Image (224x224)
    │
    ▼
┌─────────────────────────────────────────────┐
│  MobileNetV2 (pretrained ImageNet)          │
│  + Strategy Classification Head (3 classes) │
│  + Regression Head (line_scale, edge_tol)   │
│  + Preset Embedding (optional)              │
└─────────────────────────────────────────────┘
    │
    ▼
Strategy Prediction
{
  "strategy": "lattice" | "stream" | "lattice_sensitive",
  "line_scale": 12-40,
  "edge_tol": 100-500,
  "confidence": 0.92
}
```

## Training Data Format

```json
{
  "image_path": "data/images/train/arxiv_2501_page3_table1.png",
  "source_pdf": "2501_15355.pdf",
  "page": 3,
  "bbox": [100, 200, 400, 350],
  "strategy": "lattice_sensitive",
  "params": {
    "line_scale": 15,
    "edge_tol": 300,
    "flavor": "lattice"
  },
  "quality_score": 0.92,
  "fallback_used": false,
  "preset": "arxiv_scientific",
  "domain": "scientific"
}
```

## Commands

### Data Collection

| Command | Description |
|---------|-------------|
| `./run.sh collect` | Collect table images from corpus |
| `./run.sh split` | Split data into train/eval sets |
| `./run.sh stats` | Show dataset statistics |

### GRPO Training

| Command | Description |
|---------|-------------|
| `./run.sh train-full` | Full pipeline: warmup → GRPO → eval |
| `./run.sh warmup` | SFT warmup before GRPO |
| `./run.sh grpo` | GRPO training with Camelot feedback |
| `./run.sh evaluate` | Run evaluation on holdout set |

### Utilities

| Command | Description |
|---------|-------------|
| `./run.sh infer` | Test inference on image |
| `./run.sh tensorboard` | Start TensorBoard |
| `./run.sh export` | Export model for S05 integration |

## S05 Integration

After training, integrate with S05:

```python
from create_table_classifier.inference import TableStrategyPredictor

predictor = TableStrategyPredictor(
    model_path="models/table-classifier-final",
)

# Predict strategy for table region
pred = predictor.predict(region_image)
if pred.confidence > 0.8:
    strategies_to_try = [pred.to_camelot_params()] + fallback_strategies
```

## GPU Requirements

| GPU | Batch Size | Memory |
|-----|------------|--------|
| RTX 3090 (24GB) | 32 | ~8GB |
| RTX 4090 (24GB) | 64 | ~12GB |
| A100 (40GB) | 128 | ~20GB |

## Output Structure

```
models/
├── table-classifier-sft/       # SFT warmup checkpoint
│   ├── model.pth
│   └── config.json
├── table-classifier-grpo/      # GRPO trained model
│   └── attempt_N/
└── table-classifier-final/     # Best model for S05
    ├── model.pth
    ├── config.json
    └── preset_embeddings.json  # Federated Taxonomy mappings
```

## Monitoring

Training logs are saved to `logs/` and optionally to Weights & Biases.

```bash
# View training progress
./run.sh logs

# TensorBoard
./run.sh tensorboard
```

## Self-Improvement Cycle

The classifier improves through continuous learning:

1. **Extract** tables from 10K PDF corpus
2. **Collect** successful strategies from S05 outputs
3. **Train** GRPO model with execution feedback
4. **Deploy** updated model to S05
5. **Repeat** nightly on scheduler

```bash
# Run full self-improvement cycle
./run.sh self-improve --corpus /path/to/10k_pdfs --nights 7
```
