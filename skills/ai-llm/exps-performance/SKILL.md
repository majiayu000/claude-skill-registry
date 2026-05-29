---
name: exps-performance
description: Documentation for the main LLM performance experiments (exps_performance)
---

# exps_performance - Main Performance Experiments

## Purpose
Run LLM inference on algorithmic problems, collect CoT rationales and evaluate correctness.

## Key Files
| File | Purpose |
|------|---------|
| `src/exps_performance/main.py` | Main runner |
| `src/exps_performance/dataset.py` | Dataset definitions |
| `src/exps_performance/arms.py` | Evaluation arms (NL, code_sim, code_exec) |
| `src/exps_performance/llm.py` | LLM interface |
| `src/exps_performance/analysis.py` | Analysis and plotting |
| `src/exps_performance/noise.py` | Noise injection experiments |

## Results Structure
```
src/exps_performance/results/
  {model}_seed{seed}/
    tb/
      run_{timestamp}/
        res.jsonl  # Main results file
```

## res.jsonl Schema
| Field | Description |
|-------|-------------|
| `kind` | Problem type (e.g., "knap", "bellman_ford") |
| `digit` | Problem size/digits |
| `nl_correct` | NL evaluation result |
| `code_correct` | Code execution result |
| `sim_correct` | Code similarity result |
| `model` | Model name |
| `seed` | Random seed |

## Data Sources
- Performance results: `src/exps_performance/results/{model}_seed{seed}/tb/run_*/res.jsonl`
- Excludes `gsm8k` from accuracy calculations in logistic analysis

## Running Commands
```bash
# Run main experiment
uv run python src/exps_performance/main.py --model <model> --seed <seed>

# Run analysis
uv run python src/exps_performance/analysis.py
```
