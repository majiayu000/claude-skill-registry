---
name: repo-facts
description: 'Summarize an arbitrary code repo (git or non-git) into a small, high-signal
  facts packet: languages, build/test tooling clues, notable paths, and size stats.'
---

---
name: repo_facts
description: Summarize an arbitrary code repo (git or non-git) into a small, high-signal facts packet: languages, build/test tooling clues, notable paths, and size stats.
---

# repo_facts

## Purpose

Produce a compact "facts packet" about the repository so the agent does not waste tokens repeatedly re-discovering:
- What languages dominate
- What build / test systems appear to be used
- Where source code and generated artifacts likely live
- Whether it's a git repo (and basic git state if available)

This skill is intentionally small: it avoids long README ingestion and avoids speculative instructions.

## How to use

Run the script from the repo root (or pass a path):

```sh
repo_facts .
repo_facts . --no-tree
repo_facts /path/to/repo --json

# (fallback if wrappers are not on PATH)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
python3 "$CODEX_HOME/skills/repo_facts/scripts/repo_facts.py" /path/to/repo --tree
```

## Output contract (high level)

- Default: Markdown summary (human-scannable) + "Next look" file pointers.
- `--json`: machine-readable JSON for programmatic consumption.

## Notes

- Works without git. If the directory is a git worktree, it prefers `git ls-files` for fast/accurate enumeration.
- Skips common heavy dirs by default (e.g., `.git/`, `node_modules/`, `target/`, `build/`, `.venv/`).
