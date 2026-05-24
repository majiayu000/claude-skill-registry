---
name: abaqus-lhs-batch-dataset
description: Generate an Abaqus FEA training dataset for surrogate / ML models. Latin Hypercube Sampling (or sparse-pattern sampling) over a parameterized design vector, one case folder per sample, batch-submit Abaqus jobs via subprocess, recover from crashes, and write a unified dataset index. Use when the user wants to "build a training set for a surrogate model", "sweep design parameters in Abaqus", "run N FEA simulations", or "sample a design space".
difficulty: intermediate
category: engineering-simulation
tags: [abaqus, fea, finite-element, simulation, machine-learning, surrogate-model, latin-hypercube, dataset-generation]
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

# Abaqus LHS Batch Dataset Generator

End-to-end workflow for producing FEA training datasets from a parameterized Abaqus model. Designed for **surrogate model training** (Ridge, MLP, Gaussian Process, etc.) where you need hundreds to thousands of FEA samples covering a design space.

## When to Use This Skill

Activate when the user wants to:
- Build a training set for a surrogate / ML model from Abaqus FEA
- Sweep a multi-dimensional design vector (e.g. force amplitudes, geometry parameters, material properties)
- Run N independent Abaqus jobs in batch with progress tracking and crash recovery
- Generate inputs for inverse-design / topology-optimization pipelines

Do NOT use this skill for:
- Single-case Abaqus runs (use `abaqus-job` instead)
- Parametric sweeps that don't need ML-ready CSV output (use `abaqus-job` + manual analysis)
- Optimization loops where each evaluation depends on the previous one (use a different driver)

## Core Pattern

```
template_dir/                       per-case_dir/                    dataset_root/
  ├ Parameters.dat       ──copy──>  ├ Parameters.dat                 ├ sample_design.csv  (the design matrix)
  ├ MaterialParams.dat              ├ MaterialParams.dat             ├ dataset_index.csv  (one row per case)
  ├ ChannelParams.dat               ├ ChannelParams.dat              ├ sample_00001/
  ├ InData.txt                      ├ InData.txt                     │   ├ ForceAmplitude.dat   <- NEW
  └ solver_script.py                ├ ForceAmplitude.dat   <- NEW    │   ├ Membrane2D1.odb
                                    ├ <run abaqus cae noGUI>         │   ├ node_displacement.csv
                                    ├ Membrane2D1.odb       <- new   │   ├ run_stdout.log
                                    ├ node_displacement.csv <- new   │   └ run_stderr.log
                                    └ run_*.log             <- new   ├ sample_00002/
                                                                     └ ...
```

The pattern is template-driven: you keep one **canonical case** with all the static input files (geometry, material, mesh, step parameters), and per sample you only overwrite the **design vector file** (e.g. `ForceAmplitude.dat`).

## Required Inputs

The user must provide:

1. **`template_dir/`** — A folder containing one **working Abaqus case** with all the static input files. Verify by running it once standalone and confirming the .odb is produced. Required files vary by setup, but typically include:
   - `Parameters.dat` — geometry (length, width, thickness, Es, μ)
   - `StepParameters.dat` — analysis step config (StepType, time, damping)
   - `MaterialParameters.dat` — material model
   - `ChannelParameters.dat` — design dimension (number of channels / patches / load regions)
   - `InData.txt` — driver flags (output mode, force-continuity flag)
   - Optional: `PatchGrid2D.dat`, `DisturbParameters.dat`

2. **`solver_script.py`** — The Abaqus/Python solver script that:
   - Reads the template `.dat` files
   - Reads the per-case design file (e.g. `ForceAmplitude.dat`)
   - Builds the model, submits the job, opens the ODB, and writes a per-node CSV (e.g. `node_displacement.csv` with columns `frame_id, time, node_id, x0, y0, z0, ux, uy, uz, x_def, y_def, z_def`)
   - Is invoked via `abaqus cae noGUI="<path>"` from inside the case dir

3. **Design dimension `D`** — number of free parameters per sample (e.g. 16 channels)

4. **Sampling strategy** + bounds (e.g. LHS in `[-0.5, +0.5]^16`)

## Sampling Strategies

Pick one (or combine) based on the design space:

| Strategy | When to use | Implementation |
|---|---|---|
| **LHS** (Latin Hypercube) | Dense, isotropic coverage of a continuous box | Stratified per-dim shuffle (no scipy needed) — see `references/sampling.py` |
| **Uniform random** | Baseline / sanity check | `random.uniform(lo, hi)` per dim |
| **Sparse-k** | Inverse problems with sparsity prior — k of D dims are non-zero | Random k-subset selection with discrete amplitude levels |
| **Single-active** | Channel-by-channel impulse response (basis dataset) | One non-zero entry, sweep over (channel × amplitude) |
| **Pair / block** | Local correlation patterns between adjacent design slots | Enumerate (i, j) adjacencies + amplitude sweeps |

Combine them: a typical surrogate dataset uses **600 LHS + 200 sparse-k + 200 single-active** = 1000 samples.

## Workflow Steps

When the user invokes you, do this:

### Step 1 — Read the template, validate
```bash
# Read ChannelParameters.dat → channel_num (= design dimension D)
# Read PatchGrid2D.dat (if present) → grid shape, boundary mode
# Verify all required files exist
```

### Step 2 — Generate the design matrix
- Build a list of (design_id, vector) tuples per the chosen strategy
- Deduplicate (use a string key from the rounded values to drop near-duplicates)
- Write `sample_design.csv` with header `design_id, active_count, amplitude_1, ..., amplitude_D`

### Step 3 — Per-sample case execution
For each sample `i = 1..N`:

1. `case_dir = dataset_root / f"sample_{i:05d}"`
2. Copy all files from `template_dir/` into `case_dir/` (`shutil.copy2`)
3. **Overwrite** `ForceAmplitude.dat` in `case_dir/` with the new design vector — this is the only file that changes between cases. Format (Abaqus *Amplitude blocks):
   ```
   *Amplitude, name=Amplitude       1
       0.000000000000000,    -0.376581075439650
       1.000000000000000,    -0.376581075439650
   *Amplitude, name=Amplitude       2
       0.000000000000000,     0.123456789012345
       1.000000000000000,     0.123456789012345
   ...
   ```
   For static loads, the two-point amplitude is constant. For ramp loading, set `(0, 0), (t_ramp, val), (1, val)`.
4. Run Abaqus with timeout via `subprocess.run`:
   ```python
   subprocess.run(
       'abaqus cae noGUI="<solver_script>"',
       cwd=str(case_dir),
       shell=True,
       text=True,
       capture_output=True,
       timeout=timeout_s,  # default 3600
   )
   ```
5. Capture `proc.returncode`, `proc.stdout` → `run_stdout.log`, `proc.stderr` → `run_stderr.log`, elapsed time
6. Detect success: `Membrane2D1.odb` exists AND `node_displacement.csv` exists AND `returncode == 0`
7. Append a row to `dataset_index.csv`:
   ```
   sample_id, design_id, case_folder, channel_num, grid_nx, grid_ny,
   amplitude_1, ..., amplitude_D,
   max_abs_uz, status, odb_exists, csv_exists, return_code, elapsed_seconds, error_msg
   ```

### Step 4 — Resume / retry support
- Before running a case, check if `dataset_index.csv` already has a `completed` row for that `sample_id` → skip if `--reuse-existing`
- For `failed` rows, optionally retry with longer timeout

### Step 5 — Report
- Print summary: `N completed / M total, mean elapsed = X s`
- List failed sample IDs for manual inspection of `run_stderr.log`

## Critical Implementation Details

### 1. Working directory MUST be the case dir
Abaqus reads `*.dat` files relative to the launch directory. Always set `cwd=case_dir` in `subprocess.run`. **NEVER** invoke the solver from the dataset root or template dir.

### 2. Abaqus must be on PATH
Verify with `abaqus --help` before starting. On Windows, the install adds `C:\SIMULIA\Commands` to PATH.

### 3. CPU contention
Each `abaqus cae` job uses 1 CPU by default. Running batch jobs **serially** is the simplest correct approach. For parallelism, ensure `numCpus * concurrent_jobs ≤ physical_cores` and watch out for license token contention.

### 4. Disk usage
Each case generates ~50-200 MB (`.odb` + `.dat` + `.csv` + lockfiles). For 1000 samples, plan for **100-200 GB**. Optionally delete `.odb` and intermediate files after extracting the per-node CSV (see the `abaqus-odb-to-grid-csv` skill).

### 5. Failure modes (in order of frequency)
- **License timeout**: solver hangs waiting for a token → use Abaqus's `lic_check_freq` env var or detect via `*** ERROR: TIMED OUT WAITING FOR LICENSE` in stderr
- **Convergence failure**: nonlinear solve diverges (typical with extreme amplitudes) → status = "failed", check `.msg` file
- **Mesh distortion**: too-large displacements warp elements past Jacobian threshold → reduce amplitude bounds or refine mesh
- **File lock / leftover .lck files**: previous crashed run left `*.lck` → script should `rm -f *.lck` before submitting
- **Time budget**: a single case taking > timeout_s → mark as `timeout`, increase per-case budget for retry

### 6. Reproducibility
Always seed the RNG (`random.Random(seed)`) and write the seed to `dataset_meta.json`. LHS with the same seed + same N gives identical samples.

## Reference Implementation

A complete, dependency-free Python implementation is in `references/batch_runner.py` (~400 lines). It's parameterized via argparse so it works as a CLI:

```bash
python batch_runner.py \
    --template-dir ./template_case \
    --solver-script ./MyAbaqusSolver.py \
    --dataset-root ./datasets \
    --strategy lhs \
    --n-samples 1000 \
    --bounds-min -0.5 \
    --bounds-max 0.5 \
    --seed 42 \
    --timeout-s 3600
```

The `references/sampling.py` module contains pure-stdlib LHS, sparse-k, single-active, pair-adj, and block-2x2 samplers.

## Output Schema

After a complete run:

```
datasets/run_YYYYMMDD_HHMMSS/
├ sample_design.csv         # design_id, active_count, amplitude_1..D
├ dataset_index.csv         # sample_id, design_id, ..., status, return_code, elapsed
├ dataset_meta.json         # seed, strategy, bounds, template path, abaqus version
├ sample_00001/
│   ├ ForceAmplitude.dat    # the per-case design vector
│   ├ Parameters.dat        # (copied from template)
│   ├ ...other .dat files
│   ├ Membrane2D1.odb       # the FEA result
│   ├ Membrane2D1.msg       # solver log
│   ├ node_displacement.csv # per-node ux/uy/uz per frame
│   ├ input_vector.csv      # (channel_id, amplitude_value)
│   ├ sample_summary.csv    # geometry + step metadata
│   ├ run_stdout.log
│   └ run_stderr.log
├ sample_00002/
└ ...
```

The next step in the pipeline is typically the **abaqus-odb-to-grid-csv** skill, which collapses each `node_displacement.csv` into a single row of a wide-table `Y_grid_uz.csv` (sample_id × N²), giving you ML-ready `(X, Y)` matrices.

## Quick Sanity Checks

After a run completes, ask the agent to verify:

1. **Index integrity**: `pandas.read_csv("dataset_index.csv")` — count `status == "completed"`
2. **Sample diversity**: max-pairwise-correlation of `sample_design.csv` rows — should be < 0.7 for LHS
3. **Output range**: `dataset_index.csv["max_abs_uz"]` distribution — should span at least 1 order of magnitude (else the design space is too narrow)
4. **Failed cases**: `cat sample_XXXXX/run_stderr.log` for the first 3 failures

If a high failure rate (> 5%) appears, narrow the design bounds or check the solver script — don't blindly retry.
