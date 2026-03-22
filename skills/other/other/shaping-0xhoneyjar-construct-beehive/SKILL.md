---
name: shaping
description: "Golden path /shape — consolidate journey patterns across canvases and file gap issues."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Skill
---

# /shape — Consolidate Patterns

Golden path command that consolidates journey patterns across canvases and files gap issues for product work.

---

## Chain

1. **Preflight**: `gp_check_canvases_exist(min_canvases_for_shape)` (default 3)
2. **Journey consolidation**: invoke `/shape` truename (shaping-journeys)
3. **Gap filing**: if new patterns found, invoke `/gap-to-issues` for filing
4. **Status + suggest next**

---

## Execution

```bash
source scripts/observer/golden-path-lib.sh
gp_status_header "shape"

canvas_count=$(gp_count_canvases)
if ! gp_check_canvases_exist "$GP_MIN_CANVASES"; then
  gp_status_fail "canvases" "fewer than ${GP_MIN_CANVASES} canvases (have ${canvas_count}) — nothing to consolidate"
  gp_status_blocked "need at least ${GP_MIN_CANVASES} canvases — run /listen to build more"
  gp_status_footer
  return
fi

# Step 1: Journey consolidation
# Invoke /shaping-journeys truename
gp_status_ok "journeys" "consolidated across ${canvas_count} canvases"

# Step 2: Gap scan — count IDENTIFIED gaps across updated canvases
identified_gaps=0
for canvas in grimoires/observer/canvas/*.md; do
  count=$(grep -c '^\*\*Status\*\*: IDENTIFIED' "$canvas" 2>/dev/null || true)
  identified_gaps=$((identified_gaps + count))
done

# Step 3: Gap filing handoff — auto-chain to /gap-to-issues (which has source fidelity gate)
if [[ "$identified_gaps" -gt 0 ]]; then
  gp_status_ok "gap-scan" "${identified_gaps} IDENTIFIED gaps found across canvases"
  # Invoke /gap-to-issues — source fidelity gate (Step 2.5) filters category (d) inferred features
  gp_status_ok "gap-filing" "invoking /gap-to-issues for ${identified_gaps} gaps"
else
  gp_status_skip "gap-filing" "no IDENTIFIED gaps to file"
fi

gp_progression_summary
gp_suggest_next "shape"
gp_status_footer
```

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `/shaping-journeys` | Cross-canvas journey consolidation |
| `/gap-to-issues` | File identified gaps as issues |
