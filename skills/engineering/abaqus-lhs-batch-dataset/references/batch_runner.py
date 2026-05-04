#!/usr/bin/env python3
"""
Batch Abaqus dataset generator.

Pattern:
    template_dir/  -> per-case copy
    overwrite ForceAmplitude.dat with new design vector
    abaqus cae noGUI=<solver_script>
    log return code, elapsed, output existence
    append one row to dataset_index.csv

Usage:
    python batch_runner.py \\
        --template-dir ./template_case \\
        --solver-script ./MyAbaqusSolver.py \\
        --dataset-root ./datasets \\
        --strategy lhs \\
        --n-samples 1000 \\
        --bounds-min -0.5 \\
        --bounds-max 0.5 \\
        --seed 42 \\
        --timeout-s 3600

Resume: re-running the same command with the same dataset name skips already-
"completed" cases (status == "completed" in dataset_index.csv).
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from sampling import (
    build_2x2_blocks_grid,
    build_adjacent_pairs_grid,
    build_single_active,
    make_sparse_vector,
    sample_lhs,
    sample_random_k_sparse,
    sample_uniform_random,
    vector_key,
)


REQUIRED_TEMPLATE_FILES = [
    "Parameters.dat",
    "StepParameters.dat",
    "MaterialParameters.dat",
    "ChannelParameters.dat",
    "InData.txt",
]
OPTIONAL_TEMPLATE_FILES = [
    "DisturbParameters.dat",
    "PatchGrid2D.dat",
    "ForceAmplitude.dat",
]


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_first_int(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            return int(s.split()[0])
    raise ValueError(f"empty file: {path}")


def write_force_amplitude(path: Path, amps: Sequence[float], ramp: bool = False, t_ramp: float = 0.02) -> None:
    """
    Write Abaqus *Amplitude blocks for the given design vector.

    Static (default): each channel gets a 2-point amplitude (0, val) -> (1, val).
    Ramp loading (ramp=True): (0, 0) -> (t_ramp, val) -> (1, val).
    """
    lines: List[str] = []
    for i, v in enumerate(amps, start=1):
        lines.append(f"*Amplitude, name=Amplitude{i:8d}")
        v = float(v)
        if ramp:
            lines.append(f"{0.0:25.15f},{0.0:25.15f}")
            lines.append(f"{float(t_ramp):25.15f},{v:25.15f}")
            lines.append(f"{1.0:25.15f},{v:25.15f}")
        else:
            lines.append(f"{0.0:25.15f},{v:25.15f}")
            lines.append(f"{1.0:25.15f},{v:25.15f}")
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def copy_template_inputs(template_dir: Path, case_dir: Path) -> None:
    for name in REQUIRED_TEMPLATE_FILES:
        src = template_dir / name
        if not src.exists():
            raise FileNotFoundError(f"missing required template file: {src}")
        shutil.copy2(src, case_dir / name)
    for name in OPTIONAL_TEMPLATE_FILES:
        src = template_dir / name
        if src.exists():
            shutil.copy2(src, case_dir / name)


def cleanup_locks(case_dir: Path) -> None:
    """Remove leftover Abaqus lock files from any previous crashed run."""
    for p in case_dir.glob("*.lck"):
        try:
            p.unlink()
        except OSError:
            pass


def run_one_case(case_dir: Path, solver_script: Path, timeout_s: float) -> Tuple[int, float, str]:
    cleanup_locks(case_dir)
    cmd = f'abaqus cae noGUI="{solver_script}"'
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(case_dir),
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_s,
        )
        elapsed = time.perf_counter() - t0
        (case_dir / "run_stdout.log").write_text(proc.stdout or "", encoding="utf-8")
        (case_dir / "run_stderr.log").write_text(proc.stderr or "", encoding="utf-8")
        return proc.returncode, elapsed, ""
    except subprocess.TimeoutExpired:
        return 124, time.perf_counter() - t0, "timeout"
    except Exception as err:  # noqa: BLE001
        return 1, time.perf_counter() - t0, str(err)


def compute_max_abs_uz_last_frame(node_csv: Path) -> float:
    """Quick QC metric: max |uz| in the last frame of node_displacement.csv."""
    if not node_csv.exists():
        return float("nan")
    with node_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rows = list(rd)
    if not rows:
        return float("nan")
    max_frame = -1
    for r in rows:
        try:
            fid = int(float(r["frame_id"]))
            if fid > max_frame:
                max_frame = fid
        except (KeyError, ValueError):
            continue
    if max_frame < 0:
        return float("nan")
    best = 0.0
    found = False
    for r in rows:
        try:
            if int(float(r["frame_id"])) != max_frame:
                continue
            uz = abs(float(r["uz"]))
        except (KeyError, ValueError):
            continue
        found = True
        if uz > best:
            best = uz
    return best if found else float("nan")


def parse_float_list(text: str) -> List[float]:
    return [float(s.strip()) for s in text.split(",") if s.strip()]


def parse_int_list(text: str) -> List[int]:
    return [int(s.strip()) for s in text.split(",") if s.strip()]


def build_design_matrix(args: argparse.Namespace, channel_num: int, grid_nx: int, grid_ny: int) -> List[Tuple[str, List[float]]]:
    rng = random.Random(args.seed)
    samples: List[Tuple[str, List[float]]] = []
    seen: set = set()

    def add(tag: str, vals: List[float]) -> None:
        key = vector_key(vals)
        if key in seen:
            return
        seen.add(key)
        samples.append((tag, vals))

    if args.strategy == "lhs":
        for i, vals in enumerate(sample_lhs(args.n_samples, channel_num, args.bounds_min, args.bounds_max, rng), start=1):
            add(f"lhs_{i:05d}", vals)
    elif args.strategy == "uniform":
        for i, vals in enumerate(sample_uniform_random(args.n_samples, channel_num, args.bounds_min, args.bounds_max, rng), start=1):
            add(f"uniform_{i:05d}", vals)
    elif args.strategy == "sparse":
        amp_levels = parse_float_list(args.amp_levels)
        for tag, vals in build_single_active(channel_num, amp_levels, args.sign_mode):
            add(tag, vals)
        for k in parse_int_list(args.random_k_values):
            for i, vals in enumerate(
                sample_random_k_sparse(rng, channel_num, k, args.random_count_per_k, amp_levels, args.sign_mode),
                start=1,
            ):
                add(f"randk{k}_{i:04d}", vals)
    else:
        raise ValueError(f"unknown strategy: {args.strategy}")
    return samples


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch Abaqus dataset generator (LHS / sparse / uniform).")
    p.add_argument("--template-dir", type=str, required=True)
    p.add_argument("--solver-script", type=str, required=True)
    p.add_argument("--dataset-root", type=str, default="datasets")
    p.add_argument("--run-name", type=str, default="")
    p.add_argument("--strategy", type=str, default="lhs", choices=["lhs", "uniform", "sparse"])
    p.add_argument("--n-samples", type=int, default=1000)
    p.add_argument("--bounds-min", type=float, default=-0.5)
    p.add_argument("--bounds-max", type=float, default=0.5)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--timeout-s", type=float, default=3600.0)
    p.add_argument("--reuse-existing", action="store_true", help="Skip cases already marked completed in dataset_index.csv")
    p.add_argument("--dry-run", action="store_true", help="Generate folders + ForceAmplitude.dat but skip Abaqus")
    # sparse strategy options
    p.add_argument("--amp-levels", type=str, default="0.10,0.20,0.35,0.50")
    p.add_argument("--sign-mode", type=str, default="both", choices=["both", "positive_only"])
    p.add_argument("--random-k-values", type=str, default="3,4")
    p.add_argument("--random-count-per-k", type=int, default=80)
    return p.parse_args()


def load_completed_ids(index_csv: Path) -> set:
    if not index_csv.exists():
        return set()
    out: set = set()
    with index_csv.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if str(row.get("status", "")).strip() == "completed":
                out.add(str(row.get("sample_id", "")).strip())
    return out


def main() -> int:
    args = parse_args()
    template_dir = Path(args.template_dir).resolve()
    solver_script = Path(args.solver_script).resolve()
    dataset_root = Path(args.dataset_root).resolve()

    if not template_dir.is_dir():
        raise FileNotFoundError(f"template-dir not found: {template_dir}")
    if not solver_script.is_file():
        raise FileNotFoundError(f"solver-script not found: {solver_script}")

    run_name = args.run_name.strip() or f"{args.strategy}_{now_stamp()}"
    dataset_dir = dataset_root / run_name
    ensure_dir(dataset_dir)

    channel_num = read_first_int(template_dir / "ChannelParameters.dat")
    grid_nx = grid_ny = int(round(channel_num**0.5))
    pgrid = template_dir / "PatchGrid2D.dat"
    if pgrid.exists():
        line0 = next((s.strip() for s in pgrid.read_text(encoding="utf-8").splitlines() if s.strip() and not s.startswith("#")), "")
        toks = line0.split()
        if len(toks) >= 2:
            grid_nx, grid_ny = int(toks[0]), int(toks[1])

    samples = build_design_matrix(args, channel_num, grid_nx, grid_ny)

    design_csv = dataset_dir / "sample_design.csv"
    with design_csv.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["design_id", "active_count"] + [f"amplitude_{i}" for i in range(1, channel_num + 1)])
        for design_id, vals in samples:
            wr.writerow([design_id, sum(1 for v in vals if abs(v) > 1.0e-12)] + [f"{float(v):.15f}" for v in vals])

    meta_path = dataset_dir / "dataset_meta.json"
    meta_path.write_text(json.dumps({
        "run_name": run_name,
        "strategy": args.strategy,
        "n_samples_planned": len(samples),
        "channel_num": channel_num,
        "grid_nx": grid_nx,
        "grid_ny": grid_ny,
        "bounds_min": args.bounds_min,
        "bounds_max": args.bounds_max,
        "seed": args.seed,
        "timeout_s": args.timeout_s,
        "template_dir": str(template_dir),
        "solver_script": str(solver_script),
        "started_at": now_stamp(),
    }, indent=2), encoding="utf-8")

    index_csv = dataset_dir / "dataset_index.csv"
    if not index_csv.exists():
        with index_csv.open("w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(
                ["sample_id", "design_id", "case_folder", "channel_num", "grid_nx", "grid_ny"]
                + [f"amplitude_{i}" for i in range(1, channel_num + 1)]
                + ["max_abs_uz", "status", "odb_exists", "csv_exists", "return_code", "elapsed_seconds", "error_msg"]
            )

    completed = load_completed_ids(index_csv) if args.reuse_existing else set()

    print(f"[INFO] dataset_dir = {dataset_dir}")
    print(f"[INFO] template    = {template_dir}")
    print(f"[INFO] solver      = {solver_script}")
    print(f"[INFO] samples     = {len(samples)}  (already completed: {len(completed)})")

    n_done = 0
    n_fail = 0
    for i, (design_id, amps) in enumerate(samples, start=1):
        sample_id = f"{i:05d}"
        if sample_id in completed:
            continue
        case_dir = dataset_dir / f"sample_{sample_id}"
        ensure_dir(case_dir)

        copy_template_inputs(template_dir, case_dir)
        write_force_amplitude(case_dir / "ForceAmplitude.dat", amps)

        rc, elapsed, err_msg = (0, 0.0, "")
        if not args.dry_run:
            rc, elapsed, err_msg = run_one_case(case_dir, solver_script, args.timeout_s)

        odb_exists = any(case_dir.glob("*.odb"))
        csv_exists = (case_dir / "node_displacement.csv").exists()
        max_abs_uz = compute_max_abs_uz_last_frame(case_dir / "node_displacement.csv")
        status = "dry_run" if args.dry_run else ("completed" if (rc == 0 and odb_exists and csv_exists) else "failed")

        with index_csv.open("a", encoding="utf-8", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(
                [sample_id, design_id, case_dir.name, channel_num, grid_nx, grid_ny]
                + [f"{float(v):.15f}" for v in amps]
                + [
                    f"{max_abs_uz:.15f}" if max_abs_uz == max_abs_uz else "",
                    status,
                    int(odb_exists),
                    int(csv_exists),
                    rc,
                    f"{elapsed:.3f}",
                    err_msg,
                ]
            )

        if status == "completed":
            n_done += 1
        elif status == "failed":
            n_fail += 1
        print(f"[{i:05d}/{len(samples):05d}] {case_dir.name} status={status} rc={rc} elapsed={elapsed:.1f}s err={err_msg}")

    print(f"[DONE] completed={n_done}  failed={n_fail}  index={index_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
