---
name: ingesting-dms
description: Single-user conversation import that creates an enriched canvas scaffold from a DM export.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash
---

# Ingesting DMs

Import a Discord DM conversation export for a single user, resolve their wallet, pull their Score API profile, and produce an enriched User Truth Canvas with pre-populated quotes, skeleton hypotheses, and journey fragments.

This skill replaces ~10 manual steps with a single invocation. The operator refines hypotheses to Level 3 after the skill completes.

---

## Core Principle

**One quote = one data point. Hypothesize, don't conclude.** Every extracted hypothesis starts at confidence: Low unless multiple independent signals corroborate it. The canvas is a scaffold — human refinement is the final step.

---

## Triggers

```
/ingest-dm <path-to-csv-or-text>
/ingest-dm <path> --username <name>
/ingest-dm <path> --wallet <address>
/ingest-dm <path> --username <name> --wallet <address>
```

**Examples:**
```
/ingest-dm grimoires/observer/imports/xabbu-discord-export.csv
/ingest-dm grimoires/observer/imports/newuser.txt --username "NewUser" --wallet 0xabc...
/ingest-dm grimoires/observer/imports/batch/user3.csv --username "user3"
```

**Arguments:**
- `<path>`: Path to CSV export or pasted text file (required)
- `--username <name>`: Override extracted username (optional — auto-detected from conversation)
- `--wallet <address>`: Provide wallet directly (optional — resolved via wallet-resolve.sh)
- `--responds-to <message-id>`: Tag this DM as a response to a specific follow-up message (optional — for growth loop outcome tracking)
- `--signal-quality <high|medium|low>`: Rate the quality of information in this response (optional — requires `--responds-to`)

---

## When to Use

- A new beta user has shared feedback via Discord DM
- You have a conversation export (CSV or text) ready to import
- You want to create an enriched canvas for a user who doesn't have one yet
- You're processing a batch of DM exports (use `/batch-observe` for parallel processing)

---

## Workflow

### Step 0.5: Load Domain Glossary

Before interpreting any user quotes extracted from the DM conversation:

1. Read `grimoires/observer/glossary.yaml`
2. For each quote being annotated, check if any glossary term appears in the text (case-insensitive match on the `term` field)
3. If a match is found:
   - Use the `meaning` field as the canonical interpretation
   - Note the `not` field to explicitly avoid the common misinterpretation
   - Include `[glossary: {term}]` annotation in the hypothesis
4. If glossary file does not exist, proceed without — log a warning to the operator

---

### Step 1: Parse Input

Read the input file. Detect format:

**If CSV** — detect format by headers:

| Platform | Key Headers | Speaker Field | Text Field | Time Field |
|----------|-------------|--------------|------------|------------|
| Discord | `AuthorID`, `Content`, `Timestamp` | `Author` | `Content` | `Timestamp` |
| Twitter/X | `sender_screen_name`, `text`, `time` | `sender_screen_name` | `text` | `time` |
| Telegram | `from`, `text`, `date` | `from` | `text` | `date` |

**IMPORTANT**: Use Python `csv.DictReader` for all CSV parsing — never raw `cut`/`awk`. CSV fields contain embedded commas, quotes, and JSON blobs (Twitter reactions as `{"1":{"type":"STRUCT",...}}`). Filter these noise rows:
- Skip rows where `text` starts with `{"1":{"type":"STRUCT"` (Twitter reaction metadata)
- Deduplicate by `(time, sender, text[:50])` tuple
- Sort chronologically by timestamp

```python
python3 -c "
import csv, sys
with open(sys.argv[1], 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        text = row.get('text') or row.get('Content') or ''
        if text.startswith('{\"1\":{\"type\":\"STRUCT\"'): continue
        sender = row.get('sender_screen_name') or row.get('Author') or row.get('from') or ''
        time = row.get('time') or row.get('Timestamp') or row.get('date') or ''
        print(f'[{time}] @{sender}: {text}')
" "$input_file"
```

**If plain text** (pasted conversation):
- Parse line-by-line looking for `username:` or timestamp patterns
- Extract quoted messages
- Infer conversation flow from ordering

### Step 2: Extract Username

**If `--username` provided:** Use it directly.

**Otherwise:** Extract from conversation data:
- CSV: Use the non-operator `Author` field
- Text: Use the most frequent speaker name

Normalize username: lowercase, strip special characters.

### Step 3: Resolve Wallet

**If `--wallet` provided:** Use it directly.

**Otherwise:** Run wallet resolution:
```bash
scripts/observer/wallet-resolve.sh <username>
```

**If wallet found:** Proceed to enrichment.
**If "not found":** Create canvas without Score API data. Add note:
```
> Score API enrichment unavailable — wallet not resolved.
> Run: /observe --enrich @{username} --wallet 0x... when wallet is known.
```

### Step 4: Pull Score API Profile

**If wallet available:**
```bash
scripts/observer/score-api-query.sh profile <wallet> --format snapshot
```

This returns canvas-ready `score_snapshot` YAML from 4 views:
- `mv_wallet_profiles` — scores, breadth, trust
- `mv_wallet_tiers` — combined score, rank, tiers
- `mv_dimension_leaderboard` — per-dimension ranks
- `mv_wallet_badge_summary` — badge count

**On failure:** Set `score_snapshot: null` in frontmatter. Never block canvas creation.

### Step 4.5: Provenance Gate — Dedup & Hash Each Message

**Before** appending any quote to the canvas, pipe each extracted message through the provenance gate. This ensures every ingested item is content-hashed, deduplicated, and timestamp-tracked.

**For each extracted message:**

```bash
# Pipe message content via stdin. gate.sh normalizes and deduplicates.
echo -n "$message_text" | scripts/provenance/gate.sh \
  --source-type discord_dm \
  --timestamp "$parsed_utc_timestamp" \
  --timestamp-raw "$verbatim_timestamp_string" \
  --confidence exact \
  --canvas-target "$username" \
  --raw-source-ref "$input_file_path" \
  --ingested-by ingest-dm \
  --thread-id "thread-discord-${username}-${export_date}" \
  --message-index "$zero_indexed_position" \
  --parent-hash "$previous_message_content_hash" \
  --json
```

**Exit code handling:**
| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 (INGEST) | New content — add to canvas | Capture `content_hash` from JSON output for event emission |
| 1 (SKIP) | Duplicate — already ingested | Skip this message, increment skip counter |
| 2 (ERROR) | Input error | Halt and report error |
| 3 (LOCK_FAILED) | Lock contention | Retry once after 2s, halt if still fails |
| 4 (DEPENDENCY) | Missing tool | Halt — operator must install missing dependency |

**Discord timestamp parsing:**
- Discord format: `MM/DD/YY, HH:MM PM` → parse to UTC RFC 3339 (`2026-02-11T14:23:00Z`)
- Preserve verbatim string in `--timestamp-raw` (e.g., `"02/11/26, 2:23 PM"`)
- All Discord timestamps get `--confidence exact` (Discord provides authoritative timestamps)

**Telegram timestamp parsing:**
- Telegram format: `[HH:MM]` or `YYYY-MM-DD HH:MM` → parse to UTC
- If only time available (no date): use export date + time, `--confidence day_level`

**Thread context:**
- `--thread-id`: `thread-discord-{username}-{export_date}` (e.g., `thread-discord-papa-flavio-2026-02-11`)
- `--message-index`: 0-indexed position in the exported conversation
- `--parent-hash`: `content_hash` of the previous message (null for first message)

**After processing all messages, report:**
```
Provenance: Ingested {N} new messages, skipped {M} duplicates
```

Only messages with exit code 0 (INGEST) proceed to canvas creation in Step 5.

---

### Step 5: Create Enriched Canvas

Write canvas to `grimoires/observer/canvas/{username}-canvas.md` using the template below.

**Auto-populate from conversation:**

1. **Quotes Library**: Extract direct quotes from user messages. Prioritize:
   - Messages with emotional language (FEEL signals)
   - Messages mentioning scores, dimensions, rankings (WEIGHTINGS signals)
   - Messages reporting data issues (ACCURACY signals)
   - Messages about UI/navigation (UX signals)

2. **Skeleton Hypotheses**: Generate 2-4 hypotheses from conversation signals:
   - Pattern: `H{n}: {User} may {behavior/belief} because {evidence from quote}`
   - All start at `confidence: Low` (single conversation = single data source)
   - Tag with signal type: FEEL / WEIGHTINGS / ACCURACY / UX

3. **Journey Fragments**: Extract temporal sequence from conversation:
   - First interaction timestamp
   - Key moments (shared profile, asked question, reported issue, expressed emotion)
   - Conversation arc (discovery → engagement → feedback → resolution)

4. **Future Promises**: Detect promise language:
   - "I'll check...", "Let me try...", "I want to..."
   - "Can you show me...", "I'd like to see..."
   - Track as unredeemed promises for follow-up

---

## Counterfactuals — DM Format Parsing & Research Boundary

DM ingestion converts unstructured conversation exports into structured canvases. The failure modes sit at two levels: mechanical (parsing breaks) and epistemological (wrong framework applied to the data).

### Target (Correct Behavior)

The skill accepts a pasted DM transcript, identifies speaker turns by username prefix and timestamp patterns, extracts quotes attributed to the correct speaker, and builds a canvas with Level 3 hypotheses derived from the user's statements (not the operator's). Promise language is detected and tracked. The conversation arc is mapped as a journey fragment with trigger → action → expected → actual → emotion.

Timestamps are parsed tolerantly — the skill handles Discord format (`username — MM/DD/YY, HH:MM PM`), Telegram format (`[HH:MM]`), Twitter/X DM format, and bare text with no timestamps. When format detection fails, the skill falls back to sequential ordering without timestamps rather than misattributing turns.

### Near Miss — Coupling Inversion

The seductively wrong behavior: assuming consistent timestamp format within a single DM export.

Real DM exports contain format discontinuities:
- A user copies messages from Discord but includes a forwarded Telegram message within the conversation
- Timestamps switch from 12-hour to 24-hour format mid-conversation (timezone change, device switch)
- Some messages have dates, others only times (same-day vs. cross-day within the export)
- Edited messages may show both original and edit timestamps

A rigid parser that locks onto the first detected format will misparse subsequent messages, potentially:
- Merging two speaker turns into one (missed turn boundary)
- Attributing a quote to the wrong speaker (shifted alignment)
- Dropping messages entirely (unparseable format treated as noise)

The correct behavior: parse each line independently. Detect speaker turns by the username prefix pattern, not by timestamp format. Use timestamps for ordering when available, but fall back to document order. Never silently drop a line — if it can't be parsed as a new turn, append it to the previous speaker's turn as continuation.

### Category Error — Brittle Dependency

The fundamentally wrong behavior: applying Level 3 diagnostic framework to casual DM conversation as if it were a user research interview.

Level 3 analysis assumes the user is responding to questions about their goals, pain points, and workflows. A DM conversation is different:
- The user initiates (not responding to structured prompts)
- Topics shift organically (no interview guide)
- Social pleasantries are noise, not signal ("henlo" is greeting, not data)
- The operator's messages shape the user's responses (leading questions are common in casual chat)

Treating "that looks slick" as a validated usability signal, or "I thought I was active on cubquests" as a feature request, collapses the distinction between conversational reaction and considered feedback. The Mom Test framework specifically warns against this: compliments in conversation are not validation.

The correct approach: DM ingestion creates a *canvas scaffold* — hypotheses at LOW confidence with explicit "Unknown" gaps. The canvas is raw material for follow-up, not a finished research artifact. Journey fragments from DMs should be marked `source: dm-import` to distinguish them from structured observation data.

Concrete examples from this ecosystem:

- User says "looks slick" about the profile page → this is a social pleasantry, not usability validation. The Mom Test says: compliments are worthless data. Do not record this as "positive UX signal."
- User says "I thought I was active on cubquests" → this is a genuine expectation gap, but the Level 3 goal is unknown. Are they checking their score accuracy? Comparing against friends? Deciding whether to engage more? The DM doesn't tell us — flag as hypothesis, not conclusion.
- User asks "so it ranks the miberas?" → this is a comprehension question. It tells us the value proposition wasn't immediately clear from the interface. But it does not tell us whether that matters to this user's goals.

Each of these requires a different follow-up strategy. Treating them all as "user feedback" at the same confidence level collapses the signal hierarchy that makes canvases useful. The scaffold should explicitly mark which quotes are pleasantries (LOW value), which are expectation gaps (MEDIUM value, needs follow-up), and which reveal goal-level intent (HIGH value, hypothesis-worthy).

The `/follow-up` skill downstream depends on this classification to generate anchored conversation frameworks. If every DM quote is treated as equal evidence, the follow-up messages will anchor on pleasantries instead of the moments that actually reveal user intent.

---

### Step 5.5: Wire Obsidian Links

After writing the canvas file, wire it into the knowledge graph if it belongs to any journey:

```bash
source scripts/observer/golden-path-lib.sh
wire_canvas_links "grimoires/observer/canvas/{username}-canvas.md"
```

This injects `<!-- midi:journey-links -->` sentinel with Journeys and Related Canvases sections if the canvas appears in any journey's `source_canvases`. If the canvas is not in any journey, this is a silent no-op.

### Step 6: Update State

Update `grimoires/observer/state.yaml`:
- Increment `canvas_count` if new canvas
- Update `last_observation` timestamp

### Step 7: Emit FeedbackEvent

After canvas creation/update, resolve the user's wallet and emit a FeedbackEvent via the Loa event bus:

**Step 7a: Resolve wallet identity**

```bash
# Resolve wallet for data.subject enrichment
resolution_json=$(scripts/observer/wallet-resolve.sh --json "{username}" 2>/dev/null) || resolution_json='{"wallet":null,"confidence":"none","source":"none","username":null}'
```

Parse `resolution_json` to build `data.subject` (same rules as `/observe` Step 8a).

**Step 7b: Emit event with subject**

```bash
source .claude/scripts/lib/event-bus.sh

emit_event "observer.feedback_captured" \
  '{
    "domain": "research",
    "target": { "type": "user", "selector": "user:{username}" },
    "signal": {
      "direction": "{inferred from conversation sentiment: positive/negative/neutral}",
      "weight": {derived from user tier: high=0.8, medium=0.5, low=0.2},
      "specificity": 0.3,
      "content": "DM import: {N} quotes extracted, {M} hypotheses generated from conversation",
      "kind": "{dominant signal type from extracted quotes: feel | calibration | accuracy | ux}",
      "fingerprint": "{content_hash from gate.sh --json output}",
      "normalization_version": 1
    },
    "context": {
      "user_id": "{salted hash per redaction-guide.md, or omit if unavailable}",
      "user_tier": "{high | medium | low — derived from rank}",
      "artifact_path": "grimoires/observer/canvas/{username}-canvas.md"
    },
    "subject": {
      "resolution_status": "{resolved | unresolved}",
      "resolution_source": "{alias | username | leaderboard | supabase | direct | none}",
      "resolution_confidence": "{high | medium | ambiguous | none}",
      "wallet": "{0x... or omit if unresolved}",
      "wallet_checksum": "{EIP-55 checksum or omit if unresolved}"
    }
  }' \
  "observer/ingesting-dms" \
  "" "" \
  "user:{username}"
```

The bus auto-generates `id`, `time`, `specversion` in the CloudEvents envelope. The data payload follows `grimoires/shared/feedback/schema.json`.

**Weight derivation**: Same as `/observe` — use `score_snapshot` rank/tier if available, default to `medium` (0.5).

**Direction inference**: Derive from overall conversation sentiment:
- Mostly positive quotes (engaged, satisfied) → `positive`
- Mostly negative quotes (frustrated, confused, reporting issues) → `negative`
- Mixed or informational → `neutral`

See `grimoires/shared/feedback/schema.md` for full schema reference.
See `grimoires/shared/feedback/redaction-guide.md` for hashing and redaction rules.

### Step 8: Report Output

Display summary:
```
Canvas created: grimoires/observer/canvas/{username}-canvas.md
FeedbackEvent emitted: observer.feedback_captured (via Loa event bus)
  Score: Rank #{rank} | {crowd_tier}/{elite_tier} | {og}/{nft}/{onchain}
  Quotes extracted: {N}
  Hypotheses generated: {N} (all Low confidence — refine to Level 3)
  Journey fragments: {N}
  Future promises: {N}

Next steps:
  1. Review and refine hypotheses to Level 3 depth
  2. Run /level-3-diagnostic for diagnostic questioning
  3. Add context from other signal sources
```

---

## Canvas Template

```yaml
---
type: user_canvas
user: {username}
wallet: "{wallet_address}"
score_snapshot:
  captured_at: "{ISO timestamp}"
  wallet: "{wallet_address}"
  rank: {N}                          # from mv_wallet_tiers.overall_rank
  combined_score: {N}                # from mv_wallet_tiers.combined_score
  og_score: {N}                      # from mv_wallet_profiles
  nft_score: {N}
  onchain_score: {N}
  og_rank: {N}                       # from mv_dimension_leaderboard
  nft_rank: {N}
  onchain_rank: {N}
  trust_filter: {N}                  # from mv_wallet_profiles
  trust_classification: "{normal|banned_robotic|banned_cluster|flagged_single_factor|flagged_burst}"
  og_breadth: {N}
  nft_breadth: {N}
  onchain_breadth: {N}
  crowd_tier: "{tier}"               # from mv_wallet_tiers
  elite_tier: "{tier or null}"
  total_badges: {N}                  # from mv_wallet_badge_summary.badge_count
  model_version: "v0.11.0"
hivemind:
  artifact: user_truth_canvas
  workstream: discovery
  product: []                        # e.g. [user_profile, wallet_integration, user_reactivation]
  jtbd: []                           # e.g. [help_me_feel_smart, find_information, feel_connected_again]
  source: "{twitter_dm|discord_dm|supabase_feedback}"
  learning_status: directionally_correct
created: "{date}"
updated: "{date}"
linked_journeys: []
linked_observations: []
confidence:
  created_at: "{date}"
  last_validated_at: "{date}"
  last_validated_commit: ""
  validation_count: 0
  related_paths:
    - "lib/score-api/**"
    - "grimoires/observer/canvas/"
schema_version: 2
lifecycle_state: "{new_user|reactivating|power_user|churning}"
last_enriched: "{ISO timestamp}"
enrichment_trigger: ingest-dm
chronicle_refs: []
---

# {Username} Canvas

## User Profile

| Field | Value |
|-------|-------|
| **Signals Observed** | {behavioral signals extracted from conversation} |
| **Theories** | {possible interpretations — NOT conclusions} |
| **Confidence** | **{Low|Medium}** ({reason}) |
| **Unknown** | {what we cannot determine from this conversation} |
| **Stakes** | {what they have invested, engagement history} |

---

## Score Context

| Field | Value |
|-------|-------|
| **Wallet** | `{wallet_address}` |
| **Rank** | **#{rank}** |
| **Combined Score** | **{combined_score}** |
| **OG** | {og_score} / rank #{og_rank} / breadth {og_breadth} |
| **NFT** | {nft_score} / rank #{nft_rank} / breadth {nft_breadth} |
| **Onchain** | {onchain_score} / rank #{onchain_rank} / breadth {onchain_breadth} |
| **Trust** | {trust_filter} ({trust_classification}) |
| **Crowd Tier** | **{crowd_tier}** |
| **Elite Tier** | {elite_tier or None} |
| **Badges** | {total_badges} earned |
| **Signal Weight** | **{HIGH|MEDIUM|LOW}** ({crowd_tier} tier, rank #{rank}) |
| **Model Version** | {model_version} |
| **Captured At** | {date} |

> **Enrichment insight**: {analysis of dimension imbalances, breadth patterns, activity gaps}

## Level 3 Hypotheses

> Skeleton hypotheses from DM import. Refine to Level 3 depth.

### Hypothesis 1: {hypothesis_title}
<!-- hivemind:product:UNTAGGED -->

- **Quote anchor**: "{exact words that led to this theory}"
- **Context**: {surrounding context and behavioral evidence}
- **Alternative interpretations**: {other valid readings}
- **Confidence**: Low (single DM conversation)
- **What would validate**: {observable behavior or statement that confirms}
- **What would invalidate**: {observable behavior or statement that disproves}
- **Design implication**: {what this means for the product if true}

### Hypothesis 2: {hypothesis_title}
<!-- hivemind:product:UNTAGGED -->

- **Quote anchor**: "..."
- **Context**: ...
- **Alternative interpretations**: ...
- **Confidence**: Low
- **What would validate**: ...
- **What would invalidate**: ...

---

## Future Promises (Unvalidated)

| Promise | Date | Follow-up Trigger | Status |
|---------|------|-------------------|--------|
| "{promise language from conversation}" | {ISO date} | {condition for follow-up} | **PENDING** |

---

## Journey Fragments

| Trigger | Action | Expected | Actual | Emotion |
|---------|--------|----------|--------|---------|
| {what initiated} | {what user did} | {what they expected} | {what actually happened} | {emotional response} |

---

## Expectation Gaps (Code-Grounded)

*No code-grounded gaps identified yet — first session was {exploratory|bug-reporting|etc}. Gaps may emerge when {user} engages with {specific features}.*

---

## Conversation Frameworks

{Priority context for next conversation}

**If they mention [{topic from conversation}]:**
- Opener: "{anchored to their exact words}"
- Dig deeper: "{follow-up that reveals Level 3 goal}"
- Watch for: {specific behavioral signals}

**Red flags to listen for:**
- {specific to this user's pattern}

---

## Quotes Library

> "{exact user quote}"
> — {Platform} DM, {ISO date}

> "{another quote}"
> — {Platform} DM, {ISO date}

---

## Linked Artifacts

### Journeys
*None yet — will link when cross-user patterns emerge*

### Related Canvases
*Potential links: {users with similar patterns}*

---

## Feedback Entries (from UI)

| Time (UTC) | Type | Source | Page Context | Note | Signal | Weight |
|------------|------|--------|-------------|------|--------|--------|

*No UI feedback entries yet. Will be populated by /daily-synthesis.*
```

---

### Step 8.5: Record Growth Outcome (if --responds-to provided)

**If `--responds-to` flag is present**, record the response outcome in the user's growth state.
**If `--responds-to` is NOT provided**, skip this step entirely — existing behavior unchanged.

```bash
source scripts/observer/growth-state.sh

responds_to="{message-id from --responds-to flag}"
signal_quality="{value from --signal-quality flag, or null}"
user="{username}"

# Input validation — prevent yq expression injection via crafted message IDs
if [[ ! "$responds_to" =~ ^fu-[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9_-]+-[0-9]+-[0-9]+$ ]]; then
  echo "ERROR: Invalid message ID format: $responds_to"
  echo "Expected: fu-YYYY-MM-DD-username-batchseq-msgnum"
  # Continue with normal DM ingestion (do NOT halt)
  exit 0  # or skip to next step
fi

if [[ -n "$signal_quality" ]] && [[ ! "$signal_quality" =~ ^(high|medium|low)$ ]]; then
  echo "WARNING: Invalid signal_quality '$signal_quality' — ignoring"
  signal_quality=""
fi

# Check growth state exists
if ! growth_exists "$user"; then
  echo "WARNING: No growth state for $user — skipping outcome recording"
  # Continue with normal DM ingestion (do NOT halt)
else
  # Read growth state under flock
  lock_path="$(growth_lock_path "$user")"
  _ensure_flock
  exec 201>"$lock_path"
  "$_FLOCK" -x -w 10 201

  content="$(growth_read "$user")"

  # Find message and record outcome
  # Complete transition table:
  #   pending  → responded: increment responded_count
  #   silence  → responded: decrement silence_count, increment responded_count, set late_response=true
  #   unknown  → responded: decrement unknown_count, increment responded_count
  #   responded → responded: no-op (idempotent, log warning)
  #   missing  → error logged, ingestion continues

  previous_outcome=$(echo "$content" | yq -r --arg mid "$responds_to" '
    .follow_ups[].message_ids[] | select(.id == $mid) | .outcome
  ' | head -1)

  if [ -z "$previous_outcome" ] || [ "$previous_outcome" = "null" ]; then
    echo "ERROR: Message ID $responds_to not found in growth state for $user"
    exec 201>&-
    # Continue with normal DM ingestion
  elif [ "$previous_outcome" = "responded" ]; then
    echo "WARNING: Message $responds_to already responded — no-op"
    exec 201>&-
  else
    now_ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
    late_response="false"
    if [ "$previous_outcome" = "silence" ]; then
      late_response="true"
    fi

    # Update message outcome via yq (--arg binding prevents injection)
    content=$(echo "$content" | yq --arg mid "$responds_to" --arg ts "$now_ts" --arg sq "$signal_quality" --arg lr "$late_response" '
      (.follow_ups[].message_ids[] | select(.id == $mid)) .outcome = "responded" |
      (.follow_ups[].message_ids[] | select(.id == $mid)) .outcome_at = $ts |
      (.follow_ups[].message_ids[] | select(.id == $mid)) .response_date = $ts |
      (.follow_ups[].message_ids[] | select(.id == $mid)) .signal_quality = $sq |
      (.follow_ups[].message_ids[] | select(.id == $mid)) .late_response = ($lr == "true")
    ')

    # Update pattern counters (transition-safe)
    pattern=$(echo "$content" | yq -r --arg mid "$responds_to" '
      .follow_ups[].message_ids[] | select(.id == $mid) | .question_pattern
    ' | head -1)

    # Validate pattern against known allowlist (defense-in-depth against yq injection)
    allowed_patterns="probe_gap verify_action challenge_assumption explore_motivation surface_unspoken test_commitment follow_breadcrumb"
    pattern_valid="false"
    if [ -n "$pattern" ] && [ "$pattern" != "null" ]; then
      for allowed in $allowed_patterns; do
        if [ "$pattern" = "$allowed" ]; then pattern_valid="true"; break; fi
      done
    fi

    if [ "$pattern_valid" = "true" ]; then
      # Decrement old bucket
      case "$previous_outcome" in
        silence) content=$(echo "$content" | yq --arg p "$pattern" '.question_patterns[$p].silence_count -= 1') ;;
        unknown) content=$(echo "$content" | yq --arg p "$pattern" '.question_patterns[$p].unknown_count -= 1') ;;
        pending) ;; # pending has no counter bucket
      esac

      # Increment responded_count
      content=$(echo "$content" | yq --arg p "$pattern" '.question_patterns[$p].responded_count += 1')

      # Update signal quality accumulators
      sq_numeric=""
      case "$signal_quality" in
        high) sq_numeric="1.0" ;;
        medium) sq_numeric="0.5" ;;
        low) sq_numeric="0.0" ;;
      esac

      if [ -n "$sq_numeric" ]; then
        content=$(echo "$content" | yq --arg p "$pattern" --arg sq "$sq_numeric" '
          .question_patterns[$p].signal_quality_sum += ($sq | tonumber) |
          .question_patterns[$p].signal_quality_count += 1
        ')
      fi

      # Recompute derived metrics (response_rate, avg_signal_quality, effectiveness_score)
      source scripts/observer/growth-state.sh
      content=$(_recompute_pattern_metrics "$content" "$pattern")
    fi

    # Update hypothesis evidence (reset decay)
    hypothesis_ref=$(echo "$content" | yq -r --arg mid "$responds_to" '
      .follow_ups[].message_ids[] | select(.id == $mid) | .hypothesis
    ' | head -1)

    # Extract hypothesis ID (e.g., "H1" from "H1: title" or "Hypothesis H1: title")
    h_id=$(echo "$hypothesis_ref" | grep -oE 'H[0-9_]+' | head -1)
    if [ -n "$h_id" ]; then
      content=$(echo "$content" | yq --arg hid "$h_id" --arg ts "$now_ts" '
        (.hypotheses[] | select(.id == $hid)).cycles_without_evidence = 0 |
        (.hypotheses[] | select(.id == $hid)).decay_state = "active" |
        (.hypotheses[] | select(.id == $hid)).last_evidence_date = $ts
      ')
    fi

    content=$(echo "$content" | yq --arg ts "$now_ts" '.last_updated = $ts')

    # Write updated growth state (atomic, under lock)
    growth_write "$user" "$content"
    exec 201>&-

    echo "Growth outcome recorded: $responds_to → responded (was: $previous_outcome)"
    if [ "$late_response" = "true" ]; then
      echo "  Late response: silence → responded"
    fi
    if [ -n "$sq_numeric" ]; then
      echo "  Signal quality: $signal_quality ($sq_numeric)"
    fi
  fi
fi
```

**If `--responds-to` is NOT provided:** This entire step is skipped. The DM is ingested normally via Steps 1-8 without any growth state interaction.

---

### Step 9: Emit Agent Interaction Log

As the final step, append a JSONL line to `grimoires/observer/agent-logs/{YYYY-MM-DD}.jsonl`:

```json
{
  "ts": "{RFC 3339 UTC}",
  "pack": "observer",
  "skill": "ingesting-dms",
  "status": "{success | error}",
  "duration_ms": "{approximate wall-clock from skill start to end}",
  "artifacts_written": 1,
  "events_emitted": 1,
  "error": "{error message if status=error, omit if success}"
}
```

**Notes**:
- `duration_ms` is approximate (wall-clock estimate, not precise timer)
- `artifacts_written` = canvas files created/updated
- `events_emitted` = FeedbackEvents emitted
- Create `grimoires/observer/agent-logs/` directory if it doesn't exist
- See `grimoires/shared/feedback/agent-log-format.md` for format reference

---

## Signal Detection Patterns

| Signal Type | Regex Pattern | Example |
|-------------|---------------|---------|
| FEEL | Emotional language, bare reactions | "this is cool", "love it", "feels off" |
| WEIGHTINGS | `/dimension\|factor\|weight\|score.*should\|too (high\|low)/i` | "OG should matter more" |
| ACCURACY | `/missing\|wrong\|didn't\|transaction\|minted\|count\|data/i` | "I minted 3 but shows 2" |
| UX | `/can't find\|confus\|button\|page\|navigate\|broken\|UI\|UX/i` | "Can't find settings" |

## Promise Detection Patterns

| Pattern | Type |
|---------|------|
| "I'll...", "I want to...", "Let me..." | User intent |
| "Can you show me...", "I'd like to see..." | Feature request |
| "I need to check...", "Going to try..." | Deferred action |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Input file not found | Error with path suggestion |
| No messages from user in CSV | Error — operator may have wrong export |
| Wallet not resolved | Create canvas without Score API data, add enrichment note |
| Score API query fails | Create canvas with `score_snapshot: null`, add note |
| Canvas already exists for user | Append new quotes to existing canvas instead of overwriting |
| Username collision | Prompt operator to provide `--username` override |

---

## Integration Points

- **Depends on**: `scripts/observer/wallet-resolve.sh`, `scripts/observer/score-api-query.sh`
- **Feeds into**: `/level-3-diagnostic` (hypothesis refinement), `/shape` (journey synthesis)
- **Updated by**: `/daily-synthesis` (appends UI feedback entries)
- **Parallel via**: `/batch-observe` (multi-user processing)

---

## Validation

- [ ] Canvas created at correct path
- [ ] YAML frontmatter parses cleanly
- [ ] score_snapshot matches live Score API data (or is null with note)
- [ ] At least 1 quote extracted from conversation
- [ ] At least 1 hypothesis generated (confidence: Low)
- [ ] state.yaml updated
- [ ] No wallet addresses in filenames (use username)
- [ ] Existing canvas not overwritten (append mode)

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

- `/observe` — Manual single-quote observation
- `/import-research` — Bulk legacy profile conversion
- `/level-3-diagnostic` — Hypothesis refinement after canvas creation
- `/batch-observe` — Parallel multi-user processing
- `/daily-synthesis` — Automated feedback pipeline
