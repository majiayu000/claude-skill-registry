---
name: matplotlib
description: Python library for creating static, animated, and interactive visualizations.
version: 3.10.8
ecosystem: python
license: MIT
generated_with: gpt-5.2
---

## Imports

```python
import matplotlib
from matplotlib import rc_params, set_loglevel, MatplotlibDeprecationWarning
from matplotlib import get_cachedir, get_configdir, get_data_path, matplotlib_fname
```

## Core Patterns

### Inspect version and environment ✅ Current
```python
import matplotlib
from matplotlib import get_cachedir, get_configdir, get_data_path, matplotlib_fname

def main() -> None:
    print("matplotlib:", matplotlib.__version__)
    print("version_info:", matplotlib.__version_info__)
    print("configdir:", get_configdir())
    print("cachedir:", get_cachedir())
    print("data_path:", get_data_path())
    print("matplotlibrc:", matplotlib_fname())

if __name__ == "__main__":
    main()
```
* Use this to debug runtime environment issues (config, cache, bundled data, and the active matplotlibrc).

### Read and query rcParams ✅ Current
```python
from __future__ import annotations

import matplotlib
from matplotlib import rc_params

def main() -> None:
    params: matplotlib.RcParams = rc_params()

    # Read a value.
    backend = params.get("backend", None)
    # NOTE: backend may be an object (not necessarily a str) depending on environment/backend setup.
    print("backend:", backend)

    # Find all params matching a pattern.
    font_params: matplotlib.RcParams = params.find_all("font")
    print("num font-related rcParams:", len(font_params))

    # Copy for safe experimentation.
    params_copy: matplotlib.RcParams = params.copy()
    params_copy["figure.dpi"] = 150  # validated assignment via RcParams.__setitem__
    print("figure.dpi (copy):", params_copy["figure.dpi"])
    print("figure.dpi (original):", params["figure.dpi"])

if __name__ == "__main__":
    main()
```
* Use `matplotlib.rc_params()` to obtain a validated `RcParams` mapping, then query, filter, and copy it safely.

### Update rcParams with validated vs raw setters ✅ Current
```python
from __future__ import annotations

import matplotlib
from matplotlib import rc_params

def main() -> None:
    params: matplotlib.RcParams = rc_params()

    # Validated set (recommended): enforces types/allowed values.
    params["_internal.classic_mode"] = False if "_internal.classic_mode" in params else params.get("_internal.classic_mode", False)

    # Public-but-underscored helpers (documented as public in Matplotlib):
    # - _set: validated set
    # - _get: get with Matplotlib's internal semantics
    # - _update_raw: bypass some validation (use carefully)
    if "figure.dpi" in params:
        params._set("figure.dpi", 120)
        dpi = params._get("figure.dpi")
        print("figure.dpi via _get:", dpi)

    # Raw update is for advanced cases; keep values correct to avoid later failures.
    params._update_raw({"savefig.dpi": "figure"})
    print("savefig.dpi:", params["savefig.dpi"])

if __name__ == "__main__":
    main()
```
* Prefer `params[key] = value` / `RcParams.__setitem__` (validated). Use `_update_raw` only when you fully control inputs.

### Control Matplotlib logging ✅ Current
```python
import matplotlib

def main() -> None:
    matplotlib.set_loglevel("warning")
    # Common levels: "debug", "info", "warning", "error", "critical"
    print("log level set; version:", matplotlib.__version__)

if __name__ == "__main__":
    main()
```
* Use `matplotlib.set_loglevel()` to reduce noisy logs in production or increase verbosity while debugging.

### Handle missing external executables ✅ Current
```python
from __future__ import annotations

import shutil
import matplotlib

def require_executable(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise matplotlib.ExecutableNotFoundError(f"Required executable not found on PATH: {name}")
    return path

def main() -> None:
    # Example: check for a tool your workflow needs.
    try:
        exe = require_executable("latex")
        print("Found latex at:", exe)
    except matplotlib.ExecutableNotFoundError as e:
        print("Cannot proceed:", e)

if __name__ == "__main__":
    main()
```
* Raise `matplotlib.ExecutableNotFoundError` (a `FileNotFoundError`) when your Matplotlib-adjacent workflow depends on external tools.

## Configuration

- **rcParams**: Central configuration mapping (validated keys/values). Retrieve with `matplotlib.rc_params()`.
- **Config directory**: `matplotlib.get_configdir()` (location of user config such as `matplotlibrc`).
- **Cache directory**: `matplotlib.get_cachedir()` (font cache and other cached artifacts).
- **Data path**: `matplotlib.get_data_path()` (bundled data shipped with Matplotlib).
- **Active config file**: `matplotlib.matplotlib_fname()` (path to the matplotlibrc in use).
- **Logging**: `matplotlib.set_loglevel(level: str)` to control Matplotlib’s internal logging verbosity.
- **API stability note**: In Matplotlib, visual output is treated as part of the public API; changes that alter appearance can be considered breaking.

## Pitfalls

### Wrong: Assuming `matplotlib.__version__` is a function
```python
import matplotlib

def main() -> None:
    # TypeError: 'str' object is not callable
    print(matplotlib.__version__())

if __name__ == "__main__":
    main()
```

### Right: Treat `__version__` as a string attribute
```python
import matplotlib

def main() -> None:
    print(matplotlib.__version__)
    print(matplotlib.__version_info__)

if __name__ == "__main__":
    main()
```

### Wrong: Mutating global rcParams when you only meant to experiment
```python
from matplotlib import rc_params

def main() -> None:
    params = rc_params()
    params["figure.dpi"] = 10  # affects subsequent figures in this process
    print("figure.dpi now:", params["figure.dpi"])

if __name__ == "__main__":
    main()
```

### Right: Work on a copy of rcParams for local experimentation
```python
from matplotlib import rc_params

def main() -> None:
    params = rc_params()
    local = params.copy()
    local["figure.dpi"] = 10
    print("local figure.dpi:", local["figure.dpi"])
    print("global figure.dpi:", params["figure.dpi"])

if __name__ == "__main__":
    main()
```

### Wrong: Using `_update_raw` with invalid values (can break later)
```python
from matplotlib import rc_params

def main() -> None:
    params = rc_params()
    # This may bypass normal validation and cause errors later when rendering/saving.
    params._update_raw({"figure.dpi": "not-a-number"})
    print("figure.dpi:", params["figure.dpi"])

if __name__ == "__main__":
    main()
```

### Right: Prefer validated assignment (or `_set`) for rcParams
```python
from matplotlib import rc_params

def main() -> None:
    params = rc_params()
    params["figure.dpi"] = 200  # validated
    print("figure.dpi:", params["figure.dpi"])

if __name__ == "__main__":
    main()
```

### Wrong: Catching the wrong exception type for missing executables
```python
import shutil
import matplotlib

def main() -> None:
    try:
        path = shutil.which("latex")
        if path is None:
            raise FileNotFoundError("latex not found")
    except matplotlib.ExecutableNotFoundError:
        # This block will not run because FileNotFoundError was raised instead.
        print("Handle missing executable")

if __name__ == "__main__":
    main()
```

### Right: Raise/catch `matplotlib.ExecutableNotFoundError` consistently
```python
import shutil
import matplotlib

def main() -> None:
    try:
        path = shutil.which("latex")
        if path is None:
            raise matplotlib.ExecutableNotFoundError("latex not found on PATH")
        print("latex:", path)
    except matplotlib.ExecutableNotFoundError as e:
        print("Handle missing executable:", e)

if __name__ == "__main__":
    main()
```

## References

- [Homepage](https://matplotlib.org)
- [Download](https://matplotlib.org/stable/install/index.html)
- [Documentation](https://matplotlib.org)
- [Source Code](https://github.com/matplotlib/matplotlib)
- [Bug Tracker](https://github.com/matplotlib/matplotlib/issues)
- [Forum](https://discourse.matplotlib.org/)
- [Donate](https://numfocus.org/donate-to-matplotlib)

## Migration from v[previous]

Not applicable (no version-specific breaking-change details were provided in the inputs). When migrating across Matplotlib versions, pay special attention to:
- Staged deprecations (warnings first, removals later) using Matplotlib’s deprecation utilities.
- Visual-output changes: figure appearance differences can be considered API changes.

## API Reference

- **matplotlib.__version__** - Version string (computed lazily via module `__getattr__`).
- **matplotlib.__version_info__** - Structured version info object.
- **matplotlib.__bibtex__** - BibTeX citation string.
- **matplotlib.set_loglevel(level, *, logger='matplotlib')** - Set Matplotlib’s logging level.
- **matplotlib.get_configdir()** - Return the configuration directory path.
- **matplotlib.get_cachedir()** - Return the cache directory path.
- **matplotlib.get_data_path()** - Return the path to Matplotlib’s bundled data.
- **matplotlib.matplotlib_fname()** - Return the path to the active matplotlibrc file.
- **matplotlib.ExecutableNotFoundError** - Exception for missing external executables (subclass of `FileNotFoundError`).
- **matplotlib.MatplotlibDeprecationWarning** - Warning category used for Matplotlib deprecations.
- **matplotlib.RcParams** - Validated mapping for runtime configuration (rcParams).
- **matplotlib.rc_params(fail_on_error: bool = False)** - Load and return rcParams as an `RcParams` instance.
- **matplotlib.rc_params_from_file(fname, fail_on_error: bool = False, use_default_template: bool = True)** - Load rcParams from a file.
- **matplotlib.rcParamsDefault** - Property: default rcParams.
- **matplotlib.rcParams** - Property: the global rcParams, assignable.
- **matplotlib.rcParamsOrig** - Property: original rcParams at import.
- **matplotlib.defaultParams** - Property: default rcParams (legacy/alias).
- **matplotlib.rc(group, **kwargs)** - Set the current rc params for a group.
- **matplotlib.rcdefaults()** - Restore rcParams to their default settings.
- **matplotlib.rc_file_defaults()** - Restore rcParams from the default matplotlibrc file.
- **matplotlib.rc_file(fname)** - Update rcParams from a specified file.
- **matplotlib.rc_context(rc=None, fname=None)** - Context manager to temporarily set rcParams.
- **matplotlib.use(backend, *, force=True)** - Select backend; must be called before importing pyplot.
- **matplotlib.get_backend()** - Get the current backend name.
- **matplotlib.interactive(b: bool)** - Set interactive mode on or off.
- **matplotlib.is_interactive()** - Return whether interactive mode is on.
- **matplotlib.colormaps() -> list[str]** - List available colormaps.
- **matplotlib.multivar_colormaps() -> list[str]** - List available multivariate colormaps.
- **matplotlib.bivar_colormaps() -> list[str]** - List available bivariate colormaps.
- **matplotlib.color_sequences() -> list[str]** - List available color sequences.
- **matplotlib.RcParams.find_all(pattern)** - Return a filtered `RcParams` matching a pattern.
- **matplotlib.RcParams.copy()** - Return a copy of the `RcParams`.
- **matplotlib.RcParams._set(key, val)** - Public (documented) helper to set a parameter with Matplotlib semantics.

## Security

This SKILL.md teaches only safe, standard usage of the Matplotlib library. It does **not** instruct agents to access, modify, or transmit files or data outside the user's project directory. All examples are limited to configuration, debugging, and visualization. No destructive or privileged actions are included or permitted.