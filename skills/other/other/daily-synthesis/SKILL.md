---
name: daily-synthesis
description: Automated end-to-end feedback pipeline that pulls new Supabase entries, enriches, classifies, routes to canvases, and generates a synthesis report.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---

# Daily Synthesis

Automated feedback pipeline that runs daily (or on demand). Pulls new UI feedback from Supabase, enriches with Score API position, classifies signal type and weight, routes to canvases, detects gaps, and generates a synthesis report.

Builds on the existing `/synthesize-feedback` patterns with full automation via wrapper scripts.

---

## Core Principle

**Zero-friction daily operation.** This skill should require no arguments for the common case. It reads its own state, fetches only what's new, and reports what changed.

---

## Triggers

```
/daily-synthesis                           # Process all new feedback since last run
/daily-synthesis --since 7d                # Process feedback from last 7 days
/daily-synthesis --since 2026-02-01        # Process feedback since specific date
/daily-synthesis --wallet 0x...            # Filter to specific wallet only
/daily-synthesis --dry-run                 # Preview without writing any files
```

---

## When to Use

- Daily: Run once per day to process accumulated UI feedback
- On demand: After a beta expansion or known feedback burst
- Debugging: With `--wallet` to inspect a single user's feedback
- Preview: With `--dry-run` to see what would change before committing

---

## Workflow

### Phase 1: Read State

Read `grimoires/observer/synthesis/last-run.json` for processing state:
```json
{
  "last_processed_at": "2026-02-06T08:42:28Z",
  "total_processed": 6,
  "last_run_date": "2026-02-06T19:30:00Z"
}
```

Determine the `since` timestamp:
- Default: `last_processed_at` from state file
- `--since <duration>`: Calculate ISO timestamp (e.g., `7d` → 7 days ago)
- `--since <date>`: Use as-is
- If no state file exists: Use 30 days ago as default

### Phase 2: Pull New Feedback

```bash
scripts/observer/supabase-query.sh feedback --since <timestamp>
```

**If `--wallet` provided:**
```bash
scripts/observer/supabase-query.sh feedback --wallet <address>
```

Parse the JSON array response. Each entry has:
- `wallet_address`, `feedback_type` (good/neutral/bad), `note`
- `source` (pulse/profile), `page_context`, `model_version_id`
- `session_id`, `created_at`

**If no new entries:** Report "No new feedback since last run" and exit.

### Phase 3: Enrich with Score API

For each **unique wallet** in the results:

```bash
scripts/observer/score-api-query.sh profile <wallet> --format snapshot
```

Cache results per wallet (don't re-fetch for same wallet in batch).

Extract key fields for classification:
- `rank`, `combined_score`, `crowd_tier`, `elite_tier`

### Phase 3.5: Event Bus Consumption

Consume events from the Loa event bus to include in the synthesis report. This phase pulls events that were emitted by Observer skills (`/observe`, `/ingest-dm`) since the last synthesis run.

**Step 1: Consume observer.feedback_captured events**

```bash
source .claude/scripts/lib/event-bus.sh

# Define handler function
handle_feedback_event() {
  local event_json
  event_json=$(cat)
  # Extract and aggregate: direction, kind, weight from .data.signal
  # Track: total count, by_direction, by_kind, by_weight_tier
  # Check .data.subject.resolution_status — count unresolved
}

# Consume with offset tracking (exactly-once delivery)
consumed_count=$(consume_events "observer.feedback_captured" handle_feedback_event "daily-synthesis")
```

- Offset file: `grimoires/loa/a2a/events/.offsets/daily-synthesis.observer.feedback_captured.offset`
- Directory auto-created by `_init_event_bus()` via `mkdir -p`
- Events missing `data.subject` (pre-enrichment legacy events) treated as `unresolved`
- First run on clean repo succeeds with 0 events consumed

**Step 2: Aggregate event bus data**

Build aggregation summary from consumed events:
```
event_bus_summary:
  total: {N}
  by_direction: {positive: N, negative: N, neutral: N}
  by_kind: {feel: N, calibration: N, accuracy: N, ux: N}
  by_weight_tier: {high: N, medium: N, low: N}
  unresolved_count: {N}  # Events where data.subject missing or unresolved
```

**Step 3: Include in synthesis report**

If `total > 0`, add an "Event Bus Summary" section to the synthesis report:

```markdown
## Event Bus Summary

| Metric | Value |
|--------|-------|
| Events consumed | {total} |
| Positive / Negative / Neutral | {p} / {n} / {neu} |
| By kind | feel: {f}, calibration: {c}, accuracy: {a}, ux: {u} |
| Unresolved subjects | {unresolved_count} |
```

If `total == 0`, skip this section entirely.

**Step 4: Consume artisan.pattern_detected events**

```bash
# Define handler for Artisan pattern events
handle_pattern_event() {
  local event_json
  event_json=$(cat)
  # Extract: .data.signal.content (pattern description)
  # Extract: .data.context.source_event_ids (linked feedback events)
  # Extract: .data.context.pattern_key, .data.context.cohort_size
  # Map source_event_ids to canvases via wallet lookup from .data.subject
}

# Consume with offset tracking
pattern_count=$(consume_events "artisan.pattern_detected" handle_pattern_event "daily-synthesis")
```

- Offset file: `grimoires/loa/a2a/events/.offsets/daily-synthesis.artisan.pattern_detected.offset`
- For each pattern event: extract description, source_event_ids, map to canvases via wallet lookup
- **Critical invariant**: synthesis does NOT emit `observer.feedback_captured` based on consumed patterns — report-only

**Step 5: Include Cross-Construct Signals in report**

If `pattern_count > 0`, add a "Cross-Construct Signals" section to the synthesis report:

```markdown
## Cross-Construct Signals

| Pattern | Cohort | Direction | Source Events | Week |
|---------|--------|-----------|---------------|------|
| {description} | {cohort_size} users | {direction} | {N} events | {time_window} |
```

If `pattern_count == 0`, add:
```markdown
## Cross-Construct Signals

No Artisan patterns found in this period.
```

### Phase 4: Classify Signal Weight

For each enriched feedback entry, apply weight based on user position:

```
IF rank <= 50 OR crowd_tier in ['eternal', 'godfather', 'all_night']:
  signal_weight = HIGH
ELIF crowd_tier in ['devoted', 'regular'] OR rank <= 200:
  signal_weight = MEDIUM
ELSE:
  signal_weight = LOW
```

### Phase 5: Classify Signal Type

For each feedback entry, classify based on note content:

```
IF note is null or empty:
  signal_type = FEEL

ELIF note matches /dimension|factor|weight|score.*should|too (high|low)/i:
  signal_type = WEIGHTINGS

ELIF note matches /missing|wrong|didn't|transaction|minted|count|data/i:
  signal_type = ACCURACY

ELIF note matches /can't find|confus|button|page|navigate|broken|UI|UX/i:
  signal_type = UX

ELSE:
  signal_type = FEEL  (default)
```

**Classification priority**: WEIGHTINGS → ACCURACY → UX → FEEL

### Phase 6: Route to Canvases

For each feedback entry:

**Step 6a: Resolve username**

```bash
scripts/observer/wallet-resolve.sh <wallet_address>
```

If resolved: `username = result`
If not found: `username = <wallet_address first 10 chars>`

**Step 6b: Check for existing canvas**

Search `grimoires/observer/canvas/{username}*.md`

**Step 6b.5: Provenance Gate — Dedup & Hash Each Feedback Entry**

Before appending to any canvas, pipe each feedback entry through the provenance gate:

```bash
# Content = the feedback note (or "—" if empty). Use the full note text.
echo -n "$feedback_note" | scripts/provenance/gate.sh \
  --source-type supabase_feedback \
  --timestamp "$supabase_created_at" \
  --timestamp-raw "$supabase_created_at" \
  --confidence exact \
  --canvas-target "$username" \
  --raw-source-ref "$supabase_row_id" \
  --ingested-by daily-synthesis \
  --json
```

- `--timestamp`: Use full Supabase `created_at` ISO 8601 (NOT truncated to day)
- `--confidence exact`: Supabase provides authoritative timestamps
- `--raw-source-ref`: Supabase row identifier (e.g., the feedback table primary key)
- No thread context — standalone feedback items (`thread_id: null`)
- Capture `content_hash` from `--json` output for event fingerprint

| Exit Code | Action |
|-----------|--------|
| 0 (INGEST) | Proceed to canvas append. Capture `content_hash` for event emission. |
| 1 (SKIP) | Skip — already ingested. Increment skip counter. |
| 2+ (ERROR) | Halt and report error |

After processing all entries: `"Processed {N} new feedback entries, {M} duplicates"`

---

**Step 6c: Route based on conditions**

| Condition | Action |
|-----------|--------|
| Existing canvas found | Append to `## Feedback Entries (from UI)` table |
| No canvas + HIGH weight | Auto-create canvas from template |
| No canvas + note > 50 chars | Auto-create canvas from template |
| No canvas + `bad` + `profile` source | Auto-create canvas from template |
| No canvas + none of above | Log to synthesis report only |

**Feedback entry row format:**
```markdown
| {date} | {good/neutral/bad} | {note or "—"} | {source} | {signal_type} | {weight} | {model_version} |
```

**Auto-created canvas**: Use the template from `/ingest-dm` with:
- `score_snapshot` from Phase 3 enrichment
- First feedback entry in the table
- Single skeleton hypothesis based on signal type
- Empty Quotes Library and Journey Fragments (no conversation data)

### Phase 7: Detect Gaps

Scan entries for potential GAP signals:
- `feedback_type == "bad"` with note → potential gap
- `signal_type == ACCURACY` → data gap
- `signal_type == WEIGHTINGS` → calibration gap
- Multiple entries with similar notes → pattern gap

For each detected gap, note in the synthesis report for operator review.

### Phase 8: Generate Synthesis Report

Write to `grimoires/observer/synthesis/feedback-{YYYY-MM-DD}.md`:

```markdown
---
type: feedback-synthesis
period: "{start_timestamp} to {end_timestamp}"
total_entries: {N}
signal_distribution:
  feel: {N}
  weightings: {N}
  accuracy: {N}
  ux: {N}
weight_distribution:
  high: {N}
  medium: {N}
  low: {N}
canvases_updated: {N}
canvases_created: {N}
gaps_detected: {N}
---

# Feedback Synthesis: {date}

## Summary

{N} new feedback entries processed since {last_run_date}.
{N} canvases updated, {N} new canvases created.

## High-Weight Signals

| Time | Wallet | User | Type | Note | Source | Signal | Weight |
|------|--------|------|------|------|--------|--------|--------|
| ... | ... | ... | ... | ... | ... | ... | HIGH |

## Signal Distribution

- FEEL: {N} ({%})
- WEIGHTINGS: {N} ({%})
- ACCURACY: {N} ({%})
- UX: {N} ({%})

## Routing Summary

### Score API Issues (ACCURACY + WEIGHTINGS)

| Signal | User | Note | Weight |
|--------|------|------|--------|
| ... | ... | ... | ... |

### App Issues (UX)

| Signal | User | Note | Weight |
|--------|------|------|--------|
| ... | ... | ... | ... |

## Gap Detection

| Type | Evidence | Source | Severity |
|------|----------|--------|----------|
| ... | ... | ... | ... |

## Canvas Updates

| Canvas | Action | Entries Added |
|--------|--------|---------------|
| {username}.md | updated | {N} |
| {newuser}.md | created | {N} |

## Observations

{Any notable patterns or anomalies detected during processing}
```

### Phase 8.5: MER Aggregation

Scan the MER timeline for snapshots created today and include a summary in the synthesis report.

**Step 1: Scan for today's MERs**

```bash
event_date=$(date -u +"%Y-%m-%d")

# Query INDEX.json for today's MERs
todays_mers=$(jq -r --arg date "$event_date" \
    '[.entries[] | select(.date == $date)]' \
    grimoires/observer/timeline/INDEX.json 2>/dev/null || echo "[]")

mer_count=$(echo "$todays_mers" | jq 'length')
```

**Step 2: Extract MER details**

For each MER in today's list, read the MER file to extract:
- `mer_id`, `wallet_alias`, `trigger`, `signal_weight`
- `combined_score`, `overall_rank`, `crowd_tier_display`
- Perception vs Reality gaps (if any)
- Screenshot URL (if visual layer present)

```bash
for mer_entry in $(echo "$todays_mers" | jq -c '.[]'); do
    mer_id=$(echo "$mer_entry" | jq -r '.id')
    mer_file="grimoires/observer/timeline/${mer_id}.md"
    if [[ -f "$mer_file" ]]; then
        # Parse frontmatter for data fields
        # Extract perception gaps from Perception vs Reality table
    fi
done
```

**Step 3: Include MER Summary in synthesis report**

If `mer_count > 0`, add a "MER Timeline" section to the synthesis report (after Gap Detection, before Observations):

```markdown
## MER Timeline

**{mer_count} MERs captured today**

| MER ID | Wallet | Trigger | Weight | Rank | Tier | Visual |
|--------|--------|---------|--------|------|------|--------|
| [[timeline/{mer_id}]] | {alias} | {trigger} | {weight} | #{rank} | {crowd_tier} | {yes/no} |

### Perception Gaps Flagged

| MER | Gap Type | Expected | Actual |
|-----|----------|----------|--------|
| {mer_id} | {gap_type} | {expected} | {actual} |
```

Perception gaps flagged in MERs should be surfaced for follow-up. These complement the Phase 7 gap detection (which scans feedback notes) with snapshot-level gaps (which compare user perception against data state).

**Step 4: Update affected canvases**

For each MER wallet that has a canvas, append a timeline cross-reference:

```markdown
## Linked Artifacts
...
- [[timeline/{mer_id}]] — {trigger} snapshot ({event_date})
```

If the canvas already has a link to this MER (idempotency), skip.

If `mer_count == 0`, skip this phase entirely.

### Phase 9: Emit FeedbackEvent

After generating the synthesis report, emit one aggregate FeedbackEvent via the Loa event bus.

**Phase 9a: Resolve synthesis target identity (if wallet-filtered)**

If the synthesis was run with `--wallet`, resolve identity for `data.subject`:

```bash
# Only for wallet-filtered runs
if [[ -n "$FILTER_WALLET" ]]; then
  resolution_json=$(scripts/observer/wallet-resolve.sh --json "$FILTER_WALLET" 2>/dev/null) || resolution_json='{"wallet":null,"confidence":"none","source":"none","username":null}'
fi
```

For unfiltered runs (all feedback), `data.subject` uses `resolution_status: "unresolved"` with `resolution_source: "none"` (aggregate event has no single subject).

**Phase 9b: Emit event with subject**

```bash
source .claude/scripts/lib/event-bus.sh

emit_event "observer.synthesis_completed" \
  '{
    "domain": "research",
    "target": {
      "type": "artifact",
      "selector": "grimoires/observer/synthesis/feedback-{YYYY-MM-DD}.md"
    },
    "signal": {
      "direction": "neutral",
      "weight": 0.6,
      "specificity": 0.2,
      "content": "{N} entries processed, {H} high-weight, {M} medium, {L} low",
      "kind": "feel"
    },
    "context": {
      "artifact_path": "grimoires/observer/synthesis/feedback-{YYYY-MM-DD}.md"
    },
    "subject": {
      "resolution_status": "{resolved if --wallet filter matched, else unresolved}",
      "resolution_source": "{from wallet-resolve.sh or none for aggregate}",
      "resolution_confidence": "{from wallet-resolve.sh or none for aggregate}",
      "wallet": "{0x... if resolved, omit otherwise}",
      "wallet_checksum": "{EIP-55 if resolved, omit otherwise}"
    }
  }' \
  "observer/daily-synthesis"
```

The bus auto-generates `id`, `time`, `specversion` in the CloudEvents envelope.

**Notes**:
- One event per synthesis run (aggregate, not per-entry)
- Direction is always `neutral` (synthesis is an aggregate summary)
- Weight is 0.6 (synthesized = higher confidence than individual signals)
- Specificity is 0.2 (broad report, not targeted at specific entity)
- `data.subject` is resolved only for `--wallet` filtered runs; unfiltered runs emit `resolution_status: "unresolved"`
- Skip in `--dry-run` mode (no side effects)

See `grimoires/shared/feedback/schema.md` for full schema reference.

### Phase 10: Update State

Update `grimoires/observer/synthesis/last-run.json`:
```json
{
  "last_processed_at": "{latest entry created_at}",
  "total_processed": {cumulative total},
  "last_run_date": "{now}"
}
```

Update `grimoires/observer/state.yaml`:
- `canvas_count`: Updated count
- `last_observation`: Now
- `feedback_synthesis.last_run`: Now
- `feedback_synthesis.total_entries_processed`: Updated total
- `feedback_synthesis.canvases_auto_created`: Updated count if any
- `feedback_synthesis.canvases_updated`: Updated count
- `feedback_synthesis.synthesis_reports`: Incremented

---

### Phase 11: Emit Agent Interaction Log

As the final step, append a JSONL line to `grimoires/observer/agent-logs/{YYYY-MM-DD}.jsonl`:

```json
{
  "ts": "{RFC 3339 UTC}",
  "pack": "observer",
  "skill": "daily-synthesis",
  "status": "{success | error}",
  "duration_ms": "{approximate wall-clock from skill start to end}",
  "artifacts_written": "{N: synthesis report + canvases updated/created}",
  "events_emitted": 1,
  "error": "{error message if status=error, omit if success}"
}
```

**Notes**:
- `duration_ms` is approximate (wall-clock estimate, not precise timer)
- `artifacts_written` = synthesis report + number of canvases updated/created
- `events_emitted` = 1 (the aggregate FeedbackEvent from Phase 9)
- Skip in `--dry-run` mode (no side effects)
- Create `grimoires/observer/agent-logs/` directory if it doesn't exist
- See `grimoires/shared/feedback/agent-log-format.md` for format reference

---

## Counterfactuals — Stale Data Propagation & Classification Edge Cases

The synthesis pipeline aggregates signals across users and time. Its failure modes are subtle: the output *looks* correct but encodes yesterday's truth as today's, or applies classification rules that break at tier boundaries.

### Target (Correct Behavior)

The pipeline reads `last_processed_at` from state, fetches only newer feedback entries, enriches each unique wallet via Score API (once per wallet, cached within the run), classifies signal weight from the *current* rank/tier data, and writes a synthesis report with accurate counts and distributions. The state file is updated atomically only after all writes succeed.

When Score API enrichment fails for a specific wallet, that wallet's entries are classified as MEDIUM weight (unknown position ≠ low position), and a note is added to the synthesis report. The pipeline continues with remaining wallets — one failure does not block the batch.

The state file update is the last operation — if any prior phase fails, `last_processed_at` is not advanced, ensuring the failed entries will be re-processed on the next run. This guarantees exactly-once processing under the assumption that the state write is atomic.

Event bus consumption (Phase 3.5) uses offset tracking for the same reason: consumed events advance the offset only after successful processing. A crash mid-synthesis leaves the offset at the pre-run position, causing re-consumption on retry. Events are idempotent (aggregation counts are recalculated, not accumulated), so re-consumption is safe.

### Near Miss — Concept Impermanence

The seductively wrong behavior: using `last_processed_at` as the freshness boundary for feedback entries but not checking whether the Score API data used for enrichment is also fresh.

Consider: the pipeline runs daily. A user was rank #50 yesterday (HIGH weight). Overnight, a score recalculation drops them to rank #250 (MEDIUM weight). The pipeline fetches today's feedback, but the Score API cache from yesterday's run still has rank #50. Result: today's feedback is classified HIGH when it should be MEDIUM.

The staleness compounds across dimensions:
- **Feedback timestamp**: controlled by `last_processed_at` — correct
- **Score API data**: controlled by cache TTL in `score-api-query.sh` — may be stale
- **Tier boundaries**: controlled by score-api recalculation schedule — external

The correct behavior: always fetch fresh Score API data during synthesis (the `--format snapshot` call is cheap). Never reuse cross-run cached scores for classification. The wrapper script's 1-hour cache TTL is appropriate for interactive use but dangerous for batch classification where weight thresholds determine routing priority.

### Category Error — Brittle Dependency

The fundamentally wrong behavior: treating signal weight classification thresholds as absolute rather than position-relative.

The classification rule says `rank <= 50 → HIGH`. But rank is a relative position in a population. When the population grows from 500 to 5000 users, rank #50 means something very different. The threshold was calibrated for the current population size — it is not a universal constant.

Similarly, `crowd_tier in ['eternal', 'godfather', 'all_night'] → HIGH` assumes tier labels are stable. If the score-api introduces a new tier above 'eternal', or renames tiers, the classification silently miscategorizes every user in the new tier as MEDIUM (the default fallback).

The synthesis skill should not hardcode tier names as classification inputs. It should either:
1. Query the score-api for tier ordering metadata, or
2. Use rank percentile (relative) instead of absolute rank, or
3. At minimum, log unknown tier values as warnings rather than silently defaulting

The current implementation works correctly for the *current* scoring model. The counterfactual is about recognizing which assumptions are load-bearing and which are incidental.

A concrete scenario demonstrating this brittleness: the score-api team decides to rename `all_night` tier to `dedicated` in model v0.12.0. The daily-synthesis classification rule checks `crowd_tier in ['eternal', 'godfather', 'all_night']`. Every user in the renamed tier silently falls through to MEDIUM weight. No error, no warning — the synthesis report looks normal but systematically underweights a significant user cohort.

The signal distribution in the report would shift: fewer HIGH-weight entries, more MEDIUM. The operator sees the shift but attributes it to changing user behavior rather than a classification bug. This is the insidious nature of Concept Impermanence — the concept (tier label) changed but the code's reference to it did not, and the failure is silent.

Defensive measures: the synthesis report should include a "Classification Coverage" metric showing what percentage of enriched wallets mapped to a known tier. A sudden drop in coverage signals that the tier vocabulary has drifted from the hardcoded list. Similarly, the weight distribution section should flag when MEDIUM becomes dominant — this may indicate classification fallthrough rather than a genuine shift in user population.

Both failure modes share a root cause: the synthesis pipeline treats its classification rules as static when they depend on external, evolving systems. The pipeline's correctness is coupled to the score-api's data model — and that coupling is invisible until the model changes.

---

## Dry Run Mode

When `--dry-run` is passed:
- Execute Phases 1-7 normally (read and classify)
- Phase 8: Print report to stdout instead of writing file
- Phase 9: Skip state updates
- Prefix output with `[DRY RUN]`
- Show what canvases would be created/updated without modifying them

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Supabase query fails | Report error, exit with non-zero. Don't update state. |
| Score API unavailable for a wallet | Skip enrichment for that wallet, classify as MEDIUM weight, add note |
| Canvas file locked or unwritable | Skip that canvas, log warning, continue with others |
| No new entries since last run | Report "No new feedback", exit 0 |
| Malformed feedback entry | Skip entry, log warning, continue |
| last-run.json missing | Default to 30 days ago, create state file |

---

## Integration Points

- **Depends on**: `scripts/observer/supabase-query.sh`, `scripts/observer/wallet-resolve.sh`, `scripts/observer/score-api-query.sh`
- **Builds on**: `/synthesize-feedback` patterns (same classification logic, same canvas format)
- **Feeds into**: `/shape` (enriched canvases), `/gap-to-issues` (detected gaps)
- **State files**: `grimoires/observer/synthesis/last-run.json`, `grimoires/observer/state.yaml`

---

## Validation

- [ ] Processes only entries newer than `last_processed_at`
- [ ] Each unique wallet enriched exactly once per run
- [ ] Weight classification matches PIPELINE.md thresholds
- [ ] Signal type regex matches PIPELINE.md patterns
- [ ] Existing canvases appended (not overwritten)
- [ ] New canvases created with valid YAML frontmatter
- [ ] Synthesis report has accurate counts
- [ ] State files updated atomically (all or nothing)
- [ ] `--dry-run` produces no side effects
- [ ] `--since` overrides last_processed_at correctly

---

## Temporal Claim Enforcement (G-4)

**Rules for any downstream skill or agent referencing provenance data from this ingestion:**

1. **Cite provenance**: When making temporal claims about user feedback (e.g., "user said X after release Y"), you MUST cite the provenance `record_id` and verify `source_timestamp_confidence` is `exact`.

2. **Version attribution requires proof**: Attributing feedback to a specific version (e.g., "user was upset after v0.2.0") requires:
   - `source_timestamp_confidence` = `exact`
   - `feedback_timestamp ∈ [release_timestamp, next_release_timestamp)`
   - Both timestamps from authoritative sources (provenance index + chronicle)

3. **Hedging for low confidence**: If `source_timestamp_confidence` is `unknown` or `inferred`, temporal claims MUST be hedged ("around this time" / "date uncertain") and MUST NOT be used for version attribution.

4. **Raw timestamp preservation**: `--timestamp-raw` MUST be passed to gate.sh to preserve the verbatim timestamp string from the source material. This enables audit of parse correctness.

---

## Related

- `/synthesize-feedback` — Original manual synthesis skill (same patterns)
- `/ingest-dm` — DM import (complements daily UI feedback)
- `/gap-to-issues` — Batch file detected gaps as GitHub issues
- `/follow-up` — Generate follow-up messages from canvas data
