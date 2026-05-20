---
name: observing-users
description: Capture user feedback as hypothesis-first research using Level 3 diagnostic. Forms theories (not conclusions) from quotes.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit
---

# Observing Users

Capture user feedback as structured diagnostic observations using the Level 3 framework. Create or update individual user research canvases from feedback quotes.

---

## Core Principle

**Hypothesize, don't conclude.**

One quote = one data point. Never:
- Classify users into "types" from usernames or single quotes
- Claim to know their Level 3 goal (form hypotheses instead)
- Treat future promises as commitments

Always:
- Flag confidence levels explicitly
- Note what we DON'T know
- Generate frameworks for deeper conversation, not assumptions

---

## Triggers

```
/observe @{username} "{quote}"
/observe @{username} "{quote}" --context "{source}"
/observe @{username} "{quote}" --wallet 0x...
/observe @{username} "{quote}" --wallet 0x... --context "{source}"
/observe --enrich @{username} --wallet 0x...
```

**Examples:**
```bash
/observe @papa-flavio "planning henlo burns"
/observe @tchallason "realtime harvesting counter" --context "Discord #feedback"
/observe @xabbu "og score feels low" --wallet 0xabc123...
/observe --enrich @xabbu --wallet 0xabc123...
```

**Flags:**
- `--wallet 0x...` — Provide wallet address for Score API enrichment. Persisted in canvas frontmatter for future use.
- `--enrich` — Retroactive enrichment mode. Loads existing canvas, runs Score API enrichment only (no new quote, no Level 3 diagnostic). Requires existing canvas.

---

## The Three Levels

| Level | Question | Example | Value |
|-------|----------|---------|-------|
| **Level 1** | What did they say? | "Rewards aren't updating" | Surface symptom |
| **Level 2** | What do they want? | "I want to see my rewards" | Stated desire |
| **Level 3** | What are they trying to accomplish? | "Decide when to burn based on accumulation" | Actionable truth |

**Always dig to Level 3.** Level 1-2 lead to building the wrong thing.

---

## When to Use

- User reports an issue or request
- Feedback appears in Discord/Telegram/support channels
- You notice behavioral patterns worth investigating
- Before building features based on user requests

---

## Workflow

### Step 0.5: Load Domain Glossary

Before interpreting any user quotes:

1. Read `grimoires/observer/glossary.yaml`
2. For each quote being annotated, check if any glossary term appears in the text (case-insensitive match on the `term` field)
3. If a match is found:
   - Use the `meaning` field as the canonical interpretation
   - Note the `not` field to explicitly avoid the common misinterpretation
   - Include `[glossary: {term}]` annotation in the hypothesis
4. If glossary file does not exist, proceed without — log a warning to the operator

---

### Step 1: Parse Arguments

Extract from command:
- `username`: Target user (required)
- `quote`: Exact user quote (required)
- `context`: Source/channel (optional, default: "direct feedback")

### Step 2: Load or Create Canvas

Check if canvas exists:
```bash
grimoires/observer/canvas/{username}-canvas.md
```

**If exists**: Read current canvas, prepare to append
**If not exists**: Create new canvas with template

### Step 2.5: Score API Enrichment (if wallet available)

**Always attempt wallet resolution.** Only skip enrichment if resolution fails AND no wallet is available.

Determine wallet address (in priority order):
1. **Auto-resolve**: Run `scripts/observer/wallet-resolve.sh "{username}"` — cache-first resolution with Supabase fallback
2. `--wallet` flag from command invocation (overrides auto-resolve if both succeed)
3. Existing `wallet` field in canvas frontmatter (from prior enrichment)
4. Direct lookup via `midi_profiles` table if above methods fail

**If wallet address is available:**

1. Call `getWalletProfile(wallet)` from `lib/score-api/client.ts`
   - Returns `WalletProfile` (see `lib/score-api/types.ts:160-199`)
2. Call `getWalletBadges(wallet)` from `lib/score-api/client.ts`
   - Returns `WalletBadgesResponse` (see `lib/score-api/types.ts:82-93`)
3. Construct `score_snapshot` from responses:

| ScoreSnapshot Field | Source (DB View) |
|---------------------|--------|
| `captured_at` | Current ISO timestamp |
| `wallet` | Wallet address used |
| `rank` | `mv_wallet_tiers.overall_rank` |
| `combined_score` | `mv_wallet_tiers.combined_score` |
| `og_score` | `mv_wallet_profiles.og_score` |
| `nft_score` | `mv_wallet_profiles.nft_score` |
| `onchain_score` | `mv_wallet_profiles.onchain_score` |
| `og_rank` | `mv_dimension_leaderboard.og_rank` |
| `nft_rank` | `mv_dimension_leaderboard.nft_rank` |
| `onchain_rank` | `mv_dimension_leaderboard.onchain_rank` |
| `trust_filter` | `mv_wallet_profiles.trust_filter` |
| `trust_classification` | `mv_wallet_profiles.trust_classification` |
| `og_breadth` | `mv_wallet_profiles.og_breadth` |
| `nft_breadth` | `mv_wallet_profiles.nft_breadth` |
| `onchain_breadth` | `mv_wallet_profiles.onchain_breadth` |
| `crowd_tier` | `mv_wallet_tiers.crowd_tier` |
| `elite_tier` | `mv_wallet_tiers.elite_tier` |
| `total_badges` | `mv_wallet_badge_summary.badge_count` |
| `model_version` | Hardcode current version (e.g. `"v0.11.0"`) |

4. Add `wallet` and `score_snapshot` to canvas frontmatter
5. Render `## Score Context` section (after `## User Profile`) as markdown table:

```markdown
## Score Context

| Field | Value |
|-------|-------|
| **Wallet** | `{wallet}` |
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
| **Captured At** | {captured_at} |
```

**If canvas already has `score_snapshot`:**
- Compare previous snapshot with new data
- If any dimension score changed by more than 5 points, flag as `score_delta` in the canvas:
  ```markdown
  > **Score Delta Detected** ({date}): {dimension} changed from {old} → {new} ({diff})
  ```
- Update `score_snapshot` in frontmatter with latest data
- Update `## Score Context` section with latest values

**If enrichment fails** (Score API error, timeout, wallet not found):
- Proceed without enrichment — never block canvas creation
- Add note to canvas: `> Note: Score API unavailable at time of observation ({date})`
- Set `score_snapshot: null` in frontmatter if no prior snapshot exists

**If wallet not available:**
- Skip enrichment silently (no warning needed)

---

### Step 2.5E: Retroactive Enrichment Mode (`--enrich`)

When invoked with `--enrich` flag:

1. **Load existing canvas** — error if `grimoires/observer/canvas/{username}-canvas.md` not found
2. **Run Step 2.5** (Score API Enrichment) using provided `--wallet` or canvas frontmatter wallet
3. **Add/update `## Score Context` section** in canvas
4. **Update canvas frontmatter** with `wallet` and `score_snapshot`
5. **Update `updated` timestamp** in frontmatter
6. **Skip Step 3** (Level 3 diagnostic) — no new quote to analyze
7. **Skip Step 5** (Conversation Frameworks) — no new quote context
8. **Proceed to Step 7** (Update Laboratory State) and **Step 8** (Report Output)

Report output for `--enrich` mode:
```
✓ Canvas enriched: grimoires/observer/canvas/{username}-canvas.md

Score Context:
  Rank: #{rank} | Combined: {combined_score}
  Crowd Tier: {crowd_tier} | Elite: {elite_tier or None}
  Trust: {trust_filter} ({trust_classification})
  {score_delta summary if applicable}

Next Steps:
  - Add observations: /observe @{username} "..."
  - Shape journeys: /shape --run
```

---

### Step 3: Apply Level 3 Diagnostic Framework

```
Quote → Level 1 (What they said)
      → Level 2 (What they want)
      → Level 3 Hypothesis (What they might be trying to accomplish)
```

**Analyze the quote to extract:**

1. **User Profile** (if new canvas):
   - Signals Observed (behavioral evidence only)
   - Theories (possible interpretations - NOT conclusions)
   - Confidence: Low | Medium (never High from single quote)
   - Unknown (what we can't determine)
   - Stakes (what they have invested, if mentioned)

2. **Level 3 Hypothesis**:
   - What might they be trying to accomplish?
   - Quote anchor (exact words that led to theory)
   - Alternative interpretations
   - What would validate / invalidate

3. **Future Promises** (if detected):
   - Flag any "will", "would", "later", "tomorrow" statements
   - Add to Promise table for follow-up tracking

4. **Journey Fragment** (if applicable):
   - Trigger → Action → Expected → Actual → Emotion

5. **Expectation Gap** (if discovered):
   - Expected vs Actual mismatch
   - Gap type: Bug | Feature | Discoverability

### Step 3.5: Provenance Gate

Before appending the quote to the canvas, run the provenance gate to ensure idempotent ingestion and content-hash tracking.

```bash
echo -n "{quote}" | scripts/provenance/gate.sh \
  --source-type manual_quote \
  --confidence "{confidence}" \
  --canvas-target "{username}" \
  --raw-source-ref "observe-{username}-{date}" \
  --ingested-by observe
```

**Timestamp confidence resolution:**

| Operator input | `--confidence` | `--timestamp` |
|----------------|---------------|---------------|
| Full ISO 8601 (e.g. `2026-02-11T14:30:00Z`) | `exact` | The provided timestamp |
| Date only (e.g. `2026-02-11`) | `day_level` | `{date}T00:00:00Z` |
| No date provided | `unknown` | _(omit flag — gate stores null)_ |

**Context flag mapping:**
- `--context "Discord #feedback 2026-02-11"` → parse date if present, set confidence accordingly
- `--context "Discord #feedback"` → no date parseable, confidence `unknown`

**Exit code handling:**

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | INGESTED | Proceed with canvas update (Step 4) |
| 1 | SKIPPED (duplicate) | Skip canvas append for this quote. Report: "Quote already ingested (duplicate detected via content hash)" |
| 2 | ERROR (missing flags) | Log error, skip provenance tracking, proceed with canvas update (degrade gracefully) |
| 3+ | LOCK/CORRUPTION | Log warning, skip provenance tracking, proceed with canvas update |

**No thread context**: `/observe` handles standalone quotes. No `--thread-id` or `--message-index` flags.

**Provenance hash in Quotes Library**: When the gate returns exit 0, capture the provenance record ID from stdout. Include it in the Quotes Library entry:
```markdown
> "{quote}" — {context}, {date} `[prov:{record_id}]`
```

---

### Step 4: Update Canvas

**New Canvas Template:**
```markdown
---
type: user_canvas
user: {username}
wallet: "0x..."              # Persisted for future enrichment (null if not provided)
score_snapshot:              # Populated by Step 2.5 (null if no wallet/enrichment failed)
  captured_at: "{ISO timestamp}"
  wallet: "0x..."
  rank: null                 # from mv_wallet_tiers.overall_rank
  combined_score: null       # from mv_wallet_tiers.combined_score
  og_score: null             # from mv_wallet_profiles
  nft_score: null
  onchain_score: null
  og_rank: null              # from mv_dimension_leaderboard
  nft_rank: null
  onchain_rank: null
  trust_filter: null         # from mv_wallet_profiles
  trust_classification: null
  og_breadth: null
  nft_breadth: null
  onchain_breadth: null
  crowd_tier: null           # from mv_wallet_tiers
  elite_tier: null
  total_badges: null         # from mv_wallet_badge_summary.badge_count
  model_version: null
hivemind:
  artifact: user_truth_canvas
  workstream: discovery
  product: []                # e.g. [user_profile, wallet_integration, user_reactivation]
  jtbd: []                   # e.g. [help_me_feel_smart, find_information, feel_connected_again]
  source: "{direct_feedback|discord_dm|twitter_dm|supabase_feedback}"
  learning_status: directionally_correct
created: {timestamp}
updated: {timestamp}
linked_journeys: []
linked_observations: []
confidence:
  created_at: "{timestamp}"
  last_validated_at: "{timestamp}"
  last_validated_commit: ""
  validation_count: 0
  related_paths:
    - "lib/score-api/**"
    - "grimoires/observer/canvas/"
schema_version: 2
lifecycle_state: "{new_user|reactivating|power_user|churning}"
last_enriched: "{ISO timestamp or null}"
enrichment_trigger: observe
chronicle_refs: []
---

# {username} Canvas

## User Profile

| Field | Value |
|-------|-------|
| **Signals Observed** | {behavioral signals from quote} |
| **Theories** | {possible interpretations - NOT conclusions} |
| **Confidence** | Low / Medium |
| **Unknown** | {what we cannot determine from this quote} |
| **Stakes** | {what they have invested, if mentioned} |

---

## Level 3 Hypotheses

### Hypothesis 1: {theory about what they might be trying to accomplish}
<!-- hivemind:product:UNTAGGED -->

- **Quote anchor**: "{exact words that led to this theory}"
- **Context**: {surrounding context and behavioral evidence}
- **Alternative interpretations**: {other valid readings of this quote}
- **Confidence**: Low | Medium
- **What would validate**: {observable behavior or statement that confirms}
- **What would invalidate**: {observable behavior or statement that disproves}
- **Design implication**: {what this means for the product if true}

---

## Future Promises (Unvalidated)

| Promise | Date | Follow-up Trigger |
|---------|------|-------------------|
| {quoted promise} | {date} | {condition for follow-up} |

---

## Journey Fragments

| Trigger | Action | Expected | Actual | Emotion |
|---------|--------|----------|--------|---------|
| {if applicable} | | | | |

---

## Expectation Gaps

| Expected | Actual | Source | Resolution |
|----------|--------|--------|------------|

---

## Conversation Frameworks

When this user returns, anchor on their words:

**If they mention [{topic from quote}]:**
- Opener: "You mentioned [exact words]. How did that go?"
- Dig deeper: "Walk me through what happened."
- Past behavior: "When was the last time you [action]?"

**Red flags to listen for:**
- Future promises ("I would...", "I might...")
- Opinion without behavior ("That sounds useful")
- Compliments without specifics

---

## Quotes Library

> "{quote}" — {context}, {date}
```

**Existing Canvas Update:**
- Append to Level 3 Hypotheses if new hypothesis detected
- Append to Quotes Library
- Update `updated` timestamp in frontmatter
- Add to Future Promises if promise language detected
- Add Journey Fragment if quote contains flow information
- Add Expectation Gap if mismatch detected
- Update Conversation Frameworks with new anchors

### Step 4.5: Wire Obsidian Links

After canvas creation or update, wire it into the knowledge graph if it belongs to any journey:

```bash
source scripts/observer/golden-path-lib.sh
wire_canvas_links "grimoires/observer/canvas/{username}-canvas.md"
```

This injects `<!-- midi:journey-links -->` sentinel with Journeys and Related Canvases sections if the canvas appears in any journey's `source_canvases`. If the canvas is not in any journey, this is a silent no-op. Skip this step in `--enrich` mode.

### Step 5: Generate Conversation Frameworks

Create contextual follow-up frameworks (NOT template questions):

**Anchor to their words:**
- Use exact phrases from their quotes
- Reference specific topics they mentioned

**Structure:**
```markdown
**If they mention [{topic}]:**
- Opener: "You mentioned [their words]. How did that go?"
- Dig deeper: "Walk me through what happened."
- Past behavior: "When was the last time you [action]?"
```

For detailed framework patterns, see [conversation-frameworks.md](conversation-frameworks.md).

### Step 6: Link Existing Observations

Check for existing observations:
```bash
grimoires/artisan/observations/{username}-*.md
```

If found, add to `linked_observations` in frontmatter.

### Step 7: Update Laboratory State

Update `grimoires/observer/state.yaml`:
```yaml
active:
  phase: discovery
  canvas: {username}

canvases:
  {username}:
    created: {timestamp}
    updated: {timestamp}
    quotes_count: {n}
    hypotheses_count: {n}
    linked_journeys: []

queue:
  pending_synthesis:
    - {username}
```

### Step 8: Emit FeedbackEvent

After canvas write, resolve the user's wallet and emit a FeedbackEvent via the Loa event bus:

**Step 8a: Resolve wallet identity**

```bash
# Resolve wallet for data.subject enrichment
resolution_json=$(scripts/observer/wallet-resolve.sh --json "{username}" 2>/dev/null) || resolution_json='{"wallet":null,"confidence":"none","source":"none","username":null}'
```

Parse `resolution_json` to build `data.subject`:
- If `wallet` is not null → `resolution_status: "resolved"`, include `wallet` and `wallet_checksum` (EIP-55)
- If `wallet` is null → `resolution_status: "unresolved"`, omit wallet fields
- Map `confidence` and `source` directly from resolution output

**Step 8b: Emit event with subject**

```bash
source .claude/scripts/lib/event-bus.sh

emit_event "observer.feedback_captured" \
  '{
    "domain": "research",
    "target": { "type": "user", "selector": "user:{username}" },
    "signal": {
      "direction": "{inferred from Level 3 diagnostic: positive/negative/neutral}",
      "weight": {derived from user tier: high=0.8, medium=0.5, low=0.2},
      "specificity": 0.3,
      "content": "{AI-summarized redaction of the observation — NEVER raw quote}",
      "kind": "{inferred: feel | calibration | accuracy | ux}",
      "fingerprint": "{content_hash from provenance gate, or null if gate skipped}",
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
  "observer/observing-users" \
  "" "" \
  "user:{username}"
```

The bus auto-generates `id`, `time`, `specversion` in the CloudEvents envelope. The data payload above follows `grimoires/shared/feedback/schema.json`.

**Weight derivation** (from `score_snapshot` if available):
- Rank ≤ 50 or crowd_tier in [eternal, godfather, all_night] → `high` (weight 0.8)
- Rank ≤ 200 or crowd_tier in [devoted, regular] → `medium` (weight 0.5)
- Otherwise → `low` (weight 0.2)
- No score_snapshot → `medium` (weight 0.5, default)

**Direction inference**:
- Hypothesis polarity positive (user satisfied/engaged) → `positive`
- Hypothesis polarity negative (user frustrated/confused) → `negative`
- Neutral/informational observation → `neutral`

**Kind inference**:
- Signal type FEEL → `feel`
- Signal type WEIGHTINGS → `calibration`
- Signal type ACCURACY → `accuracy`
- Signal type UX → `ux`

See `grimoires/shared/feedback/schema.md` for full schema reference.
See `grimoires/shared/feedback/redaction-guide.md` for hashing and redaction rules.

**Skip this step in `--enrich` mode** (no new observation to emit).

### Step 9: Report Output

Display summary to user:

```
✓ Canvas updated: grimoires/observer/canvas/{username}-canvas.md
✓ FeedbackEvent emitted: observer.feedback_captured (via Loa event bus)

Level 3 Hypothesis Extracted:
  "{summarized hypothesis}"
  Confidence: Low | Medium
  Unknown: {what we don't know}

Canvas Status:
  - Quotes: {n}
  - Hypotheses: {n}
  - Promises Tracked: {n}

Next Steps:
  - Add more quotes: /observe @{username} "..."
  - Shape journeys: /shape --run
```

---

## Counterfactuals — Wallet Enrichment & Canvas Fidelity

Understanding where this skill fails requires distinguishing between data absence and data unavailability — and between behavioral evidence and identity assumptions.

### Target (Correct Behavior)

When a wallet is provided or resolved, the skill calls the Score API, receives dimension scores, tiers, trust classification, and badge counts. This data populates the `score_snapshot` in frontmatter and renders the `## Score Context` section. The user's signal weight (HIGH/MEDIUM/LOW) is derived from their rank and crowd tier — *behavioral position*, not identity.

When enrichment fails (timeout, 404, network error), the skill proceeds without enrichment, adds a timestamped note to the canvas (`> Note: Score API unavailable at time of observation`), and sets `score_snapshot: null`. The canvas is still created with the Level 3 diagnostic intact. Signal weight defaults to MEDIUM (unknown ≠ low).

When no wallet is available at all, enrichment is silently skipped. No warning, no note — the absence is expected, not exceptional.

The three states — enriched, failed-enrichment, and no-wallet — must remain distinguishable in the canvas frontmatter. Collapsing them into a single "no score data" state destroys information that downstream skills need for correct behavior.

### Near Miss — Concept Impermanence

The seductively wrong behavior: treating enrichment failure as "no data" rather than "data unavailable." The difference matters because:

- **"No data"** implies the user has no score position → weight defaults to LOW
- **"Data unavailable"** implies we don't know their position → weight defaults to MEDIUM

A canvas created during a Score API outage should not permanently encode the user as low-weight. The `score_snapshot: null` field is a *temporal marker* — it says "we haven't looked yet," not "there's nothing to find." If the skill treats null snapshots as equivalent to low scores, every user onboarded during an outage gets permanently deprioritized in synthesis.

The correct fix: always check `score_snapshot` presence vs. value. Null means "enrich later" (flag for `/refresh`). Zero means "Score API returned zeros" (real data). Missing field means "pre-enrichment era canvas" (backfill candidate).

The downstream consequences propagate silently:
- `/daily-synthesis` uses `score_snapshot` for signal weight classification — null snapshot → MEDIUM default
- `/shape` aggregates canvases by weight tier — misclassified canvases skew pattern detection
- `/follow-up` prioritizes by weight — a whale classified as MEDIUM gets deprioritized follow-ups

Each skill downstream trusts the canvas frontmatter. A single enrichment error at observation time cascades through the entire pipeline unless the null-vs-zero-vs-missing distinction is preserved.

### Category Error — Semantic Collapse

The fundamentally wrong behavior: inferring user tier, engagement level, or conviction from their username, greeting style, or message tone instead of wallet data.

Examples of this collapse:
- "Bear-themed name" → must be a whale (identity ≠ position)
- "henlo" greeting → casual user (cultural norm ≠ engagement)
- Short message → low effort (brevity ≠ disinterest)
- Enthusiastic tone → high conviction (sentiment ≠ behavior)
- Active in Discord → must be high-conviction (social presence ≠ on-chain activity)
- Multiple DMs sent → engaged user (frequency ≠ depth)

The Observer skill exists precisely because **what people say is not what they do**. The Level 3 framework drills past stated desires to actual goals. Applying the same surface-level inference to the *observer's* classification of the user defeats the entire purpose.

The wallet data provides the only behavioral ground truth available: on-chain actions, badge accumulation, governance participation. Everything else is hypothesis material, never classification input.

A concrete example from this ecosystem: a user with a bear-themed name who sends enthusiastic messages daily in Discord might have zero on-chain activity (rank > 1000, no badges). Conversely, a user who sends one terse DM per month might be rank #5 with 20 badges. The observation skill must resist the intuitive mapping of communication style to conviction — that mapping is the exact bias the scoring system was built to correct.

---

### Step 10: Emit Agent Interaction Log

As the final step, append a JSONL line to `grimoires/observer/agent-logs/{YYYY-MM-DD}.jsonl`:

```json
{
  "ts": "{RFC 3339 UTC}",
  "pack": "observer",
  "skill": "observing-users",
  "status": "{success | error}",
  "duration_ms": "{approximate wall-clock from skill start to end}",
  "artifacts_written": 1,
  "events_emitted": 1,
  "error": "{error message if status=error, omit if success}"
}
```

**Notes**:
- `duration_ms` is approximate (wall-clock estimate, not precise timer)
- `artifacts_written` = number of canvas files written/updated
- `events_emitted` = number of FeedbackEvents emitted (0 for `--enrich` mode)
- Create `grimoires/observer/agent-logs/` directory if it doesn't exist
- See `grimoires/shared/feedback/agent-log-format.md` for format reference

---

## Canvas Template Reference

```yaml
---
type: user_canvas
user: {username}
wallet: "0x..." | null
score_snapshot: {ScoreSnapshot} | null   # See Step 2.5 for field mapping
hivemind:
  artifact: user_truth_canvas
  workstream: discovery
  product: []
  jtbd: []
  source: "{direct_feedback|discord_dm|twitter_dm|supabase_feedback}"
  learning_status: directionally_correct
created: {ISO timestamp}
updated: {ISO timestamp}
linked_journeys: []
linked_observations: []
confidence:
  created_at: "{ISO timestamp}"
  last_validated_at: "{ISO timestamp}"
  last_validated_commit: ""
  validation_count: 0
  related_paths: []
schema_version: 2
lifecycle_state: "{new_user|reactivating|power_user|churning}"
last_enriched: "{ISO timestamp or null}"
enrichment_trigger: observe
chronicle_refs: []
---
```

**Sections:**
1. User Profile (signals, theories, confidence, unknown, stakes)
2. Score Context (rank, percentile, dimension scores, tiers, trust, breadth, badges) — via Step 2.5
3. Level 3 Hypotheses (hypotheses with validation criteria)
4. Future Promises (unvalidated commitments to track)
5. Journey Fragments (trigger → action → expected → actual → emotion)
6. Expectation Gaps (expected vs actual mismatches)
7. Conversation Frameworks (anchored follow-up patterns)
8. Quotes Library (raw quotes with context)

---

## Reference Material

For detailed guidance, see these supporting files:

- [Cultural Context (Berachain/Crypto)](cultural-context.md) - Signal patterns, what NOT to infer from usernames
- [Conversation Frameworks](conversation-frameworks.md) - Mom Test principles, red/green flags, promise detection
- [Complete Example](examples/complete-diagnostic.md) - Full diagnostic walkthrough with new format

---

## Signal Patterns

Behavioral signals that may indicate user intent (use as hypotheses, not classifications):

| Signal Pattern | Possible Interpretation | Confidence Limit |
|----------------|------------------------|------------------|
| "planning", "deciding" | May be optimizing timing | Low-Medium |
| "checking", "verify" | May be validating expectations | Low |
| "API", "integrate" | May want programmatic access | Low-Medium |
| "trying", "wondering" | Exploring, not committed | Low |

**Important**: These are hypothesis generators, not type classifiers. See [cultural-context.md](cultural-context.md) for what NOT to infer.

---

## Promise Detection

Flag these signal words and add to Future Promises table:

| Category | Signal Words |
|----------|--------------|
| Future intent | will, would, might, going to, plan to |
| Temporal | later, tomorrow, soon, eventually |
| Conditional | if I..., when I..., once I... |
| Hedged | probably, maybe, I think I'll |

**Note**: Insights are synthesized only after validation, not from initial quotes.

---

## Integration Points

- **shaping-journeys**: Canvases feed into journey synthesis (Score Context provides user weight for pattern prioritization)
- **Laboratory state**: Updates `state.yaml` for cross-session tracking
- **level-3-diagnostic**: Uses same diagnostic framework
- **Score API** (`lib/score-api/client.ts`): `getWalletProfile()` and `getWalletBadges()` for enrichment
- **synthesizing-feedback**: Feedback entries share `score_snapshot` format for consistent enrichment

---

## Validation

After canvas update:
- [ ] YAML frontmatter is valid
- [ ] Quote preserved exactly (skip for `--enrich` mode)
- [ ] Level 3 hypothesis extracted (not asserted as goal) (skip for `--enrich` mode)
- [ ] Confidence level explicit (Low or Medium) (skip for `--enrich` mode)
- [ ] Unknown field populated (skip for `--enrich` mode)
- [ ] No user type classification from username
- [ ] State.yaml updated with canvas entry
- [ ] If `--wallet` provided: `wallet` field persisted in frontmatter
- [ ] If enrichment ran: `score_snapshot` in frontmatter matches ScoreSnapshot interface from SDD C1
- [ ] If enrichment ran: `## Score Context` section rendered with correct field values
- [ ] If re-enrichment: `score_delta` flagged for dimension changes > 5 points
- [ ] If enrichment failed: graceful fallback with note, canvas still created/updated

---

## Error Handling

| Error | Resolution |
|-------|------------|
| No username provided | Prompt for @username |
| No quote provided | Prompt for quote in quotes (not required for `--enrich` mode) |
| Canvas corrupted | Create backup, reinitialize |
| Observation link broken | Remove from linked_observations |
| `--enrich` but no existing canvas | Error: "No canvas found for @{username}. Use `/observe @{username} \"quote\"` to create one first." |
| Score API timeout/error | Proceed without enrichment, add note to canvas |
| Wallet not found in Score API (404) | Proceed without enrichment, add note: "Wallet not found in Score API" |
| Invalid wallet address format | Warn user, skip enrichment |

---

## Temporal Claim Enforcement (G-4)

**Rules for any downstream skill or agent referencing provenance data from this ingestion:**

1. **Cite provenance**: When making temporal claims about user feedback (e.g., "user said X after release Y"), you MUST cite the provenance `record_id` and verify `source_timestamp_confidence` is `exact`.

2. **Version attribution requires proof**: Attributing feedback to a specific version (e.g., "user was upset after v0.2.0") requires:
   - `source_timestamp_confidence` = `exact`
   - `feedback_timestamp ∈ [release_timestamp, next_release_timestamp)`
   - Both timestamps from authoritative sources (provenance index + chronicle)

3. **Hedging for low confidence**: If `source_timestamp_confidence` is `unknown` or `inferred`, temporal claims MUST be hedged ("around this time" / "date uncertain") and MUST NOT be used for version attribution.

4. **Raw timestamp preservation**: For `/observe`, the operator may not provide a timestamp. When `--confidence unknown` is used, downstream skills MUST NOT fabricate temporal context.

---

## Related

- `/shape` - Extract journeys from canvases
- `/diagram` - Generate diagrams from journeys
- `/craft` - Generate with observation context
- `/plan-and-analyze` - Full PRD discovery
