"""
Grid resampling utilities for Abaqus mesh -> regular learning grid.

Two paths:
- structured_resample: fast vectorized bilinear when the FEA mesh is itself
  a regular MxM grid (typical for membrane / plate problems)
- unstructured_resample: scipy-based scattered interpolation (fallback)
"""

from __future__ import annotations

from typing import Tuple

import numpy as np


def precompute_bilinear_weights(src_n: int, dst_n: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Per-output-cell (i_low, i_high, fraction) interpolation weights for resampling
    a 1D index from length src_n to length dst_n.

    Output cell i covers source position s = i * (src_n - 1) / (dst_n - 1).
    """
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


def structured_resample(grid_src: np.ndarray, dst_n: int) -> np.ndarray:
    """
    Vectorized 2D bilinear resample from (src_n, src_n) -> (dst_n, dst_n).

    Pre-computes weights internally. For batch use, call precompute_bilinear_weights
    once and inline the operations to amortize the setup cost.
    """
    src_n = grid_src.shape[0]
    if grid_src.shape[1] != src_n:
        raise ValueError(f"expected square source grid, got {grid_src.shape}")
    if src_n == dst_n:
        return grid_src.astype(np.float64, copy=False)

    y_idx0, y_idx1, y_frac = precompute_bilinear_weights(src_n, dst_n)
    x_idx0, x_idx1, x_frac = precompute_bilinear_weights(src_n, dst_n)

    r0 = grid_src[y_idx0, :]
    r1 = grid_src[y_idx1, :]
    fy = y_frac[:, None]
    row_interp = r0 * (1.0 - fy) + r1 * fy

    c0 = row_interp[:, x_idx0]
    c1 = row_interp[:, x_idx1]
    fx = x_frac[None, :]
    return c0 * (1.0 - fx) + c1 * fx


def detect_structured_mesh(x0: np.ndarray, y0: np.ndarray, decimals: int = 2) -> Tuple[bool, int]:
    """
    Decide whether a node cloud (x0, y0) is a regular square grid.

    Returns (is_structured, mesh_n). Rounds coordinates by `decimals` to absorb
    floating-point noise.
    """
    xr = np.round(x0, decimals)
    yr = np.round(y0, decimals)
    n_unique_x = np.unique(xr).size
    n_unique_y = np.unique(yr).size
    if n_unique_x != n_unique_y:
        return False, 0
    n = n_unique_x
    return n * n == x0.size, n


def bin_into_grid(x0: np.ndarray, y0: np.ndarray, vals: np.ndarray, mesh_n: int, decimals: int = 2) -> np.ndarray:
    """
    Place each node value into a regular (mesh_n, mesh_n) grid by sorted unique
    coordinate. Assumes detect_structured_mesh returned (True, mesh_n).

    Output convention: out[row=y_index_from_top, col=x_index_from_left].
    """
    xr = np.round(x0, decimals)
    yr = np.round(y0, decimals)
    x_unique = np.sort(np.unique(xr))
    y_unique = np.sort(np.unique(yr))[::-1]  # top -> bottom (row 0 = max y)
    if x_unique.size != mesh_n or y_unique.size != mesh_n:
        raise ValueError(f"unique-coord count mismatch: x={x_unique.size}, y={y_unique.size}, expected {mesh_n}")
    x_to_col = {float(v): i for i, v in enumerate(x_unique)}
    y_to_row = {float(v): i for i, v in enumerate(y_unique)}

    out = np.full((mesh_n, mesh_n), np.nan, dtype=np.float64)
    for xv, yv, vv in zip(xr, yr, vals):
        out[y_to_row[float(yv)], x_to_col[float(xv)]] = vv
    if not np.isfinite(out).all():
        raise ValueError("structured binning left holes — node coords likely not exactly aligned")
    return out


def unstructured_resample(x0: np.ndarray, y0: np.ndarray, vals: np.ndarray, dst_n: int) -> np.ndarray:
    """
    Scattered interpolation onto a regular (dst_n, dst_n) grid via scipy.griddata.

    Output convention: out[row=y_index_from_top, col=x_index_from_left].
    """
    try:
        from scipy.interpolate import griddata
    except ImportError as err:  # noqa: BLE001
        raise RuntimeError("unstructured_resample requires scipy. install via `pip install scipy`.") from err

    x_lo, x_hi = float(x0.min()), float(x0.max())
    y_lo, y_hi = float(y0.min()), float(y0.max())

    xq = np.linspace(x_lo, x_hi, dst_n)
    yq = np.linspace(y_hi, y_lo, dst_n)  # top -> bottom
    Xq, Yq = np.meshgrid(xq, yq)

    grid = griddata((x0, y0), vals, (Xq, Yq), method="linear", fill_value=0.0)
    return np.asarray(grid, dtype=np.float64)
