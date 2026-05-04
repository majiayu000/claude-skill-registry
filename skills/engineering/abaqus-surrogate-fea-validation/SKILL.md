---
name: abaqus-surrogate-fea-validation
description: Closed-loop inverse-design validation. Given a target deformation field, solve the inverse problem on a trained surrogate (Ridge / linear), then run an Abaqus FEA verification and compare surrogate-predicted vs. true displacement field. Reports MSE / MAE / max-abs-error / NRMSE side-by-side, plus saturated-channel count, so you can quantify the surrogate-FEA gap. Use when the user wants to evaluate "is my surrogate good enough for inverse design?", "how big is the surrogate-FEA gap on this target?", "did the optimizer find a real solution or just a surrogate hallucination?"
difficulty: intermediate
category: engineering-simulation
tags: [abaqus, fea, finite-element, simulation, surrogate-model, inverse-design, validation, ridge, l-bfgs-b]
platforms: [claude, openclaw, opencode, cursor, codex, cline]
quality: community
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Abaqus Surrogate ↔ FEA Validation Loop

Closes the verification loop on a surrogate-driven inverse design. Surrogates are fast but optimistic — they extrapolate, hallucinate, and reward saturated solutions that the real FEA cannot reproduce. This skill **forces a side-by-side comparison** between what the surrogate thinks it found and what Abaqus actually delivers, on the same target shape.

## When to Use This Skill

Activate when the user wants to:
- Sanity-check a surrogate that was just trained ("is the model trustworthy?")
- Quantify the **surrogate-FEA gap** on a fixed set of validation targets before publishing claims
- Compare optimizer choices (PGD vs. L-BFGS-B vs. multi-start) under equal-FEA-budget conditions
- Generate a reproducible benchmark table for a paper / report
- Debug why an optimizer's surrogate solution looks great but FEA verification fails

Do NOT use this skill for:
- Forward-only FEA runs without a surrogate (use `abaqus-lhs-batch-dataset`)
- Surrogate **training** (this skill assumes `X_amplitude.csv` + `Y_grid_uz.csv` already exist; pair with the dataset / grid skills upstream)
- Real-time hardware-in-the-loop (FEA validation is too slow; use a different loop)

## The Loop

```
target shape (N x N csv)
        │
        │  load + bilinear resample to learning grid
        │  scale to reachable peak amplitude
        ▼
  y_target  (flattened, N²)
        │
        │  standardize with (y_mean, y_std) from training data
        ▼
  y_target_std
        │
        │  solve  argmin_z  ||z @ W - y_target_std||² + λ ||z||²
        │   subject to  z_lo ≤ z ≤ z_hi   (standardized box constraint)
        │   solver ∈ { PGD, L-BFGS-B, multistart L-BFGS-B, Nelder-Mead }
        ▼
  z_sol (standardized solution)
        │
        │  unstandardize: x_sol = z_sol * x_std + x_mean
        │  hard-clip to [bounds_min, bounds_max]
        ▼
  x_sol (the design vector to physically realize)
        │
        ├──── surrogate forward predict ────► y_pred
        │                                       │
        │                                       │  vs. target
        │                                       ▼
        │                                  surrogate_metrics
        │                                  (MSE, MAE, max_abs, NRMSE)
        │
        ├──── write ForceAmplitude.dat
        │     copy_template_inputs(template_dir, case_dir)
        │     subprocess: abaqus cae noGUI="<solver_script>"
        │     extract_grid(node_displacement.csv, N, N)
        │                                       │
        │                                       │  vs. target
        │                                       ▼
        │                                  true_metrics
        │                                  (MSE, MAE, max_abs, NRMSE)
        ▼
  summary.csv:  surrogate_metrics + true_metrics + saturated_channels + return_code
```

The key signal is the **gap** between `surrogate_metrics` and `true_metrics`. A small gap means the surrogate is faithful; a large gap means it's overfitting or extrapolating into unphysical regions.

## Required Inputs

The user must provide:

1. **Aggregated training data** (typically from the `abaqus-odb-to-grid-csv` skill upstream):
   - `X_amplitude.csv` — `sample_id, amplitude_0000..amplitude_(D-1)`
   - `Y_grid_uz.csv` — `sample_id, uz_0000..uz_(N²-1)`

2. **Target shape file(s)** — one or more N×N CSV / TXT matrices of the desired deformation field. Common formats:
   - Plain matrix CSV (no header, N rows × N columns)
   - Headered CSV with `uz_0000..uz_(N²-1)` columns (single row)

3. **`template_dir/` + `solver_script.py`** — same as the `abaqus-lhs-batch-dataset` skill. Required for the FEA verification step.

4. **Design bounds** `[bounds_min, bounds_max]` (e.g. `[-0.5, +0.5]`) — must match the bounds the training data was sampled from. Mismatched bounds will produce saturated solutions that the FEA cannot realize.

5. **Target peak amplitude** — most published targets are normalized. Scale them to a peak the surrogate's training range can actually produce (e.g. `target_peak = 2.5` mm if training data uz spans ±3 mm).

## The 4 Inverse Solvers

For a **linear** Ridge surrogate `y_std = z @ W`, the inverse problem is convex quadratic. Pick the solver based on your needs:

| Solver | When to use | Iters / cost | Notes |
|---|---|---|---|
| **PGD** | Fastest, deterministic, no scipy needed | 1200 fixed steps | Good baseline; sensitive to `lr`. Default for stdlib-only environments. |
| **L-BFGS-B** | Best convergence per iteration; needs scipy | ~50-200 iters | Initialize from closed-form solution; converges in O(D) on linear surrogates. **Recommended default.** |
| **multistart L-BFGS-B** | Avoids saddle / boundary local minima | n_starts × ~100 iters | Use when D is large (>50) or bounds are tight (`saturated_channels > D/4`). |
| **Nelder-Mead** | Derivative-free fallback; debug only | 5000 fevals | Slowest, no gradient; only useful when you suspect bugs in the gradient path. |

For **nonlinear** surrogates (MLP), only L-BFGS-B and Nelder-Mead are practical (the closed-form initialization step doesn't apply).

## Workflow Steps

### Step 1 — Fit / load surrogate

```python
X = read_matrix_csv("X_amplitude.csv", "amplitude")    # (N_samples, D)
Y = read_matrix_csv("Y_grid_uz.csv", "uz")             # (N_samples, N²)
x_mean, x_std = fit_standardizer(X)
y_mean, y_std = fit_standardizer(Y)
W = train_ridge((X - x_mean) / x_std, (Y - y_mean) / y_std, alpha=1.0)
```

The Ridge weights `W` of shape `(D, N²)` constitute the **standardized** linear surrogate.

### Step 2 — Per target

For each target file:

1. Load matrix, bilinear-resample to the learning grid (`N×N`), scale to `target_peak`
2. Flatten + standardize: `y_target_std = (y_target - y_mean) / y_std`
3. Standardize design bounds: `z_lo = (x_lo - x_mean) / x_std`, similarly `z_hi`
4. Solve inverse with the chosen solver → `z_sol`
5. Unstandardize: `x_sol = z_sol * x_std + x_mean`, then hard-clip to `[bounds_min, bounds_max]`

### Step 3 — Surrogate-side metrics

```python
y_pred_std = z_sol @ W
y_pred = y_pred_std * y_std + y_mean
surrogate_metrics = mse_mae_max(y_pred, y_target, normalize="target_max_abs")
# NRMSE = sqrt(mse) / max(|y_target|), reported as norm_mse
```

### Step 4 — FEA verification

```python
case_dir = work_root / target_name
copy_template_inputs(template_dir, case_dir)
write_force_amp(case_dir / "ForceAmplitude.dat", x_sol)   # the same *Amplitude format
rc, elapsed, err = run_one_case(case_dir, solver_script, timeout_s=3600)

if rc == 0 and (case_dir / "node_displacement.csv").exists():
    final_frame_id, y_true_flat = extract_grid(case_dir / "node_displacement.csv", N, N)
    true_metrics = mse_mae_max(y_true_flat, y_target, normalize="target_max_abs")
```

### Step 5 — Side-by-side report

Per target: write `summary.csv` with **both** `surrogate_*` and `true_*` metrics + `saturated_channels` + `return_code` + `elapsed_seconds`.

Across all targets: aggregate into `surrogate_inverse_summary.csv`. The columns make a publication table directly:

```
target_name | scale_factor | surrogate_mse | surrogate_mae | surrogate_norm_mse | true_mse | true_mae | true_norm_mse | saturated_channels | return_code | elapsed_seconds
```

## Critical Implementation Details

### 1. Standardization MUST be consistent
The same `(x_mean, x_std, y_mean, y_std)` used during training must be used at validation. Saving them to a `.npz` next to the trained surrogate avoids skew.

### 2. Hard-clip after unstandardize
`z_sol` lives in standardized space and respects `(z_lo, z_hi)`. After converting back to `x_sol`, **always re-clip** to `[bounds_min, bounds_max]` because numerical drift can produce values like `0.5000001` that would crash the FEA's amplitude validation.

### 3. `saturated_channels` is the early-warning metric
Count entries within `tol=1e-6` of the bounds. **If > D/4 channels are saturated**, the surrogate is asking the optimizer to extrapolate beyond the training distribution. The FEA will likely diverge or produce nonsense. Lower `target_peak` and re-run; don't trust either set of metrics in this regime.

### 4. NRMSE normalization choice
`norm_mse = mse / max(|y_target|)²` (the `target_max_abs` mode) makes errors directly comparable across targets of different magnitudes. **Always specify the normalization** in any reported number. Other valid choices: `target_range = max(y_target) - min(y_target)`.

### 5. The 4 modes of failure
| Mode | Symptom | Diagnosis |
|---|---|---|
| **Surrogate hallucination** | small surrogate_mse, large true_mse | Saturated channels, training data too narrow, or nonlinearity not captured |
| **FEA divergence** | rc != 0, true metrics = NaN | Amplitudes too aggressive — reduce `target_peak` or tighten bounds |
| **Both fail** | both metrics large | Target shape itself unreachable in the design space; check whether the basis can express it at all |
| **Both succeed but disagree** | small surrogate_mse, small true_mse, but predicted-uz heatmap differs from FEA-uz heatmap | Mode-mixing — the L-BFGS-B found a local optimum the surrogate likes but the FEA reaches differently. Try multi-start. |

### 6. FEA cost dominates total runtime
Surrogate inverse solve takes ~milliseconds. Each FEA verification takes 2-5 minutes. **Cache the surrogate fit** (write Ridge weights to `model_ridge.npz` once) and reuse across targets. Do not re-fit on every target.

### 7. Reproducibility
Set `numpy.random.seed(42)` for any solver with stochastic initialization (multi-start). Record the seed in `summary.csv`. Without this, the multi-start results are not reproducible across runs.

## Reference Implementation

A complete, dependency-light Python implementation is in `references/surrogate_validation.py` (~400 lines). It supports all 4 solvers, is parameterized via argparse, and produces the side-by-side summary CSV.

```bash
python surrogate_validation.py \
    --data-dir ./aggregated/v1 \
    --template-dir ./template_case \
    --solver-script ./MyAbaqusSolver.py \
    --work-root ./validation_runs \
    --grid-n 21 \
    --target-peak 2.5 \
    --bounds-min -0.5 --bounds-max 0.5 \
    --solver lbfgsb \
    --targets target_dome.csv target_saddle.csv target_gaussian.csv
```

`references/inverse_solvers.py` — the 4 inverse-solver implementations (PGD pure stdlib + numpy; L-BFGS-B / multi-start / Nelder-Mead via scipy).

## Output Schema

```
work_root/
├ surrogate_inverse_summary.csv      # one row per target, all metrics side-by-side
├ target_dome/
│   ├ target_scaled_NxN.csv          # the rescaled target the optimizer aimed at
│   ├ inverse_solution.csv           # x_sol + scale_factor + saturated_channels
│   ├ predicted_surrogate_NxN.csv    # what the surrogate said x_sol would produce
│   ├ predicted_true_NxN.csv         # what Abaqus actually produced (final frame)
│   ├ ForceAmplitude.dat             # the per-case design vector for FEA
│   ├ Membrane2D1.odb                # FEA result
│   ├ node_displacement.csv          # raw Abaqus output
│   ├ summary.csv                    # all metrics for this target
│   └ run_*.log
├ target_saddle/
└ ...
```

The 3 NxN CSVs (`target_scaled`, `predicted_surrogate`, `predicted_true`) are designed for direct heatmap plotting via `matplotlib.imshow`. Their per-cell errors are the most diagnostic visualization for "is the surrogate trustworthy" questions.

## Quick Sanity Checks

After a validation run completes:

1. **Saturation rate**: average `saturated_channels / D` across targets — if > 30%, your bounds or target_peak are wrong, redo with tighter peak before trusting any metric
2. **Gap statistics**: `mean(true_norm_mse) / mean(surrogate_norm_mse)` — if > 3.0, the surrogate is over-confident; consider an MLP or richer feature basis
3. **FEA success rate**: `sum(return_code == 0) / N_targets` — should be > 90%; if lower, diagnose `run_stderr.log` of failures (typically convergence / mesh distortion)
4. **Spot-check**: pick one target with the largest gap, plot the 3 heatmaps side-by-side. The error structure (smooth offset / oscillation / boundary artifact) tells you whether to add training data, regularize more, or change the surrogate class.

## Pairs Well With

- **`abaqus-lhs-batch-dataset`** (upstream): produces the `sample_*/` directories
- **`abaqus-odb-to-grid-csv`** (upstream): produces the `X_amplitude.csv` + `Y_grid_uz.csv` this skill consumes
- **`abaqus-job`** / **`abaqus-odb`** (peer skills from JaimeCernuda/abaqus-scripting): for hand-debugging individual failed validation cases
