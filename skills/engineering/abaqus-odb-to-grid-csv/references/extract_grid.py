#!/usr/bin/env python3
"""
Aggregate per-case Abaqus FEA outputs into ML-ready (X, Y) wide-table CSVs.

Pattern:
    for each completed sample:
        read input vector       -> row of X
        read final-frame uz     -> regular N x N grid -> flatten -> row of Y

Usage:
    python extract_grid.py \\
        --dataset-root ./datasets/lhs_20260427_120000 \\
        --output-dir ./aggregated/v1 \\
        --target-grid-n 21 \\
        --frame final \\
        --dedupe-by-input
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from grid_resample import (
    bin_into_grid,
    detect_structured_mesh,
    structured_resample,
    unstructured_resample,
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Abaqus FEA outputs -> ML-ready (X, Y) CSVs")
    p.add_argument("--dataset-root", type=str, required=True, help="Folder produced by abaqus-lhs-batch-dataset (contains dataset_index.csv + sample_*/)")
    p.add_argument("--output-dir", type=str, required=True)
    p.add_argument("--target-grid-n", type=int, default=21, help="Target learning grid edge length (e.g. 21 -> 21x21 = 441 cells)")
    p.add_argument("--frame", type=str, default="final", choices=["final", "all"])
    p.add_argument("--dedupe-by-input", action="store_true")
    p.add_argument("--coord-decimals", type=int, default=2, help="Round x0/y0 to this many decimals before binning")
    p.add_argument("--require-completed", action="store_true", help="Only process cases marked status=completed in dataset_index.csv")
    return p.parse_args()


def read_input_vector(case_dir: Path) -> Optional[np.ndarray]:
    iv_path = case_dir / "input_vector.csv"
    if iv_path.exists():
        try:
            with iv_path.open("r", encoding="utf-8-sig", newline="") as f:
                rows = list(csv.DictReader(f))
            rows.sort(key=lambda r: int(float(r["channel_id"])))
            return np.array([float(r["amplitude_value"]) for r in rows], dtype=np.float64)
        except (KeyError, ValueError):
            pass

    fa_path = case_dir / "ForceAmplitude.dat"
    if fa_path.exists():
        vals: List[float] = []
        cur_block: List[str] = []
        for line in fa_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if not s:
                continue
            if s.lower().startswith("*amplitude"):
                if cur_block:
                    parts = cur_block[0].split(",")
                    if len(parts) >= 2:
                        vals.append(float(parts[1]))
                    cur_block = []
                continue
            if s.startswith("*"):
                if cur_block:
                    parts = cur_block[0].split(",")
                    if len(parts) >= 2:
                        vals.append(float(parts[1]))
                    cur_block = []
                continue
            cur_block.append(s)
        if cur_block:
            parts = cur_block[0].split(",")
            if len(parts) >= 2:
                vals.append(float(parts[1]))
        return np.array(vals, dtype=np.float64) if vals else None
    return None


def read_final_frame_uz(node_csv: Path) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray], int]:
    """
    Read node_displacement.csv, return (x0, y0, uz, frame_id) for the final frame.
    Returns (None, None, None, -1) on failure.
    """
    try:
        data = np.genfromtxt(node_csv, delimiter=",", names=True, dtype=None, encoding="utf-8")
    except Exception:  # noqa: BLE001
        return None, None, None, -1

    if data.size == 0:
        return None, None, None, -1
    if "frame_id" not in data.dtype.names or "uz" not in data.dtype.names:
        return None, None, None, -1

    frame_ids = np.asarray(data["frame_id"], dtype=np.int64)
    max_fid = int(frame_ids.max())
    mask = frame_ids == max_fid
    return (
        np.asarray(data["x0"][mask], dtype=np.float64),
        np.asarray(data["y0"][mask], dtype=np.float64),
        np.asarray(data["uz"][mask], dtype=np.float64),
        max_fid,
    )


def load_index(dataset_root: Path) -> List[Dict[str, str]]:
    idx = dataset_root / "dataset_index.csv"
    if not idx.exists():
        raise FileNotFoundError(f"dataset_index.csv not found in {dataset_root}")
    with idx.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> int:
    args = parse_args()
    dataset_root = Path(args.dataset_root).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    target_n = args.target_grid_n

    rows = load_index(dataset_root)
    if args.require_completed:
        rows = [r for r in rows if str(r.get("status", "")).strip() == "completed"]

    print(f"[INFO] cases to process: {len(rows)}")

    X_rows: List[Tuple[str, np.ndarray]] = []
    Y_rows: List[np.ndarray] = []
    meta_rows: List[Dict[str, object]] = []

    mesh_n_detected: Optional[int] = None
    is_structured: Optional[bool] = None

    for row in rows:
        sample_id = str(row.get("sample_id", "")).strip()
        case_folder = str(row.get("case_folder", "")).strip()
        case_dir = dataset_root / case_folder
        if not case_dir.is_dir():
            print(f"[WARN] {sample_id}: case dir missing", file=sys.stderr)
            continue

        x_in = read_input_vector(case_dir)
        if x_in is None:
            print(f"[WARN] {sample_id}: input vector unreadable", file=sys.stderr)
            continue

        x0, y0, uz, frame_id = read_final_frame_uz(case_dir / "node_displacement.csv")
        if uz is None or uz.size == 0:
            print(f"[WARN] {sample_id}: node_displacement.csv unreadable / empty", file=sys.stderr)
            continue

        if mesh_n_detected is None:
            is_structured, mesh_n_detected = detect_structured_mesh(x0, y0, decimals=args.coord_decimals)
            print(f"[INFO] mesh detected: {'structured' if is_structured else 'unstructured'} mesh_n={mesh_n_detected}")

        if is_structured:
            grid_src = bin_into_grid(x0, y0, uz, mesh_n_detected, decimals=args.coord_decimals)
            grid = grid_src if mesh_n_detected == target_n else structured_resample(grid_src, target_n)
        else:
            grid = unstructured_resample(x0, y0, uz, target_n)

        if not np.isfinite(grid).all():
            print(f"[WARN] {sample_id}: non-finite values in resampled grid", file=sys.stderr)
            continue

        X_rows.append((sample_id, x_in))
        Y_rows.append(grid.flatten())
        meta_rows.append({
            "sample_id": sample_id,
            "source_case": case_folder,
            "mesh_n": mesh_n_detected,
            "frame_id": frame_id,
            "max_abs_uz": float(np.max(np.abs(grid))),
        })

    if not X_rows:
        print("[ERROR] no usable cases extracted", file=sys.stderr)
        return 1

    n = len(X_rows)
    D = max(x.size for _, x in X_rows)
    M = target_n * target_n

    X_mat = np.zeros((n, D), dtype=np.float64)
    Y_mat = np.zeros((n, M), dtype=np.float64)
    for i, (_, x) in enumerate(X_rows):
        X_mat[i, : x.size] = x
    for i, y in enumerate(Y_rows):
        Y_mat[i, :] = y

    if args.dedupe_by_input:
        keys = ["|".join(f"{v:.10f}" for v in row) for row in X_mat]
        seen: Dict[str, int] = {}
        keep_idx: List[int] = []
        for i, key in enumerate(keys):
            if key in seen:
                continue
            seen[key] = i
            keep_idx.append(i)
        if len(keep_idx) != n:
            print(f"[INFO] deduped {n} -> {len(keep_idx)} unique inputs")
        X_mat = X_mat[keep_idx]
        Y_mat = Y_mat[keep_idx]
        X_rows = [X_rows[i] for i in keep_idx]
        meta_rows = [meta_rows[i] for i in keep_idx]
        n = len(keep_idx)

    sample_ids = [sid for sid, _ in X_rows]

    x_path = output_dir / "X_amplitude.csv"
    with x_path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["sample_id"] + [f"amplitude_{i:04d}" for i in range(D)])
        for sid, vec in zip(sample_ids, X_mat):
            wr.writerow([sid] + [f"{float(v):.15f}" for v in vec])

    y_path = output_dir / "Y_grid_uz.csv"
    with y_path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["sample_id"] + [f"uz_{i:04d}" for i in range(M)])
        for sid, vec in zip(sample_ids, Y_mat):
            wr.writerow([sid] + [f"{float(v):.15f}" for v in vec])

    meta_path = output_dir / "sample_meta.csv"
    with meta_path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["sample_id", "source_case", "mesh_n", "frame_id", "max_abs_uz"])
        wr.writeheader()
        for r in meta_rows:
            wr.writerow(r)

    summary_path = output_dir / "aggregate_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["key", "value"])
        wr.writerow(["n_total_in_index", len(rows)])
        wr.writerow(["n_extracted", n])
        wr.writerow(["mesh_n", mesh_n_detected])
        wr.writerow(["target_n", target_n])
        wr.writerow(["mesh_kind", "structured" if is_structured else "unstructured"])
        wr.writerow(["dedupe_by_input", int(bool(args.dedupe_by_input))])
        wr.writerow(["input_dim", D])
        wr.writerow(["output_dim", M])

    print(f"[DONE] X={x_path} ({n} x {D})")
    print(f"[DONE] Y={y_path} ({n} x {M})")
    print(f"[DONE] meta={meta_path}")
    print(f"[DONE] summary={summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
