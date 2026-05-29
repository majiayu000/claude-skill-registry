---
name: distilling
description: "Analyze a user canvas and distill structured fears, steering targets, and synthesis features into a cognition sidecar file."
allowed-tools: []
---

# /distill — Cognition Distillation

Analyze a single user's canvas state and produce structured cognition output. This skill runs as a **prompt-only subagent** — it receives all data in its prompt and returns YAML text. The parent orchestrator (`/think` or `/follow-up` auto-refresh) handles filesystem operations.

## Input Contract

The parent orchestrator provides these sections in the prompt:

| Input | Description |
|-------|-------------|
| Canvas body | Full markdown of `grimoires/observer/canvas/{user}.md` |
| Score API snapshot | JSON from `score-api-query.sh profile <wallet> --format snapshot` (or null if unavailable) |
| Growth state | YAML from `grimoires/observer/growth/{user}.yaml` (or null if new user) |
| Provenance records | Filtered JSONL entries for this user from `grimoires/mining/provenance/index.jsonl` |
| Config | `observer.cognition.*` values (fear_types, max_fears_per_user, stale_after_cycles) |

## Output Contract

Return a single YAML document matching the cognition sidecar schema (SDD §2). The parent validates this output against required keys and types before writing to disk.

**Required top-level keys**: `schema_version`, `user`, `fears`, `steering_targets`, `synthesis_features`

The parent orchestrator injects these computed fields after validation (do NOT include them in output):
- `generated_at`
- `distilled_at_cycle_index`
- `input_anchors`
- `stale_after_cycles`

## Algorithm

### Step 1: Inventory Hypotheses

Extract all hypotheses from the canvas. Each has:
- `id` (e.g., H1, H2)
- `text` (hypothesis statement)
- `confidence` (High, Medium, Low)
- `evidence_quotes` (list of quotes with optional provenance hashes)
- `gaps` (associated gap sections)

### Step 2: Classify User State

```
has_quotes = len(provenance_records where canvas_target == user) > 0
is_bootstrap = NOT has_quotes
```

### Step 3: Identify Fears

#### Bootstrap Path (no quotes yet)

Generate 1-3 **exploratory** fears derived from:
- Score position (rank, tier, dimension strengths/weaknesses)
- Lifecycle state (from canvas frontmatter or inferred)
- Gap types (if any exist in canvas)

Every bootstrap fear MUST have:
- `class: exploratory`
- `evidence_plan` describing what to ask/observe to obtain first evidence
- `backing_quote_hash: null`

Bootstrap output uses `stale_after_cycles: 1` (parent sets this).

#### Established Path (has quotes)

##### 3a. Hypothesis-based fears

For each hypothesis with confidence < High:

**Gate check**: Does this hypothesis have at least one quote with a verified provenance hash?

- **YES** → Generate `evidence_backed` fear:
  ```yaml
  class: evidence_backed
  type: <classified_type>
  text: "what if <invalidation scenario>?"
  backing_hypothesis: <hypothesis.id>
  backing_quote_hash: <strongest evidence quote hash>
  invalidation_signal: <observable behavior that would confirm or kill this fear>
  confidence_impact: "would <validate|kill> <hypothesis.id>"
  priority: <from confidence: Low=1, Medium=2>
  ```

- **NO** → Downgrade to `exploratory` fear:
  ```yaml
  class: exploratory
  type: <classified_type>
  text: "what if <invalidation scenario>?"
  backing_hypothesis: <hypothesis.id>
  backing_quote_hash: null
  evidence_plan: "obtain direct quote from user about <hypothesis.text> — ask in next follow-up"
  invalidation_signal: <observable behavior>
  confidence_impact: "would <validate|kill> <hypothesis.id>"
  priority: <from confidence>
  ```

##### 3b. Gap-based fears

For each gap with status != Resolved:
- If gap maps to a fear type and has supporting evidence → `evidence_backed` fear
- If gap maps to a fear type but lacks evidence → `exploratory` fear

##### 3c. Growth-based fears

If growth state shows ineffective patterns (effectiveness < 20):
- Generate `exploratory` fear about engagement approach
- Type: typically `engagement` or `irrelevance`

##### 3d. Score-position fears

If score_snapshot shows rank <= 10 AND no active progression hypothesis:
- Generate `exploratory` fear about progression ceiling
- Type: `progression`

##### 3e. Rank and cap

```
fears = sort_by_priority(fears)[:config.max_fears_per_user]
```

### Step 4: Generate Steering Targets

For each fear, generate a steering target:
```yaml
steering_targets:
  - fear_id: <fear.id>
    approach: "<how to steer conversation toward this fear>"
    pattern_preference: "<best matching pattern name>"  # E9 L4: from effectiveness data
```

The approach should be a concrete conversational strategy, not a template. Reference specific user data (scores, quotes, badges, rank) when available.

**Pattern preference** (E9 L4): If pattern effectiveness data is provided in the prompt context, set `pattern_preference` to the name of the most effective question pattern that fits this steering target's approach. If no effectiveness data is available, omit the `pattern_preference` field entirely (backward-compatible).

### Step 5: Build Synthesis Features

```yaml
synthesis_features:
  lifecycle_state: <from canvas frontmatter or inferred>
  dominant_fear_type: <mode of fear types, or null if no fears>
  hypothesis_ids: [<H_IDs from canvas>]
  hypothesis_confidences: {<H_ID>: <confidence>, ...}
  gap_types: [<unique gap types from canvas>]
  behavior_tags: [<extracted from canvas + growth state>]
  score_summary: {og: <int>, nft: <int>, onchain: <int>, rank: <int>}
```

**Safe defaults**: If no fears were generated, set `dominant_fear_type: null`. If no hypotheses exist, set empty lists/objects.

## Fear Type Classification Heuristic

```
FUNCTION classify_fear_type(hypothesis, growth_state):
  IF hypothesis.cycles_without_evidence >= 3 AND growth has silence outcomes:
    RETURN "engagement"
  IF hypothesis relates to fixed bug AND no subsequent engagement:
    RETURN "irrelevance"
  IF hypothesis references data accuracy or wrong scores:
    RETURN "trust_erosion"
  IF hypothesis references "what's the plan" or evaluation language:
    RETURN "pmf"
  IF hypothesis references negative labeling of system:
    RETURN "identity"
  IF user rank is top-10 AND hypothesis relates to goals:
    RETURN "progression"
  IF hypothesis references confusion about scoring:
    RETURN "complexity"
  IF hypothesis references feature we won't build:
    RETURN "constraint_mismatch"
  RETURN "engagement"  # default
```

## Validation Rules

The parent orchestrator validates output against these rules:

| Rule | Condition |
|------|-----------|
| `evidence_backed` fears | `backing_quote_hash` MUST be non-null |
| `exploratory` fears | `evidence_plan` MUST be non-null, `backing_quote_hash` MUST be null |
| All fears | `invalidation_signal` and `confidence_impact` MUST be non-null |
| `constraint_mismatch` type | `non_goal_constraint` and `salvage_question` MUST be non-null |
| Established canvases | >= 2 evidence_backed fears (if sufficient quotes available) |
| Bootstrap canvases | >= 1 exploratory fear |
| Fear IDs | Format `FEAR-<user>-<N>`, sequential starting at 1 |

## `constraint_mismatch` Additional Fields

When `type: constraint_mismatch`, include:
```yaml
non_goal_constraint: "<what we won't build>"
salvage_question: "<what alternative value could still work>"
exit_signal: "<what indicates churn>"
```

## Output Example

```yaml
schema_version: 1
user: xabbu

fears:
  - id: FEAR-xabbu-1
    class: evidence_backed
    type: irrelevance
    text: "xabbu reports issues as a completionist, not because they matter to him"
    backing_hypothesis: H1_2
    backing_quote_hash: "sha256:abc123..."
    invalidation_signal: "stops checking scores for 2+ weeks"
    confidence_impact: "would kill H1_2 if confirmed"
    priority: 1

  - id: FEAR-xabbu-2
    class: evidence_backed
    type: trust_erosion
    text: "the badge system feels arbitrary — pioneer badges earned but unclear value"
    backing_hypothesis: H4
    backing_quote_hash: "sha256:def456..."
    invalidation_signal: "mentions badges positively without prompting"
    confidence_impact: "would validate H4 if disconfirmed"
    priority: 2

  - id: FEAR-xabbu-3
    class: exploratory
    type: progression
    text: "rank #1 means no progression left — the game is over"
    backing_hypothesis: null
    backing_quote_hash: null
    evidence_plan: "ask what their goals are now that ranking is maxed — look for engagement signals beyond leaderboard"
    invalidation_signal: "describes new goals beyond ranking"
    confidence_impact: "new hypothesis if confirmed"
    priority: 3

steering_targets:
  - fear_id: FEAR-xabbu-1
    approach: "probe whether checking scores is a habit or intentional — ask about last time they checked without a notification"
    pattern_preference: "verify_action"
  - fear_id: FEAR-xabbu-2
    approach: "reference a specific badge they earned and ask what they thought it meant"
    pattern_preference: "probe_gap"
  - fear_id: FEAR-xabbu-3
    approach: "ask what happens next now that they're #1 — does the game change?"
    pattern_preference: "explore_motivation"

synthesis_features:
  lifecycle_state: power_user
  dominant_fear_type: irrelevance
  hypothesis_ids: [H1_2, H3, H4]
  hypothesis_confidences: {H1_2: high, H3: medium, H4: low}
  gap_types: [feature, ux]
  behavior_tags: [completionist, data_auditor]
  score_summary: {og: 98, nft: 99, onchain: 99, rank: 1}
```
