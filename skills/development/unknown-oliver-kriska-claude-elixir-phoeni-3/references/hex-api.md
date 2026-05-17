# Hex API Enrichment

Adds metadata (owners, downloads, publish dates) to each audited package.
Drives Rule 6 (maintainer change) and Rule 8 (typosquat download delta).

## Endpoints

| Call | Endpoint | Why |
|------|----------|-----|
| Package metadata | `GET https://hex.pm/api/packages/:name` | Owners, downloads, inserted_at |
| Per-release metadata | `GET https://hex.pm/api/packages/:name/releases/:version` | Per-release publisher, inserted_at |
| Top-500 by downloads | `GET https://hex.pm/api/packages?sort=downloads&page=1..7` | Typosquat denominator (Rule 8) |

All require `Accept: application/vnd.hex+json` header.

## Computed signals per package

```elixir
%{
  pkg: "phoenix",
  owners: ["chrismccord", "josevalim", "..."],
  owner_age_days: 3650,             # min(inserted_at across owners)
  downloads_all: 50_000_000,
  downloads_recent: 800_000,         # weekly
  inserted_at: "2014-04-17T...",
  days_since_publish_latest: 14,
  download_velocity: 800_000 / 7,    # downloads/day, recent
  release_publisher: "josevalim"     # at the version being audited
}
```

## Rate limit

**5 req/sec.** Hex API doesn't publish official limits but the Hex.pm team
has stated this is the polite ceiling.

**Use `python3` + `urllib`, not curl.** A `curl "...${var}"` wrapper is
fragile to whitespace/newline contamination in the interpolated path
(dogfood: `curl: (3) Malformed input to a URL function`). `python3` is
already a hard dependency of the audit and is robust here. Canonical:

```bash
hex_api_get() {  # usage: hex_api_get <api-path>   e.g. packages/phoenix
  AUDIT_TMPDIR="$(cat "${TMPDIR:-/tmp}/phx-audit-dir.txt")"
  python3 - "$1" "$AUDIT_TMPDIR" <<'PY'
import sys, os, json, time, urllib.request, pathlib
path, tmp = sys.argv[1].strip(), sys.argv[2]
cache = pathlib.Path(tmp, "hex-api", path.replace("/", "_") + ".json")
ttl = 7 * 86400
if cache.is_file() and time.time() - cache.stat().st_mtime < ttl:
    print(cache.read_text()); sys.exit(0)
cache.parent.mkdir(parents=True, exist_ok=True)
req = urllib.request.Request(
    "https://hex.pm/api/" + path,
    headers={"Accept": "application/vnd.hex+json",
             "User-Agent": "phx-deps-audit/0.1 (+claude-elixir-phoenix)"})
with urllib.request.urlopen(req, timeout=20) as r:
    body = r.read().decode()
cache.write_text(body)
time.sleep(0.2)   # 5 req/sec ceiling
print(body)
PY
}
```

The `sleep 0.2` blocks the calling process; keep Hex calls serial
(parallelism 1) or the effective rate becomes `parallelism / 0.2`.

> **curl fallback** (only if `python3` is unavailable, which the audit
> otherwise assumes): `curl -fsSL -H "Accept: application/vnd.hex+json"
> "https://hex.pm/api/${path}"` — but trim the path first
> (`path="${path//[$'\n\r\t ']/}"`) to avoid the malformed-URL failure.

## Cache TTL

| Resource | TTL | Justification |
|----------|-----|---------------|
| Package metadata | 7 days | Owners change rarely; we want fresh-ish data |
| Per-release metadata | 30 days | Immutable once published |
| Top-500 list | 24 hours | Daily refresh is industry standard |

Override with `--no-cache` for debugging.

## Top-500 list — typosquat denominator

```bash
fetch_top_500() {
  AUDIT_TMPDIR="$(cat "${TMPDIR:-/tmp}/phx-audit-dir.txt")"
  python3 - "$AUDIT_TMPDIR" <<'PY'
import sys, time, json, urllib.request, pathlib
cache = pathlib.Path(sys.argv[1], "hex-api", "top-500.json")
if cache.is_file() and time.time() - cache.stat().st_mtime < 24 * 3600:
    sys.exit(0)
cache.parent.mkdir(parents=True, exist_ok=True)
out = []
for page in range(1, 8):
    req = urllib.request.Request(
        f"https://hex.pm/api/packages?sort=downloads&page={page}",
        headers={"Accept": "application/vnd.hex+json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        out += json.loads(r.read().decode())
    time.sleep(0.5)
cache.write_text(json.dumps(out))
PY
}
```

> curl fallback: same `for page in 1..7; curl … | jq -s 'add'` loop as
> before — use only if `python3` is missing.

7 pages × 100 packages/page = 700 entries; we use the first 500 (the tail
has thin signal for typosquat denominator anyway). Total fetch: ~3 seconds
on cold cache, free on warm.

## Computing signals

```bash
package_signals() {
  local pkg="$1"
  local data
  data=$(hex_api_get "packages/${pkg}")

  jq -r --arg today "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '
    {
      pkg: .name,
      owners: [.owners[]?.username],
      downloads_all: .downloads.all,
      downloads_recent: .downloads.recent,
      inserted_at: .inserted_at,
      latest_version: .releases[0].version,
      latest_version_inserted_at: .releases[0].inserted_at
    } | tojson
  ' <<<"${data}"
}
```

`owner_age_days` requires a second call per owner (to `/users/:username`)
— deferred to Phase 2 to keep rate-limit pressure low. For Phase 1, we
treat "owner list" as a static set and only diff between versions (Rule 6).

## Rule 6 — Maintainer change detector

```bash
maintainer_change() {
  local pkg="$1" old_ver="$2" new_ver="$3"

  local old_pub new_pub
  old_pub=$(hex_api_get "packages/${pkg}/releases/${old_ver}" \
            | jq -r '.publisher.username // empty')
  new_pub=$(hex_api_get "packages/${pkg}/releases/${new_ver}" \
            | jq -r '.publisher.username // empty')

  if [ -n "${old_pub}" ] && [ -n "${new_pub}" ] && [ "${old_pub}" != "${new_pub}" ]; then
    echo "BLOCK|6|maintainer changed: ${old_pub} → ${new_pub}"
  fi
}
```

Note: `publisher` is the user who *published the release*. `owners` is the
package-level list. The two CAN diverge (publisher is a delegate of an
owner). For Phase 1 we flag *publisher* change at release boundary.

## Rule 8 — Typosquat detector

```bash
typosquat_check() {
  local pkg="$1"

  # Pre-fetched top-500 list
  fetch_top_500

  jq -r --arg pkg "${pkg}" '
    .[] | select(.name != $pkg)
        | [.name, .downloads.all] | @tsv
  ' ${AUDIT_TMPDIR}/hex-api/top-500.json \
  | while IFS=$'\t' read -r candidate dl_count; do
      local dist
      dist=$(levenshtein "${pkg}" "${candidate}")
      if [ "${dist}" -le 2 ]; then
        local target_dl
        target_dl=$(hex_api_get "packages/${pkg}" | jq -r '.downloads.all // 0')
        if [ "${dl_count}" -gt $((target_dl * 1000)) ]; then
          echo "BLOCK|8|typosquat candidate: '${pkg}' (${target_dl} DLs) vs '${candidate}' (${dl_count} DLs, distance ${dist})"
        fi
      fi
    done
}
```

Levenshtein helper (inline awk impl or `string_distance` Hex pkg if
available):

```bash
levenshtein() {
  awk -v a="$1" -v b="$2" 'BEGIN {
    la = length(a); lb = length(b)
    if (la == 0) { print lb; exit }
    if (lb == 0) { print la; exit }
    for (i = 0; i <= la; i++) d[i,0] = i
    for (j = 0; j <= lb; j++) d[0,j] = j
    for (i = 1; i <= la; i++) for (j = 1; j <= lb; j++) {
      c = (substr(a,i,1) == substr(b,j,1)) ? 0 : 1
      v = d[i-1,j] + 1
      h = d[i,j-1] + 1
      diag = d[i-1,j-1] + c
      d[i,j] = (v < h ? (v < diag ? v : diag) : (h < diag ? h : diag))
    }
    print d[la,lb]
  }'
}
```

## Failure modes

| Failure | Behavior |
|---------|----------|
| Rate-limit response (429) | Sleep 5s, retry once. Second 429 → skip API enrichment for this pkg with WARN |
| 404 on package | Mark `unknown` (likely renamed or removed); skip API rules |
| Network timeout | Use stale cache if available; else skip with WARN |
| Malformed JSON | Log + skip (Hex API is stable; this means corruption) |
| Cache disk full | Bypass cache, fall back to direct call |

## Why no `mix hex.search` / `mix hex.info`?

Both are interactive shells under the hood — slow to parse, not designed for
machine output. Direct HTTP is 5-10× faster.
