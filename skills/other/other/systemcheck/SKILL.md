---
name: SystemCheck
description: "Check the forge ecosystem for staleness — installed skills vs source, binary freshness, lib consistency, version drift, submodule pointers, hook config. USE WHEN stale, freshness, out of date, check staleness, need to rebuild, make install needed, system check."
version: 0.1.0
---

# SystemCheck

Quick diagnostic that answers: "is everything current, or do I need to `make install`?"

Checks six staleness vectors across the forge ecosystem and produces a pass/fail summary with actionable fixes.

## Companion Script

`system-check.sh` in this skill directory implements all six checks. Run it first:

```bash
bash "${FORGE_MODULE_ROOT:-Modules/forge-core}/skills/SystemCheck/system-check.sh"
```

For per-item breakdown, add `--verbose`:

```bash
bash "${FORGE_MODULE_ROOT:-Modules/forge-core}/skills/SystemCheck/system-check.sh" --verbose
```

## Instructions

1. Run the companion script (compact mode).

2. Present the output table to the user as-is.

3. If any check fails, the script prints a `Fixes:` section. Offer to run the suggested commands.

4. If the user asks to drill down into a specific check, re-run with `--verbose` and explain the details.

5. If the script is unavailable or a check needs manual investigation, use the check procedures below.

## Checks

### Check 1: Installed Skills vs Source

Read `.claude/skills/.manifest` (written by `install-skills`) to determine which module owns each installed skill. For each entry, compare the installed SKILL.md body against its source using `shasum -a 256` (strip frontmatter first — `install-skills` merges `claude:` keys, so frontmatter will differ by design).

Three failure modes:
- **stale**: installed body differs from source
- **orphaned**: installed skill not listed in `.manifest`
- **ghost**: manifest says module X owns it, but source SKILL.md is missing (module removed or skill deleted)

Falls back to directory scanning if `.manifest` is absent.

### Check 2: Binary Freshness

For each symlink in `~/.local/bin` that points into the forge root, find the crate's `src/` directory and compare the binary mtime against the newest `.rs` source file. If any source is newer, the binary is stale.

### Check 3: Lib Submodule Consistency

For each module that has a `lib/` submodule, read its commit SHA. Report if any module's `lib/` points to a different commit than the others. All modules should track the same forge-lib commit.

### Check 4: Version Drift

For each module, read version from up to three sources and report mismatches within a module:

| Source | How to read |
|--------|-------------|
| `module.yaml` | `awk '/^version:/{print $2; exit}'` |
| `plugin.json` | `python3 -c "import json; print(json.load(open('plugin.json'))['version'])"` |
| `Cargo.toml` | `awk -F'"' '/^version/{print $2; exit}'` |

### Check 5: Submodule Pointer Drift

Compare the parent repo's recorded submodule pointer against each submodule's actual HEAD. A `+` prefix in `git submodule status` means the submodule HEAD has moved beyond the recorded pointer. A `-` means not initialized.

### Check 6: Hook Config Completeness

Read `.claude/settings.json` and verify all expected dispatch events are present:

`SessionStart`, `PreToolUse`, `PostToolUse`, `Stop`, `PreCompact`, `UserPromptSubmit`, `SubagentStop`, `SessionEnd`, `Notification`

## Fixes Reference

| Problem | Fix |
|---------|-----|
| Skills stale | `make install-skills` |
| Binaries stale | `make build && make install-binaries` |
| Lib drift | Update lib submodules to canonical commit |
| Version drift | Align versions in the affected module |
| Submodule pointers dirty | Commit parent repo |
| Hook config incomplete | `make install-hooks` |

## Constraints

- Read-only — never modify files, only report
- Use `shasum -a 256` (macOS compatible), not `sha256sum`
- Use `git -C` directly for submodule operations (RTK does not support `-C`)
- Skip checks gracefully when a module is not initialized or a file is missing
- Compact summary table by default — only drill down into details when the user asks
