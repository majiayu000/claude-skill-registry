---
name: gpt-lab
description: >
  Benchmark and compare small GPTs for task-specific inference. Tests base, fine-tuned,
  and prompted models against shared eval datasets. Finds minimum viable model,
  compares fine-tuned vs prompted, and generates reports.
allowed-tools: Bash, Read
triggers:
  - benchmark gpt models
  - compare gpt models
  - gpt lab benchmark
  - find minimum model
  - compare fine-tuned vs prompted
  - model benchmarking
  - gpt evaluation
metadata:
  short-description: Benchmark and compare small GPTs for task-specific inference
provides:
  - skill-creation
composes:
  - scillm
  - memory
  - create-gpt
  - create-figure
  - task-monitor

taxonomy:
  - creation
  - training
  - benchmarking
---

# GPT Lab

Benchmark and compare small GPTs trained by `/create-gpt` against prompted alternatives.
Answers the key question: **"Is fine-tuning worth it for this task?"**

## Quick Start

```bash
cd .pi/skills/gpt-lab

# Benchmark multiple models on a task
./run.sh benchmark --task qra-validator --models "qwen2.5-0.5b,qwen2.5-1.5b"

# Find the smallest model meeting a threshold
./run.sh find-minimum --task qra-validator --threshold 0.85

# Compare fine-tuned vs prompted
./run.sh compare --task qra-validator \
  --finetuned ../create-gpt/models/qra-validator/model.gguf \
  --prompted deepseek-v3.2

# Profile a single model
./run.sh profile --model ../create-gpt/models/qra-validator/model.gguf --samples 100

# Generate report
./run.sh report --task qra-validator --format markdown
```

## Commands

```bash
./run.sh benchmark --task NAME --models "model1,model2,..."
./run.sh compare --task NAME --finetuned PATH --prompted MODEL_NAME
./run.sh find-minimum --task NAME --threshold FLOAT
./run.sh profile --model PATH --samples N
./run.sh report --task NAME [--format markdown|json]
./run.sh history --task NAME
```

## Fine-Tuned vs Prompted Verdict

```
accuracy delta < -5%                          → NOT_WORTH_IT
accuracy delta >= -2% AND speedup >= 5x       → WORTH_IT
otherwise                                     → MARGINAL
```

## Integration

- **`/create-gpt`**: Trains the models that this skill benchmarks
- **`/scillm`**: Provides prompted baseline via Chutes API
- **`/prompt-lab`**: find-minimum pattern adapted from this skill
- **`/classifier-lab`**: Benchmark engine pattern adapted from this skill
