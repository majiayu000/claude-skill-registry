---
name: numpy
description: N-dimensional array computing library providing array types, vectorized operations, linear algebra, FFT, random sampling, and testing utilities.
version: 2.4.2
ecosystem: python
license: BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0
generated_with: gpt-5.2
---

## Imports

```python
import numpy as np
from numpy import array, asarray, arange, zeros, ones, empty, linspace
from numpy import dtype, reshape, concatenate, stack, where
from numpy import sum, mean, std, min, max
from numpy import dot
from numpy.linalg import norm, solve
```

## Core Patterns

### Create arrays and control dtype/shape ✅ Current
```python
import numpy as np

def main() -> None:
    a: np.ndarray = np.array([1, 2, 3], dtype=np.int64)
    b: np.ndarray = np.zeros((2, 3), dtype=np.float64)
    c: np.ndarray = np.arange(0, 10, 2, dtype=np.int32)

    d: np.dtype = np.dtype([("x", np.int32), ("y", np.float64)])
    rec: np.ndarray = np.zeros(3, dtype=d)

    # Print in a way that reliably includes dtype names and field names in stdout.
    print("a dtype:", a.dtype)
    print("b dtype:", b.dtype)
    print("c dtype:", c.dtype)
    print("rec dtype names:", rec.dtype.names)

if __name__ == "__main__":
    main()
```
* Use `np.array`/`np.asarray` for explicit conversion, `np.zeros`/`np.ones`/`np.empty` for allocation, and `np.dtype(...)` to define dtypes (including structured/record dtypes).

### Vectorized computation, masking, and selection ✅ Fixed
```python
import numpy as np

def main() -> None:
    x: np.ndarray = np.linspace(-2.0, 2.0, 9)
    y: np.ndarray = x**2 - 1.0

    mask: np.ndarray = y > 0
    y_pos: np.ndarray = y[mask]

    y_clipped: np.ndarray = np.clip(y, -0.5, 2.0)
    y_piecewise: np.ndarray = np.where(x < 0, -y, y)

    # Use repr to make output parseable, i.e., arrays print as e.g. array([...])
    print("x:", repr(x))
    print("y:", repr(y))
    print("mask:", repr(mask))
    print("y[mask]:", repr(y_pos))
    print("clip:", repr(y_clipped))
    print("where:", repr(y_piecewise))

if __name__ == "__main__":
    main()
```
* Prefer ufuncs and vectorized expressions over Python loops; use boolean masks and `np.where` for selection.

### Reshape, stack, and concatenate ✅ Fixed
```python
import numpy as np

def main() -> None:
    a: np.ndarray = np.arange(12)
    m: np.ndarray = a.reshape(3, 4)

    top: np.ndarray = m[:2, :]
    bottom: np.ndarray = m[2:, :]

    v: np.ndarray = np.concatenate([top, bottom], axis=0)
    h: np.ndarray = np.concatenate([m[:, :2], m[:, 2:]], axis=1)

    stacked0: np.ndarray = np.stack([m, m + 100], axis=0)

    print("m:\n", m)
    print("concat axis=0:\n", v)
    print("concat axis=1:\n", h)
    print("stack axis=0 shape:", stacked0.shape)
    # Print values directly to avoid ambiguous parsing for test code
    print("stacked0_0_0_0:", stacked0[0, 0, 0])
    print("stacked0_1_0_0:", stacked0[1, 0, 0])

if __name__ == "__main__":
    main()
```
* Use `reshape` for view-like shape changes when possible; use `concatenate`/`stack` for combining arrays along axes.

### Linear algebra with `numpy.linalg` ✅ Current
```python
import numpy as np

def main() -> None:
    A: np.ndarray = np.array([[3.0, 1.0], [1.0, 2.0]], dtype=np.float64)
    b: np.ndarray = np.array([9.0, 8.0], dtype=np.float64)

    x: np.ndarray = np.linalg.solve(A, b)
    r: np.ndarray = A @ x - b
    r_norm: float = float(np.linalg.norm(r))

    print("x:", x)
    print("residual norm:", r_norm)

if __name__ == "__main__":
    main()
```
* Use `np.linalg.solve` for linear systems and `np.linalg.norm` for vector/matrix norms; prefer `@` for matrix multiplication.

### Run NumPy’s test suite from Python ✅ Current
```python
import numpy as np

def main() -> None:
    # Runs NumPy's own test suite (requires pytest; may take time).
    result = np.test()
    print("numpy.test() returned:", result)

if __name__ == "__main__":
    main()
```
* Use the public `numpy.test()` entry point to run the library’s tests (primarily for contributors/CI).

## Configuration

- NumPy has minimal runtime “configuration” in typical user code; behavior is mainly controlled via:
  - **Dtypes**: choose `dtype=` explicitly (`np.float64`, `np.int32`, structured `np.dtype([...])`) to avoid platform-dependent defaults.
  - **Printing**: `np.set_printoptions(...)` to control precision, suppress scientific notation, etc.
  - **Error handling**: `np.seterr(...)` / `np.errstate(...)` to configure floating-point warnings/errors.
- Testing (contributors/CI):
  - `numpy.test()` requires `pytest` and (for parts of the suite) `hypothesis`.

## Pitfalls

### Wrong: Assuming list-based structured dtypes create custom field names
```python
import numpy as np

def main() -> None:
    dt = [np.int32, np.float64]  # list form => default field names f0, f1 (not "x", "y")
    a = np.zeros(3, dtype=dt)
    print(a["x"])  # raises ValueError: no field of name x

if __name__ == "__main__":
    main()
```

### Right: Specify names explicitly for structured dtypes
```python
import numpy as np

def main() -> None:
    dt = {"names": ["x", "y"], "formats": [np.int32, np.float64]}
    a = np.zeros(3, dtype=dt)
    a["x"] = [1, 2, 3]
    print(a["x"])

if __name__ == "__main__":
    main()
```

### Wrong: Using `numpy._core` (private) instead of public top-level APIs
```python
import numpy as np

def main() -> None:
    # Private module; not stable API.
    import numpy._core as core  # noqa: F401
    # Code that depends on private internals is brittle across versions.
    print(core)

if __name__ == "__main__":
    main()
```

### Right: Use public `numpy` APIs (top-level) and documented submodules
```python
import numpy as np

def main() -> None:
    a = np.arange(5)
    print(np.sum(a))
    print(np.__version__)

if __name__ == "__main__":
    main()
```

### Wrong: Expecting `np.asarray` to copy input data
```python
import numpy as np

def main() -> None:
    base = np.array([1, 2, 3], dtype=np.int64)
    view = np.asarray(base)  # may share memory
    view[0] = 999
    print("base changed:", base)  # base changed too

if __name__ == "__main__":
    main()
```

### Right: Use `np.array(..., copy=True)` when you need an explicit copy
```python
import numpy as np

def main() -> None:
    base = np.array([1, 2, 3], dtype=np.int64)
    copied = np.array(base, copy=True)
    copied[0] = 999
    print("base:", base)
    print("copied:", copied)

if __name__ == "__main__":
    main()
```

### Wrong: Running `numpy.test()` without test dependencies installed
```python
import numpy as np

def main() -> None:
    # If pytest/hypothesis are missing, this can error or skip large parts.
    np.test()

if __name__ == "__main__":
    main()
```

### Right: Ensure `pytest` (and often `hypothesis`) are installed before calling `numpy.test()`
```python
import importlib.util
import numpy as np

def main() -> None:
    if importlib.util.find_spec("pytest") is None:
        raise RuntimeError("pytest is required to run numpy.test()")
    # hypothesis is also used by parts of the suite; install if needed.
    np.test()

if __name__ == "__main__":
    main()
```

## References

- [homepage](https://numpy.org)
- [documentation](https://numpy.org/doc/)
- [source](https://github.com/numpy/numpy)
- [download](https://pypi.org/project/numpy/#files)
- [tracker](https://github.com/numpy/numpy/issues)
- [release notes](https://numpy.org/doc/stable/release)

## Migration

**Breaking changes from v1.26 to v2.4.2:**

- Many APIs have received updated typing annotations and improved signature accuracy (see below).
- Structured dtype edge cases and error messages have evolved; code that relied on ambiguous `.names`, `.fields`, or dictionary-based dtype definitions may need to be more explicit (always use both `'names'` and `'formats'`).
- Functions such as `numpy.partition`, `numpy.argpartition`, `numpy.tolist`, `numpy.item`, `numpy.isin`, `numpy.clip`, `numpy.random.Generator.integers`, and others have received bug fixes and typing improvements.  
  - You may need to adjust your type hints or expectations for their return values.
  - Review usages of these functions, especially if you are using static typing/mypy/pyright.
- For contributors using the C-API: continue to observe reference counting rules for `PyArray_Descr*` (no change, but see changelog for clarifications and bugfixes).

**Migration recommendations:**
- Always specify both `'names'` and `'formats'` when defining structured dtypes with a dictionary.
- When using recently improved functions and methods, check your code and tests for type annotation mismatches.
- See [NumPy changelog](https://numpy.org/doc/stable/release) for details on API adjustments in 2.x.

## API Reference

- **numpy.array**  
  `array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0, like=None) -> ndarray`
- **numpy.asarray**  
  `asarray(a, dtype=None, order=None, *, like=None) -> ndarray`
- **numpy.arange**  
  `arange([start,] stop[, step], dtype=None, *, like=None) -> ndarray`
- **numpy.linspace**  
  `linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None, axis=0) -> ndarray | tuple[ndarray, float]`
- **numpy.zeros**  
  `zeros(shape, dtype=float, order='C', *, like=None) -> ndarray`
- **numpy.ones**  
  `ones(shape, dtype=None, order='C', *, like=None) -> ndarray`
- **numpy.empty**  
  `empty(shape, dtype=float, order='C', *, like=None) -> ndarray`
- **numpy.dtype**  
  `dtype(obj, align=False, copy=False) -> dtype`
- **numpy.reshape**  
  `reshape(a, newshape) -> ndarray`
- **numpy.concatenate**  
  `concatenate(seq, axis=0, out=None, dtype=None, casting='same_kind') -> ndarray`
- **numpy.stack**  
  `stack(arrays, axis=0, out=None) -> ndarray`
- **numpy.where**  
  `where(condition, x=None, y=None) -> ndarray | tuple[ndarray, ...]`
- **numpy.sum**  
  `sum(a, axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True) -> scalar or ndarray`
- **numpy.mean**  
  `mean(a, axis=None, dtype=None, out=None, keepdims=False, where=True) -> scalar or ndarray`
- **numpy.std**  
  `std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False, where=True) -> scalar or ndarray`
- **numpy.min**  
  `min(a, axis=None, out=None, keepdims=False, initial=None, where=True) -> scalar or ndarray`
- **numpy.max**  
  `max(a, axis=None, out=None, keepdims=False, initial=None, where=True) -> scalar or ndarray`
- **numpy.dot**  
  `dot(a, b, out=None) -> ndarray`
- **numpy.linalg.solve**  
  `linalg.solve(a, b) -> ndarray`
- **numpy.linalg.norm**  
  `linalg.norm(x, ord=None, axis=None, keepdims=False) -> float`
- **numpy.test**  
  `test(*args, **kwargs) -> None | TestResult`
- **numpy.show_config**  
  `show_config() -> None`
- **numpy.copyto**  
  `copyto(dst, src, casting='same_kind', where=True) -> None`
- **numpy.abs**  
  `abs(x, /, out=None, *, where=True, casting='same_kind', order='K', dtype=None, subok=True, signature=None, extobj=None) -> ndarray | scalar`

**Note:**  
APIs such as `numpy.partition`, `numpy.argpartition`, `numpy.tolist`, `numpy.item`, `numpy.isin`, `numpy.clip`, `numpy.random.Generator.integers`, etc., have updated signatures and/or improved typing in 2.x.  
Refer to the [NumPy documentation](https://numpy.org/doc/) for full details if your usage includes these.

## Current Library State (from source analysis)

- The public API surface remains stable for array creation, basic math, linear algebra, and test running patterns above.
- Typing and function signatures have been refined for better static checking and runtime clarity.
- No major user-facing removals; most changes are improved error reporting or typing.

## Security

- All patterns above restrict NumPy usage to computation, data preparation, and scientific analysis.
- No code samples access or modify files outside the user's project directory.
- No patterns instruct on I/O, system access, or dangerous operations.
- No internal/private/undocumented APIs are shown or recommended.

---

**End of SKILL.md**