# Operating Modes — A / B / C

The audit engine is **mode-agnostic**:

```
audit(pkg, old_version, new_version) → findings[]
```

Modes only change how `(old, new)` pairs get resolved. The engine never
inspects how the diff came to be.

## Mode B — Default (working vs HEAD)

```
/phx:deps-audit
```

Compares the working-tree `mix.lock` against `git show HEAD:mix.lock`.

| | |
|---|---|
| **Old source** | `git show HEAD:mix.lock` |
| **New source** | working `mix.lock` |
| **Use case** | Post-`mix deps.update` safety net. Pre-commit gate. |
| **Cost** | Cheapest mode — no remote calls for diff resolution |
| **Why default** | Catches Igniter / auto-update footguns retroactively, before commit |

If HEAD has no `mix.lock` (initial commit, brand new dep), every locked
package is treated as a NEW package (`old_version = nil`). Diff-only rules
(Rule 5, Rule 6) are skipped for new packages; static rules (1, 2, 3, 4, 7)
still run.

## Mode C — PR / branch comparison

```
/phx:deps-audit --base main
/phx:deps-audit --base origin/main
/phx:deps-audit --base abc1234
```

Compares the working-tree `mix.lock` against `git show <ref>:mix.lock`.

| | |
|---|---|
| **Old source** | `git show <ref>:mix.lock` |
| **New source** | working `mix.lock` |
| **Use case** | CI on PRs that touch `mix.lock`. Pre-PR self-review. |
| **Cost** | Same as Mode B |
| **CI hint** | `/phx:deps-audit --base origin/main --json` for machine-readable output |

`<ref>` is any valid Git revision: branch name, tag, commit SHA, `HEAD~N`.

## Mode A — Preview (locked vs Hex latest)

```
/phx:deps-audit --preview                 # all locked deps vs latest
/phx:deps-audit --preview httpoison       # one package
/phx:deps-audit --preview httpoison req   # multiple
```

Compares the locked version against the latest version on Hex.pm.

| | |
|---|---|
| **Old source** | Version in working `mix.lock` |
| **New source** | Latest version from Hex API (`GET /api/packages/:name`) |
| **Use case** | "If I run `mix deps.update X`, what lands?" Pre-update analysis. |
| **Cost** | Adds 1 Hex API call per package (cached 1h) |
| **Limitation** | Does not resolve transitive deps. Only the named packages. |

If no packages are specified, all packages from `mix.lock` are previewed.
Cap at 50 packages to avoid Hex API spam — show a warning and stop if
exceeded.

## Resolver pseudocode

```elixir
def resolve_pairs(mode) do
  case mode do
    :working_vs_head ->
      old = parse_lock(git_show("HEAD:mix.lock"))
      new = parse_lock(File.read!("mix.lock"))
      diff_pairs(old, new)

    {:base, ref} ->
      old = parse_lock(git_show("#{ref}:mix.lock"))
      new = parse_lock(File.read!("mix.lock"))
      diff_pairs(old, new)

    {:preview, packages} ->
      locked = parse_lock(File.read!("mix.lock"))
      pkgs = if packages == [], do: Map.keys(locked), else: packages
      Enum.map(pkgs, fn pkg ->
        latest = hex_api_latest(pkg)
        {pkg, locked[pkg], latest}
      end)
  end
end

defp diff_pairs(old_map, new_map) do
  changed =
    for {pkg, new_v} <- new_map, old_v = old_map[pkg], new_v != old_v do
      {pkg, old_v, new_v}
    end

  added =
    for {pkg, new_v} <- new_map, !Map.has_key?(old_map, pkg) do
      {pkg, nil, new_v}
    end

  removed =
    for {pkg, old_v} <- old_map, !Map.has_key?(new_map, pkg) do
      {pkg, old_v, nil}
    end

  %{changed: changed, added: added, removed: removed}
end
```

(Pseudocode — actual implementation lives inline in the skill body as shell
or `mix run -e` snippets. Plugin has no `lib/` directory.)

## `mix.lock` format

Erlang term format:

```elixir
%{
  "phoenix" => {:hex, :phoenix, "1.7.14", "checksum", :mix, [...], "hexpm", "hash"},
  ...
}
```

Position 3 is the version string. Use `Code.eval_file("mix.lock")` or a
simple regex to extract; the format has been stable for years.

## Why Mode B is the default

1. **Zero new infra** — `git show` is one shell call
2. **Retroactive Igniter check** — catches auto-update footguns before commit
3. **Natural pre-commit hook integration** — Phase 3 PreToolUse hook just
   invokes Mode B on the working-tree diff
4. **Mode A needs more work** — Hex API resolver for latest versions plus
   transitive resolution. Strictly more code paths than Mode B.

## What modes deliberately do NOT do

- **No transitive resolution in Mode A** — we audit only the packages
  named or already in `mix.lock`. Use `mix deps.tree` for full transitive.
- **No fetch of removed packages** — a `removed: [...]` package is reported
  in the table as "removed", but no rule runs on it. There's no NEW to audit.
- **No automatic mode promotion** — the user picks. Default = B.

## Mode selection examples

| Situation | Command |
|-----------|---------|
| Just ran `mix deps.update`, want pre-commit check | `/phx:deps-audit` |
| Reviewing a PR that bumped `mix.lock` | `/phx:deps-audit --base origin/main` |
| Considering whether to update `httpoison` | `/phx:deps-audit --preview httpoison` |
| Curious which deps could update | `/phx:deps-audit --preview` (capped at 50) |
| Just merged main, want fresh audit on whole tree | `git fetch && /phx:deps-audit --base origin/main~1` |
