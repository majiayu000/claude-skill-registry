# `hex_vet.exs` — schema, parser, and lookup

The audit ledger. Lives at **project root**, alongside `mix.exs` and
`mix.lock`. Modeled on cargo-vet's `audits.toml` — same trust-chain
intent, idiomatic Elixir surface.

## Why project root, not `.claude/`

`hex_vet.exs` is a **deliverable security artifact**, not an ephemeral
sidecar. Three properties of root placement that `.claude/` doesn't
give us:

1. **Visible in PR review.** Adding a vetted dep shows up as a diff
   line on the same file as `mix.lock`, prompting the reviewer to
   look at both.
2. **CI-discoverable without configuration.** The triple
   `mix.lock` / `mix.exs` / `hex_vet.exs` is recognizable —
   security tooling can find the ledger without project-specific
   config.
3. **Survives `.claude/` deletion.** Some teams treat `.claude/` as
   per-developer state and gitignore it. The audit ledger has to be
   shared.

Phase 1's `last-run.json` stays under `.claude/deps-audit/`
intentionally — that file is ephemeral run state, not durable trust.

## Schema

```elixir
# hex_vet.exs
%{
  imports: %{
    # Phase 3+ feature — distributed audit imports. Ignored in Phase 2.
    # mozilla: "https://hg.mozilla.org/.../audits.toml"
  },
  audits: [
    %{
      package: "phoenix",
      version: "1.7.21",
      criteria: :safe_to_deploy,
      reviewer: "oliver@ideax.sk",
      notes: "Reviewed against rules 1-8; diff.hex.pm checked clean.",
      reviewed_at: ~D[2026-05-12]
    },
    %{
      package: "jason",
      version: "1.4.4",
      criteria: :safe_to_deploy,
      reviewer: "team@example.com",
      notes: "No findings; widely-used (>50M downloads).",
      reviewed_at: ~D[2026-05-10]
    }
  ],
  policy: %{
    criteria_required: :safe_to_deploy,
    block_on_unvetted: :new_only  # Phase 3 default; see Tri-mode section
  }
}
```

### Tri-mode `block_on_unvetted` (Phase 3)

Phase 2 shipped a boolean. Real-world deployment exposed two
failure modes: `false` is too loose for teams serious about
supply-chain hygiene; `true` (strict) breaks every existing repo
before its ledger is seeded. Phase 3 replaces the boolean with an
atom that fits the actual workflow shape.

| Mode | Hook behavior | When to pick |
|------|---------------|--------------|
| `false` | Warn-only; `mix deps.get` exits 0 | Phase 2 compat; opt-out |
| `:new_only` | Block if PR ADDS an unvetted version; allow re-locks of already-locked unvetted pkgs | **Recommended default** for new projects |
| `:strict` | Block ANY `mix deps.get` while any locked version is unvetted | Mature ledger; enforce on whole graph |
| `:full` | Run Tier 2 audit pipeline (Semgrep + YARA + LLM) then apply `:strict` rules | High-stakes (financial, healthcare); accept 30-90s per `mix deps.get` |

**Why `:new_only` is the default:** strict mode fails CI on
existing repos before seed import; warn is too loose for teams
serious about supply-chain. `:new_only` blocks the specific risk
(introducing an unvetted dep) without holding the team hostage on
historical un-audited locks.

### Migration from Phase 2 boolean

The hook reads `policy.block_on_unvetted` and normalizes:

```elixir
defp normalize_block_mode(false), do: false
defp normalize_block_mode(true) do
  IO.warn("""
  block_on_unvetted: true is deprecated and will be removed in v4.0.
  Replaced with :strict (same semantics). For new projects, consider
  :new_only — blocks only NEW unvetted versions, allows re-locks.
  """)
  :strict
end
defp normalize_block_mode(mode) when mode in [:new_only, :strict, :full], do: mode
defp normalize_block_mode(other) do
  raise "Invalid block_on_unvetted: #{inspect(other)} — must be one of: false, :new_only, :strict, :full"
end
```

The one-time `IO.warn` surfaces in `mix deps.get` output. Migrate
to `:strict` (drop-in) or `:new_only` (recommended) to silence.

### `:new_only` semantics

"New" means: the package+version pair in the **current** `mix.lock`
was NOT in `mix.lock` at the hook's reference commit (default:
`origin/main`, override via `PHX_DEPS_AUDIT_BASE`). The reference
diff isolates additions:

```bash
git show "${PHX_DEPS_AUDIT_BASE:-origin/main}":mix.lock 2>/dev/null \
  > /tmp/mix.lock.base
diff <(awk '/^  "[^"]+":/' /tmp/mix.lock.base) \
     <(awk '/^  "[^"]+":/' mix.lock) \
  | grep '^>' | sed 's/^> *//'
```

Each added line is one `<pkg>: <version>` pair; block if any added
pair is missing from `audits`. Re-locks of already-locked unvetted
pkgs are ignored — those are pre-existing tech debt, not new risk.

### Criteria atoms

Following cargo-vet's vocabulary, three Phase 2 criteria are
recognized:

| Atom | Meaning |
|------|---------|
| `:safe_to_deploy` | Reviewed; safe in production. Highest trust. |
| `:safe_to_run` | Safe in non-production envs (test/dev deps). |
| `:does_not_implement_crypto` | Sub-criterion; package contains no cryptographic implementation, so transitive crypto-review obligations don't apply. |

Other atoms are valid but unrecognized — Phase 2 treats them as a
softer match (logged, never trusted).

### Empty ledger stub

Used when `hex_vet.exs` doesn't exist. New ledgers default to
`:new_only` (Phase 3) — opt-in to enforcement on the additions
without blocking historical un-audited locks:

```elixir
%{
  imports: %{},
  audits: [],
  policy: %{criteria_required: :safe_to_deploy, block_on_unvetted: :new_only}
}
```

## Parser

Use `Code.eval_file/1` — Elixir's own parser, no Sourceror needed:

```bash
# One-line read:
mix run --no-mix-exs -e '
  {ledger, _} = Code.eval_file("hex_vet.exs")
  IO.inspect(ledger.audits, limit: :infinity)
'
```

Inside a skill script the same call works via `mix run -e`. For lookup
performance, the ledger is small (target: <2,000 entries; 50K LOC
file). No streaming parser needed.

### Lookup function

```elixir
def vetted?(ledger, pkg, version, required \\ :safe_to_deploy) do
  Enum.any?(ledger.audits, fn audit ->
    audit.package == pkg and
      audit.version == version and
      meets_criteria?(audit.criteria, required)
  end)
end

defp meets_criteria?(:safe_to_deploy, _required), do: true
defp meets_criteria?(:safe_to_run, :safe_to_run), do: true
defp meets_criteria?(other, other), do: true
defp meets_criteria?(_, _), do: false
```

`:safe_to_deploy` satisfies every requirement (deploy implies run).
`:safe_to_run` only satisfies `:safe_to_run`.

## Lock-vs-ledger disagreement (Day-1 decision: lock wins)

When `mix.lock` says `phoenix 1.7.21` and the ledger has an entry for
`phoenix 1.7.20`:

- The unmatched lock version (1.7.21) is **unvetted**.
- The orphaned ledger entry (1.7.20) is **informational** — emit an
  INFO finding "ledger entry exists for older version 1.7.20; treating
  1.7.21 as unvetted."
- The audit runs the full Phase 1 rule pass on 1.7.21 with normal
  severities.

This is the conservative call. The alternative ("lock-version-or-higher
trust") would let attackers exploit version-bump attacks where the
ledger entry was approved on a safe version.

## Append flow

Round-trip through `inspect/2` to preserve Elixir term semantics:

```bash
mix run --no-mix-exs -e '
  {ledger, _} = Code.eval_file("hex_vet.exs")
  new_audit = %{
    package: "<pkg>",
    version: "<ver>",
    criteria: :safe_to_deploy,
    reviewer: System.cmd("git", ["config", "user.email"]) |> elem(0) |> String.trim(),
    notes: "<notes>",
    reviewed_at: Date.utc_today()
  }
  updated = Map.update!(ledger, :audits, &[new_audit | &1])
  formatted = updated
              |> inspect(pretty: true, limit: :infinity, width: 80)
              |> Code.format_string!()
              |> IO.iodata_to_binary()
  File.write!("hex_vet.exs", formatted <> "\n")
'
```

`Code.format_string!/1` ensures the output matches the project's
formatter config (incl. `.formatter.exs` overrides). Test the
round-trip on a fixture before relying on it — version pinning matters.

## Migration from existing trust artifacts

For projects using ad-hoc trust mechanisms (a comment in `mix.exs`,
README sections, internal wiki pages), the seed-import flow
(`/phx:deps-vet --seed`) lets a team bootstrap a real ledger from
the top-100 list and then layer in project-specific audits.

The seed is regenerated monthly; entries older than 90 days emit a
stale-warning. See `seed.md` for the regeneration job.

## Distributed imports (Phase 3 — single-source v1)

cargo-vet supports trusting other organizations' audit ledgers via
the `imports:` table. Phase 3 ships **explicit allow-list v1**: any
import URL listed in `imports` must be opted into per-project — no
implicit trust, no transitive imports.

### Schema

```elixir
imports: %{
  # key = canonical handle, value = ledger URL
  "elixir-phoenix-plugin" =>
    "https://raw.githubusercontent.com/oliver-kriska/claude-elixir-phoenix/main/plugins/elixir-phoenix/skills/deps-vet/priv/hex_vet_seed.exs"
}
```

The handle (left side) is the attribution the renderer uses when a
finding is downgraded via an imported audit: "vetted via
`elixir-phoenix-plugin` (imported)". The URL (right side) must
resolve to a file with the same `hex_vet.exs` map shape (`audits:` is
the only key consumed; `imports:` of the imported ledger is ignored
to prevent transitive trust chains).

### v1 allow-list

Phase 3 v1 hardcodes the recognized import set:

```elixir
@allowed_imports %{
  "elixir-phoenix-plugin" =>
    "https://raw.githubusercontent.com/oliver-kriska/claude-elixir-phoenix/main/plugins/elixir-phoenix/skills/deps-vet/priv/hex_vet_seed.exs"
}
```

Imports listed in `hex_vet.exs` that aren't in `@allowed_imports` are
**ignored with stderr warning**, never silently trusted. Multi-org
imports (Phoenix team, EEF, etc.) stay drafted until the trust-chain
semantics are battle-tested through one full cycle of single-import
production use.

### Fetch + cache

Imports fetch on first use and cache 24h under
`.claude/deps-audit/cache/imports/<handle>.exs`. On cache miss or
TTL expiry, re-fetch via `curl -fsSL`. Fetch failures fall back to
the cached copy with a "stale import" stderr warning.

### Lookup precedence

```text
project audits         (hex_vet.exs `audits:`)
        ↓ not found
imported audits        (each allowed import, parallel)
        ↓ not found
unvetted               (Phase 1 rules apply at full severity)
```

A local audit always wins over an import — explicit project trust
is more durable than implicit shared trust. Conflicts (local
`:safe_to_run` vs import `:safe_to_deploy`) resolve to local.

### Attribution in output

The renderer surfaces import provenance:

```text
phoenix 1.7.21 — vetted via elixir-phoenix-plugin (imported), :safe_to_deploy
plug    1.16.1 — vetted locally (oliver@ideax.sk, 2026-05-12), :safe_to_deploy
unknown 0.1.0  — unvetted (no local or imported audit)
```

Reviewers see exactly where the trust came from. Out-of-policy
imports (anything not in the allow-list) get a one-time stderr
warning `ignored import: <handle> — not in v1 allow-list` but
never silently downgrade severity.

### Publishing your org's audit ledger

The plugin's seed file is the reference shape. Mirror the pattern:

1. Maintain an `hex_vet.exs` (or any `.exs` returning the same map)
   in a repository your team controls.
2. Open a PR to add your URL to the plugin's `@allowed_imports`.
3. Add a `README` covering: review process, criteria meaning for
   your org, signing/checksums.
4. Cross-reference: your `hex_vet.exs` lists `imports:` of
   `elixir-phoenix-plugin` for symmetry.

Allow-list reviews enforce trust-chain hygiene: a malicious import
URL would compromise every plugin user. The plugin maintainers are
the final gate.
