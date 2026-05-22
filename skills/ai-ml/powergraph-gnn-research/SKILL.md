---
name: powergraph-gnn-research
description: Research pipeline for topology-aware GNN representation learning on power grids using the PowerGraph benchmark. Use when (1) building physics-guided GNNs for power flow (PF), optimal power flow (OPF), or cascading failure prediction, (2) implementing self-supervised pretraining for power systems, (3) evaluating cascade explanation fidelity against ground-truth masks, or (4) conducting reproducible ML-for-power-systems research. Triggers include "PowerGraph", "power flow GNN", "OPF surrogate", "cascade prediction", "physics-guided GNN", "grid analytics ML", "power system representation learning".
---

# PowerGraph GNN Research Pipeline

**Primary claim**: A grid-specific self-supervised, physics-consistent GNN encoder improves PF/OPF learning (especially low-label/OOD), and transfers to cascading-failure prediction and explanation.

## Scripts

| Task | Script |
|------|--------|
| Data ingestion | `scripts/load_powergraph.py` |
| PF baseline | `scripts/train_pf_baseline.py` |
| Physics metrics | `scripts/physics_residual.py` |
| SSL pretraining | `scripts/pretrain_ssl.py` |
| Multi-task training | `scripts/train_multitask.py` |
| Explanation eval | `scripts/eval_cascade_explanation.py` |

## Workflow

1. **Data** → PowerGraph → PyG (PF/OPF node targets + cascade graph labels + exp masks)
2. **Baseline** → PF regression with sin/cos angles + physics residual metric
3. **Multi-task** → Shared encoder + PF/OPF/Cascade heads
4. **SSL** → Masked injection/edge reconstruction → fine-tune
5. **Evaluation** → Explanation AUC vs ground-truth masks + robustness tests

## Validity Anchors (Critical)

**Angle handling**: Predict `sin(θ), cos(θ)`, recover via `atan2`. Direct MSE on raw angles fails at ±π wrap-around.

**Physics residual**: Report KCL mismatch alongside accuracy. Ground truth ≈ 0, random >> 1.

**Blocked splits**: PowerGraph uses 1-year load @ 15-min. Use months 1-9 train / 10 val / 11-12 test. Random splits leak seasonal patterns.

**Explanation fidelity**: Use PowerGraph `exp.mat` ground-truth masks. Report AUC + Precision@K.

## Reference Docs

- `references/data_pipeline.md` — PowerGraph → PyG conversion, splits
- `references/model_architecture.md` — Physics-guided message passing, heads
- `references/ssl_pretraining.md` — Masked tasks, low-label experiments
- `references/uncertainty_quantification.md` — Ensembles, MC dropout, calibration
- `references/evaluation_protocols.md` — Metrics, robustness, statistical tests
- `references/publication_soundness.md` — Reviewer risks, claim framing
- `references/experiment_configs.md` — YAML config structure, sweeps

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Angle wrap-around | sin/cos representation |
| Data leakage | Blocked time splits |
| Cascade imbalance | Weighted/focal loss |
| OOM large grids | Gradient checkpointing |
| SSL collapse | Stop-gradient + EMA encoder |
| Physics violations | Residual regularization |

## Publication Checklist

- [ ] Ablation: single-task vs multi-task vs SSL+multi-task
- [ ] Low-label curves: 10/20/50/100% training data
- [ ] Physics residual alongside accuracy metrics
- [ ] Blocked splits (not random)
- [ ] Explanation AUC against exp.mat ground truth
- [ ] Robustness under edge-drop perturbations
- [ ] Statistical significance with 95% CI
- [ ] One-command reproducibility (`python analysis/run_all.py`)
