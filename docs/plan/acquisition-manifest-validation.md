# Acquisition Manifest Validation Plan

## Goal
Validate that the acquisition manifest improves `skill` fetch efficiency without reducing correctness.

## Scope
- Script: `scripts/sync_and_download.py`
- Feature flags:
  - Baseline: `--disable-acquisition-manifest`
  - Candidate: default (manifest enabled)

## Required Metrics
- `downloaded`
- `failed`
- `url_attempts`
- `manifest_hits`
- `manifest_misses`
- elapsed seconds (wall clock)

Data source:
- `failure_report.json` for each run
- command elapsed time via shell `time`

## Acceptance Thresholds
For the same input registry and same environment:
1. Correctness guard:
   - `downloaded(candidate) >= downloaded(baseline)`
   - `failed(candidate) <= failed(baseline) * 1.02` (allow <=2% noise)
2. Efficiency guard:
   - `url_attempts(candidate) <= url_attempts(baseline) * 0.70` (>=30% reduction)
3. Runtime guard:
   - elapsed(candidate) <= elapsed(baseline)

If (1) fails, reject.
If (1) passes but (2)/(3) fail, keep disabled and inspect probe order + manifest quality.

## Repro Commands
Run in `claude-skill-registry-core` root.

```bash
# Baseline (manifest off)
cp registry.json /tmp/registry.baseline.json
/usr/bin/time -p python scripts/sync_and_download.py \
  --download-only \
  --disable-acquisition-manifest \
  --max-pending 2000
cp failure_report.json /tmp/failure_report.baseline.json

# Candidate (manifest on)
cp /tmp/registry.baseline.json registry.json
/usr/bin/time -p python scripts/sync_and_download.py \
  --download-only \
  --max-pending 2000
cp failure_report.json /tmp/failure_report.candidate.json
```

## Quick Comparator
```bash
python - <<'PY'
import json
from pathlib import Path

base = json.loads(Path('/tmp/failure_report.baseline.json').read_text())['stats']
new = json.loads(Path('/tmp/failure_report.candidate.json').read_text())['stats']

print('baseline:', base)
print('candidate:', new)

def ratio(a, b):
    return (a / b) if b else None

print('url_attempt_ratio(candidate/base):', ratio(new.get('url_attempts', 0), base.get('url_attempts', 0)))
print('download_delta:', new.get('downloaded', 0) - base.get('downloaded', 0))
print('failed_delta:', new.get('failed', 0) - base.get('failed', 0))
print('manifest_hits:', new.get('manifest_hits', 0), 'manifest_misses:', new.get('manifest_misses', 0))
PY
```

## CI Recommendation
Add a scheduled benchmark job that executes both modes on the same capped registry sample and uploads both reports as artifacts.
