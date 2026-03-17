---
name: bump-version
description: Bump the version of the zenoh-ros2-sdk package across all configuration files. Use when the user asks to update, bump, or change the package version, or when preparing a new release.
---

# Bump Version

This skill guides you through upgrading the version number of the `zenoh-ros2-sdk` package.

## When to Use

- User asks to "bump", "update", or "change" the version
- Preparing a new release (major, minor, or patch)
- Version numbers are out of sync across config files

## 1. Determine the New Version

Decide whether this is a Major, Minor, or Patch release.
- **Current Version**: Check `pyproject.toml` or `zenoh_ros2_sdk/__init__.py`.
- **Example**: `0.1.2` -> `0.1.3` (Patch)

## 2. Update Files

You must update the version string in the following **3 files**. Ensure they all match exactly.

### A. `pyproject.toml`
Update the `version` field under `[project]`:
```toml
[project]
name = "zenoh-ros2-sdk"
version = "0.1.3"  # <--- Update this
```

### B. `zenoh_ros2_sdk/__init__.py`
Update the `__version__` variable:
```python
__version__ = "0.1.3"  # <--- Update this
```

### C. `setup.py`
Update the `version` argument in the `setup()` call:
```python
setup(
    name="zenoh-ros2-sdk",
    version="0.1.3",  # <--- Update this
    # ...
)
```

## 3. Verify Changes

Run the following command to verify consistency:
```bash
python3 setup.py --version
```
The output **must** match your new version.

## 4. Commit Changes

Commit the changes with a standard message:
```bash
git add pyproject.toml setup.py zenoh_ros2_sdk/__init__.py
git commit -m "bump(version): update version to 0.1.3"
```
