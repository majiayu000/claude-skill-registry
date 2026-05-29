---
name: seeing
description: "Golden path /see — refresh stale score snapshots and identify canvases needing MER capture."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Skill
---

# /see — Refresh Score Snapshots

Golden path command that identifies stale canvases and refreshes their score API snapshots. Surfaces canvases missing MER (Most Engaged Response) data.

---

## Chain

1. **Preflight**: `gp_check_score_api`
2. **Stale detection**: identify canvases with `score_snapshot.captured_at` older than `stale_snapshot_hours`
3. **Refresh**: for each stale canvas, pull fresh score API snapshot, update canvas frontmatter
4. **MER check**: identify canvases missing MER sections → suggest MER capture
5. **Status + suggest next**

---

## Execution

```bash
source scripts/observer/golden-path-lib.sh
gp_status_header "see"

# Step 1: Score API preflight
if ! gp_check_score_api; then
  gp_status_fail "score-api" "unreachable — showing staleness ages without refreshing"
  # Degrade: just show how stale each canvas is
fi

# Step 2: Find stale canvases
stale_count=0
refreshed_count=0
for canvas in $(gp_list_canvases); do
  # Extract captured_at from frontmatter
  # Compare against current time - stale_snapshot_hours
  # If stale: refresh via score-api-query.sh, update frontmatter
done

if [[ "$refreshed_count" -gt 0 ]]; then
  gp_status_ok "refresh" "${refreshed_count} canvases refreshed"
else
  gp_status_skip "refresh" "all snapshots current"
fi

# Step 3: MER check
missing_mer=0
for canvas in $(gp_list_canvases); do
  # Check if canvas has MER section
done
if [[ "$missing_mer" -gt 0 ]]; then
  gp_status_ok "mer-check" "${missing_mer} canvases need MER capture"
else
  gp_status_skip "mer-check" "all canvases have MERs"
fi

gp_progression_summary
gp_suggest_next "see"
gp_status_footer
```

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `score-api-query.sh` | Fetch fresh score snapshots |
| `/observe` | Update canvas frontmatter |
