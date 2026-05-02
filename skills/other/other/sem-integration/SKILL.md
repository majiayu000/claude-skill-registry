---
name: sem-integration
description: >
  Foundation skill for sem (semantic diff CLI) integration.
  Provides detection, install-on-first-use, and output
  normalization patterns for consumer skills.
version: 1.9.3
alwaysApply: false
category: infrastructure
tags:
- sem
- semantic-diff
- git
- foundation
provides:
  infrastructure:
  - sem-detection
  - sem-fallback
  patterns:
  - install-on-first-use
  - graceful-degradation
estimated_tokens: 400
progressive_loading: true
module_strategy: reference-based
modules:
- modules/detection.md
- modules/fallback.md
---

# sem Integration

Foundation patterns for using
[sem](https://github.com/Ataraxy-Labs/sem) semantic
diffs in night-market skills.

## When To Use

Consult this skill when building or modifying skills that
consume git diff output. It provides the detection,
installation, and fallback patterns.

## When NOT To Use

- Direct sem CLI usage (just run `sem diff` yourself)
- Skills that don't consume diff output

## Detection Pattern

Check sem availability once per session:

```bash
# Detection (cache per session)
_sem_check() {
  local cache="${CLAUDE_CODE_TMPDIR:-/tmp}/sem-available"
  if [ -f "$cache" ]; then
    cat "$cache"
    return
  fi
  if command -v sem &>/dev/null; then
    echo "1" | tee "$cache"
  else
    echo "0" | tee "$cache"
  fi
}
```

When `_sem_check` returns `0`, offer installation.
See `modules/detection.md` for install-on-first-use
logic and platform-specific commands.

## Semantic Diff Pattern

Primary path (sem available):

```bash
sem diff --format json <baseline>
```

Fallback path (sem unavailable):

```bash
git diff --name-only --diff-filter=A <baseline>
git diff --name-only --diff-filter=M <baseline>
git diff --name-only --diff-filter=D <baseline>
git diff --name-only --diff-filter=R <baseline>
```

See `modules/fallback.md` for output normalization
that produces the same entity schema from both paths.

## Impact Analysis Pattern

Primary path (sem available):

```bash
sem impact --json <file-or-entity>
```

Fallback path (sem unavailable): use rg/grep to trace
callers by filename. See `modules/fallback.md`.
