# Tarball Fetcher — `mix hex.package fetch` (ephemeral, per-run)

Fetches and unpacks Hex tarballs for both old and new versions of each
changed package. All artifacts live in `${AUDIT_TMPDIR}/tarballs/` and
are removed by the driver's EXIT trap (see `audit-tmpdir.md`).

## Tmpdir layout

```
${AUDIT_TMPDIR}/
├── lock.old              # diff-resolver: HEAD/base mix.lock
├── lock.new              # diff-resolver: working mix.lock
├── diff.json             # diff-resolver: {changed, added, removed}
├── hex-api/
│   ├── packages/<pkg>.json
│   └── top-500.json
├── tarballs/
│   ├── phoenix/
│   │   ├── 1.7.14/        # unpacked tarball — old
│   │   └── 1.7.20/        # unpacked tarball — new
│   └── <pkg>/<version>/
├── mix-audit.json
└── cves_{old,new}.json
```

`.claude/deps-audit/last-run.json` is the only **persistent** output —
written at the end of rendering, just before the tmpdir is torn down.

## Single-version fetch

```bash
fetch_version() {
  local pkg="$1" version="$2"
  : "${AUDIT_TMPDIR:?AUDIT_TMPDIR not set}"
  local dest="${AUDIT_TMPDIR}/tarballs/${pkg}/${version}"

  # Skip if already fetched this run (e.g., transitive dep listed twice
  # in the diff). The audit is ephemeral, so this is the only kind of
  # cache hit that exists.
  if [ -f "${dest}/hex_metadata.config" ]; then
    return 0
  fi

  mkdir -p "$(dirname "${dest}")"
  mix hex.package fetch "${pkg}" "${version}" --unpack -o "${dest}" 2>&1 \
    | grep -v "Fetching\|Unpacked\|^$" || true

  if [ ! -f "${dest}/hex_metadata.config" ]; then
    echo "ERROR: fetch failed for ${pkg} ${version}" >&2
    return 2
  fi
}
```

`mix hex.package fetch` exit code is 0 on success and 1 on network/checksum
failure. Always verify `hex_metadata.config` exists before reporting success
— `mix` is occasionally non-zero on success and zero on transient failure.

## Bulk fetch from `diff.json`

Reads the resolver's output and fetches every `(pkg, old?, new?)` pair:

```bash
fetch_from_diff() {
  jq -c '
    (.changed[] | [.[0], .[1], .[2]]),
    (.added[]   | [.[0], "_skip_old_", .[2]]),
    (.removed[] | [.[0], .[1], "_skip_new_"])
  ' "${AUDIT_TMPDIR}/diff.json" \
  | while IFS= read -r row; do
      pkg=$(echo "$row" | jq -r '.[0]')
      old=$(echo "$row" | jq -r '.[1]')
      new=$(echo "$row" | jq -r '.[2]')

      [ "$old" != "_skip_old_" ] && [ "$old" != "null" ] && fetch_version "$pkg" "$old"
      [ "$new" != "_skip_new_" ] && [ "$new" != "null" ] && fetch_version "$pkg" "$new"
    done
}
```

`added` packages have no old to fetch. `removed` packages have no new to
fetch. Both forms produce a single tarball; rules that need both versions
(Rule 5 dep diff, Rule 6 maintainer diff) skip these entries.

## Parallelism

**4-way parallel fetch is the default.** Do **not** use
`xargs … bash -c 'fetch_version …'` — that needs `export -f
fetch_version`, which is bash-only (no-op under zsh) and does not
survive across separate Bash tool calls anyway (see
`audit-tmpdir.md` "Cross-tool-call handoff"). Materialize a
self-contained script with the tmpdir path **baked in** (unquoted
heredoc), then fan it out with `xargs`:

```bash
AUDIT_TMPDIR="$(cat "${TMPDIR:-/tmp}/phx-audit-dir.txt")"
cat > "${AUDIT_TMPDIR}/fetch.sh" <<EOF
#!/bin/bash
AUDIT_TMPDIR="${AUDIT_TMPDIR}"
pkg="\$1"; ver="\$2"
out="\${AUDIT_TMPDIR}/tarballs/\${pkg}/\${ver}"
mkdir -p "\$out"
mix hex.package fetch "\$pkg" "\$ver" --unpack -o "\$out" >/dev/null 2>&1 \\
  && echo "OK  \$pkg \$ver" || echo "ERR \$pkg \$ver"
EOF
chmod +x "${AUDIT_TMPDIR}/fetch.sh"

jq -r '(.changed[]|"\(.[0]) \(.[2])"),(.added[]|"\(.[0]) \(.[2])")' \
  "${AUDIT_TMPDIR}/diff.json" \
  | xargs -P 4 -n 2 "${AUDIT_TMPDIR}/fetch.sh"
```

Cap at 4 parallel fetches — `hex.pm` is fine with this and avoids
rate-limit headers (`X-Ratelimit-Remaining`). Higher concurrency
(`-P 8` or `-P 16`) trips Hex CDN throttling without meaningful speedup.

## Latency budget

Measured on the 2026-05-12 virgil dogfood (25-package update,
residential ISP). The ephemeral-tmpdir architecture means **every run
pays the cold-fetch cost** — there is no on-disk cache to reuse between
audit invocations.

| Diff size | Wall time |
|-----------|-----------|
| 1-5 packages | 15-25s |
| 10-25 packages | **60-90s** |
| 50-100 packages | 3-5 min |
| 200+ packages | 8-15 min |

Earlier docs claimed 5-10 min was realistic for 25 packages and assumed
a persistent cache could amortize the cost. That was wrong on both
counts: the 4-way parallel fetcher is fast, and re-auditing identical
locks is a rare workflow (people don't re-audit a lock they haven't
touched).

**Implications for UX:**

- Default scan on a 25-package update completes in ~75s total. The
  user sees streaming progress (see `execution-flow.md`) so the wait
  feels active, not stalled.
- `--quick` mode skips the tarball fetch entirely (it doesn't need
  unpacked sources — `mix_audit` and `mix hex.audit` read the lock).
  Target latency: <10s for 25 packages.
- The `${AUDIT_TMPDIR}` is wiped on driver exit. There is no "second
  run is faster" — by design.

## No prune step

Pre-Phase-5 versions of this fetcher included a `prune_cache()` walking
`.claude/deps-audit/cache/` and removing entries older than 30 days.
**That function is gone.** The driver's `trap "rm -rf ${AUDIT_TMPDIR}" EXIT`
makes pruning irrelevant — every audit starts fresh and ends clean.

If you're upgrading from a pre-2.12 release and `.claude/deps-audit/cache/`
exists in your project, it's safe to delete: `rm -rf .claude/deps-audit/cache/`.
The new code never writes there. Keep `.claude/deps-audit/last-run.json`
and `.claude/deps-audit/policy.exs` — those are the persistent hook
contract.

## `.gitignore` rule

The `${AUDIT_TMPDIR}` lives under `${TMPDIR}` (system temp), not in the
project tree — no .gitignore entry needed for the working artifacts.

Keep `.claude/deps-audit/last-run.json` tracked? **Default: ignore.**
It's a snapshot that becomes stale; the next audit regenerates it.
Phase 3 PreToolUse hook reads it to detect "recently audited" but the
file is expected to be local. `.claude/deps-audit/policy.exs` (Phase 3
gate config) is user-owned — track or ignore per your team's policy.

## Failure modes

| Failure | Behavior |
|---------|----------|
| Network timeout to `hex.pm` | Print warning, retry once, then BLOCK with exit 2 |
| Package not on `hex.pm` (e.g., `:git` dep) | Skip with note, audit proceeds |
| Disk full | Bail immediately — `mix hex.package fetch` will fail loudly |
| Concurrent audit on same project | Each run has its own `mktemp -d`; no contention |
| `${TMPDIR}` unwritable | Driver `mktemp -d` fails at startup, returns 2 |

## Hex API alternative (transport-only)

For Mode A `--preview` we already hit `GET /api/packages/:name` for the
latest version. The tarball is also at:

```
https://repo.hex.pm/tarballs/<pkg>-<version>.tar
```

But that needs manual `tar -xf` + checksum verification. Using
`mix hex.package fetch` is one line and handles signature checking. Stick
with mix.
