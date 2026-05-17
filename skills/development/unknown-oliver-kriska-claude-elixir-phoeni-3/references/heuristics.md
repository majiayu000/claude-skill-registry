# Hex Supply-Chain Heuristics — Full Catalogue

Full 35-rule catalogue. **Rules marked ✅ MVP are implemented in Phase 1.**
Remaining rules are deferred to Phase 2.

Severity scale:

- **BLOCK** — high-confidence malicious indicator. Refuse to "pass" the audit.
- **WARN** — suspicious but plausibly legitimate. Surface for human review.
- **INFO** — context only, never alone.

Scoring weights: BLOCK = 10 · WARN = 3 · INFO = 1.

## Category 1 — Compile-Time Code Execution (7 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 1.1 | Top-level expressions outside `def`/`defp`/`defmacro` body | WARN | AST module-body walk | ~5% | — |
| 1.2 | `Code.eval_string` / `Code.eval_quoted` with non-literal arg | BLOCK | AST | ~1% | ✅ Rule 2 |
| 1.3 | `:erlang.apply(Mod, Fun, Args)` with non-literal MFA at module scope | BLOCK | AST | ~1% | ✅ Rule 2 |
| 1.4 | `System.cmd` / `:os.cmd` / `Port.open` at compile time | BLOCK | AST scope check | ~3% | ✅ Rule 3 |
| 1.5 | `@on_load` / `@on_definition` callbacks | WARN | Attribute scan | ~10% | — |
| 1.6 | Mix alias wrapping `deps.get` / `deps.update` | WARN | Parse `mix.exs` aliases | ~5% | — |
| 1.7 | Excessive macro density (>20% of file is `defmacro`) | INFO | AST node counting | ~15% | — |

## Category 2 — Network Egress During Compile (5 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 2.1 | `:httpc.request` / `HTTPoison.*` / `Req.*` / `Tesla.*` at module load | BLOCK | AST scope check | ~2% | — (covered partially by 1.4 if shelling out) |
| 2.2 | `:gen_tcp.connect` / `:ssl.connect` outside function bodies | BLOCK | AST | ~1% | — |
| 2.3 | NIF socket calls (`:inet.*`) at compile time | BLOCK | AST | ~1% | — |
| 2.4 | Webhook-style URLs (Discord/Slack/IPFS) in source | WARN | Regex on `.ex`/`.exs` | ~10% | — |
| 2.5 | DNS exfil patterns (long subdomains, base64 in host) | WARN | Regex | ~12% | — |

## Category 3 — Obfuscation / Hidden Payloads (6 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 3.1 | Base64 string literals >256 chars outside `priv/static/`, `test/fixtures/`, `assets/` | WARN | Regex with directory exclude | ~8% | ✅ Rule 7 |
| 3.2 | Hex binaries >128 bytes (`<<0x..., ...>>` literal) | WARN | AST literal scan | ~6% | — |
| 3.3 | `:erlang.binary_to_term/1` on literal without `:safe` opt | BLOCK | AST | ~2% | ✅ Rule 4 |
| 3.4 | Unicode homoglyph identifiers (Cyrillic/Greek lookalikes in `def` names) | WARN | Char-class regex | ~3% | — |
| 3.5 | Bidi control characters in source (CVE-2021-42574 Trojan Source) | BLOCK | Grep `[‪-‮⁦-⁩؜‎‏]` | ~0% | ✅ Rule 1 |
| 3.6 | String concat to hide reserved words (`"Sy" <> "stem" <> ".cmd"`) | WARN | AST concat-of-string-literals scan | ~5% | — |

## Category 4 — NIF / Port Driver Red Flags (4 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 4.1 | Native source presence (`c_src/`, `native/`, `.c`, `.rs`, `.zig`) | INFO | `find` | ~30% | — |
| 4.2 | Build scripts invoking `curl` / `wget` / `sh -c` | BLOCK | Grep in `Makefile`, `*.sh`, `build.rs` | ~3% | — |
| 4.3 | Precompiled binaries in `priv/` (any non-text file > 10KB) | WARN | `file -i` MIME check | ~15% | — |
| 4.4 | `rustler` / `zigler` / `:erlang.load_nif` newly added | WARN | AST diff old vs new `mix.exs` | ~10% | — |

## Category 5 — Typosquatting & Impersonation (5 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 5.1 | Levenshtein ≤ 2 from top-500 Hex packages + download delta >1000× | BLOCK | Hex API + fuzzy distance | ~1% | ✅ Rule 8 |
| 5.2 | Homoglyph package names (`phoeniх` with Cyrillic х) | BLOCK | Unicode confusable check | ~0.5% | — |
| 5.3 | Identical package description but different author | WARN | Hex API description diff | ~5% | — |
| 5.4 | New author + sudden traction (>1k DLs in week 1) | WARN | Hex API + insertedat math | ~8% | — |
| 5.5 | Cross-ecosystem name reuse (npm/PyPI package with same name + different author) | INFO | npm/PyPI registry lookup | ~20% | — |

## Category 6 — Maintainer / Publishing Signals (5 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 6.1 | Maintainer change between versions | BLOCK | Hex API `owners` diff | ~2% | ✅ Rule 6 |
| 6.2 | Single-maintainer package with >500 transitive dependents | INFO | Hex API + reverse deps | ~0% | — |
| 6.3 | Anomalous version bump (major skip, non-semver) | WARN | Version string parsing | ~5% | — |
| 6.4 | `days_since_publish < 7` ("let it cook" rule) | WARN | Hex API `inserted_at` | ~30% | — |
| 6.5 | Yank-then-republish at same version | BLOCK | Hex API `retirements` history | ~0.5% | — |

## Category 7 — Diff-Based Checks (6 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 7.1 | New top-level expressions vs old version | WARN | AST diff of module bodies | ~7% | — |
| 7.2 | New `System.cmd` / network calls vs old | BLOCK | AST diff | ~4% | — |
| 7.3 | New files in `priv/` (esp. binary) | WARN | `diff` of file lists | ~10% | — |
| 7.4 | New `:git` / `:path` dep in `mix.exs` | BLOCK | AST diff of `deps/0` | ~5% | ✅ Rule 5 |
| 7.5 | License change between versions | WARN | Read `LICENSE` / `mix.exs` `:licenses` | ~5% | — |
| 7.6 | `.hex` / `metadata.config` tampering (checksum mismatch) | BLOCK | `mix hex.audit` already covers retirement; this extends | ~1% | — |

## Category 8 — Mix-Specific (4 rules)

| # | Rule | Sev | Method | FP | MVP |
|---|------|-----|--------|----|-----|
| 8.1 | `:git` / `:path` dep in `mix.exs` (any, not just new) | INFO | Parse `mix.exs` | ~40% (legit local dev) | — |
| 8.2 | Custom compilers (`:compilers` modified) | WARN | Parse `project/0` | ~10% | — |
| 8.3 | Aliases wrapping `deps.get` / `deps.update` | WARN | Parse aliases | ~5% | — |
| 8.4 | `override: true` on transitive deps | INFO | Parse `deps/0` | ~20% | — |

## MVP Summary — 8 Rules

The 8 MVP rules (Phase 1) target the highest-confidence indicators with
aggregate FP <5%:

| MVP # | From | Rule |
|-------|------|------|
| 1 | 3.5 | Bidi Unicode control chars |
| 2 | 1.2 + 1.3 | `Code.eval_*` / `:erlang.apply` non-literal at module scope |
| 3 | 1.4 | `System.cmd` / `:os.cmd` / `Port.open` at compile time |
| 4 | 3.3 | `:erlang.binary_to_term/1` literal without `:safe` |
| 5 | 7.4 | New `:git`/`:path` dep vs old `mix.exs` |
| 6 | 6.1 | Maintainer change between versions |
| 7 | 3.1 | Base64 >256 chars outside allowlisted dirs |
| 8 | 5.1 | Typosquat: Levenshtein ≤ 2 + download delta >1000× |

Covers Trojan Source, compile-time RCE, BEAM deser, dep confusion,
account takeover, and typosquatting. Each finding shape:

```elixir
%{
  rule_id: 1..8,
  severity: :block | :warn | :info,
  file: "lib/foo.ex" | nil,
  line: integer | nil,
  snippet: "...",
  message: "..."
}
```

## Prior Art

- **Trojan Source / CVE-2021-42574** — bidi control chars in source. Rule 1.
- **diff-CodeQL (Froh et al., SCORED '23)** — 41 CodeQL queries on npm diffs,
  1.4% FP. Rules 7.1–7.4 port the diff-of-findings pattern.
- **Socket.dev signal model** — multi-signal scoring. Our weighted sum is a
  simplified version.
- **`cargo-vet` audit ledger** — Phase 2 `hex_vet.exs` ledger derives from it.
- **`npq` pre-flight pattern** — score before download. Mode A (`--preview`)
  replicates this.
- **CVE-2026-21619** — `hex_core` unsafe `binary_to_term` (RCE). Motivates
  Rule 4.

## Tuning Notes

- Rule 7 (base64) dominates noise. If FP rate exceeds 10% in real use,
  raise threshold to 512 chars or add more exclude directories.
- Rule 8 (typosquat) requires daily refresh of top-500 list. Cache in
  `${AUDIT_TMPDIR}/hex-api/top-500.json` with 24h TTL.
- Rule 6 (maintainer change) needs cross-referencing release timestamps
  with owner-list timestamps. Hex API `inserted_at` per release helps.

## Out of Scope (Phase 2)

- Differential rules 7.1–7.6 (full old vs new diff per file) — currently
  only 7.4 (`mix.exs` deps) is in MVP because it's the cheapest diff.
- All NIF rules (Category 4) — requires `file -i` MIME detection, deferred.
- Semgrep ruleset (Category 1–2 expanded) — adds binary dependency.
- YARA byte-pattern scan — adds binary dependency.
- LLM triage on high-score findings — Phase 2 once FP rate proven.
