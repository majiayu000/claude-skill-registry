---
name: disk-space-analyzer
description: Analyze disk space and find cleanable files. Use when user wants to clean disk, free up space, find large files, analyze disk usage, or asks about what's taking up space. Triggers on requests like "clean my disk", "free up space on C:", "find large files", "what's using my disk space", "disk cleanup".
---

# Disk Space Analyzer

Analyze disk space usage and identify files that can be safely cleaned. **Data source and scripts differ by OS** — do not reuse Windows scripts on macOS or vice versa.

**First: determine the current operating system**, then follow the workflow for that system only.

## System check

Before any workflow steps, determine the OS:

- **Windows**: `sys.platform == "win32"` or user is on Windows.
- **macOS**: `sys.platform == "darwin"` or user is on Mac.

You can run:
```bash
python3 -c "import sys; print(sys.platform)"
```
(`win32` → Windows, `darwin` → macOS)

## Next steps by system

- **If Windows** → Read and follow **[docs/windows.md](docs/windows.md)** for the full workflow (WizTree, scripts in `scripts/windows/`, analysis commands).
- **If macOS** → Read and follow **[docs/macos.md](docs/macos.md)** for the full workflow (different data source and scripts; no WizTree).

Do not mix: Windows workflow uses `scripts/windows/` (WizTree + CSV analysis). macOS workflow uses its own data source and scripts as described in `docs/macos.md`.
