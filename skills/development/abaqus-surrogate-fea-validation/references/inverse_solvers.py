"""
Inverse-problem solvers for Ridge-style linear surrogates.

Surrogate model:  y_std = z @ W
  W is the Ridge weight matrix of shape (D, M), where D = design dim
  and M = output dim (e.g. flattened N x N grid).

Inverse problem (per target, in standardized space):
    argmin_z  || z @ W - y_target_std ||² / M  +  lambda * ||z||² / D
    subject to z_lo <= z <= z_hi

This is convex quadratic, so 4 solvers are useful:
  - solve_inverse_pgd: pure stdlib + numpy, deterministic
  - solve_inverse_lbfgsb: scipy L-BFGS-B with analytical gradient
  - solve_inverse_multistart_lbfgsb: multi-start variant for tight bounds
  - solve_inverse_nelder_mead: derivative-free debug fallback
"""

from __future__ import annotations

from typing import Tuple

import numpy as np

try:
    from scipy.optimize import minimize as scipy_minimize
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def clip_vec(z: np.ndarray, z_lo: np.ndarray, z_hi: np.ndarray) -> np.ndarray:
    return np.minimum(np.maximum(z, z_lo), z_hi)


def closed_form_init(W: np.ndarray, y_target_std: np.ndarray, inv_reg: float) -> np.ndarray:
    """
    Ridge closed-form solution in standardized space:
        z = (W W^T + lambda I)^-1 W y_target_std
    """
    ww_t = W @ W.T
    rhs = W @ y_target_std
    return np.linalg.solve(ww_t + inv_reg * np.eye(W.shape[0], dtype=np.float64), rhs)


def solve_inverse_pgd(
    W: np.ndarray,
    y_target_std: np.ndarray,
    z_lo: np.ndarray,
    z_hi: np.ndarray,
    inv_reg: float = 1.0e-4,
    steps: int = 1200,
    lr: float = 0.05,
) -> np.ndarray:
    """
    Projected gradient descent. Fixed step count, deterministic.
    """
    z = closed_form_init(W, y_target_std, inv_reg)
    z = clip_vec(z, z_lo, z_hi)

    n_out = float(W.shape[1])
    n_in = float(W.shape[0])
    for _ in range(max(1, steps)):
        err = z @ W - y_target_std
        grad = (2.0 / n_out) * (err @ W.T) + (2.0 * inv_reg / n_in) * z
        z = clip_vec(z - lr * grad, z_lo, z_hi)
    return z


def solve_inverse_lbfgsb(
    W: np.ndarray,
    y_target_std: np.ndarray,
    z_lo: np.ndarray,
    z_hi: np.ndarray,
    inv_reg: float = 1.0e-4,
    max_iter: int = 200,
) -> np.ndarray:
    """
    L-BFGS-B with analytical gradient. Initialize from closed-form solution.
    For a linear surrogate this converges in O(D) iterations, much faster
    than PGD's 1200 fixed steps.
    """
    if not HAS_SCIPY:
        raise RuntimeError("scipy is required for L-BFGS-B solver")

    n_out = float(W.shape[1])
    n_in = float(W.shape[0])

    def objective_and_grad(z: np.ndarray) -> Tuple[float, np.ndarray]:
        err = z @ W - y_target_std
        obj = float(np.mean(err ** 2)) + inv_reg * float(np.mean(z ** 2))
        grad = (2.0 / n_out) * (err @ W.T) + (2.0 * inv_reg / n_in) * z
        return obj, grad

    z0 = clip_vec(closed_form_init(W, y_target_std, inv_reg), z_lo, z_hi)
    bounds = list(zip(z_lo.tolist(), z_hi.tolist()))
    res = scipy_minimize(
        objective_and_grad,
        z0,
        method="L-BFGS-B",
        jac=True,
        bounds=bounds,
        options={"maxiter": max_iter, "ftol": 1e-15, "gtol": 1e-12},
    )
    return res.x


def solve_inverse_multistart_lbfgsb(
    W: np.ndarray,
    y_target_std: np.ndarray,
    z_lo: np.ndarray,
    z_hi: np.ndarray,
    inv_reg: float = 1.0e-4,
    n_starts: int = 10,
    seed: int = 42,
    max_iter: int = 200,
) -> np.ndarray:
    """
    Run L-BFGS-B from n_starts initial points (closed-form, zero,
    plus random uniforms in the box) and keep the best.

    Useful when (a) the box constraint is tight and the boundary creates
    multiple local minima, or (b) D is large enough that single-start
    L-BFGS-B occasionally lands on a saddle.
    """
    if not HAS_SCIPY:
        raise RuntimeError("scipy is required for multi-start L-BFGS-B")

    n_out = float(W.shape[1])
    n_in = float(W.shape[0])
    dim = W.shape[0]

    def objective_and_grad(z: np.ndarray) -> Tuple[float, np.ndarray]:
        err = z @ W - y_target_std
        obj = float(np.mean(err ** 2)) + inv_reg * float(np.mean(z ** 2))
        grad = (2.0 / n_out) * (err @ W.T) + (2.0 * inv_reg / n_in) * z
        return obj, grad

    bounds = list(zip(z_lo.tolist(), z_hi.tolist()))

    rng = np.random.default_rng(seed)
    z_cf = clip_vec(closed_form_init(W, y_target_std, inv_reg), z_lo, z_hi)
    starts = [z_cf, np.zeros(dim)]
    for _ in range(max(0, n_starts - len(starts))):
        starts.append(rng.uniform(z_lo, z_hi))

    best_z = starts[0]
    best_obj = float("inf")
    for z0 in starts:
        res = scipy_minimize(
            objective_and_grad,
            z0,
            method="L-BFGS-B",
            jac=True,
            bounds=bounds,
            options={"maxiter": max_iter, "ftol": 1e-15, "gtol": 1e-12},
        )
        if res.fun < best_obj:
            best_obj = res.fun
            best_z = res.x
    return best_z


def solve_inverse_nelder_mead(
    W: np.ndarray,
    y_target_std: np.ndarray,
    z_lo: np.ndarray,
    z_hi: np.ndarray,
    inv_reg: float = 1.0e-4,
    max_evals: int = 5000,
) -> np.ndarray:
    """
    Derivative-free Nelder-Mead with soft penalty box constraint.
    Slowest of the four; only use to debug suspected bugs in the gradient
    path of the L-BFGS-B solvers.
    """
    if not HAS_SCIPY:
        raise RuntimeError("scipy is required for Nelder-Mead solver")

    def objective(z: np.ndarray) -> float:
        z_c = clip_vec(z, z_lo, z_hi)
        err = z_c @ W - y_target_std
        obj = float(np.mean(err ** 2)) + inv_reg * float(np.mean(z_c ** 2))
        penalty = 100.0 * float(np.sum((z - z_c) ** 2))
        return obj + penalty

    z0 = clip_vec(closed_form_init(W, y_target_std, inv_reg), z_lo, z_hi)
    res = scipy_minimize(
        objective,
        z0,
        method="Nelder-Mead",
        options={"maxfev": max_evals, "xatol": 1e-10, "fatol": 1e-12},
    )
    return clip_vec(res.x, z_lo, z_hi)


SOLVERS = {
    "pgd": solve_inverse_pgd,
    "lbfgsb": solve_inverse_lbfgsb,
    "multistart_lbfgsb": solve_inverse_multistart_lbfgsb,
    "nelder_mead": solve_inverse_nelder_mead,
}
