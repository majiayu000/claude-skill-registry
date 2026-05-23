---
name: shellck
description: Run shellcheck on shell scripts after editing scripts or when debugging shell errors. Use for linting scripts in a repo (especially scripts/), catching issues like set -u with unset vars, bad subshell usage, or quoting mistakes.
---

# Shellck

## Overview

Provide a fast, repeatable shellcheck pass for repo scripts. Use this skill after editing shell scripts or when a script fails unexpectedly.

## Workflow

1) Ensure `shellcheck` is installed.
2) From the repo root, run the helper script.

### Quick start

Run against the default `scripts/` directory:

```bash
./scripts/run_shellck.sh
```

Run against specific files or directories:

```bash
./scripts/run_shellck.sh scripts/perf-profiler
./scripts/run_shellck.sh scripts/ other/dir/some.sh
```

## Behavior

- If no paths are provided, it scans `scripts/` for shell scripts.
- If paths are provided, it accepts files or directories and filters to shell scripts.
- Detects shell scripts by:
  - Extension: `.sh`, `.bash`, `.zsh`, `.ksh`, `.command`
  - Shebang: `#!/bin/bash`, `#!/usr/bin/env bash`, etc. (sh/bash/zsh/ksh)
- Exits non-zero on shellcheck failures.

### Debug mode

Set `SHELLCK_DEBUG=1` to see which files are matched/skipped:

```bash
SHELLCK_DEBUG=1 ./scripts/run_shellck.sh
```

## Resources

### scripts/

- `run_shellck.sh`: shellcheck runner with sensible defaults and directory filtering.
