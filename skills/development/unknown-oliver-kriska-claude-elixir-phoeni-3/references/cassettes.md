# VCR cassettes — Hex API fixtures for Rules 6 + 8

Rules 6 (maintainer change) and 8 (typosquat) hit the Hex API. To keep
smoke fast and offline, we ship JSON cassettes that mock the two
endpoints those rules consume.

## Iron Laws

1. **Cassettes are SHA-pinned.** Each cassette has a `_meta.sha`
   recording the sha256 of the response body at capture time. Rules
   that depend on a cassette validate the SHA before consuming it —
   silent corruption is worse than no cassette.
2. **NEVER auto-refresh.** Cassettes are committed artifacts. A
   maintainer's owner-change in real life MUST update a cassette
   in a real PR with an explicit reviewer — not via a CI auto-bump.
3. **Cassette mode opts in via env var.** `HEX_API_BASE` defaults
   to `https://hex.pm/api`; tests set
   `HEX_API_BASE=file://test-assets/hex-api-cassettes/`. Production
   audits never touch the cassettes.
4. **Empty cassette ≠ no maintainer.** When a cassette is absent,
   skip the rule with a logged warning, never silently pass.

## Endpoints covered

| Endpoint | Cassette filename | Used by |
|----------|-------------------|---------|
| `GET /api/packages/:name` | `<pkg>.packages.json` | Rule 6, Rule 8 |
| `GET /api/packages/:name/releases/:version` | `<pkg>.releases.<v>.json` | Rule 6 |

## Cassette layout

```text
plugins/elixir-phoenix/skills/deps-audit/test-assets/hex-api-cassettes/
├── phoenix.packages.json
├── phoenix.releases.1.7.20.json
├── phoenix.releases.1.7.21.json
├── jason.packages.json
├── jason.releases.1.4.4.json
├── phoeniix.packages.json          # synthetic typosquat for Rule 8
└── _meta.json                       # SHA index, capture timestamps
```

## `_meta.json` shape

```json
{
  "captured_at": "2026-05-12T18:00:00Z",
  "capture_source": "https://hex.pm/api",
  "files": {
    "phoenix.packages.json": {
      "sha256": "abc123...",
      "endpoint": "/api/packages/phoenix",
      "captured_at": "2026-05-12T18:00:00Z"
    }
  }
}
```

## Response shape — `<pkg>.packages.json`

Mirrors `hex.pm` API verbatim (only fields we consume):

```json
{
  "name": "phoenix",
  "downloads": {
    "all": 192345678,
    "recent": 2345678
  },
  "owners": [
    {"username": "chrismccord", "email": "chris@example.com"},
    {"username": "team-phoenix", "email": "team@example.com"}
  ],
  "inserted_at": "2014-04-21T22:33:00Z",
  "updated_at": "2026-04-15T10:00:00Z",
  "latest_stable_version": "1.7.21"
}
```

## Response shape — `<pkg>.releases.<v>.json`

```json
{
  "version": "1.7.21",
  "inserted_at": "2026-04-15T10:00:00Z",
  "publisher": {
    "username": "chrismccord",
    "email": "chris@example.com"
  },
  "checksum": "0123456789abcdef...",
  "retired": null
}
```

## Capturing a cassette

```bash
# Helper script — capture.sh
pkg=$1
ver=$2
out_dir=plugins/elixir-phoenix/skills/deps-audit/test-assets/hex-api-cassettes

curl -fsSL "https://hex.pm/api/packages/${pkg}" \
  | jq '.' > "${out_dir}/${pkg}.packages.json"

if [ -n "${ver}" ]; then
  curl -fsSL "https://hex.pm/api/packages/${pkg}/releases/${ver}" \
    | jq '.' > "${out_dir}/${pkg}.releases.${ver}.json"
fi

# Update _meta.json with sha + timestamp.
python3 -c "
import json, hashlib, sys
from datetime import datetime, timezone
meta_path = '${out_dir}/_meta.json'
meta = json.load(open(meta_path)) if open(meta_path, 'r').readable() else {'files': {}}
for fname in ['${pkg}.packages.json', '${pkg}.releases.${ver}.json']:
    path = '${out_dir}/' + fname
    try:
        body = open(path, 'rb').read()
        meta['files'][fname] = {
            'sha256': hashlib.sha256(body).hexdigest(),
            'captured_at': datetime.now(timezone.utc).isoformat()
        }
    except FileNotFoundError:
        pass
meta['captured_at'] = datetime.now(timezone.utc).isoformat()
json.dump(meta, open(meta_path, 'w'), indent=2)
"
```

## Consumer pattern (Rules 6 + 8)

```bash
hex_api_get() {
  local endpoint="$1"
  if [[ "${HEX_API_BASE:-https://hex.pm/api}" == file://* ]]; then
    local base="${HEX_API_BASE#file://}"
    local cassette
    cassette=$(printf '%s' "${endpoint}" \
      | sed -E 's|^/api/packages/([^/]+)$|\1.packages.json|;
                s|^/api/packages/([^/]+)/releases/(.+)$|\1.releases.\2.json|')
    cat "${base}/${cassette}" 2>/dev/null || {
      echo "cassette missing: ${cassette}" >&2
      return 1
    }
  else
    curl -fsSL "${HEX_API_BASE:-https://hex.pm/api}${endpoint}"
  fi
}
```

## Cassettes shipped with Phase 2

Phase 2 ships cassettes for:

- The 10 synthetic malicious fixtures' supporting packages
- A sample of 5 benign top-100 packages for smoke calibration
- The 5 real-world calibration packages (`hex_core`, `hex`, `rebar3`,
  `tls_certificate_check`, plus mix.lock crossing CVE-2026-23940)

Full top-100 cassettes are NOT shipped — they regenerate via the seed
job (see `seed.md`).

## Validation in smoke

The smoke `runner.sh` does not currently consume cassettes (Rules 6 + 8
aren't in the offline smoke surface). When Phase 2 wires them in,
`runner.sh` will gain:

```bash
export HEX_API_BASE="file://${HARNESS_ROOT}/../test-assets/hex-api-cassettes"
```

Per-fixture `expected.txt` then asserts on `rule:6` / `rule:8` counts.

## Lifecycle — Phase 3 monthly regen + drift detection

Cassettes captured ad-hoc go stale without a refresh schedule. Phase 3
ships a monthly regeneration workflow and drift detection at audit
runtime.

### Monthly regen workflow

`.github/workflows/cassette-regen.yml` runs on the 5th of every month
(staggered from the seed-regen run on the 1st) and on manual
`workflow_dispatch`:

1. Check out repo, install jq + Python 3.
2. Iterate over the top-100 seed list (`smoke-test/corpus.d/benign-100.txt`).
3. For each package, call `bash priv/cassettes/capture.sh <pkg>` against
   live `https://hex.pm/api`. The script updates `_meta.json` SHA
   entries.
4. If any cassette content changed, open a PR via
   `peter-evans/create-pull-request@v6` with summary "Monthly cassette
   regen: N packages updated."

### 403 fallback

Some org GitHub policies deny `GITHUB_TOKEN` PR creation
("Actions cannot create pull requests"). The workflow checks the
`create-pull-request` action's exit + status, and on 403:

1. Uploads the regenerated `test-assets/hex-api-cassettes/` tree as a
   workflow artifact (90-day retention).
2. Writes a job summary: "cassettes regenerated as artifact; PR
   creation requires a repo admin to enable
   Settings → Actions → Allow GitHub Actions to create pull requests."
3. Exits 0 — the regen ran successfully even if the PR didn't.
4. Optional: posts to `${SLACK_WEBHOOK_URL}` if the secret exists.

The artifact path is `cassettes-regen-<run-id>.zip`. Maintainers
download it, run `tar xf …`, commit manually.

### Drift detection at audit runtime

The audit body reads `_meta.json` before consuming any cassette:

```bash
expected_sha=$(jq -r ".files[\"${cassette}\"].sha256" "${meta_path}")
actual_sha=$(shasum -a 256 "${cassette_path}" | awk '{print $1}')
if [ "${expected_sha}" != "${actual_sha}" ]; then
  echo "phx-deps-audit: cassette stale — ${cassette} (sha mismatch)" >&2
  # Continue, but emit INFO so the renderer surfaces "stale cassette" in output.
  emit_finding rule:6 severity:info \
    "Cassette ${cassette} SHA drift — consider regenerating."
fi
```

Drift on a single cassette doesn't fail the audit. It surfaces in
the renderer's "carried-over risks" section. If >10% of cassettes
drift in one run, the renderer's tail prints a one-liner pointing
at the regen workflow.

### Per-PR capture pattern (manual)

When a user adds a `hex_vet.exs` entry for a package without a
cassette, document the manual flow in the PR:

```bash
bash plugins/elixir-phoenix/skills/deps-audit/priv/cassettes/capture.sh <pkg> <ver>
git add plugins/elixir-phoenix/skills/deps-audit/test-assets/hex-api-cassettes/
```

Reviewers should diff the cassette body and the `_meta.json` SHA
update together — a maintainer change in the captured response
should match the package's actual maintainer history. This catches
the scenario where a malicious cassette is committed alongside a
seemingly-benign code change.

### Why monthly, not weekly

Weekly regen would catch drift sooner but doubles the PR noise. The
audit body's drift detection covers the "I haven't run regen in 6
weeks" case by surfacing stale cassettes as INFO — users get a clear
nudge without the maintainer overhead of weekly merges. Re-evaluate
after the first 6 months of operation.
