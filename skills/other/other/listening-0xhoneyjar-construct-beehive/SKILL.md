---
name: listening
description: "Golden path /listen — ingest all new signals: chronicle releases, Supabase feedback, DM exports, growth matches."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Skill
---

# /listen — Ingest All New Signals

Golden path command that auto-chains the Observer's intake pipeline. Ingests chronicle releases, daily synthesis feedback, unprocessed DM exports, and growth response matching.

---

## Chain

1. **Preflight**: `gp_check_gh_auth`, `gp_check_supabase_key`
2. **Chronicle ingest** (if gh auth passes): `scripts/observer/chronicle-ingest.sh` → count new entries
3. **Daily synthesis**: invoke `/daily-synthesis` truename → count new signals
4. **DM export scan**: check `grimoires/observer/dm-exports/` for unprocessed files → invoke `/ingest-dm` for each
5. **Growth matching**: run `scripts/observer/growth-state.sh` outcome matching for new responses
6. **Gap state sync**: run `scripts/observer/gap-sync.sh` to pull GitHub issue closures back to canvases
7. **Status + suggest next**

---

## Execution

```bash
source scripts/observer/golden-path-lib.sh
gp_status_header "listen"

# Step 1: Chronicle ingest
if gp_check_gh_auth; then
  chronicle_output=$(scripts/observer/chronicle-ingest.sh 2>&1)
  new_entries=$(echo "$chronicle_output" | grep -o '[0-9]* new entries' | head -1 | grep -o '[0-9]*')
  if [[ "${new_entries:-0}" -gt 0 ]]; then
    gp_status_ok "chronicle" "${new_entries} new entries ingested"
  else
    gp_status_skip "chronicle" "no new releases"
  fi
else
  gp_status_fail "chronicle" "gh not authenticated — run: gh auth login"
fi

# Step 2: Daily synthesis
if gp_check_supabase_key; then
  # Invoke /daily-synthesis truename
  gp_status_ok "daily-synthesis" "processing new feedback"
else
  gp_status_fail "daily-synthesis" "Supabase key not found — set SUPABASE_KEY"
fi

# Step 3: DM exports
dm_dir="grimoires/observer/dm-exports"
if [[ -d "$dm_dir" ]]; then
  pending=$(find "$dm_dir" -name "*.txt" -o -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$pending" -gt 0 ]]; then
    # Invoke /ingest-dm for each
    gp_status_ok "ingest-dm" "${pending} pending exports"
  else
    gp_status_skip "ingest-dm" "no pending exports"
  fi
else
  gp_status_skip "ingest-dm" "no exports directory"
fi

# Step 4: Growth matching (E9 L4 — response attribution)
# Match newly ingested signals to outstanding follow-ups using growth-match.sh.
# Signals come from provenance records created by Steps 1-3 of this /listen run.
proposed_count=0
dedup_count=0
if gp_check_growth_dir; then
  # Collect newly ingested signals from this /listen run.
  # Each signal has: signal_id (provenance content_hash), user, raw_text, timestamp, thread_id.
  # Source: provenance records created by Steps 1-3 (chronicle, daily-synthesis, ingest-dm).
  # Query recent provenance entries to find signals from this session.

  # Clean up orphaned .tmp files from previous crashed runs (see scripts/staleness.md)
  find grimoires/observer/growth/ -name "*.tmp" -mmin +5 -delete 2>/dev/null

  # BATCH SIGNALS BY USER to avoid per-signal lock contention under burst conditions.
  # Without batching, a 50-signal burst causes 50 lock acquire/release cycles.
  # With batching, we acquire each user's lock once and process all their signals.
  declare -A signals_by_user  # user → array of signals
  FOR each newly_ingested_signal:
    user = signal.user
    growth_path = "grimoires/observer/growth/${user}.yaml"
    IF NOT exists(growth_path): CONTINUE
    signals_by_user[$user] += signal

  FOR user, signals IN signals_by_user:
    # Run matching for all signals (pure function — reads growth state, outputs to stdout)
    all_matches = []
    FOR signal IN signals:
      match_result = Run: scripts/observer/growth-match.sh \
        "$user" "$signal.signal_id" "$signal.raw_text" "$signal.timestamp" "${signal.thread_id:-}"
      IF match_result is not empty:
        all_matches += parse_yaml_documents(match_result)

    IF all_matches is empty: CONTINUE

    # Acquire lock ONCE per user, process all matches
    proposed_path = "grimoires/observer/growth/${user}.proposed_matches.yaml"
    lock_path = "grimoires/observer/growth/${user}.yaml.lock"
    WITH flock(lock_path):
      # Re-read inside lock (avoids TOCTOU)
      IF NOT exists(proposed_path):
        proposed_content = {schema_version: 1, user: "$user", matches: []}
      ELSE:
        proposed_content = read_yaml(proposed_path)

      FOR match_entry in all_matches:
        # Idempotency: dedupe by (signal_id, follow_up_id)
        existing = any(m for m in proposed_content.matches
                       where m.signal_id == match_entry.signal_id
                       AND m.follow_up_id == match_entry.follow_up_id)
        IF existing:
          dedup_count += 1
          CONTINUE

        match_entry.proposed_at = now_iso8601()
        match_entry.status = "pending"
        match_entry.confirmed_at = null
        proposed_content.matches.append(match_entry)
        proposed_count += 1

      # Atomic write: temp file + mv (see scripts/staleness.md for crash recovery)
      write_yaml(proposed_path + ".tmp", proposed_content)
      mv(proposed_path + ".tmp", proposed_path)

  if [[ "$proposed_count" -gt 0 ]]; then
    msg="${proposed_count} proposed matches (run /grow to confirm)"
    if [[ "$dedup_count" -gt 0 ]]; then
      msg="$msg (${dedup_count} duplicates skipped)"
    fi
    gp_status_ok "growth-matching" "$msg"
  else
    gp_status_skip "growth-matching" "no new responses matched"
  fi
else
  gp_status_skip "growth-matching" "no growth files yet"
fi

# Step 5: Gap state sync — pull GitHub issue state back to canvases
if [[ -f "grimoires/observer/gap-index.jsonl" ]]; then
  if command -v gh &>/dev/null && gh auth status &>/dev/null 2>&1; then
    sync_output=$(scripts/observer/gap-sync.sh 2>&1)
    resolved_count=$(echo "$sync_output" | grep -c "FILED → RESOLVED" || true)
    if [[ "$resolved_count" -gt 0 ]]; then
      gp_status_ok "gap-sync" "${resolved_count} gaps resolved (issues closed on GitHub)"
    else
      gp_status_skip "gap-sync" "no state changes"
    fi
  else
    gp_status_fail "gap-sync" "gh not authenticated — run: gh auth login"
  fi
else
  gp_status_skip "gap-sync" "no gap-index.jsonl — run gap-index-backfill.sh first"
fi

# Progression + suggest next
gp_progression_summary
gp_suggest_next "listen"
gp_status_footer
```

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `/daily-synthesis` | Pull + classify Supabase feedback |
| `/ingest-dm` | Import DM conversations |
| `growth-state.sh` | Match responses to follow-ups |
| `chronicle-ingest.sh` | Poll GitHub releases |
| `gap-sync.sh` | Pull GitHub issue state back to canvases |
