# Execution Flow (Phase 5)

Authoritative pacing for `/phx:deps-audit`. The SKILL.md "Execution Flow"
section is a thin pointer; the runtime contract lives here.

## Default = full scan

The default invocation runs **all 8 MVP rules** plus all available external
tools (`mix hex.audit`, `mix_audit`, `osv-scanner`) plus Hex API enrichment
plus the differential CVE pass.

**There is no interactive choice prompt.** Earlier prototypes asked the
user "run heuristics?" before kicking off rule execution. That created a
silent-failure footgun on large diffs — the user picked "no" to save
time, the skill reported "no findings," and a bidi-char trojan landed in
the lock with no warning. **Removed.** Heuristics run by default.

```
/phx:deps-audit          ← runs the full pipeline
/phx:deps-audit --base main
/phx:deps-audit --preview httpoison
```

## `--quick`: CVE + retirement only

The opt-out is `--quick`. When set, the audit skips the 8 native rules,
Hex API enrichment, and the differential CVE pass — keeping only:

- `mix hex.audit` (retired-package check)
- `mix_audit` (GHSA CVE check, current lock only)

Use case: very large diffs (>50 packages), CI gates where wall-time
matters more than novel-attack detection, or pre-PR triage where the
maintainer just wants to confirm no known-CVE updates are merging dirty.

Target latency on a 25-package update: **<10s**.

```
/phx:deps-audit --quick
```

Flag synonyms considered: `--cve-only`, `--no-heuristics`, `--fast`.
**`--quick`** was chosen for brevity and cultural alignment with
`mix test --quick`.

## Streaming progress

The full scan emits one line per package per phase to stdout:

```
[ 1/25] cowboy 2.13.0 — fetching tarball...
[ 2/25] cowlib 2.15.0 — fetching tarball...
...
[ 1/25] cowboy 2.13.0 — running rule 1 (bidi)...
[ 1/25] cowboy 2.13.0 — running rule 2 (eval)...
...
[ 1/25] cowboy 2.13.0 — Hex API: owners, downloads
[12/25] decimal 3.1.0 — running rule 8 (typosquat)...
[25/25] phoenix 1.8.7 — done (0 findings)
```

This was previously a `--verbose` opt-in. The dogfood session
(2026-05-12) showed users staring at silent terminals for 60-90s with
no signal — they assumed the skill had hung and Ctrl-C'd before
results came back. Streaming progress is now the default UX.

Format spec:

- `[N/M]` — package counter (current/total), zero-padded to align
- `pkg ver` — package name and NEW version
- ` — ` em-dash separator
- Phase verb in present continuous (`fetching`, `running`, `enriching`)
- Phase noun (optional but encouraged)

Render to stdout, not stderr, so the user sees it interactively but
machine consumers (`--json`, `--sarif`) can suppress with `--quiet`.

## Suppressing progress

| Flag | Effect |
|------|--------|
| `--quiet` | No streaming output; final result only |
| `--json` | Implies `--quiet`; JSON to stdout |
| `--sarif PATH` | Implies `--quiet`; SARIF to PATH |
| `--ci` | Implies `--quiet`; exits non-zero on BLOCK |

## Phase ordering

Default pipeline in order. Each step is independent and parallelism-safe
unless noted.

1. **Resolve diff** — `(pkg, old, new)` tuples from mix.lock pair
2. **Fetch tarballs** — 4-way parallel; both OLD and NEW versions
3. **Run 8 native rules** on NEW tarballs (per-package, parallel up to 4)
4. **External CVE pass** — `mix_audit_diff` (OLD + NEW), then `diff_cves.py`
5. **External retirement** — `mix hex.audit` (current lock)
6. **Hex API enrichment** — owner, downloads, rule 6/8 (rate-limited 5/s)
7. **`hex_vet.exs` ledger** — downgrade vetted versions to INFO
8. **Differential native subtract** — Phase 2 `diff_findings.py`
9. **LLM triage** (if score >10 per package) — `hex-deps-triager` agent
10. **Render** — markdown table + sidecar JSON, with security-changelog headline

`--quick` skips steps 1, 3, 5b, 6, 7, 8, 9 — keeping only steps 1-lite,
2-lite (NEW only), 5a (`mix hex.audit`), 4-lite (`mix_audit` on NEW only,
no diff), and 10-lite (no headline, just table).

## When to break from these defaults

| Situation | Override |
|-----------|----------|
| CI gate, time-sensitive | `--quick --ci` |
| Pre-merge PR review | (default — full scan) |
| One-off package preview | `--preview pkg [pkg...]` (skips diff resolution) |
| Already-vetted batch | Run normally; `hex_vet.exs` handles downgrades |
| Air-gapped CI (no Hex API) | `--no-hex-api` (Phase 4 flag) |

## Wall-time budgets

| Diff size | Default scan | `--quick` |
|-----------|--------------|-----------|
| 1-5 packages | 5-15s | <3s |
| 10-25 packages | 30-90s | <10s |
| 50-100 packages | 2-4 min | 15-30s |
| 200+ packages | 5-10 min | <60s |

Numbers from the 2026-05-12 virgil dogfood (25 packages, ~75s default).
Older tarball-fetcher.md claimed 5-10 min was realistic; that was
pessimistic — the 4-way parallel fetcher is actually fast.

## `--trace` flag (Iron Law #1 auditability)

The 2026-05-13 enaia-main dogfood surfaced a verification gap: when
the audit reports "8 rules clean", there's no on-disk evidence the
rules actually ran. The tmpdir is gone, no Bash trace is captured by
ccrider, and a fast model could in principle synthesize a plausible
verdict from the lock-diff text alone — exactly the Iron Law #1 false
pass.

`--trace` writes a verifiable audit log to
`.claude/deps-audit/last-run.trace.log` documenting every shell command
the audit ran (one per line, prefixed with timestamp + duration):

```
2026-05-13T11:01:50.123Z [3.4s] mix hex.package fetch decimal 2.3.0 --unpack -o /tmp/phx-deps-audit-XXX/tarballs/decimal/2.3.0
2026-05-13T11:01:53.501Z [3.1s] mix hex.package fetch decimal 2.4.1 --unpack -o /tmp/phx-deps-audit-XXX/tarballs/decimal/2.4.1
2026-05-13T11:01:56.612Z [0.4s] grep -rP '[\x{202a}-\x{202e}\x{2066}-\x{2069}]' /tmp/phx-deps-audit-XXX/tarballs/decimal/2.4.1
...
```

The trace file is the single piece of evidence that Iron Law #1 was
upheld for a given run. It's not under `${AUDIT_TMPDIR}` — it survives
audit completion so a reviewer can verify after the fact. The model
SHOULD enable `--trace` by default when the gate hook is configured
(`policy.exs` exists), and otherwise leave it opt-in.
