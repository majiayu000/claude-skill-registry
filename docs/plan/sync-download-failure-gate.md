# Sync Download Failure Gate

## Problem

On March 28, 2026, the `sync-data` workflow reported success even though the
registry download phase logged `Downloaded: 0` and `Failed: 2215`. The workflow
left no visible artifact for the saved `failure_report.json`, so operators could
not inspect the actual failure reasons from the GitHub UI.

## Change

1. Add a CLI gate in `scripts/sync_and_download.py` so workflow callers can opt
   into failing when the download stage produces zero successful downloads and
   one or more failures.
2. Update `.github/workflows/sync-data.yml` to use that gate for both daily and
   full registry download steps.
3. Upload `failure_report.json` as a workflow artifact so failed runs retain the
   underlying failure details.
4. Add pytest coverage for the new download gate behavior.

## Done When

- `python scripts/sync_and_download.py --download-only --fail-on-empty-download`
  exits non-zero when `downloaded == 0` and `failed > 0`.
- Partial success remains non-blocking.
- The workflow uploads `failure_report.json` when present.
- A failed gated download stops the later rebuild/push steps from running.
