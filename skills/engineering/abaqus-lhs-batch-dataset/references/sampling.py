"""
Pure-stdlib samplers for Abaqus FEA design-vector generation.

No scipy dependency — all samplers use only random + math.

Usage:
    from sampling import sample_lhs, sample_random_k_sparse, build_single_active

    rng = random.Random(42)
    samples = sample_lhs(num_samples=1000, dim=16, amp_min=-0.5, amp_max=0.5, rng=rng)
"""

from __future__ import annotations

import random
from typing import List, Sequence, Set, Tuple


def sample_lhs(
    num_samples: int,
    dim: int,
    amp_min: float,
    amp_max: float,
    rng: random.Random,
) -> List[List[float]]:
    """
    Latin hypercube sample in [amp_min, amp_max]^dim.

    For each dim independently:
        - partition [amp_min, amp_max] into num_samples equal bins
        - put one stratified sample in each bin (uniform within the bin)
        - permute the bin->sample assignment

    The result has the LHS property: when projected onto any single dimension,
    each of the num_samples bins contains exactly one point.
    """
    if num_samples <= 0:
        return []
    span = amp_max - amp_min
    bin_width = span / num_samples

    cols: List[List[float]] = []
    for _ in range(dim):
        perm = list(range(num_samples))
        rng.shuffle(perm)
        col_vals: List[float] = []
        for k in perm:
            col_vals.append(amp_min + (k + rng.random()) * bin_width)
        cols.append(col_vals)

    out: List[List[float]] = []
    for i in range(num_samples):
        out.append([cols[d][i] for d in range(dim)])
    return out


def sample_uniform_random(
    num_samples: int,
    dim: int,
    amp_min: float,
    amp_max: float,
    rng: random.Random,
) -> List[List[float]]:
    return [[rng.uniform(amp_min, amp_max) for _ in range(dim)] for _ in range(num_samples)]


def make_sparse_vector(dim: int, active_ids_1based: Sequence[int], amp: float) -> List[float]:
    out = [0.0] * dim
    for pid in active_ids_1based:
        out[pid - 1] = float(amp)
    return out


def vector_key(vals: Sequence[float], precision: int = 12) -> str:
    fmt = f"{{:.{precision}f}}"
    return ",".join(fmt.format(float(v)) for v in vals)


def sample_random_k_sparse(
    rng: random.Random,
    dim: int,
    k: int,
    count: int,
    amp_levels: Sequence[float],
    sign_mode: str = "both",
) -> List[List[float]]:
    """
    Sample `count` distinct k-sparse vectors of dimension `dim`.

    Each non-zero entry takes a value from `amp_levels` (possibly negated when
    sign_mode == "both"). De-duplication uses string keys at 12-digit precision.
    """
    out: List[List[float]] = []
    seen: Set[str] = set()
    signs = [1.0] if sign_mode == "positive_only" else [1.0, -1.0]
    max_tries = max(1000, count * 20)
    tries = 0
    while len(out) < count and tries < max_tries:
        tries += 1
        ids = sorted(rng.sample(range(1, dim + 1), k))
        vals = [0.0] * dim
        for pid in ids:
            sgn = rng.choice(signs)
            amp = rng.choice(amp_levels)
            vals[pid - 1] = sgn * amp
        key = vector_key(vals)
        if key in seen:
            continue
        seen.add(key)
        out.append(vals)
    return out


def build_single_active(
    dim: int,
    amp_levels: Sequence[float],
    sign_mode: str = "both",
) -> List[Tuple[str, List[float]]]:
    """
    Channel-by-channel impulse response basis. Useful as a "linearization probe".

    Returns (tag, vector) pairs.
    """
    signs = [1.0] if sign_mode == "positive_only" else [1.0, -1.0]
    out: List[Tuple[str, List[float]]] = []
    for pid in range(1, dim + 1):
        for amp in amp_levels:
            for sgn in signs:
                tag = f"single_p{pid}_a{amp:g}_s{int(sgn)}"
                out.append((tag, make_sparse_vector(dim, [pid], sgn * amp)))
    return out


def build_adjacent_pairs_grid(nx: int, ny: int) -> List[Tuple[int, int]]:
    """
    Enumerate (a, b) 1-based id pairs that are horizontally or vertically
    adjacent on an nx-by-ny grid (row-major).
    """
    pairs: List[Tuple[int, int]] = []
    for r in range(ny):
        for c in range(nx):
            a = r * nx + c + 1
            if c + 1 < nx:
                pairs.append((a, r * nx + (c + 1) + 1))
            if r + 1 < ny:
                pairs.append((a, (r + 1) * nx + c + 1))
    return pairs


def build_2x2_blocks_grid(nx: int, ny: int) -> List[Tuple[int, int, int, int]]:
    """
    Enumerate all 2x2 blocks of 1-based ids on an nx-by-ny grid (row-major).
    """
    blocks: List[Tuple[int, int, int, int]] = []
    for r in range(ny - 1):
        for c in range(nx - 1):
            p1 = r * nx + c + 1
            p2 = r * nx + (c + 1) + 1
            p3 = (r + 1) * nx + c + 1
            p4 = (r + 1) * nx + (c + 1) + 1
            blocks.append((p1, p2, p3, p4))
    return blocks
