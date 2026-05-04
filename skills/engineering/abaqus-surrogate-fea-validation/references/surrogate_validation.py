#!/usr/bin/env python3
"""
Closed-loop surrogate <-> Abaqus FEA validation.

Loads aggregated training data + targets, fits a Ridge surrogate, solves the
inverse design problem on the surrogate, runs an Abaqus FEA verification, and
emits a side-by-side comparison of surrogate vs. true (FEA) deformation
metrics across all targets.

Usage:
    python surrogate_validation.py \\
        --data-dir ./aggregated/v1 \\
        --template-dir ./template_case \\
        --solver-script ./MyAbaqusSolver.py \\
        --work-root ./validation_runs \\
        --grid-n 21 \\
        --target-peak 2.5 \\
        --bounds-min -0.5 --bounds-max 0.5 \\
        --solver lbfgsb \\
        --targets target_dome.csv target_saddle.csv

Output:
    work_root/<target_tag>/
        target_scaled_NxN.csv      target rescaled to peak
        inverse_solution.csv       solved x_sol + scale + saturation
        predicted_surrogate_NxN.csv  surrogate-predicted deformation
        predicted_true_NxN.csv       FEA-true deformation
        ForceAmplitude.dat         per-case design vector
        Membrane2D1.odb            FEA result
        node_displacement.csv      raw FEA output
        summary.csv                per-target metrics
    work_root/surrogate_inverse_summary.csv   one-row-per-target master
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

from inverse_solvers import SOLVERS, clip_vec


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


# ── Surrogate fit / standardize ────────────────────────────────────────────


def read_matrix_csv(path: Path, prefix: str) -> np.ndarray:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        rows = list(rd)
    cols = [k for k in rows[0].keys() if k.startswith(prefix + "_")]
    cols.sort(key=lambda x: int(x.split("_")[1]))
    return np.asarray([[float(r[c]) for c in cols] for r in rows], dtype=np.float64)


def fit_standardizer(mat: np.ndarray, eps: float = 1e-8) -> Tuple[np.ndarray, np.ndarray]:
    mean = mat.mean(axis=0, keepdims=True)
    std = mat.std(axis=0, keepdims=True)
    std = np.where(std < eps, 1.0, std)
    return mean, std


def train_ridge(x_std: np.ndarray, y_std: np.ndarray, alpha: float) -> np.ndarray:
    """Closed-form Ridge: W = (X^T X + alpha I)^-1 X^T Y, returned as (D, M)."""
    d = x_std.shape[1]
    A = x_std.T @ x_std + alpha * np.eye(d, dtype=np.float64)
    return np.linalg.solve(A, x_std.T @ y_std)


# ── Target IO + reshape ────────────────────────────────────────────────────


def load_target_matrix(path: Path) -> np.ndarray:
    """
    Auto-detect: headered single-row uz CSV, or plain N x N matrix.
    """
    text = path.read_text(encoding="utf-8-sig")
    first = text.splitlines()[0]
    if "uz_" in first:
        # single-row wide table
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            rd = csv.DictReader(f)
            rows = list(rd)
        cols = [k for k in rows[0].keys() if k.startswith("uz_")]
        cols.sort(key=lambda x: int(x.split("_")[1]))
        flat = np.asarray([float(rows[0][c]) for c in cols], dtype=np.float64)
        n = int(round(flat.size ** 0.5))
        if n * n != flat.size:
            raise ValueError(f"non-square uz row in {path}: {flat.size} cells")
        return flat.reshape(n, n)

    rows: List[List[float]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p for p in line.replace(",", " ").split() if p]
        rows.append([float(p) for p in parts])
    return np.asarray(rows, dtype=np.float64)


def bilinear_resample(src: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
    src_h, src_w = src.shape
    if src_h == out_h and src_w == out_w:
        return src.astype(np.float64, copy=True)
    out = np.zeros((out_h, out_w), dtype=np.float64)
    for i in range(out_h):
        sy = i * (src_h - 1) / max(out_h - 1, 1)
        i0 = int(sy)
        i1 = min(i0 + 1, src_h - 1)
        fy = sy - i0
        for j in range(out_w):
            sx = j * (src_w - 1) / max(out_w - 1, 1)
            j0 = int(sx)
            j1 = min(j0 + 1, src_w - 1)
            fx = sx - j0
            v = (
                src[i0, j0] * (1 - fy) * (1 - fx)
                + src[i0, j1] * (1 - fy) * fx
                + src[i1, j0] * fy * (1 - fx)
                + src[i1, j1] * fy * fx
            )
            out[i, j] = v
    return out


def scale_target_to_peak(mat: np.ndarray, peak: float) -> Tuple[np.ndarray, float]:
    cur = float(np.max(np.abs(mat)))
    if cur <= 1.0e-12:
        return mat.copy(), 1.0
    scale = peak / cur
    return mat * scale, scale


# ── Metrics ────────────────────────────────────────────────────────────────


def mse_mae_max(pred: np.ndarray, target: np.ndarray, normalize: str = "target_max_abs") -> Dict[str, float]:
    err = pred - target
    mse = float(np.mean(err * err))
    mae = float(np.mean(np.abs(err)))
    max_abs = float(np.max(np.abs(err)))
    if normalize == "target_max_abs":
        denom = float(np.max(np.abs(target)))
    elif normalize == "target_range":
        denom = float(np.max(target) - np.min(target))
    else:
        denom = 1.0
    if denom <= 1e-12:
        denom = 1.0
    return {
        "mse": mse,
        "mae": mae,
        "max_abs_error": max_abs,
        "norm_mse": mse / (denom * denom),
        "norm_scale": denom,
    }


def count_saturated(x: np.ndarray, lo: float, hi: float, tol: float = 1.0e-6) -> int:
    return int(np.sum((x <= lo + tol) | (x >= hi - tol)))


# ── FEA verification ──────────────────────────────────────────────────────


def write_force_amplitude(path: Path, x: Sequence[float]) -> None:
    lines = []
    for i, v in enumerate(x, start=1):
        lines.append(f"*Amplitude, name=Amplitude{i:8d}")
        v = float(v)
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


def extract_final_frame_grid(node_csv: Path, n: int) -> Tuple[int, np.ndarray]:
    """
    Read node_displacement.csv, take the final frame, bin (x0, y0, uz) into
    a regular n x n grid via direct lookup if the FEA mesh is structured;
    otherwise inverse-distance interpolate.

    Returns (final_frame_id, flat_grid_n_squared).
    """
    data = np.genfromtxt(node_csv, delimiter=",", names=True, dtype=None, encoding="utf-8")
    if data.size == 0:
        raise RuntimeError("empty node_displacement.csv")

    frame_ids = np.asarray(data["frame_id"], dtype=np.int64)
    max_fid = int(frame_ids.max())
    mask = frame_ids == max_fid
    x0 = np.asarray(data["x0"][mask], dtype=np.float64)
    y0 = np.asarray(data["y0"][mask], dtype=np.float64)
    uz = np.asarray(data["uz"][mask], dtype=np.float64)

    x_lo, x_hi = float(x0.min()), float(x0.max())
    y_lo, y_hi = float(y0.min()), float(y0.max())
    xq = np.linspace(x_lo, x_hi, n)
    yq = np.linspace(y_hi, y_lo, n)  # row 0 = max y

    xr = np.round(x0, 2)
    yr = np.round(y0, 2)
    x_unique = np.sort(np.unique(xr))
    y_unique = np.sort(np.unique(yr))[::-1]

    if x_unique.size == y_unique.size and x_unique.size * y_unique.size == x0.size:
        mesh_n = x_unique.size
        x_to_col = {float(v): i for i, v in enumerate(x_unique)}
        y_to_row = {float(v): i for i, v in enumerate(y_unique)}
        src = np.full((mesh_n, mesh_n), np.nan, dtype=np.float64)
        for xv, yv, vv in zip(xr, yr, uz):
            src[y_to_row[float(yv)], x_to_col[float(xv)]] = vv
        if not np.isfinite(src).all():
            raise RuntimeError("structured binning left NaN cells")
        if mesh_n == n:
            return max_fid, src.flatten()
        # bilinear resample mesh_n -> n
        return max_fid, bilinear_resample(src, n, n).flatten()

    # IDW fallback
    out = np.empty(n * n, dtype=np.float64)
    idx = 0
    for y in yq:
        for x in xq:
            d2 = (x0 - x) ** 2 + (y0 - y) ** 2
            w = 1.0 / np.maximum(d2, 1e-12)
            out[idx] = float(np.sum(w * uz) / np.sum(w))
            idx += 1
    return max_fid, out


# ── Main ──────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Surrogate <-> Abaqus FEA validation loop")
    p.add_argument("--data-dir", type=str, required=True, help="Aggregated training data dir (X_amplitude.csv + Y_grid_uz.csv)")
    p.add_argument("--template-dir", type=str, required=True)
    p.add_argument("--solver-script", type=str, required=True)
    p.add_argument("--work-root", type=str, default="validation_runs")
    p.add_argument("--targets", nargs="+", required=True, help="Target N x N CSV files")
    p.add_argument("--grid-n", type=int, default=21)
    p.add_argument("--target-peak", type=float, default=2.5)
    p.add_argument("--bounds-min", type=float, default=-0.5)
    p.add_argument("--bounds-max", type=float, default=0.5)
    p.add_argument("--ridge-alpha", type=float, default=1.0)
    p.add_argument("--inv-reg", type=float, default=1.0e-4)
    p.add_argument("--solver", type=str, default="lbfgsb", choices=list(SOLVERS.keys()))
    p.add_argument("--pgd-steps", type=int, default=1200)
    p.add_argument("--pgd-lr", type=float, default=0.05)
    p.add_argument("--n-starts", type=int, default=10)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--timeout-s", type=float, default=3600.0)
    return p.parse_args()


def write_matrix(path: Path, mat: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        for row in mat:
            wr.writerow([f"{float(v):.15f}" for v in row])


def main() -> int:
    args = parse_args()
    data_dir = Path(args.data_dir).resolve()
    template_dir = Path(args.template_dir).resolve()
    solver_script = Path(args.solver_script).resolve()
    work_root = Path(args.work_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    np.random.seed(args.seed)

    # Fit surrogate once
    X = read_matrix_csv(data_dir / "X_amplitude.csv", "amplitude")
    Y = read_matrix_csv(data_dir / "Y_grid_uz.csv", "uz")
    x_mean, x_std = fit_standardizer(X)
    y_mean, y_std = fit_standardizer(Y)
    X_std = (X - x_mean) / x_std
    Y_std = (Y - y_mean) / y_std
    W = train_ridge(X_std, Y_std, args.ridge_alpha)

    D = X.shape[1]
    M = Y.shape[1]
    n = int(round(M ** 0.5))
    if n * n != M:
        raise SystemExit(f"Y_grid_uz.csv has {M} columns, not a perfect square")
    if n != args.grid_n:
        print(f"[WARN] training data uses grid {n}, --grid-n={args.grid_n}; resampling targets to {n}")

    x_lo = np.full((D,), float(args.bounds_min), dtype=np.float64)
    x_hi = np.full((D,), float(args.bounds_max), dtype=np.float64)
    z_lo = ((x_lo - x_mean.flatten()) / x_std.flatten())
    z_hi = ((x_hi - x_mean.flatten()) / x_std.flatten())

    solver_fn = SOLVERS[args.solver]

    summary_rows: List[List[object]] = []

    for target_path_str in args.targets:
        target_path = Path(target_path_str).resolve()
        case_tag = target_path.stem.replace("target_", "")
        case_dir = work_root / case_tag
        if case_dir.exists():
            shutil.rmtree(case_dir)
        case_dir.mkdir(parents=True)

        # Target -> learning grid
        target_mat_raw = load_target_matrix(target_path)
        target_mat = bilinear_resample(target_mat_raw, n, n)
        scaled_mat, scale_factor = scale_target_to_peak(target_mat, args.target_peak)
        target_flat = scaled_mat.flatten()
        y_target_std = (target_flat - y_mean.flatten()) / y_std.flatten()

        # Solve inverse
        if args.solver == "pgd":
            z_sol = solver_fn(W, y_target_std, z_lo, z_hi, args.inv_reg, args.pgd_steps, args.pgd_lr)
        elif args.solver == "multistart_lbfgsb":
            z_sol = solver_fn(W, y_target_std, z_lo, z_hi, args.inv_reg, args.n_starts, args.seed)
        else:
            z_sol = solver_fn(W, y_target_std, z_lo, z_hi, args.inv_reg)

        x_sol = z_sol * x_std.flatten() + x_mean.flatten()
        x_sol = np.clip(x_sol, args.bounds_min, args.bounds_max)
        sat = count_saturated(x_sol, args.bounds_min, args.bounds_max)

        # Surrogate-predicted deformation
        y_pred_std = z_sol @ W
        y_pred_flat = y_pred_std * y_std.flatten() + y_mean.flatten()
        surrogate_metrics = mse_mae_max(y_pred_flat, target_flat, "target_max_abs")

        # Persist intermediate artifacts
        write_matrix(case_dir / f"target_scaled_{n}x{n}.csv", scaled_mat)
        write_matrix(case_dir / f"predicted_surrogate_{n}x{n}.csv", y_pred_flat.reshape(n, n))

        with (case_dir / "inverse_solution.csv").open("w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f)
            wr.writerow([f"amplitude_{i+1}" for i in range(D)] + ["scale_factor", "saturated_channels"])
            wr.writerow([f"{float(v):.15f}" for v in x_sol] + [f"{scale_factor:.15f}", sat])

        # FEA verification
        copy_template_inputs(template_dir, case_dir)
        write_force_amplitude(case_dir / "ForceAmplitude.dat", x_sol.tolist())
        rc, elapsed, err_msg = run_one_case(case_dir, solver_script, args.timeout_s)

        true_metrics = {"mse": float("nan"), "mae": float("nan"), "max_abs_error": float("nan"), "norm_mse": float("nan"), "norm_scale": float("nan")}
        ff = -1
        if rc == 0 and (case_dir / "node_displacement.csv").exists():
            try:
                ff, y_true_flat = extract_final_frame_grid(case_dir / "node_displacement.csv", n)
                write_matrix(case_dir / f"predicted_true_{n}x{n}.csv", y_true_flat.reshape(n, n))
                true_metrics = mse_mae_max(y_true_flat, target_flat, "target_max_abs")
            except Exception as ex:  # noqa: BLE001
                err_msg = f"extract failed: {ex}"

        with (case_dir / "summary.csv").open("w", encoding="utf-8", newline="") as f:
            wr = csv.writer(f)
            wr.writerow(["key", "value"])
            wr.writerow(["target_file", str(target_path)])
            wr.writerow(["solver", args.solver])
            wr.writerow(["scale_factor", f"{scale_factor:.15f}"])
            wr.writerow(["target_peak", f"{args.target_peak:.15f}"])
            wr.writerow(["return_code", rc])
            wr.writerow(["elapsed_seconds", f"{elapsed:.6f}"])
            wr.writerow(["error_msg", err_msg])
            wr.writerow(["final_frame", ff])
            wr.writerow(["surrogate_mse", f"{surrogate_metrics['mse']:.15f}"])
            wr.writerow(["surrogate_mae", f"{surrogate_metrics['mae']:.15f}"])
            wr.writerow(["surrogate_norm_mse", f"{surrogate_metrics['norm_mse']:.15f}"])
            wr.writerow(["true_mse", "" if true_metrics["mse"] != true_metrics["mse"] else f"{true_metrics['mse']:.15f}"])
            wr.writerow(["true_mae", "" if true_metrics["mae"] != true_metrics["mae"] else f"{true_metrics['mae']:.15f}"])
            wr.writerow(["true_norm_mse", "" if true_metrics["norm_mse"] != true_metrics["norm_mse"] else f"{true_metrics['norm_mse']:.15f}"])
            wr.writerow(["saturated_channels", sat])
            wr.writerow(["seed", args.seed])

        summary_rows.append([
            case_tag,
            args.solver,
            f"{scale_factor:.6f}",
            f"{surrogate_metrics['mse']:.6e}",
            f"{surrogate_metrics['mae']:.6e}",
            f"{surrogate_metrics['norm_mse']:.6e}",
            "" if true_metrics["mse"] != true_metrics["mse"] else f"{true_metrics['mse']:.6e}",
            "" if true_metrics["mae"] != true_metrics["mae"] else f"{true_metrics['mae']:.6e}",
            "" if true_metrics["norm_mse"] != true_metrics["norm_mse"] else f"{true_metrics['norm_mse']:.6e}",
            sat,
            rc,
            f"{elapsed:.3f}",
        ])

        true_str = "nan" if true_metrics["mse"] != true_metrics["mse"] else f"{true_metrics['mse']:.4e}"
        print(
            f"[DONE] {case_tag}  rc={rc}  scale={scale_factor:.3f}  "
            f"surrogate_mse={surrogate_metrics['mse']:.4e}  true_mse={true_str}  sat={sat}/{D}"
        )

    summary_path = work_root / "surrogate_inverse_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([
            "target_name", "solver", "scale_factor",
            "surrogate_mse", "surrogate_mae", "surrogate_norm_mse",
            "true_mse", "true_mae", "true_norm_mse",
            "saturated_channels", "return_code", "elapsed_seconds",
        ])
        wr.writerows(summary_rows)
    print(f"[INFO] summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
