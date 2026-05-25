---
name: phx:deps-vet
description: "Record a vetted Hex package version in hex_vet.exs after a security review — manages the audit ledger, not the scanner. Use to approve a dep after /phx:deps-audit findings or to initialize hex_vet.exs."
argument-hint: "<pkg> <version> | --seed | --list | --check"
effort: medium
---

# Deps Vet — Hex package audit ledger

Review a Hex package version, run Phase 1 supply-chain rules against it,
prompt the user for a verdict, append the result to `hex_vet.exs`
(project-root audit ledger). Vetted versions get downgraded to `INFO`
on subsequent `/phx:deps-audit` runs.

Run this AFTER `/phx:deps-audit` to clear findings.
Run this BEFORE merging a `mix.lock` PR to certify new versions.

## Usage

```text
/phx:deps-vet phoenix 1.7.21      # vet a single package version
/phx:deps-vet --seed              # import curated baseline seed (~30 pkgs)
/phx:deps-vet --list              # show existing ledger entries
/phx:deps-vet --check             # cross-check mix.lock vs ledger
```

## Iron Laws

1. **NEVER auto-approve.** Every entry MUST come from an `AskUserQuestion`
   confirmation. Drive-by trust ruins the ledger's value.
2. **Lock wins on disagreement.** If `mix.lock` has version X and the
   ledger vets X-1, emit INFO and treat X as unvetted. Don't silently
   trust the older entry.
3. **Ledger lives at project root.** `hex_vet.exs` is a first-class
   security artifact, visible in PR review. Don't move it into `.claude/`.
4. **Round-trip via `inspect/2`.** When appending, read the file with
   `Code.eval_file/1`, mutate the map, and write back via
   `inspect(term, pretty: true, limit: :infinity)`. Hand-rolled string
   appends drift over time.
5. **Always show findings before prompting.** The user must see what's
   being vetted. No silent `:safe_to_deploy` defaults.
6. **Confirmation counts are COMPUTED, never estimated.** Any number in
   an `AskUserQuestion` (criteria split, new/overwrite/no-op) MUST be
   derived from the loaded data *before* prompting — e.g.
   `Enum.frequencies_by(seed.audits, & &1.criteria)`. Eyeballing the
   file and approving on wrong numbers corrupts the consent.

## Execution flow

### Step 1: Locate or seed `hex_vet.exs`

```text
If hex_vet.exs exists at project root:
    Read it via Code.eval_file/1
Else:
    Write the empty-ledger stub (see references/hex-vet.md §"Empty ledger")
    Inform user: "Created hex_vet.exs at project root."
```

### Step 2: Branch by mode

- **`<pkg> <version>`** → single-vet path (Step 3-7).
- **`--seed`** → import `priv/hex_vet_seed.exs`. Before prompting,
  `Code.eval_file/1` the seed and **compute** (Iron Law #6): the
  `criteria` split (`Enum.frequencies_by(seed.audits, & &1.criteria)`)
  and, against any existing ledger, exact new / overwrite / no-op
  counts. Put those computed numbers in the `AskUserQuestion`. Also
  state up front that the seed is a **provenance baseline, not
  certification of your current `mix.lock`** (per Iron Law #2, seed
  versions older than the locked ones stay unvetted). Ask before
  overwriting existing entries.
- **`--list`** → render the audits table; exit.
- **`--check`** → compare ledger entries with `mix.lock`; warn on
  drift. Read the lock via `Code.eval_file("mix.lock")` with
  **`2>/dev/null`** — modern locks have quoted keys and emit a
  `found quoted keyword` warning per package (tens of KB of noise that
  gets persisted as an oversized tool result otherwise).

### Step 3: Fetch the tarball (single-vet)

Run the deps-audit corpus loader. Cache lives at
`~/.cache/phx-deps-audit/corpus/<pkg>/<version>/contents/`. Use:

```text
bash plugins/elixir-phoenix/skills/deps-audit/smoke-test/corpus.d/fetch.sh \
    <pkg> <version>
```

### Step 4: Run Phase 1 rules

Source the rules from `../deps-audit/references/rules-impl.md`.
Run `run_all_rules` over the cached dir. Write findings to a temp
`vet-findings.jsonl`. Set `FINDINGS_FILE` to override default path.

### Step 5: Present findings

Print the findings table per `../deps-audit/references/output-renderer.md`.
On zero findings: say "No findings — vet from a clean baseline."
On any finding: show severity, file, line, snippet inline.

### Step 6: Prompt for verdict

Call `AskUserQuestion` with these 4 options:

- **`:safe_to_deploy`** — full trust; findings investigated and cleared.
- **`:safe_to_run`** — trust in non-production envs only (test deps).
- **`:does_not_implement_crypto`** — Mozilla-style sub-criterion.
- **`Skip`** — defer decision; don't write an entry.

If any finding is BLOCK severity: default-highlight `Skip`. Require
explicit override before writing `:safe_to_deploy` over a BLOCK.

### Step 7: Append to ledger

Read existing `hex_vet.exs` via `Code.eval_file/1`. Append the audit
map below to `:audits`. Write back via
`Code.format_string!(inspect(...))`.

```elixir
%{
  package: "<pkg>",
  version: "<version>",
  criteria: <verdict_atom>,
  reviewer: "<git config user.email>",
  notes: "<user-provided one-liner OR findings summary>",
  reviewed_at: ~D[<today>]
}
```

Write back via `Code.format_string!(inspect(term, pretty: true))`.
Confirm to user: "Added `<pkg>` `<version>` to hex_vet.exs."

## Integration

- **Run after** `/phx:deps-audit` to clear vetted findings.
- **Run before** merging a `mix.lock` PR to certify new versions.
- **Run `/phx:deps-vet --check`** to detect ledger drift vs `mix.lock`.
- **`/phx:deps-audit`** auto-downgrades vetted findings to INFO.

## References

- `${CLAUDE_SKILL_DIR}/references/hex-vet.md` — schema, parser, lookup
- `${CLAUDE_SKILL_DIR}/references/seed.md` — `--seed` flag, curated baseline
- `${CLAUDE_SKILL_DIR}/../deps-audit/references/rules-impl.md` — the
  same rules `/phx:deps-audit` runs

## Out of scope (Phase 3+)

- **Mix task surface** — defer `mix phx.deps_vet` to a separate Hex
  package `phx_deps_vet` for non-CC users.
- **Block-on-unvetted enforcement** — defer to a PreToolUse hook
  that gates `mix deps.get`.
- **Distributed imports** — defer cargo-vet `imports:` until
  trust-chain semantics are designed.
