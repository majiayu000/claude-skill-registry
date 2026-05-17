# Output Renderer

Two outputs from every audit:

1. **Stdout** — markdown table + per-package detail (terminal-first)
2. **Sidecar** — `.claude/deps-audit/last-run.json` (machine-readable)

## Scoring weights & risk bands

```
BLOCK = 10 points
WARN  =  3 points
INFO  =  1 point

Per-package risk = sum of findings' points

Risk band:
   0          → clean
   1–5        → low
   6–15       → medium
   16+        → high
```

Risk emoji used in markdown for skim-readability:

| Band | Emoji | Meaning |
|------|-------|---------|
| clean | ✅ | No findings |
| low | 🟢 | INFO / minor WARN |
| medium | 🟡 | Multiple WARNs or 1 BLOCK |
| high | 🔴 | Multiple BLOCKs |

(Emoji is the *only* place this skill uses Unicode glyphs in output; the
rest of the renderer is ASCII to keep diff/grep-friendly.)

## Security-changelog headline (Phase 5)

When `diff_cves.py` emits any `patched`, `introduced`, or `still_exposed`
findings, the renderer **prepends a headline section** before the
package table. This is the actionable narrative the 2026-05-12 virgil
dogfood revealed was missing.

### Render order

```
1. (BLOCK headline)    introduced + still_exposed CVEs    ← if any
2. (INFO  headline)    patched CVEs (the security changelog)
3.                     existing markdown table
4.                     per-package detail sections
5.                     editorial framing (major bumps, etc.)
```

`patched` is `info` severity but lifts to the headline regardless —
it's the user-facing security story for the update.

### Patched (informational, lifted to top)

```markdown
# Hex Dependency Audit — Mode B (working vs HEAD)

🚨 4 of 25 updates patched real CVEs. You were exposed:

- decimal 2.3.0 → 3.1.0: CVE-2026-32686 (high) — DoS via unbounded exponent
  Disclosed 2026-05-07. 6 days exposed.
- bandit 1.10.3 → 1.11.0: CVE-2026-39805 (high) — HTTP/1.1 request smuggling
  Disclosed 2026-05-01. 12 days exposed. (+1 more CVE in this bump)
- phoenix 1.8.5 → 1.8.7: CVE-2026-32689 (high) — long-poll NDJSON DoS
  Disclosed 2026-05-05. 8 days exposed.
- postgrex 0.22.0 → 0.22.1: CVE-2026-32687 (critical) — SQL injection in Notifications.listen/3
  Disclosed 2026-05-12. 1 day exposed.

**Recommendation:** ship these updates ASAP.
```

Format spec:

- Leading `🚨 N of M` line ONLY when patched findings exist — single
  emoji per report, never per-finding.
- One bullet per (package, GHSA) pair. Bundle multi-CVE bumps with
  `(+N more CVE in this bump)` to keep the list scannable.
- `Disclosed YYYY-MM-DD. N days exposed.` from `exposure_days` field.
- Final line: "**Recommendation: ship these updates ASAP.**"

### Introduced (regression — BLOCK at top)

```markdown
🛑 BLOCKED — 1 update INTRODUCED a CVE (regression):

- examplepkg 1.0.0 → 1.0.1: CVE-2026-99999 (critical) — Compromised release introduces RCE
  Disclosed 2026-05-10. This update should NOT be merged.

This is a regression: the OLD version did not have this CVE; the NEW
version does. Investigate the release (`mix hex.package diff <pkg> <old> <new>`)
before proceeding.
```

Format spec:

- `🛑 BLOCKED — N update(s) INTRODUCED a CVE`
- Bullet per finding, ending "This update should NOT be merged."
- Followup line with the `mix hex.package diff` command stub.

### Still exposed (didn't fix it — BLOCK at top)

```markdown
🛑 BLOCKED — 1 CVE STILL EXPOSED after this update:

- decimal 2.3.0 → 2.3.1: CVE-2026-32686 (high) — DoS via unbounded exponent
  The fix is in decimal >= 3.0.0; this bump did not address the CVE.
  Disclosed 2026-05-07.

**Recommendation:** bump further (mix deps.update decimal to >= 3.0.0).
```

Format spec:

- `🛑 BLOCKED — N CVE(s) STILL EXPOSED after this update`
- Include `patched_versions` constraint from advisory ("fix is in X >= Y").
- Recommend a more-aggressive bump.

### Combining

If both `introduced` and `still_exposed` exist, render both headlines
(introduced first — it's the more urgent failure mode). `patched` only
renders if NO blockers exist for the same packages — the user has
bigger problems than the security changelog when something is blocked.

## Markdown table — top section

```markdown
# Hex Dependency Audit — Mode B (working vs HEAD)

Audited 4 changed · 1 added · 0 removed packages.
Tools run: mix hex.audit ✓ · mix_audit ✓ · osv-scanner ✗ (not installed)

| Package | Change | Risk | Findings | diff.hex.pm |
|---------|--------|------|----------|-------------|
| phoenix | 1.7.14 → 1.7.20 | ✅ clean | — | [view](https://diff.hex.pm/diff/phoenix/1.7.14..1.7.20) |
| ecto    | 3.13.2 → 3.13.4 | 🟢 low (3) | 1× WARN: base64 in priv/img | [view](https://diff.hex.pm/diff/ecto/3.13.2..3.13.4) |
| req     | 0.5.0 → 0.5.1 | 🔴 high (23) | 2× BLOCK · 1× WARN — maintainer changed | [view](https://diff.hex.pm/diff/req/0.5.0..0.5.1) |
| **new_logger** (added) | — → 0.1.0 | 🔴 high (10) | 1× BLOCK: typosquat of `logger` (50× DLs) | [view](https://hex.pm/packages/new_logger) |
```

When the security-changelog headline above already covered a package,
the table still includes it (consistent grain) — but the per-package
detail section refers back to the headline rather than repeating CVE
text.

## Markdown — per-package detail (only for non-clean)

For every row with score > 0, emit a detail section in order:

```markdown
## req — 🔴 high (score 23)

Maintainer changed: alice_dev → bob_unknown (between 0.5.0 and 0.5.1)

### Findings

- **BLOCK · rule 6 · maintainer change**
  `release publisher`: bob_unknown (was alice_dev)
  GHSA: n/a · CVE: n/a

- **BLOCK · rule 3 · System.cmd at compile time**
  `lib/req/setup.ex:14`
      System.cmd("curl", ["-fsSL", url])
  Triggered inside `__before_compile__/1`.

- **WARN · rule 7 · base64 blob >256 chars**
  `lib/req/templates.ex:42`
      "TG9yZW0gaXBzdW0gZG9sb3Igc2l0IGFtZXQs..." (412 chars)
```

Layout rules:

- Header includes risk emoji, band name, and score in parens
- One blank line between findings
- Code blocks for snippets are indented 4 spaces, never fenced
  (so they render cleanly even when output is piped through grep)
- File:line shown as plain `path:line` for terminal hyperlinking
- diff.hex.pm link **only** appears in the top table, not per-finding

## Markdown footer

```markdown
---

**Aggregate risk:** 🔴 high (1 package over threshold)

Re-run after fix: `/phx:deps-audit`
Inspect one package: `/phx:deps-audit --preview req`
Compare against main: `/phx:deps-audit --base origin/main`

Detailed findings: `.claude/deps-audit/last-run.json`
```

## `--json` flag

Replaces the markdown stdout with the same data the sidecar would receive.
Useful for CI consumers. Schema:

```json
{
  "version": 1,
  "generated_at": "2026-05-12T10:32:18Z",
  "mode": "B",
  "base": "HEAD",
  "tools": {
    "hex_audit": {"available": true, "ran": true},
    "mix_audit": {"available": true, "ran": true},
    "osv_scanner": {"available": false, "ran": false}
  },
  "summary": {
    "changed": 4, "added": 1, "removed": 0,
    "packages_with_findings": 2,
    "highest_risk_band": "high",
    "blocks_total": 3, "warns_total": 2, "infos_total": 0
  },
  "packages": [
    {
      "pkg": "req",
      "old_version": "0.5.0",
      "new_version": "0.5.1",
      "diff_url": "https://diff.hex.pm/diff/req/0.5.0..0.5.1",
      "risk_score": 23,
      "risk_band": "high",
      "maintainer_change": {"from": "alice_dev", "to": "bob_unknown"},
      "findings": [
        {
          "rule_id": 6,
          "severity": "block",
          "file": null, "line": null,
          "snippet": "alice_dev → bob_unknown",
          "message": "Maintainer changed between 0.5.0 and 0.5.1"
        },
        {
          "rule_id": 3,
          "severity": "block",
          "file": "lib/req/setup.ex", "line": 14,
          "snippet": "System.cmd(\"curl\", [\"-fsSL\", url])",
          "message": "System.cmd at compile time (inside __before_compile__/1)"
        }
      ],
      "external_findings": []
    }
  ]
}
```

Schema versioned with `"version": 1` so Phase 3 hook can detect
incompatible upgrades without parsing.

## Sidecar file

Always written to `.claude/deps-audit/last-run.json` regardless of `--json`
flag. Phase 3 PreToolUse hook reads this file to detect "recently audited"
state — if `generated_at` is within the last 10 minutes AND the working
`mix.lock` has the same SHA-256, allow `mix deps.get`/`update` without
re-audit prompt.

## Quiet mode

`--quiet` suppresses clean rows from the markdown table. Useful for
CI/pre-commit hooks that should only chime on findings.

## Exit code rubric

| Outcome | Exit code |
|---------|-----------|
| All packages clean | 0 |
| Some WARNs, no BLOCKs | 0 |
| Any BLOCK finding | 2 |
| Audit infrastructure failed (missing tools, bad network) | 3 |

Exit `2` is the conventional CC plugin convention for "findings present,
human review needed." Exit `3` separates "you can't trust this audit" from
"this audit caught something."

## Implementation entry point

The renderer reads `${AUDIT_TMPDIR}/findings.json` (a flat array
written by each rule + tool wrapper) and the original `diff.json` from the
resolver, then emits both outputs.

```bash
render() {
  local fmt="${1:-markdown}"
  local findings="${AUDIT_TMPDIR}/findings.json"
  local diff="${AUDIT_TMPDIR}/diff.json"

  case "${fmt}" in
    markdown) render_markdown "${diff}" "${findings}" ;;
    json)     render_json     "${diff}" "${findings}" ;;
  esac

  write_sidecar "${diff}" "${findings}" > .claude/deps-audit/last-run.json
}
```

`render_markdown` and `render_json` are jq programs (kept inline in
the skill body — see [implementation skeleton in heuristics.md](heuristics.md)
for the per-rule shape contract findings must obey).

## Anti-pattern: emoji-only signals

Some renderers use emoji as the *only* severity marker. Don't. Always
include the band name in text (`high`, `medium`, etc.) so the output is
greppable and accessible to terminals without emoji rendering.
