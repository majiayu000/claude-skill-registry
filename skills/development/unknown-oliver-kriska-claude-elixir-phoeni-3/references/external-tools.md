# External Tool Wrappers

Three external CVE scanners layered on top of the 8 MVP rules. All optional
except `mix hex.audit` (ships with mix). **Never install — even if asked.**
Detect, warn with install instructions, skip cleanly.

## If the user asks "install mix_audit and re-run"

**Refuse the install. Run the audit with what's available.**

The audit skill is non-mutating. `mix.exs`, `mix.lock`, and the project
build state must stay untouched. If the user explicitly requests an
install, respond with the exact command for them to run, then continue
the audit with `mix_audit` skipped:

```
I can't install mix_audit — the audit skill is non-mutating and won't
modify mix.exs/mix.lock. Run this yourself, then re-invoke me:

    mix deps.add mix_audit --only dev
    mix deps.get

Meanwhile, I'll continue with mix_audit skipped. CVE coverage via GHSA
will be missing for this run; mix hex.audit (retirement check) and the
8 heuristic rules still cover novel-attack detection.
```

This is consent-resistant by design — a skill that mutates the project
"because the user asked" is indistinguishable, from a security review
perspective, from one that mutates on its own. See SKILL.md Iron Law #2.

## 1. `mix hex.audit` — retired-package check

Ships with Mix. Zero-config. Detects packages explicitly retired by their
maintainers via Hex.pm (security, deprecated, invalid, renamed, etc.).

```bash
hex_audit() {
  mix hex.audit 2>&1 | tee "${AUDIT_TMPDIR}/hex-audit.txt"
}
```

Output format (line per retirement):

```
phoenix_html 2.14.3
  Reason: invalid
  Message: Upgrade to 4.x for new HTML escaping API
```

Parse with awk:

```bash
awk '
  /^[a-z_][a-z0-9_]* [0-9]/ { pkg=$1; ver=$2 }
  /Reason:/ { reason=$2 }
  /Message:/ { msg=substr($0, 11); print pkg"|"ver"|"reason"|"msg }
' "${AUDIT_TMPDIR}/hex-audit.txt"
```

Severity mapping: `security` → BLOCK · `invalid` / `deprecated` / `renamed`
→ WARN.

**FP rate:** ~0%. Always integrate.

## 2. `mix_audit` — CVE check via GitHub Advisory Database

Hex package (`{:mix_audit, "~> 2.1", only: [:dev, :test], runtime: false}`).
Checks GHSA `pkg:hex` advisories.

```bash
mix_audit_run() {
  if ! mix help deps.audit >/dev/null 2>&1; then
    cat >&2 <<'EOF'
WARN: mix_audit not installed — skipping CVE check via GHSA.

To enable:
  mix archive.install hex mix_audit
  # or add to mix.exs:
  # {:mix_audit, "~> 2.1", only: [:dev, :test], runtime: false}
EOF
    _mix_audit_warn_cve_corpus_overlap >&2 || true
    return 0
  fi

  local lock_file="${LOCK_FILE:-mix.lock}"
  local out_path="${MIX_AUDIT_OUT:-${AUDIT_TMPDIR:?AUDIT_TMPDIR not set}/mix-audit.json}"

  # GHSA freshness check (Phase 5). If the cache directory is >N hours
  # old, emit a WARN — recent disclosures may be missing. Threshold is
  # 24h by default; override via GHSA_MAX_AGE_HOURS.
  _mix_audit_check_ghsa_freshness >&2 || true

  # First `mix deps.audit` of a session triggers a full dependency
  # compile (`Compiling N files (.ex)` for every dep). This is
  # EXPECTED — `mix_audit` has `runtime: false` but `mix` still
  # ensures the dep tree is built. It is slow (tens of seconds) and
  # noisy, NOT a failure. Always send JSON to a file and only `tail`
  # stdout for the verdict; never echo the raw compile log.

  if [ "${lock_file}" = "mix.lock" ]; then
    # Fast path: scan the project as-is.
    mix deps.audit --format json 2>/dev/null > "${out_path}"
  else
    # Differential path: scan against a non-default lock. We MUST NOT
    # mutate the project's mix.lock (Iron Law #2). Strategy: copy the
    # project to a tmpdir, swap in the requested lock, run mix
    # deps.audit, discard.
    _mix_audit_run_with_lock "${lock_file}" "${out_path}"
  fi
}

# Phase 5 — differential CVE pass.
#
# Run mix_audit against both OLD and NEW mix.lock states to detect
# CVEs patched by the update (the actionable narrative — "you were
# exposed for N days"). Use tmpdir copy strategy because:
#   - MIX_LOCKFILE env var is not Mix-supported as of 1.18.
#   - git worktree mutates .git/ and creates branch state.
#   - tmpdir copy is the simplest non-mutating option.
#
# Inputs (env):
#   OLD_LOCK_FILE — path to OLD mix.lock (e.g., from `git show HEAD:mix.lock`)
#   NEW_LOCK_FILE — path to NEW mix.lock (default: working mix.lock)
#
# Outputs (under per-run tmpdir — see references/audit-tmpdir.md):
#   ${AUDIT_TMPDIR}/cves_old.json
#   ${AUDIT_TMPDIR}/cves_new.json
mix_audit_diff() {
  local old_lock="${OLD_LOCK_FILE:?OLD_LOCK_FILE required for differential pass}"
  local new_lock="${NEW_LOCK_FILE:-mix.lock}"
  : "${AUDIT_TMPDIR:?AUDIT_TMPDIR not set — driver must establish per-run tmpdir first}"

  LOCK_FILE="${old_lock}" MIX_AUDIT_OUT="${AUDIT_TMPDIR}/cves_old.json" \
    mix_audit_run

  LOCK_FILE="${new_lock}" MIX_AUDIT_OUT="${AUDIT_TMPDIR}/cves_new.json" \
    mix_audit_run
}

# Internal: run mix deps.audit against an arbitrary mix.lock without
# mutating the project. Copies project to tmpdir, swaps lock, runs.
#
# Defense-in-depth for Iron Law #2: unsets MIX_* env vars that could
# otherwise redirect Mix back to the real project (MIX_DEPS_PATH,
# MIX_LOCKFILE, MIX_PROJECT, etc.). MIX_HOME is preserved so the Hex
# cache is reused.
_mix_audit_run_with_lock() {
  local lock_src="$1" out_path="$2"

  # Fail fast if the requested lock doesn't exist. Silent fall-through
  # would produce a false-green ("no vulnerabilities") report — the
  # worst possible failure mode for a security tool.
  if [ ! -f "${lock_src}" ]; then
    echo "ERROR: lock file not found: ${lock_src}" >&2
    return 2
  fi

  local tmpdir
  tmpdir="$(mktemp -d -t deps-audit-XXXXXX)" || {
    echo "ERROR: mktemp failed" >&2
    return 2
  }
  # Trap cleanup at function scope — caller may have its own EXIT trap.
  # shellcheck disable=SC2064
  trap "rm -rf '${tmpdir}'" RETURN

  # Reflink/hardlink-friendly copy. Exclude _build and deps to keep
  # the copy cheap; mix will resolve deps from Hex cache anyway.
  cp mix.exs "${tmpdir}/" 2>/dev/null || true
  [ -f mix.exs.lock ] && cp mix.exs.lock "${tmpdir}/" 2>/dev/null || true
  [ -d config ] && cp -R config "${tmpdir}/" 2>/dev/null || true
  # cp -L: dereference symlinks (don't trust a symlinked lock to point
  # where the caller thinks). Bubble cp failure to the caller.
  if ! cp -L "${lock_src}" "${tmpdir}/mix.lock"; then
    echo "ERROR: cannot copy ${lock_src} to tmpdir" >&2
    return 2
  fi

  (
    cd "${tmpdir}" || exit 1
    # Defense-in-depth: scrub MIX_* vars that could redirect Mix to
    # the real project. Keep MIX_HOME (Hex cache reuse) and PATH.
    unset MIX_DEPS_PATH MIX_BUILD_PATH MIX_LOCKFILE MIX_PROJECT MIX_ENV
    # mix deps.audit doesn't require deps to be fetched — it reads the
    # lock and queries the local GHSA cache. Avoid `mix deps.get` to
    # keep the run offline-fast and non-mutating.
    mix deps.audit --format json 2>/dev/null > "${out_path}"
  )
}

# Internal: when mix_audit is skipped because not installed, check if
# the diff contains packages with recent EEF CNA CVEs and emit a loud
# alert. The 2026-05-13 enaia-main dogfood exposed this gap: a diff
# touched `decimal 2.3 → 2.4`, `phoenix 1.8.5 → 1.8.7`, `postgrex 0.22.0
# → 0.22.2` — all three patch real EEF CNA CVEs (32686/32689/32687) —
# and the audit emitted the same generic "install mix_audit" hint as
# for any other skip, with no signal that this specific diff would have
# triggered three CVE matches.
#
# The corpus list is hand-curated from cna.erlef.org and refreshed in
# tandem with smoke fixtures (corpus.d/). Conservative pattern: only
# packages with at least one published CVE in the last 12 months.
_mix_audit_warn_cve_corpus_overlap() {
  local diff_json="${AUDIT_TMPDIR:-}/diff.json"
  [ -f "${diff_json}" ] || return 0

  # Subset of EEF CNA-tracked Hex packages with recent CVEs. Keep
  # narrow — false positives here erode trust faster than misses.
  local corpus="decimal phoenix postgrex bandit cowlib plug ecto"
  local hits=()
  for pkg in ${corpus}; do
    if jq -e --arg p "${pkg}" '.changed[]? | select(.package == $p)' \
         "${diff_json}" >/dev/null 2>&1; then
      hits+=("${pkg}")
    fi
  done

  [ "${#hits[@]}" -eq 0 ] && return 0

  cat <<EOF

🚨 mix_audit is not installed AND this diff touches packages with
   known recent CVEs on the EEF CNA list: ${hits[*]}

   The audit cannot confirm whether this update patches or introduces
   any of those CVEs. Install mix_audit and re-run for coverage:

     mix archive.install hex mix_audit

   Canonical Elixir CVE list: https://cna.erlef.org/cves/
EOF
}

# Internal: warn if the GHSA cache is staler than GHSA_MAX_AGE_HOURS.
# The mix_audit Hex package ships its advisory database as part of the
# Hex archive; it's refreshed when the user runs `mix deps.audit`
# directly, but the cache itself can lag behind cna.erlef.org.
_mix_audit_check_ghsa_freshness() {
  local max_age="${GHSA_MAX_AGE_HOURS:-24}"
  local cache_dir=""

  # Locate the GHSA advisory cache. mix_audit stores it under
  # _build/<env>/lib/mix_audit/priv/advisories/ when installed as a dep,
  # or under ~/.mix/archives/ when installed as an archive. Try both.
  for candidate in \
    "_build/dev/lib/mix_audit/priv/advisories" \
    "_build/test/lib/mix_audit/priv/advisories" \
    "$HOME/.mix/archives/mix_audit"*; do
    if [ -d "${candidate}" ]; then
      cache_dir="${candidate}"
      break
    fi
  done

  [ -z "${cache_dir}" ] && return 0  # Can't locate cache — skip warn.

  local mtime now age_hours
  # macOS stat -f %m, GNU stat -c %Y. Try both.
  mtime="$(stat -f %m "${cache_dir}" 2>/dev/null || stat -c %Y "${cache_dir}" 2>/dev/null)"
  [ -z "${mtime}" ] && return 0

  now="$(date +%s)"
  age_hours=$(( (now - mtime) / 3600 ))

  if [ "${age_hours}" -gt "${max_age}" ]; then
    cat <<EOF
WARN: GHSA advisory cache is ${age_hours} hours old (>${max_age}h threshold).
Recent disclosures (last 7 days) may be missing. Refresh with:

    mix deps.update mix_audit  # if installed as dep
    mix archive.install hex mix_audit --force  # if installed as archive

Canonical Elixir CVE list: https://cna.erlef.org/cves/
EOF
    return 1
  fi
  return 0
}
```

Output is JSON:

```json
{
  "pass": false,
  "vulnerabilities": [
    {
      "advisory": {"id": "GHSA-xxxx-xxxx-xxxx", "cve": "CVE-2026-12345",
                   "title": "...", "description": "...",
                   "severity": "high", "patched_versions": "~> 1.2.3"},
      "dependency": {"package": "...", "version": "..."}
    }
  ]
}
```

Severity mapping: `critical` / `high` → BLOCK · `moderate` → WARN ·
`low` → INFO.

**FP rate:** ~0% (advisory DB is curated). Coverage gap: GHSA has fewer Hex
entries than npm/RustSec, so absence is not proof of safety.

## 2a. GHSA cache freshness (Phase 5)

`mix_audit` ships its GHSA advisory database as part of the Hex package
or archive. The advisory DB is **not** refreshed automatically on each
`mix deps.audit` invocation — it updates only when the user explicitly
runs `mix deps.update mix_audit` or `mix archive.install hex mix_audit
--force`.

This matters because the EEF CNA disclosure cadence has accelerated:
14 Hex package CVEs were published in April-May 2026 alone (e.g.,
`postgrex 0.22.0 → 0.22.1` patched a SQL-injection CVE disclosed
**the same day** the 2026-05-12 virgil dogfood ran). A 1-week-old
advisory cache will miss these.

**Behavior:** `mix_audit_run` checks the mtime of the GHSA advisory
directory before running. If older than `GHSA_MAX_AGE_HOURS` (default
24), it emits a WARN to stderr with refresh instructions and a link to
the canonical EEF CNA list (<https://cna.erlef.org/cves/>).

**How to refresh manually:**

```bash
# If installed as a dep in mix.exs:
mix deps.update mix_audit

# If installed as a Mix archive:
mix archive.install hex mix_audit --force

# Verify freshness:
ls -la _build/dev/lib/mix_audit/priv/advisories/ | head
```

**Override the threshold:**

```bash
GHSA_MAX_AGE_HOURS=72 /phx:deps-audit  # tolerate 3-day-old cache
GHSA_MAX_AGE_HOURS=1  /phx:deps-audit  # paranoid mode
```

**Future (Phase 6+):** auto-refresh via a PreToolUse hook that watches
for `mix deps.audit` invocations and triggers `mix deps.update mix_audit`
if the cache is >24h old. Deferred until we can prove the refresh
itself is non-flaky (Hex registry can rate-limit or 503).

**Why not a `mix deps.update`?** Mutating `mix.lock` violates Iron
Law #2. The wrapper warns and continues — the user must refresh
explicitly. This is consent-resistant by the same logic as the
mix_audit-install refusal above.

## 3. `osv-scanner` — CVE check via OSV.dev

Standalone Go binary (`go install github.com/google/osv-scanner@latest`).
v2.3.5+ supports Elixir/Hex.

```bash
osv_scan() {
  if ! command -v osv-scanner >/dev/null 2>&1; then
    cat >&2 <<'EOF'
WARN: osv-scanner not installed — skipping CVE check via OSV.dev.

To enable:
  go install github.com/google/osv-scanner@latest
  # or: brew install osv-scanner
EOF
    return 0
  fi

  osv-scanner \
    --lockfile mix.lock \
    --format json \
  > "${AUDIT_TMPDIR}/osv-scan.json" 2>/dev/null || true
}
```

Output is JSON with `results[].packages[].vulnerabilities[]`. Each
vulnerability has `id` (OSV ID), `aliases` (CVE list), `severity` (array of
CVSS strings).

Severity mapping: parse highest CVSS score from `severity[].score`:

- ≥ 9.0 → BLOCK (critical)
- ≥ 7.0 → BLOCK (high)
- ≥ 4.0 → WARN (medium)
- < 4.0 → INFO (low)

**FP rate:** ~0%. **Why integrate both `mix_audit` and `osv-scanner`?** GHSA
and OSV.dev have non-overlapping coverage. Running both catches more
real-world CVEs.

## Aggregation into findings format

Each external-tool finding maps to the same shape as MVP-rule findings,
with `rule_id = "ext:<tool>"`:

```elixir
%{
  rule_id: "ext:hex-audit" | "ext:mix-audit" | "ext:osv-scanner",
  severity: :block | :warn | :info,
  file: nil,         # CVEs are package-level, not file-level
  line: nil,
  snippet: "<advisory-id>",
  message: "<title or description>"
}
```

Attach to the per-package finding list before scoring.

## Parallelism

All three tools run independently. Spawn in background:

```bash
hex_audit &           pid_hex=$!
mix_audit_run &       pid_mix=$!
osv_scan &            pid_osv=$!

wait $pid_hex $pid_mix $pid_osv
```

`mix hex.audit` and `mix deps.audit` may contend on the `mix` lock; if so,
serialize the two mix-based scanners and only parallelize `osv-scanner`.

## Exit-code handling

| Tool | 0 | Non-zero |
|------|---|----------|
| `mix hex.audit` | No retirements | Retirements found (informational, NOT fatal) |
| `mix deps.audit` | No CVEs | CVEs found |
| `osv-scanner` | No CVEs | CVEs found OR scan error |

Treat non-zero as "findings to parse", not "skill failure". The skill itself
returns 0 unless the *audit infrastructure* fails (missing `mix`, bad
network, corrupt cache).

## Why not Snyk / Phylum / Endor?

| Tool | Why skipped |
|------|-------------|
| Snyk CLI | Paid for org use, signal duplicates `mix_audit` for free |
| Phylum | Thin Hex support (per 2026 research) |
| Endor Labs | No reliable BEAM reachability — not credible |
| Semgrep SC | Paid tier; OSS Semgrep covered separately in Phase 2 |
| Socket.dev | No Hex support; we **reimplement** their signal model |

## Future: SARIF output (Phase 2)

`osv-scanner --format sarif` and `mix deps.audit --format sarif` (proposed)
would let us emit a single SARIF file for GitHub Code Scanning. Deferred to
Phase 2 alongside Semgrep ruleset.
