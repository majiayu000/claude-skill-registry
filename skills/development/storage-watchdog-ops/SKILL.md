---
name: storage-watchdog-ops
description: |-
  Operate ACFS storage watchdog: inspect disk pressure, logs, and Rust target cleanup.
  Triggers: storage, watchdog, disk pressure, target cleanup.
practices:
- devsecops-cdlc
- pragmatic-programmer
- testable-architecture
hexagonal_role: supporting
consumes:
- error-reports
- runtime-metrics
- runtime-configuration
produces:
- triage-finding
- remediation-action
- escalation-note
context_rel:
- kind: partnership
  with: system-performance-remediation
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: judgment
  stability: stable
  external_dependencies:
  - systemd (user)
  - storage-watchdog daemon
output_contract: "A storage-watchdog operating decision: the observed disk + daemon state, the interpretation (pressure active? did safe cleanup run? is it blocked?), the chosen remediation (let it run, force a dry-run tick, hand-clean a Rust target/, or adjust thresholds), and an escalation note when cleanup cannot relieve pressure."
---

# storage-watchdog-ops

Operator runbook for the **ACFS storage watchdog** — the Go daemon
(`acfs-storage-watchdog.service`, built from `~/acfs/ops/storage-watchdog`).
This skill is the human/agent **trigger and remediation layer** over that
daemon; it does not reimplement cleanup. When you need to know *is the disk
under pressure, did the watchdog handle it, and what do I do if it didn't* —
this is the runbook.

## What the daemon actually does (so you interpret it correctly)

- It is a **narrow, safe** disk-reclaimer. It deletes **only** directories
  literally named `target` whose **parent directory contains `Cargo.toml`**
  (Rust build artifacts). Nothing else is ever removed.
- It **does not follow symlinks**, never deletes the filesystem root, `.`, or
  `""`, and never touches source files or non-Rust `target/` directories.
- Cleanup **starts only under pressure**: free space below `--min-free-gb`
  (service default 50) **OR** used percent at/above `--max-used-pct` (default
  90). With no pressure it logs `ok: no pressure` and deletes nothing.
- Under pressure it sorts candidates **oldest-mtime first** and deletes until
  free space reaches `--target-free-gb` (default 100) or candidates are
  exhausted, then logs `cleanup complete`.
- It runs as a **user** systemd service, `Nice=19` / `IOSchedulingClass=idle`,
  ticking every `--interval-seconds` (default 600). Default scan roots:
  `~/dev ~/acfs ~/.cargo`.

Thresholds are also overridable by env (`STORAGE_WATCHDOG_MIN_FREE_GB`,
`STORAGE_WATCHDOG_MAX_USED_PCT`, `STORAGE_WATCHDOG_TARGET_FREE_GB`,
`STORAGE_WATCHDOG_INTERVAL_SECONDS`, `STORAGE_WATCHDOG_STATE_DIR`,
`STORAGE_WATCHDOG_LOG_FILE`).

## 1. Check status

```bash
# Is the daemon alive and ticking?
systemctl --user status acfs-storage-watchdog.service

# Recent decisions from the service journal
journalctl --user -u acfs-storage-watchdog.service -n 50 --no-pager

# Persistent decision log (survives restarts)
tail -n 50 "${STORAGE_WATCHDOG_LOG_FILE:-$HOME/.local/state/acfs-storage-watchdog/watchdog.log}"

# Ground truth on the disk it is protecting
df -h "$HOME/dev" "$HOME/acfs" 2>/dev/null
```

Key log lines to find (each tick emits a `check`):

```
storage-watchdog: check avail_kb=… used_pct=… min_free_gb=50 max_used_pct=90 target_free_gb=100 dry_run=false roots=…
storage-watchdog: ok: no pressure
storage-watchdog: delete target size_kb=… mtime=… path=…
storage-watchdog: cleanup complete candidates=… deleted_kb=… avail_kb=…
```

## 2. Interpret

| Observation | Meaning | Action |
|---|---|---|
| `active (running)`, recent `check`, `ok: no pressure` | Healthy. Disk is above thresholds; nothing to clean. | None. |
| `check` with `avail_kb` low / `used_pct` ≥ max, then `delete target …` / `cleanup complete` | Working as designed; it reclaimed Rust artifacts. | Confirm `df -h` recovered. None. |
| Pressure in `check` but **no** `delete`/`cleanup` lines and `cleanup complete candidates=0` | Pressure is real but **no safe candidates exist** — nothing on disk is a Rust `target/` under a `Cargo.toml`. The watchdog can't help. | Go to §3 manual + §4 escalate. The bloat is elsewhere. |
| `delete failed path=… err=…` | A specific target couldn't be removed (perms, busy). It continues to the next. | Investigate that path manually (§3). |
| `failed`/`inactive`, no recent `check` | Daemon down — it is **not** protecting the disk. | Go to §3 restart. |
| `no scan roots exist: …` (exit) | Configured roots are absent on this host. | Fix `--root` flags in the unit (§3 thresholds). |

The watchdog **only ever frees Rust `target/` space**. If `df` says the disk is
full of media, logs, container layers, or a single huge non-Rust dir, a healthy
watchdog will correctly do nothing — that is not a watchdog bug, it is a
different remediation (see system-performance-remediation).

## 3. Remediate

**Restart a down daemon:**

```bash
systemctl --user restart acfs-storage-watchdog.service
systemctl --user status acfs-storage-watchdog.service
journalctl --user -u acfs-storage-watchdog.service -n 20 --no-pager
```

**Force an immediate, non-destructive assessment** (does not wait for the next
tick; deletes nothing — shows exactly what it *would* remove, oldest first):

```bash
cd "$HOME/acfs/ops/storage-watchdog"
go run ./cmd/storage-watchdog --once --dry-run --root "$HOME/dev" --root "$HOME/acfs"
```

**Force a real one-shot cleanup** (same safety policy; only Rust targets):

```bash
cd "$HOME/acfs/ops/storage-watchdog"
go run ./cmd/storage-watchdog --once --root "$HOME/dev" --root "$HOME/acfs"
```

**Prove the safety policy still holds** before trusting a forced run (creates a
throwaway fixture, asserts old/new Rust targets deleted but source + non-Rust
`target/` preserved):

```bash
cd "$HOME/acfs/ops/storage-watchdog"
go run ./cmd/storage-watchdog --self-test
```

**Hand-clean a single Rust target the daemon flagged but couldn't remove**
(verify it really is a Rust target first — never blind `rm -rf`):

```bash
p="<path from the delete-failed log line>"
test -f "$(dirname "$p")/Cargo.toml" && test "$(basename "$p")" = target \
  && du -sh "$p" && rm -rf "$p"   # only after both tests pass
```

**Adjust thresholds** (e.g. start cleaning earlier on a small disk) — edit the
unit's `ExecStart` flags or set env, then reload:

```bash
systemctl --user edit acfs-storage-watchdog.service   # override min/max/target or roots
systemctl --user daemon-reload
systemctl --user restart acfs-storage-watchdog.service
```

## 4. Escalate

Escalate beyond this skill when:

- **Pressure persists after a real `--once` run** and `cleanup complete` shows
  `candidates=0` or `deleted_kb` far below what's needed — the disk is full of
  something the watchdog is (correctly) not allowed to touch. Hand off to
  **system-performance-remediation** to find the actual hog (`du -xh … | sort -h`,
  container/image layers, logs, datasets).
- **Repeated `delete failed`** on the same path → a permissions/ownership or
  busy-mount issue the watchdog can't resolve; needs host admin.
- **Daemon won't stay up** (`Restart=always` but flapping) → inspect
  `journalctl` for the `FATAL`/exit reason; likely bad flags or absent roots.
- The host is a **non-ACFS / non-Rust** box where this daemon was mis-deployed —
  disable it (`systemctl --user disable --now acfs-storage-watchdog.service`)
  rather than fighting `candidates=0`.

Never widen the deletion policy as a "fix" (deleting non-`target` dirs, removing
the `Cargo.toml`-parent check, or following symlinks). The narrow policy is the
safety guarantee; broadening it turns a reclaimer into a data-loss incident.

## Related

- `system-performance-remediation` — the broader disk/CPU/memory remediation rule
  this daemon was specialized from; use it when the watchdog has no candidates.
- ACFS source of truth: `~/acfs/ops/storage-watchdog/README.md` and
  `cmd/storage-watchdog/`.
