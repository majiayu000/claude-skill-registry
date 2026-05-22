---
name: create-intent-map
description: >
  Train LoRA intent mappers for structured query generation using GRPO with execution feedback.
  Uses DeepSeek-R1-Distill-Qwen-7B as base model. Supports SFT warmup, GRPO training with
  ArangoDB rewards, and iterative improvement with automatic retry on eval failure.
allowed-tools: Bash, Read
triggers:
  - train intent mapper
  - intent map training
  - create intent model
  - lora training
  - query spec training
  - train query mapper
  - grpo training
  - execution feedback training
metadata:
  short-description: GRPO training for intent mapping with execution feedback

provides:
  - create-intent-map
composes: [, task-monitor]
---

# Create Intent Map

Train LoRA adapters for converting natural language queries into structured QuerySpec JSON.
Uses GRPO (Group Relative Policy Optimization) with execution feedback from ArangoDB.

## Training Approaches

| Approach | Description | Use When |
|----------|-------------|----------|
| **GRPO (Recommended)** | RL with execution feedback | Production training |
| **SFT Only** | Supervised fine-tuning | Quick baseline |
| **Docker SFT** | Dockerized training | RunPod deployment |

## Quick Start (GRPO with Execution Feedback)

```bash
cd .pi/skills/create-intent-map

# 1. Setup environment
cp .env.example .env
# Edit .env with HF_TOKEN, CHUTES_API_KEY, ARANGO_* credentials

# 2. Generate question variations (2K examples)
./run.sh variations --input data/sft/train_from_qra.json --limit 2000

# 3. Split data into train/eval
./run.sh split --input data/sft/train_augmented.jsonl --train-ratio 0.85

# 4. Run full training pipeline (warmup -> GRPO -> eval -> retry)
./run.sh train-full \
    --train-file data/sft/train.jsonl \
    --query-file data/queries.txt \
    --eval-file data/eval/test.jsonl \
    --wandb

# 5. Test inference
./run.sh infer "How do I detect RF jamming attacks?"
```

## Quick Start (Docker SFT - for RunPod)

```bash
# 1. Build Docker image
./run.sh build

# 2. Prepare training data
./run.sh prepare --input data/sft/train_from_qra.json --output data/sft/train.jsonl

# 3. Train LoRA
./run.sh train --epochs 3 --batch-size 4

# 4. Export merged model (optional)
./run.sh merge --output models/intent-mapper-merged
```

## GRPO Training Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    GRPO Training Pipeline                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Variation Generation (scillm/Chutes)                        │
│     Original Query ──▶ [Layperson, PM, Expert, Reversal]        │
│                                                                  │
│  2. SFT Warmup (1 epoch)                                        │
│     Initialize policy near reasonable outputs                    │
│                                                                  │
│  3. GRPO Training Loop                                          │
│     ┌───────────────────────────────────────────────────────┐   │
│     │  Query ──▶ Generate N completions ──▶ Execute AQL     │   │
│     │                                           │            │   │
│     │  ┌─────────────────────────────────────────┐          │   │
│     │  │ Reward = 0.4×Grounding + 0.4×Relevance │          │   │
│     │  │        + 0.2×Format                     │          │   │
│     │  └─────────────────────────────────────────┘          │   │
│     │                    │                                   │   │
│     │                    ▼                                   │   │
│     │  Group-relative advantage ──▶ Policy update           │   │
│     └───────────────────────────────────────────────────────┘   │
│                                                                  │
│  4. Evaluation on Holdout                                       │
│     If fails: Retry with adjusted hyperparameters               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Reward Functions

| Reward | Weight | Source | Description |
|--------|--------|--------|-------------|
| Grounding | 40% | ArangoDB execution | Avg grounding_score of retrieved QRAs |
| Relevance | 40% | LLM judge (scillm) | Semantic match between query and results |
| Format | 20% | JSON validation | Valid QuerySpec structure |

## Evaluation Thresholds

| Metric | Threshold | Description |
|--------|-----------|-------------|
| accuracy | ≥0.80 | Action prediction (QUERY/NO_MATCH/CLARIFY) |
| entity_f1 | ≥0.70 | Entity extraction F1 score |
| avg_grounding | ≥0.75 | Mean grounding of retrieved results |
| format_valid | ≥0.95 | Valid JSON output rate |

## Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│  DeepSeek-R1-Distill-Qwen-7B + LoRA Adapter │
└─────────────────────────────────────────────┘
    │
    ▼
QuerySpec JSON
{
  "action": "QUERY" | "CLARIFY" | "NO_MATCH",
  "entities": ["T1071", "CWE-787"],
  "tier1": ["Detect", "Mitigate"],
  "lanes": ["entity", "bm25"],
  "k": 12
}
```

## Training Data Format

Input JSON (from QRA generation):
```json
{
  "input": "How do I detect RF jamming attacks on satellite uplinks?",
  "output": {
    "action": "QUERY",
    "entities": [],
    "tier1": ["Detect"],
    "lanes": ["bm25", "dense"],
    "k": 12
  },
  "type": "QUERY"
}
```

Converted to chat format for SFT:
```json
{
  "messages": [
    {"role": "system", "content": "Convert user queries to SPARTA QuerySpec JSON."},
    {"role": "user", "content": "How do I detect RF jamming attacks on satellite uplinks?"},
    {"role": "assistant", "content": "{\"action\": \"QUERY\", \"entities\": [], ...}"}
  ]
}
```

## Commands

### Data Preparation

| Command | Description |
|---------|-------------|
| `./run.sh variations` | Generate question variations with scillm |
| `./run.sh split` | Split data into train/eval sets |
| `./run.sh prepare` | Convert training data to chat format |

### GRPO Training (Recommended)

| Command | Description |
|---------|-------------|
| `./run.sh train-full` | Full pipeline: warmup → GRPO → eval → retry |
| `./run.sh warmup` | SFT warmup before GRPO |
| `./run.sh grpo` | GRPO training with execution feedback |
| `./run.sh evaluate` | Run evaluation on holdout set |

### Docker SFT Training

| Command | Description |
|---------|-------------|
| `./run.sh build` | Build Docker training image |
| `./run.sh train` | Run Docker-based SFT training |
| `./run.sh merge` | Merge LoRA into base model |
| `./run.sh shell` | Interactive shell in container |

### Utilities

| Command | Description |
|---------|-------------|
| `./run.sh infer` | Test inference with query |
| `./run.sh tensorboard` | Start TensorBoard |
| `./run.sh logs` | Tail training logs |

## Configuration

### Environment Variables (.env)

```bash
HF_TOKEN=hf_xxxxx              # HuggingFace token (required)
WANDB_API_KEY=xxxxx            # Weights & Biases (optional)
CUDA_VISIBLE_DEVICES=0         # GPU selection
```

### Training Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--base-model` | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | Base model |
| `--epochs` | 3 | Training epochs |
| `--batch-size` | 4 | Batch size (adjust for GPU memory) |
| `--learning-rate` | 2e-4 | Learning rate |
| `--lora-r` | 16 | LoRA rank |
| `--lora-alpha` | 32 | LoRA alpha |
| `--max-length` | 512 | Max sequence length |

## GPU Requirements

| GPU | Batch Size | Memory |
|-----|------------|--------|
| RTX 3090 (24GB) | 4 | ~20GB |
| RTX 4090 (24GB) | 4 | ~20GB |
| A100 (40GB) | 8 | ~32GB |
| A100 (80GB) | 16 | ~60GB |

For RunPod, use `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`.

## Output Structure

```
models/
├── intent-mapper-lora/          # LoRA adapter weights
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── training_args.json
└── intent-mapper-merged/        # Merged model (optional)
    ├── config.json
    ├── model.safetensors
    └── tokenizer/
```

## Integration

After training, update `sparta-intent` skill to use the model:

```python
from sparta_intent.inference import IntentMapper

mapper = IntentMapper(
    model_path="models/intent-mapper-lora",
    use_llm=True
)
result = mapper.infer("How do I detect command injection?")
```

## Monitoring

Training logs are saved to `logs/` and optionally to Weights & Biases.

```bash
# View training progress
./run.sh logs

# TensorBoard (if enabled)
./run.sh tensorboard
```
