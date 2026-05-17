# Differential CVE Pass

Phase 5 capability. The audit runs external CVE scanners against both
the OLD and NEW `mix.lock` and diffs the result, so the user learns
**what each dep update actually patched** — not just "no current
vulnerabilities."

## Why

`mix_audit` only sees the current lock. If a 25-package update closes
four CVEs disclosed in the last two weeks (real virgil example,
2026-05-12), the user just sees "No vulnerabilities found" — and never
learns they were exposed for up to 12 days. The differential pass
turns that into a security changelog.

## Architecture

```
mix_audit_diff (references/external-tools.md)
  ├─► run mix_audit against OLD mix.lock → cves_old.json
  └─► run mix_audit against NEW mix.lock → cves_new.json
                  │
                  ▼
         scripts/diff_cves.py
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
    patched  introduced  still_exposed
    (info)    (block)      (block)
                  │
                  ▼
       output-renderer.md headline:
       "🚨 N updates patched real CVEs"
```

## Lock-swap mechanics

Three strategies considered. We use **tmpdir copy** (option b).

| Option | Verdict |
|--------|---------|
| (a) `MIX_LOCKFILE` env var | Mix 1.18 has no such variable — rejected |
| **(b) tmpdir copy** | Chosen — simplest, no git state mutation |
| (c) `git worktree add` | Mutates `.git/`; branch state to clean up; rejected |

Implementation in `_mix_audit_run_with_lock` (external-tools.md):

```bash
tmpdir="$(mktemp -d -t deps-audit-XXXXXX)"
cp mix.exs config/* "${tmpdir}/"
cp "${OLD_LOCK_FILE}" "${tmpdir}/mix.lock"
( cd "${tmpdir}" && mix deps.audit --format json )
rm -rf "${tmpdir}"
```

Crucially, the real `mix.lock` is **never touched**. Iron Law #2
(non-mutating) holds.

`mix deps.audit` reads the lock and queries its locally-cached GHSA
advisory DB. It does **not** require `mix deps.get` to run — the
tmpdir copy works offline.

## CVE finding schema

Each finding emitted by `diff_cves.py` (NDJSON, one per line):

| Field | Type | Notes |
|-------|------|-------|
| `category` | `patched`/`introduced`/`still_exposed` | Set membership |
| `rule_id` | `"ext:mix-audit:diff"` | Distinct from `ext:mix-audit` |
| `severity` | `info`/`warn`/`block` | Per category × raw_severity |
| `ghsa_id` | `GHSA-xxxx-xxxx-xxxx` | Primary key |
| `cve_id` | `CVE-2026-12345` | Display only — may be absent |
| `package` | `decimal` | Primary key |
| `old_version` | `2.3.0` or `null` | Null when `introduced` |
| `new_version` | `3.1.0` or `null` | Null when `patched` |
| `severity_label` | `critical`/`high`/`moderate`/`low` | mix_audit raw |
| `title` | `"DoS via unbounded exponent"` | From advisory |
| `disclosed_at` | `"2026-05-07"` | ISO date or null |
| `exposure_days` | `5` | `today - disclosed_at` |
| `message` | `"decimal 2.3.0 → 3.1.0: CVE-... (high) — DoS"` | Pre-rendered |

## Severity per category

| Category | Raw severity | Final |
|----------|--------------|-------|
| `patched` | (any) | `info` |
| `introduced` | critical/high | `block` |
| `introduced` | moderate | `warn` |
| `still_exposed` | critical/high | `block` |
| `still_exposed` | moderate | `warn` |

`patched` is intentionally `info` — the update **is** the fix. The
renderer (`output-renderer.md`) lifts these to the headline section
despite their low severity, so the user sees the security changelog
before any other report content.

## Set key

`(ghsa_id, package)`. Version is deliberately NOT part of the key:
a CVE that affected OLD `decimal 2.3.0` and ALSO affects NEW
`decimal 2.4.0` is "still exposed" — the bump didn't address the CVE.

When the GHSA advisory has no ID (rare), we fall back to the CVE ID.
If neither is present, the entry is skipped (can't deduplicate).

## Caller flow

Invoked by the audit driver after `mix_audit_run` (Step 4 of SKILL.md
Execution Flow):

```bash
# All artifacts live under ${AUDIT_TMPDIR} (per-run tmpdir established
# by the driver — see references/audit-tmpdir.md). The driver's
# `trap "rm -rf ${AUDIT_TMPDIR}" EXIT` removes everything on exit.

# 1. Resolve OLD lock (Mode B: HEAD; Mode C: --base ref).
git show "${BASE_REF:-HEAD}:mix.lock" > "${AUDIT_TMPDIR}/lock.old"

# 2. Run mix_audit against both states (emits cves_old.json + cves_new.json).
OLD_LOCK_FILE="${AUDIT_TMPDIR}/lock.old" \
NEW_LOCK_FILE=mix.lock \
  mix_audit_diff

# 3. Compute diff.
python3 scripts/diff_cves.py \
  --old "${AUDIT_TMPDIR}/cves_old.json" \
  --new "${AUDIT_TMPDIR}/cves_new.json" \
  --out "${AUDIT_TMPDIR}/diff_cves.jsonl" \
  --summary

# 4. Renderer reads diff_cves.jsonl, prepends the headline section
#    when any patched/introduced/still_exposed findings exist.
```

## Disabling

`--no-differential` skips the diff pass and runs only single-state
`mix_audit_run` against the NEW lock (Phase 4 behavior). The CLI flag
maps to setting `DIFFERENTIAL=0` in the driver.

## Failure modes

| Failure | Behavior |
|---------|----------|
| OLD lock not in git (new project) | Skip diff; treat all NEW CVEs as `introduced` |
| `mix_audit` not installed | Skip diff entirely (warn) |
| Tmpdir copy fails (no disk) | Surface error; DO NOT fall back to mutating real lock |
| GHSA cache stale | Emit freshness WARN; continue (results may miss new disclosures) |
| OLD lock parse error | Skip diff; emit WARN |

## Related

- `external-tools.md` — `mix_audit_run` wrapper + `mix_audit_diff` driver
- `output-renderer.md` — security-changelog headline section
- `differential.md` — Phase 2 native-rule differential (file-scoped, distinct from this CVE pass)
- `../scripts/diff_cves.py` — the diff implementation
