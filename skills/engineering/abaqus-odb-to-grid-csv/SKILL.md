---
name: abaqus-odb-to-grid-csv
description: Convert per-case Abaqus FEA outputs into ML-ready (X, Y) wide-table CSVs. Pivots irregular FEA mesh node displacements onto a regular N×N grid via direct binning (structured mesh) or bilinear resampling, picks the final frame as the deformation target, and aggregates across many cases into X_amplitude.csv (design vectors) + Y_grid_uz.csv (flattened grid displacement). Use when the user has a folder of completed FEA cases and wants to train a Ridge / MLP / Gaussian Process surrogate on the (input → displacement field) mapping.
difficulty: intermediate
category: engineering-simulation
tags: [abaqus, fea, finite-element, simulation, machine-learning, data-pipeline, mesh-resampling]
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

# Abaqus ODB → ML-Ready Grid CSV

The post-processing half of a surrogate-model pipeline. Takes a folder of completed Abaqus FEA cases (typically produced by the **abaqus-lhs-batch-dataset** skill) and produces two flat CSVs ready for `numpy.loadtxt` / `pandas.read_csv` / scikit-learn:

- **`X_amplitude.csv`** — `sample_id, amplitude_0000, amplitude_0001, ..., amplitude_(D-1)` — the input design vectors
- **`Y_grid_uz.csv`** — `sample_id, uz_0000, uz_0001, ..., uz_(N²-1)` — the resulting deformation field flattened from N×N grid (row-major)

These are the two matrices a surrogate model trains on: shape `(N_samples, D)` and `(N_samples, N²)`.

## When to Use This Skill

Activate when the user wants to:
- Convert a directory of `sample_*/Membrane2D1.odb` (or `node_displacement.csv`) cases into ML-ready training matrices
- Resample a fine FEA mesh (e.g. 81×81) onto a coarser learning grid (e.g. 41×41 or 21×21)
- Aggregate multiple dataset runs and deduplicate by input vector
- Inspect / validate a dataset before training

Do NOT use this skill for:
- Single-case ODB inspection (use `abaqus-odb` instead)
- Time-series outputs where you need every frame (this skill takes the **final frame** by default)
- Stress / strain field extraction (this skill is targeted at displacement; extending to other fields is straightforward, see below)

## The Two Mesh-to-Grid Paths

### Path A — Structured FEA mesh (preferred, fast)

The FEA mesh is a regular grid (e.g. 81×81 nodes for a square membrane), and you want to either keep it or downsample to a smaller learning grid. This is the case for membrane / plate problems where you set the mesh seed to give exact node spacing.

**Steps:**
1. Detect mesh size: `unique(x0)` and `unique(y0)` from `node_displacement.csv` give `MESH_N`
2. Use rounded `(x0, y0)` as a hash key → directly bin each node into a `(MESH_N, MESH_N)` array
3. If `target_N != MESH_N`: bilinear resample to `(target_N, target_N)` using **precomputed** weights (10-100× faster than `scipy.interpolate`)
4. Flatten row-major to length `target_N²`

**Latency:** ~50 ms / case. 1000 cases = ~1 minute.

### Path B — Unstructured FEA mesh (fallback)

The FEA mesh is unstructured (tet / triangular / mixed). Need scattered interpolation.

**Steps:**
1. Stack `(x0, y0, uz)` from final frame
2. Build a regular target grid: `linspace(x_min, x_max, N)` × `linspace(y_min, y_max, N)`
3. `scipy.interpolate.griddata((x0, y0), uz, (xq, yq), method="linear")`
4. Fill NaNs (outside-hull points) with 0 or nearest-neighbor value
5. Flatten row-major

**Latency:** ~1-3 s / case. 1000 cases = ~30 minutes. Requires scipy.

## Required Inputs

The user must provide:

1. **Dataset root** — A folder produced by a batch FEA run, with subfolders `sample_*/` each containing:
   - `node_displacement.csv` — produced by the Abaqus solver script. Schema: `frame_id, time, node_id, x0, y0, z0, ux, uy, uz, x_def, y_def, z_def`
   - `input_vector.csv` (or `ForceAmplitude.dat`) — the design vector for that case
   - `dataset_index.csv` (at the dataset root) — the per-case status log; only `status == "completed"` cases are processed

2. **Target grid size `N`** — typically 21, 41, or 81 nodes per side. If `N` matches the FEA mesh, no resampling is done.

3. **Frame selection** — by default, the last frame (final deformed state). For dynamic problems, the user may want a specific time or all frames.

## Workflow Steps

### Step 1 — Scan and validate

```python
dataset_root = Path(...)
index = pd.read_csv(dataset_root / "dataset_index.csv")
completed = index[index["status"] == "completed"]
```

Reject the run if `< 80%` of planned cases completed — surface the failure rate to the user.

### Step 2 — Detect mesh structure (one-time)

Open the first completed case's `node_displacement.csv`. Count unique `x0` and `y0` (rounded to 2 decimals to absorb floating-point noise). If `len(unique_x) * len(unique_y) == NODES_PER_FRAME`, the mesh is **structured** (Path A). Otherwise **unstructured** (Path B).

### Step 3 — Per-case extraction

For each completed case (in parallel via `ThreadPoolExecutor` or serially):

1. Read input vector → shape `(D,)`
2. Read final frame from `node_displacement.csv`:
   - Fast path: `tail -NODES_PER_FRAME` (Linux/macOS) or read whole file + filter by `frame_id == max_frame_id`
3. Extract `(x0, y0, uz)` columns
4. Apply Path A or Path B to produce `(target_N, target_N)` displacement field
5. Flatten row-major to `(target_N²,)`
6. Append to in-memory accumulator

### Step 4 — Aggregate + deduplicate

- Stack all input vectors into `X` of shape `(N_completed, D)`
- Stack all flattened grids into `Y` of shape `(N_completed, target_N²)`
- Optional: deduplicate identical input vectors using `numpy.unique` with `return_index=True`. **Why dedupe**: identical inputs but slightly different outputs (numerical noise) can confuse the regularization; pick one representative per input.
- Write CSVs:
  - `X_amplitude.csv` — header `sample_id, amplitude_0000, ..., amplitude_(D-1)`
  - `Y_grid_uz.csv` — header `sample_id, uz_0000, ..., uz_(target_N²-1)`
  - `sample_meta.csv` — `sample_id, source_dataset, source_case, length, width, thickness, mesh_n, frame_id` for provenance

### Step 5 — Quick QC

Print:
- `N_completed = ?, N_dedup = ?`
- `Y` percentiles: `p1, p50, p99` — sanity check the displacement range is reasonable (no `nan` / `inf`)
- Top-5 largest `|uz|` cases — visually inspect to make sure they aren't obviously diverged

## Critical Implementation Details

### 1. Node coordinates may not align exactly across cases
Floating-point: a node nominally at `x = 1.0` may show up as `0.99999998` in one case and `1.00000002` in another. **Always round** `x0, y0` to the nearest `mesh_pitch / 100` (e.g. `np.round(x0, 2)` for mm-scale meshes). Otherwise the unique-coordinate detection will fail.

### 2. The final frame is **not always** the last row
Some Abaqus output configurations write the initial (zero) frame at the start, the loading frames, and a final equilibrium frame. **Always select by `max(frame_id)`**, not by tail-N.

### 3. Bilinear resample weights are precomputable
For a fixed `MESH_N → target_N` mapping, the per-target-cell `(idx0, idx1, frac)` weights only depend on the grid sizes. Precompute once and reuse for all cases:

```python
def precompute_bilinear_weights(src_n, dst_n):
    indices_0 = np.empty(dst_n, dtype=np.int32)
    indices_1 = np.empty(dst_n, dtype=np.int32)
    fracs = np.empty(dst_n, dtype=np.float64)
    for i in range(dst_n):
        s = i * (src_n - 1) / (dst_n - 1)
        i0 = int(s)
        i1 = min(i0 + 1, src_n - 1)
        indices_0[i] = i0
        indices_1[i] = i1
        fracs[i] = s - i0
    return indices_0, indices_1, fracs
```

Then per-case bilinear is a vectorized numpy operation, **no Python loop over grid cells**.

### 4. Handle large `node_displacement.csv` files efficiently
Each file is per-frame × per-node × 12 columns. For 81×81 mesh × 20 frames × 12 cols × ~30 bytes ≈ 47 MB per case. Reading the full file with `csv.DictReader` is slow.

**Fast read**: skip to the last `NODES_PER_FRAME` lines via `subprocess.run(["tail", "-N", path])` (Linux/macOS only). On Windows, use `numpy.genfromtxt` with `skip_header=` set to `(num_frames - 1) * NODES_PER_FRAME + 1`. Even faster: have the FEA solver script output ONLY the final frame to a separate file like `final_frame.csv`, eliminating the parse step.

### 5. Memory budget
- `Y` for 1000 samples × 21×21 grid = `1000 × 441 × 8 bytes` = 3.5 MB → fine in memory
- `Y` for 10,000 samples × 81×81 grid = `10000 × 6561 × 8 bytes` = 525 MB → still in memory, but write CSV incrementally
- For larger sizes: write each row to disk immediately (no in-memory accumulator)

### 6. Failure modes
- **Mismatched dimensions**: a case has `len(unique_x) != MESH_N` — log and skip, don't crash
- **NaN in `uz`**: solver diverged silently. Should never happen if `dataset_index.csv` says "completed", but check `np.isfinite(uz).all()` per case anyway
- **Missing `input_vector.csv`**: fall back to parsing `ForceAmplitude.dat` directly (the `*Amplitude` value lines)

## Reference Implementation

`references/extract_grid.py` (~250 lines) — full pipeline as a CLI:

```bash
python extract_grid.py \
    --dataset-root ./datasets/lhs_20260427_120000 \
    --output-dir ./aggregated/v1 \
    --target-grid-n 21 \
    --frame final \
    --dedupe-by-input
```

`references/grid_resample.py` — bilinear resample with precomputed weights, structured-mesh detection, and unstructured-mesh fallback (scipy-only).

## Output Schema

```
output_dir/
├ X_amplitude.csv         # sample_id, amplitude_0000..(D-1)
├ Y_grid_uz.csv           # sample_id, uz_0000..(N²-1)
├ sample_meta.csv         # sample_id, source_case, mesh_n, frame_id, max_abs_uz, ...
└ aggregate_summary.csv   # n_total, n_completed, n_dedup, mesh_n, target_n, dedupe_method, ...
```

## Extension Hooks

The skill is written for `uz` (out-of-plane displacement) but extending to other fields is mechanical:

- **In-plane displacement**: read `ux, uy` columns instead → produce `Y_grid_ux.csv` + `Y_grid_uy.csv`
- **Stress**: requires the FEA solver script to output element stress (e.g. S22, Mises) at element centroids, then the same binning + resampling pattern
- **Time-series targets**: instead of selecting `max(frame_id)`, keep all frames and produce `Y_grid_uz_t<frame_id>.csv` per frame
- **Multi-target stacking**: concatenate `[Y_grid_ux, Y_grid_uy, Y_grid_uz]` column-wise → 3N² output dim

## Quick Sanity Checks

After producing `X_amplitude.csv` and `Y_grid_uz.csv`:

1. **Shape match**: `len(X) == len(Y)` and both index by the same `sample_id`
2. **Y range**: `Y.abs().max()` between sane bounds (not `inf`, not `0`)
3. **Linear fit baseline**: train a Ridge with `alpha=1.0` and check `R²` on a 80/20 split. Should be > 0.9 for well-behaved problems. R² < 0.5 implies the design space is too noisy or the FEA setup is suspect — surface this to the user.
4. **Dedup ratio**: if `n_dedup / n_total < 0.7`, the design space sampler is producing too many duplicates — narrow the precision threshold or use a different sampler.
