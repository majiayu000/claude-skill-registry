---
name: installer-quality-audit
description: |-
  Use when auditing install, setup, bootstrap, or update scripts for safe, idempotent behavior.
  Triggers:
practices:
- pragmatic-programmer
skill_api_version: 1
user-invocable: false
hexagonal_role: supporting
context:
  window: inherit
  intent:
    mode: task
metadata:
  tier: judgment
  stability: stable
  dependencies: []
  category: engineering-quality
  maturity: source
  clean_room: true
  owner: agentops
  primary_artifacts:
  - install.sh
  - uninstall.sh
output_contract: 'workmanship_report with sections: verdict, findings, changes, verification, residual_risk.'
---

# Installer Workmanship

Use this skill to write or repair an install script so a stranger can run it on
their machine, run it again, and undo it — without losing config, getting a
surprise password prompt, or being forced to reboot. An installer is a guest in
someone's home directory; it behaves accordingly.

## ⚠️ Critical Constraints

- **Idempotent: re-running changes nothing the second time.** Every action
  checks state before acting. **Why:** users re-run installers to repair or
  upgrade; a non-idempotent script duplicates lines, restacks PATH, or fails.
  - WRONG: `echo 'export PATH=$PATH:/opt/tool/bin' >> ~/.zshrc`
  - CORRECT: `grep -qF '/opt/tool/bin' ~/.zshrc || echo '...' >> ~/.zshrc`
- **Additive: never clobber the user's existing config.** Append, merge, or
  write a new file — never overwrite one you did not create. **Why:** a single
  `cp config ~/.config/app/config` can erase hours of someone's customization.
  - WRONG: `cp ./gitconfig ~/.gitconfig`
  - CORRECT: back up first (`cp ~/.gitconfig ~/.gitconfig.bak-$(date +%s)`),
    then merge or write only the keys you own.
- **No surprise sudo or reboots.** Detect when privilege is needed, explain
  why, and ask — never wrap the whole script in `sudo`. **Why:** a script that
  silently escalates or reboots is indistinguishable from malware to a wary user.
- **Preflight before any mutation.** Check OS, shell, required tools, disk,
  network, and write permissions up front; fail with a clear message before
  touching anything. **Why:** a half-applied install is worse than a refused one.
- **Fail loud, leave clean.** Use `set -euo pipefail`; on error the host is in a
  known state (untouched or rolled back), never half-configured.

## Why This Exists

Most install scripts are written for the author's machine on the happy path:
they assume bash, assume sudo, assume nothing already exists, and assume one OS.
The first time a real user re-runs one, or runs it on a slightly different
system, it duplicates config, clobbers a dotfile, hangs on a password prompt, or
dies halfway and leaves a mess with no way back. This skill is the forcing
function for the trustworthy installer: safe to re-run, safe on a config that
already exists, honest about privilege, and reversible.

## Quick Start

1. Locate or create the installer (`install.sh`, `setup.sh`, `bootstrap.sh`).
2. Inventory what it touches: files written, PATH/RC edits, packages, services.
3. For each action, confirm it is **guarded** (state-checked) and **additive**.
4. Add a **preflight** block at the top and an **uninstall** counterpart.
5. Run the four-way check: fresh run, re-run, partial-failure, uninstall.
6. Run `bash scripts/validate.sh` and report the verdict.

## The Five Properties of a Trustworthy Installer

### 1. Idempotent (safe to re-run)
Every mutating step is preceded by a check. The pattern is *test, then act*:

```bash
command -v tool >/dev/null 2>&1 || install_tool          # tool present?
line='export PATH="$PATH:/opt/tool/bin"'
grep -qF "$line" "$RC" || printf '%s\n' "$line" >> "$RC"  # line in rc file?
[ -d "$DEST" ] || mkdir -p "$DEST"                        # dir exists?
[ "$(readlink "$LINK" 2>/dev/null)" = "$TARGET" ] || ln -sfn "$TARGET" "$LINK"
```

A second run prints "already installed / up to date" and exits 0.

### 2. Additive (no clobbering)
You own only the files and config keys you create. For anything pre-existing,
back it up before touching it, and prefer merge over overwrite.

```bash
backup() { [ -e "$1" ] && cp -a "$1" "$1.bak-$(date +%Y%m%d-%H%M%S)"; }
backup "$HOME/.gitconfig"
```

Use idempotent markers so a managed block can be updated in place without eating
user edits around it:

```bash
# >>> tool managed block >>>
...your lines...
# <<< tool managed block <<<
```

Re-runs replace only the text between the markers.

### 3. Cross-platform
Detect, do not assume. Branch on OS and package manager; pick the user's real
shell rc, not a hardcoded one. Fail closed for unknown platforms.

```bash
case "$(uname -s)" in
  Darwin) PKG="brew install" ;;
  Linux)  command -v apt >/dev/null && PKG="sudo apt-get install -y" \
            || { command -v dnf >/dev/null && PKG="sudo dnf install -y"; } ;;
  *) echo "Unsupported OS: $(uname -s)" >&2; exit 1 ;;
esac
```

Avoid bashisms if the shebang is `#!/bin/sh`; quote every path (spaces, `~`).

### 4. No surprise privilege or reboots
Run as the invoking user by default. When a step genuinely needs root, isolate
it, explain it, and let the user decline:

```bash
need_sudo() {
  command -v sudo >/dev/null || { echo "This step needs root; re-run as root." >&2; return 1; }
  echo "About to install system packages (requires sudo): $*"
  sudo "$@"
}
```

Never call `reboot`; if a change needs a restart or a new shell, *print the
instruction* and let the user choose when.

### 5. Recovery and uninstall
Ship the undo with the install. A clear `uninstall.sh` (or `install.sh
--uninstall`) removes what you added — and only what you added — restoring
backups where they exist. Print where backups went so recovery is obvious. Use
atomic writes for generated files (write to a temp path, validate, then `mv`
into place) so an interrupted run never leaves a half-written file.

## Preflight Checks

Run before any mutation; fail fast with a precise message:

- **OS / arch** supported (`uname -s`, `uname -m`).
- **Required tools** present (`command -v git curl ...`), or installable.
- **Write permission** to every target dir (`[ -w "$DEST" ]`).
- **Disk space / network** if the install needs a download or sizeable write.
- **Existing install** detected → switch to upgrade/repair, do not duplicate.

## Audit Flow (for an existing installer)

1. List every side effect: file write, RC edit, package, service, symlink,
   download, permission change.
2. For each side effect, ask: is it guarded (idempotent)? Is it additive (backs
   up / merges)? Rewrite any that are not.
3. Confirm a preflight block exists and covers OS, tools, and permissions.
4. Model at least three runs: fresh install, repeat install, and partial install
   after an early failure. Each must leave a sane state.
5. Check privilege: is `sudo` scoped to the steps that need it, with an
   explanation? Is there any silent `reboot`?
6. Confirm an uninstall/recovery path exists and reverses exactly the install;
   confirm verification proves the thing works, not just that files exist.

## Output Specification

Return a workmanship report (also applied to the installer when repairing):

- **Verdict:** pass, needs work, or blocked.
- **Findings:** ordered by severity, each tied to one of the five properties.
- **Changes:** what was edited and why.
- **Verification:** the commands run (fresh / re-run / uninstall) and results.
- **Residual risk:** untested platforms, unbacked-up files, irreversible steps.

## Quality Rubric

- Running the installer twice in a row leaves the host byte-identical after the
  first run and exits 0 both times (idempotency proven, not asserted).
- No pre-existing user file is overwritten without a timestamped backup, and no
  `sudo` or `reboot` runs without an explicit, declinable prompt.
- An uninstall path exists, removes only what the installer added, and a
  preflight block fails clearly before any mutation on an unmet requirement.

## Examples

Turning a clobbering, non-idempotent fragment into a workmanlike one:

- Input:
  ```bash
  echo 'alias g=git' >> ~/.bashrc
  cp ./config.toml ~/.config/app/config.toml
  ```
- Output:
  ```bash
  grep -qxF 'alias g=git' "$RC" || echo 'alias g=git' >> "$RC"
  dest="$HOME/.config/app/config.toml"
  [ -e "$dest" ] && cp -a "$dest" "$dest.bak-$(date +%s)"
  mkdir -p "$(dirname "$dest")"; install -m 0644 ./config.toml "$dest"
  ```

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Re-running duplicates PATH/alias lines | Unguarded `>>` appends | Guard with `grep -qF ... \|\| echo ...` or a managed marker block. |
| User lost their dotfile customizations | `cp`/overwrite of an existing file | Back up before writing; merge or write only owned keys. |
| Script hangs on a password prompt | Whole script wrapped in `sudo` | Scope `sudo` to the steps that need it; explain and let the user decline. |
| Works on the author's Mac, fails on Linux | Hardcoded paths / package manager | Detect OS + package manager; pick the real shell rc; quote paths. |
| Half-installed mess after an error | No `set -e` / no rollback | Add `set -euo pipefail`; trap errors; restore backups or leave untouched. |
| No way to undo the install | No uninstall path shipped | Add `uninstall.sh` that reverses exactly what install added. |

## See Also

- `scripts/validate.sh` — structural self-check for this skill.
- `changelog-md-workmanship` — sibling workmanship skill for release history.
