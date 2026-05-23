# Deal Hygiene Skill

---
name: deal-hygiene
description: Check and fix HubSpot pipeline hygiene issues - past close dates, missing next steps, stale deals. Triggers on "deal hygiene", "pipeline cleanup", "fix close dates", "stale deals", "pipeline health check".
---

## Purpose

Automated HubSpot deal hygiene maintenance to keep the pipeline clean and accurate.

## Triggers

- "deal hygiene"
- "pipeline cleanup"
- "fix close dates"
- "stale deals"
- "pipeline health check"
- "check pipeline hygiene"

## What It Checks

### 1. Past Close Dates
Deals with close dates in the past get auto-pushed to future based on stage:
- Prospecting: +60 days
- Discovery: +45 days
- Rate Creation: +30 days
- Proposal: +21 days
- Negotiation: +14 days
- Implementation: +14 days
- Shipping: +30 days

### 2. Missing Next Steps
Deals without `hs_next_step` populated (shows as "--" in HubSpot).

### 3. Stale Deals
Deals with no activity for 14+ days (excluding Closed and Shipping stages).

## Usage

### Report Only (Check Mode)
```bash
python scripts/deal_hygiene_check.py
```

### Auto-Fix Close Dates
```bash
python scripts/deal_hygiene_check.py --fix
```

### Custom Stale Threshold
```bash
python scripts/deal_hygiene_check.py --fix --days 30
```

## Integration with Daily Sync

Add to EOD sync for automatic hygiene maintenance:

```python
# In unified_sync.py eod_sync():
subprocess.run(['python', 'scripts/deal_hygiene_check.py', '--fix'])
```

## Output Example

```
============================================================
HUBSPOT DEAL HYGIENE CHECK
Date: 2025-12-30 14:30
Mode: FIX
============================================================

Checking 45 active deals...

----------------------------------------
1. PAST CLOSE DATES
----------------------------------------
  [FIXED] Athleta - Parcel Shipping Optimiz
          2025-11-30 -> 2026-01-31 (30d past)

----------------------------------------
2. MISSING NEXT STEPS
----------------------------------------
  [NEEDS ATTENTION] Everything's On The Table
                    Stage: 04-Proposal

----------------------------------------
3. STALE DEALS (>14 days)
----------------------------------------
  [21d stale] Some Deal Name                   $500,000
              Stage: 02-Discovery

============================================================
SUMMARY
============================================================
  Past close dates:      1 (fixed)
  Missing next steps:    1
  Stale deals:           1

  Total issues: 3
```

## HubSpot Fields Used

| Field | Purpose |
|-------|---------|
| `closedate` | Close date (Unix ms) |
| `hs_next_step` | Next step text |
| `hs_lastmodifieddate` | Last activity date |
| `dealstage` | Current pipeline stage |

## Related Skills

- `/pipeline-health` - Quick pipeline overview
- `/check-tasks` - Task hygiene
- `/cvm-goals` - Goal tracking
