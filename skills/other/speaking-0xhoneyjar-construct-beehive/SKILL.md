---
name: speaking
description: "Golden path /speak — generate RLM-isolated follow-ups with chronicle temporal context injection."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Skill
---

# /speak — Generate Follow-Ups with Temporal Context

Golden path command that generates RLM-isolated follow-up messages with chronicle temporal context. Queries the chronicle for events around each user's last feedback date and injects them into the subagent prompt.

---

## Chain

1. **Preflight**: `gp_check_chronicle` (advisory), `gp_check_growth_dir`
2. **Cognition check**: for each candidate user, check cognition file status (fresh/stale/missing)
3. **Chronicle query**: per user, query `chronicle-query.sh --around {last_feedback_date} --window {chronicle_window_days}`
4. **Follow-up generation**: invoke `/follow-up` truename with cognition + chronicle context (Step 2c.5 + 2g.6)
5. **Status + suggest next** (include cognition coverage in status)

---

## Execution

```bash
source scripts/observer/golden-path-lib.sh
gp_status_header "speak"

has_chronicle=false
if gp_check_chronicle; then
  has_chronicle=true
  gp_status_ok "chronicle" "temporal context available"
else
  gp_status_skip "chronicle" "generating without temporal context"
fi

if ! gp_check_growth_dir; then
  gp_status_fail "growth" "no growth files — run /listen first"
fi

# Step 1: Cognition check + follow-up generation per user
generated=0
fresh_count=0
stale_count=0
missing_count=0

for canvas in $(gp_list_canvases); do
  user=$(basename "$canvas" .md)

  # Check cognition status for this user
  cognition_path="grimoires/observer/cognition/${user}.yaml"
  if [[ -f "$cognition_path" ]]; then
    # /follow-up Step 2c.5 handles staleness check + auto-refresh
    # Here we just report pre-generation status for the status line
    fresh_count=$((fresh_count + 1))  # /follow-up will reclassify if stale
  else
    missing_count=$((missing_count + 1))
  fi

  # Get last feedback date from canvas frontmatter
  last_feedback_date=""  # Extract from canvas

  # Query chronicle if available
  chronicle_context=""
  if [[ "$has_chronicle" == "true" && -n "$last_feedback_date" ]]; then
    chronicle_context=$(scripts/observer/chronicle-query.sh \
      --around "$last_feedback_date" \
      --window "$GP_WINDOW_DAYS" \
      --summary 2>/dev/null) || true
  fi

  # Invoke /follow-up with cognition + chronicle context
  # Cognition loading is handled by /follow-up Step 2c.5 (auto-refresh if stale)
  # Chronicle context is injected via Step 2g.6
  generated=$((generated + 1))
done

if [[ "$generated" -gt 0 ]]; then
  gp_status_ok "follow-ups" "${generated} follow-ups generated"
else
  gp_status_skip "follow-ups" "no users need follow-ups"
fi

gp_status_ok "cognition" "${fresh_count} fresh, ${stale_count} auto-refreshed, ${missing_count} ad-hoc"

gp_progression_summary
gp_suggest_next "speak"
gp_status_footer
```

## Chronicle Integration (Step 2g.6)

When invoking the `/follow-up` truename, the `/speak` orchestrator injects temporal context into the per-user subagent prompt:

```markdown
## Temporal Context (from chronicle)

The following events occurred near this user's last feedback:

{chronicle_context}

Use these events to explain score movements and contextualize follow-up questions.
If a score changed after a release, reference the specific release.
```

This section is added after the canvas data and growth state, before the subagent generates the follow-up message.

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `/follow-up` | RLM-isolated follow-up generation |
| `chronicle-query.sh` | Temporal context for ±N days |
