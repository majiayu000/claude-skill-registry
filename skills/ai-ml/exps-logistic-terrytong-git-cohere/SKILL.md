---
name: exps-logistic
description: Documentation for the logistic regression MI estimation experiment (exps_logistic)
---

# exps_logistic - Logistic Regression MI Estimation

## Purpose
Measure mutual information (MI) lower bound between CoT rationales and problem parameters using multinomial logistic regression on embeddings. Compares code vs NL representations.

## Key Files
| File | Purpose |
|------|---------|
| `src/exps_logistic/main.py` | Main experiment runner |
| `src/exps_logistic/config.py` | Configuration, CLI args, kind presets |
| `src/exps_logistic/data_utils.py` | Data loading, gamma label creation |
| `src/exps_logistic/classifier.py` | Logistic regression classifier |
| `src/exps_logistic/featurizer.py` | Embedding extraction (BERT, TF-IDF) |
| `src/exps_logistic/run.sh` | Dev script for single model |
| `src/exps_logistic/prod_logistic.sh` | Production script for all models |
| `src/exps_logistic/notebooks/generate_plots.py` | Plot generation |

## Kind Presets (in config.py)

```python
FG_KINDS = {"add", "sub", "mul", "lcs", "knap", "rod", "ilp_assign", "ilp_prod", "ilp_partition"}

CLRS_KINDS = {
    "activity_selector", "articulation_points", "bellman_ford", "bfs",
    "binary_search", "bridges", "bubble_sort", "dag_shortest_paths",
    "dfs", "dijkstra", "find_maximum_subarray_kadane", "floyd_warshall",
    "graham_scan", "heapsort", "insertion_sort", "jarvis_march",
    "kmp_matcher", "lcs_length", "matrix_chain_order", "minimum",
    "mst_kruskal", "mst_prim", "naive_string_matcher", "optimal_bst",
    "quickselect", "quicksort", "segments_intersect",
    "strongly_connected_components", "task_scheduling", "topological_sort",
}

NPHARD_KINDS = {"edp", "gcp", "ksp", "spp", "tsp"}

EXTENDED_KINDS = FG_KINDS | CLRS_KINDS | NPHARD_KINDS  # 44 total kinds
```

## Gamma Labels
Format: `{kind}|d{digits}|b{bin}` (e.g., `knap|d8|b24`)
- Fine-grained kinds have parsed bin values based on problem parameters
- CLRS/NP-hard kinds get `bNA` (no fine-grained parsing)

## CLI Arguments
| Arg | Description |
|-----|-------------|
| `--results-dir` | Path to exps_performance results |
| `--models` | Model filter (e.g., `anthropic/claude-haiku-4.5`) |
| `--rep` | Representation: `code` or `nl` |
| `--label` | Label type: `kind`, `theta_new`, or `gamma` |
| `--kinds-preset` | Kind filter: `fg`, `clrs`, `nphard`, or `extended` |
| `--feats` | Featurizer: `hf-cls`, `tfidf`, `st`, `openai` |
| `--embed-model` | HuggingFace model for embeddings |
| `--no-cv` | Disable cross-validation |
| `--bits` | Report cross-entropy in bits |

## Generated Plots (in `src/exps_logistic/notebooks/`)
| Plot | Description |
|------|-------------|
| `boxplot_extended.png` | Code vs NL MI comparison |
| `kde_extended.png` | KDE density comparison |
| `mi_vs_accuracy_extended.png` | MI vs task accuracy correlation |
| `contrast_extended.png` | Per-model contrast (code - nl) |
| `label_dist_by_kind.png` | Sample counts by problem kind |
| `label_dist_by_digits.png` | Fine-grained distribution by digits |
| `label_dist_heatmap.png` | Kind × Digits heatmap |
| `label_dist_top30.png` | Top 30 most frequent labels |
| `label_dist_zipf.png` | Zipf-like frequency distribution |
| `label_dist_pie.png` | Category breakdown pie chart |

## Key Results (Extended Kinds - Jan 9, 2026)
- **28 successful runs** across 6 models
- **Pearson r = 0.486, p = 0.009** (MI vs accuracy correlation)
- **500 unique labels** across 44 problem kinds
- Code representation shows higher MI lower bounds than NL
- Models tested: claude-haiku-4.5, gemini-2.5-flash, gpt-4o-mini, llama-3.1-405b-instruct, ministral-14b-2512, qwen-2.5-coder-32b-instruct

## Running Commands
```bash
# Dev run (single model)
bash src/exps_logistic/run.sh

# Production run (all models, all seeds)
bash src/exps_logistic/prod_logistic.sh

# Generate plots
uv run --no-sync python src/exps_logistic/notebooks/generate_plots.py
```
