---
name: phx:deps-audit
description: Audit Hex deps for supply-chain security risk — bidi chars, compile-time exec, maintainer changes, typosquats, CVEs. Use after mix deps.update, when checking if a package upgrade is safe, or reviewing mix.lock PR diffs.
effort: medium
argument-hint: "[--base <ref> | --preview [pkg...]] [--quick] [--json] [--sarif <path>] [--ci] [--strict] [--no-differential] [--no-llm | --llm] [--trace]"
allowed-tools: Read, Grep, Glob, Bash, WebFetch
---

# Hex Dependency Audit

Non-mutating supply-chain audit for Hex packages. Runs an 8-rule MVP catalogue
against changed packages, enriches with Hex API metadata, wraps existing tools
(`mix hex.audit`, `mix_audit`, OSV-Scanner), and emits a triage table.

## When to Use

- After `mix deps.update` or `mix deps.get` brought in new versions
- On PRs that touch `mix.lock` (pre-merge gate)
- Before manually updating a single package (`--preview <pkg>`)
- When investigating a dependency you don't recognize

## Iron Laws

1. **NEVER claim a diff is clean without inspecting it.** Run all 8 rules
   on the unpacked NEW tarball. "Looks fine" without a tool run is a false
   pass. **Always write `.claude/deps-audit/last-run.json`** — its absence
   is evidence the audit didn't actually run.
2. **NEVER install `mix_audit` / `osv-scanner` — even if asked.** Detect,
   warn with install instructions, skip cleanly if missing. If the user
   says "install it," respond with the install command (e.g.,
   `mix deps.add mix_audit --only dev`) and **do not execute it**. The
   audit skill is non-mutating; `mix.exs` / `mix.lock` are off-limits
   regardless of consent.
3. **NEVER promote a finding to BLOCK without rule citation.** Every finding
   shows `rule_id`, `severity`, `file:line`, `snippet`, `message`. No
   handwaving.
4. **NEVER fetch from Hex API without rate-limiting.** Cap at 5 req/sec.
   Cache metadata 7 days, top-500 list 1 day.
5. **NEVER run the audit on already-committed lock changes silently** —
   tell the user which mode (A/B/C) is active and which `(old, new)` pairs
   resolved.
6. **LLM triage only above threshold.** Native rules + Semgrep + YARA
   are deterministic. The `hex-deps-triager` agent runs only when score
   > 10 (1 BLOCK or 3+ WARNs), and its verdicts are advisory — never
   auto-suppress a finding without human review.

## Operating Modes

| Mode | Trigger | Old source | New source |
|------|---------|-----------|-----------|
| **B** (default) | `/phx:deps-audit` | `git show HEAD:mix.lock` | working `mix.lock` |
| **C** (PR) | `/phx:deps-audit --base main` | `git show <ref>:mix.lock` | working `mix.lock` |
| **A** (preview) | `/phx:deps-audit --preview httpoison` | locked version | Hex API latest |

See `${CLAUDE_SKILL_DIR}/references/operating-modes.md` for full resolver logic.

## Execution Flow

Default = full 8-rule scan with streaming progress. `--quick` opts out
to CVE + retirement only. See `${CLAUDE_SKILL_DIR}/references/execution-flow.md`.

### Step 1: Resolve the diff

Parse the `mix.lock` Erlang term format for both old and new sources. Emit a
list of `{pkg, old_version, new_version}` tuples. Surface
new-only and removed-only packages separately (a removed package is not
audited; a brand-new package gets `old_version = nil` and skips diff-only
rules).

See `${CLAUDE_SKILL_DIR}/references/diff-resolver.md` for shell + `mix run -e` snippets per mode and the JSON output contract.

### Step 2: Fetch tarballs (per-run tmpdir)

For each `(pkg, old, new)`:

```
mix hex.package fetch <pkg> <old> --unpack -o ${AUDIT_TMPDIR}/tarballs/<pkg>/<old>/
mix hex.package fetch <pkg> <new> --unpack -o ${AUDIT_TMPDIR}/tarballs/<pkg>/<new>/
```

All ephemeral artifacts live under `${AUDIT_TMPDIR}` (driver-owned, removed
on exit). See `${CLAUDE_SKILL_DIR}/references/audit-tmpdir.md` and
`${CLAUDE_SKILL_DIR}/references/tarball-fetcher.md`.

### Step 3: Run the 8 MVP rules on each NEW tarball

| # | Rule | Sev | Method |
|---|------|-----|--------|
| 1 | Bidi Unicode control chars in `.ex`/`.exs`/`.erl` | BLOCK | grep |
| 2 | `Code.eval_*` / `:erlang.apply` with non-literal MFA at module scope | BLOCK | AST (Sourceror or regex+scope) |
| 3 | `System.cmd` / `:os.cmd` / `Port.open` at compile time | BLOCK | AST |
| 4 | `:erlang.binary_to_term/1` on literal without `:safe` | BLOCK | AST |
| 5 | New `:git`/`:path` dep in `mix.exs` (vs old) | BLOCK | AST diff |
| 6 | Maintainer change between versions | BLOCK | Hex API |
| 7 | Base64 blobs >256 chars outside `priv/static/`, `test/fixtures/`, `assets/` | WARN | regex |
| 8 | Levenshtein ≤2 from top-500 + download delta >1000× | BLOCK | Hex API + fuzzy |

Full catalogue (35 rules, MVP marked) in `${CLAUDE_SKILL_DIR}/references/heuristics.md`.
Bash + `mix run -e` implementations for all 8 MVP rules in
`${CLAUDE_SKILL_DIR}/references/rules-impl.md` (single-pass NEW + diff rules +
Hex API rules, with `run_all_rules` master loop).

### Step 4: External tool wrappers (parallel)

- `mix hex.audit` — retired-package check, always available
- `mix_audit` — CVE check via GHSA, if installed (else warn + skip; do NOT install)
- `osv-scanner` — CVE check via OSV.dev, if installed (else warn + skip; do NOT install)

See `${CLAUDE_SKILL_DIR}/references/external-tools.md` for detection, output parsing, and severity mapping per tool.

### Step 5: Hex API enrichment (per package)

- `GET /api/packages/:name` — owners, downloads, inserted_at
- `GET /api/packages/:name/releases/:version` — per-release publisher
- Compute: `days_since_publish`, `owner_age_days`, `download_velocity`

Cap at 5 req/sec. Per-run cache under `${AUDIT_TMPDIR}/hex-api/`.
See `${CLAUDE_SKILL_DIR}/references/hex-api.md` for endpoint contracts,
caching strategy, Rule 6/8 detection, and Levenshtein implementation.

### Step 5.5: Apply `hex_vet.exs` ledger (if present)

If `hex_vet.exs` exists at project root, vetted-version findings are
**downgraded to INFO**. Unvetted versions retain their severity.
Lock-vs-ledger disagreement: lock wins. See the deps-vet skill's
hex-vet schema doc for the "Lock-vs-ledger disagreement" section.

Use `/phx:deps-vet <pkg> <version>` (separate skill) to add entries.

### Step 5.7: Differential subtract

When run with `DIFFERENTIAL=1` (default), findings that existed in the
OLD tarball are downgraded to INFO. Net-new signals reach the renderer
at full severity. See `${CLAUDE_SKILL_DIR}/references/differential.md`.

### Step 5.8: LLM triage (when score > threshold)

For packages where the aggregate score exceeds 10, the
`hex-deps-triager` sonnet agent reads finding + diff windows and
produces structured verdicts (`confidence`, `verdict`, `rationale`,
`fp_reasons[]`). A `context-supervisor` (haiku) consolidates verdicts
across packages into `triage/consolidated.md`. Main skill reads only
the consolidated file.

See `${CLAUDE_SKILL_DIR}/references/llm-triage.md`.

### Step 6: Score & render

Per-package weighted sum: BLOCK = 10, WARN = 3, INFO = 1.
Risk band: 0 clean · 1–5 low · 6–15 medium · 16+ high.

Output:

1. **Stdout:** markdown table — `pkg | old → new | risk | findings | diff.hex.pm | maintainer-change` plus a per-package detail section for any non-clean row.
2. **Sidecar (MANDATORY):** Write `.claude/deps-audit/last-run.json`. The Phase 3 gate reads this; an audit that doesn't write it is a no-op for the gate. Always emit, even on clean runs.

`--json` flag emits JSON to stdout instead of markdown. See
`${CLAUDE_SKILL_DIR}/references/output-renderer.md` for table format,
sidecar schema, exit-code rubric, and `--quiet` mode.

## Out of scope / Phase 3 surface

- **NEVER modify** `mix.lock`, `mix.exs`, or any project file (non-mutating)
- **NEVER auto-install** missing tools (warn + skip)
- **Gate** `mix deps.{get,update,compile}` via `deps-audit-gate.sh`. See `references/hook.md`.
- **Prompt** for `/phx:compound` after BLOCK findings — corpus self-feeds.
- **Emit** SARIF 2.1.0 via `--sarif <path>` and gate CI via `--ci`.

## References

- `${CLAUDE_SKILL_DIR}/references/heuristics.md` — full 35-rule catalogue
- `${CLAUDE_SKILL_DIR}/references/rules-impl.md` — bash + `mix run -e` for the 8 MVP rules
- `${CLAUDE_SKILL_DIR}/references/operating-modes.md` — Mode A/B/C resolver
- `${CLAUDE_SKILL_DIR}/references/diff-resolver.md` — shell snippets, lock parser
- `${CLAUDE_SKILL_DIR}/references/tarball-fetcher.md` — fetch wrapper, parallel cap, cache prune
- `${CLAUDE_SKILL_DIR}/references/external-tools.md` — `mix_audit`, `osv-scanner` wrappers
- `${CLAUDE_SKILL_DIR}/references/hex-api.md` — endpoint contracts, rate limit, Rule 6/8
- `${CLAUDE_SKILL_DIR}/references/output-renderer.md` — markdown, JSON v1, exit codes, SARIF
- `${CLAUDE_SKILL_DIR}/references/testing.md` — smoke runner, fixture matrix
- `${CLAUDE_SKILL_DIR}/references/differential.md` / `llm-triage.md` — Phase 2 NDJSON subtract + triager
- `${CLAUDE_SKILL_DIR}/references/semgrep.md` / `yara.md` — Phase 2 precision layers (soft deps)
- `${CLAUDE_SKILL_DIR}/references/cassettes.md` / `sarif.md` / `hook.md` / `ci-integration.md` — Phase 3 surface
- `${CLAUDE_SKILL_DIR}/references/trusted-publishers.md` / `skill-checklist.md` — upstream + eval
- `${CLAUDE_SKILL_DIR}/references/audit-tmpdir.md` — Phase 5 per-run ephemeral storage contract
- `${CLAUDE_SKILL_DIR}/references/execution-flow.md` / `differential-cve.md` — Phase 5 default scan + CVE diff
