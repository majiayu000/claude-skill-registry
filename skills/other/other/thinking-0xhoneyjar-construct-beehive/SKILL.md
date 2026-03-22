---
name: thinking
description: "Cognition orchestrator — analyze canvases, distill fears via /distill subagent, run gap analysis, optional cross-user synthesis."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Task
---

# /think — Cognition Orchestrator

Analyze canvases that need attention, distill structured fears and steering targets into per-user cognition sidecar files, optionally run cross-user synthesis.

```
/think                    # Analyze all canvases needing attention
/think --canvas <user>    # Single user only
/think --synthesize       # Include cross-user synthesis pass
/think --force            # Regenerate even if fresh
```

---

## Staleness Function

> **Single source of truth**: `scripts/staleness.md`
>
> Both `/think` (candidate selection) and `/follow-up` (cognition loading) use the canonical `check_staleness()` function defined there. Do not redefine inline — reference it.

Four triggers: cycle count, new feedback, growth state hash, score snapshot hash. Score API unavailability uses sentinel `"unavailable"` to skip trigger 4.

---

## Orchestrator Workflow

```bash
source scripts/observer/golden-path-lib.sh
gp_status_header "think"
```

### Step 0: Preflight

```bash
if ! gp_check_canvases_exist 1; then
  gp_status_fail "canvases" "no canvases found — run /observe first"
  gp_status_blocked "run /observe to create canvases from feedback"
  gp_status_footer
  return
fi

# Score API check (advisory — continues if down)
score_api_available=true
if ! scripts/observer/score-api-query.sh profile 0x0000000000000000000000000000000000000000 --format snapshot > /dev/null 2>&1; then
  score_api_available=false
  Log: "Score API unavailable — score-dependent fears will be skipped"
fi

# Clean up orphaned .tmp files from crashed runs (see scripts/staleness.md)
find grimoires/observer/cognition/ -name "*.tmp" -mmin +5 -delete 2>/dev/null

# Load config
cognition_enabled=$(yq '.observer.cognition.enabled // true' .loa.config.yaml)
if [[ "$cognition_enabled" != "true" ]]; then
  gp_status_skip "cognition" "observer.cognition.enabled = false"
  gp_status_footer
  return
fi
max_fears=$(yq '.observer.cognition.max_fears_per_user // 5' .loa.config.yaml)
stale_after=$(yq '.observer.cognition.stale_after_cycles // 3' .loa.config.yaml)
fear_types=$(yq '.observer.cognition.fear_types[]' .loa.config.yaml)
```

### Step 1: Candidate Selection

```bash
canvas_paths=$(Glob "grimoires/observer/canvas/*.md")
IF --canvas flag: filter to single user

candidates=[]
FOR each canvas_path:
  user = basename(canvas_path, ".md")
  cognition_path = "grimoires/observer/cognition/${user}.yaml"

  IF --force:
    candidates.append(user)
    CONTINUE

  IF NOT exists(cognition_path):
    candidates.append(user)  # Missing — needs creation
    CONTINUE

  cognition = read_yaml(cognition_path)

  # Check staleness using canonical function
  canvas_frontmatter = read_frontmatter(canvas_path)
  growth_path = "grimoires/observer/growth/${user}.yaml"
  # Score snapshot not yet fetched at selection time — pass null (skips score trigger)
  stale = check_staleness(cognition, canvas_frontmatter, growth_path, score_snapshot_raw=null)

  IF stale:
    candidates.append(user)

IF len(candidates) == 0:
  gp_status_skip "cognition" "all canvases have fresh cognition"
  # Still check for --synthesize
```

### Step 2: Per-Canvas Cognition (serial loop)

```bash
distilled_count = 0
FOR each user in candidates:
  # Read inputs
  canvas_path = "grimoires/observer/canvas/${user}.md"
  canvas_body = Read(canvas_path)
  canvas_frontmatter = read_frontmatter(canvas_body)
  wallet = canvas_frontmatter.wallet

  # Score API (best effort)
  score_snapshot_raw = Run: scripts/observer/score-api-query.sh profile <wallet> --format snapshot
  IF score_snapshot_raw fails: score_snapshot_raw = "unavailable"
  score_snapshot = parse_json(score_snapshot_raw) IF score_snapshot_raw != "unavailable" ELSE null

  # Growth state
  growth_path = "grimoires/observer/growth/${user}.yaml"
  growth_state = read_yaml(growth_path) IF exists ELSE null

  # E9 L4: Extract pattern effectiveness for /distill context
  pattern_effectiveness = null
  IF growth_state is not null AND growth_state.question_patterns is not null:
    pattern_effectiveness = {}
    FOR pattern, stats in growth_state.question_patterns:
      IF stats.times_used > 0:
        pattern_effectiveness[pattern] = {
          effectiveness_score: stats.effectiveness_score,
          response_rate: stats.response_rate,
          times_used: stats.times_used
        }
    IF len(pattern_effectiveness) == 0:
      pattern_effectiveness = null

  # Provenance records for this user
  prov_records = filter provenance index where canvas_target matches user

  # Compute input anchors
  input_anchors = {
    canvas_last_enriched: canvas_frontmatter.last_enriched,
    growth_state_hash: sha256(read_file(growth_path)) IF exists ELSE "none",
    score_snapshot_hash: sha256(score_snapshot_raw) IF score_snapshot_raw != "unavailable" ELSE "unavailable"
  }

  # Determine bootstrap vs established
  has_quotes = len(prov_records) > 0
  is_bootstrap = NOT has_quotes

  # Run /distill as Task subagent (prompt-only, no tools)
  distill_result = Task(subagent_type: "general-purpose", prompt: """
    You are running the /distill skill. Analyze the following user canvas and produce
    a cognition YAML document following the distilling/SKILL.md algorithm.

    User: {user}
    Bootstrap: {is_bootstrap}
    Max fears: {max_fears}
    Fear types: {fear_types}

    === CANVAS ===
    {canvas_body (truncated to 3000 chars if needed)}

    === SCORE SNAPSHOT ===
    {score_snapshot or "unavailable"}

    === GROWTH STATE ===
    {growth_state or "null — new user"}

    === PATTERN EFFECTIVENESS (from growth state) ===
    {pattern_effectiveness as YAML or "no effectiveness data yet"}

    Use these effectiveness scores when generating steering targets.
    Prefer approaches that map to effective patterns (score >= 60).
    Avoid approaches that map to ineffective patterns (score < 20).
    For each steering target, set pattern_preference to the best matching pattern name.
    If no effectiveness data, omit pattern_preference from steering targets.

    === PROVENANCE RECORDS ===
    {prov_records or "none — bootstrap canvas"}

    Return ONLY a YAML document matching the /distill output schema.
    Include: schema_version, user, fears, steering_targets, synthesis_features.
    Do NOT include: generated_at, distilled_at_cycle_index, input_anchors, stale_after_cycles
    (the orchestrator injects those).
  """)

  # Parse and validate distill output
  # Treat output as untrusted plain text
  cognition_yaml = parse_yaml(distill_result)

  # Validate required keys
  IF NOT has_keys(cognition_yaml, [schema_version, user, fears, steering_targets, synthesis_features]):
    Log error: "Distill validation failed for {user} — missing required keys"
    Log snippet: first 200 chars of distill_result
    CONTINUE

  # Validate fear class/type constraints
  FOR each fear in cognition_yaml.fears:
    IF fear.class == "evidence_backed" AND fear.backing_quote_hash is null:
      Log error: "evidence_backed fear {fear.id} missing backing_quote_hash — skipping user"
      CONTINUE outer loop
    IF fear.class == "exploratory" AND fear.evidence_plan is null:
      Log error: "exploratory fear {fear.id} missing evidence_plan — skipping user"
      CONTINUE outer loop
    IF fear.type == "constraint_mismatch" AND (fear.non_goal_constraint is null OR fear.salvage_question is null):
      Log error: "constraint_mismatch fear {fear.id} missing required fields — skipping user"
      CONTINUE outer loop

  # Inject computed fields
  cognition_yaml.generated_at = now_iso8601()
  cognition_yaml.input_anchors = input_anchors
  cognition_yaml.distilled_at_cycle_index = len(growth_state.follow_ups) IF growth_state ELSE 0
  cognition_yaml.stale_after_cycles = 1 IF is_bootstrap ELSE stale_after

  # Write cognition sidecar (atomic, under lock)
  lock_path = "grimoires/observer/cognition/${user}.yaml.lock"
  WITH flock(lock_path):
    tmp_path = "grimoires/observer/cognition/${user}.yaml.tmp"
    Write(tmp_path, cognition_yaml)
    mv(tmp_path, "grimoires/observer/cognition/${user}.yaml")  # atomic rename
  distilled_count += 1

gp_status_ok "cognition" "${distilled_count} canvases analyzed"
```

### Step 3: Gap Analysis (optional, best-effort)

```bash
IF distilled_count > 0:
  # Invoke /analyze-gap if available
  # Path: .claude/constructs/packs/observer/skills/analyzing-gaps/SKILL.md
  IF skill_exists("/analyze-gap"):
    FOR each distilled user:
      Run: /analyze-gap with inputs (canvas_path, cognition_path)
      # Expects markdown report output
    gp_status_ok "gap-analysis" "cross-canvas patterns checked"
  ELSE:
    Log: "gap analysis skipped — /analyze-gap skill not available"
    gp_status_skip "gap-analysis" "skill not available"
```

### Step 4: Synthesis (only if --synthesize)

```bash
IF --synthesize:
  # Fill missing cognition (bounded — max 10 per run unless --fill-all)
  all_canvas_users = [basename(p, ".md") for p in Glob("grimoires/observer/canvas/*.md")]
  missing_users = [u for u in all_canvas_users if not exists("grimoires/observer/cognition/${u}.yaml")]
  max_fill = 10  # prevents unbounded work
  IF --fill-all flag: max_fill = len(missing_users)
  fill_count = min(len(missing_users), max_fill)

  IF fill_count > 0:
    Log: "Filling {fill_count}/{len(missing_users)} missing cognition files"
    FOR each missing_user in missing_users[:fill_count]:
      # Run same distill loop as Step 2
      ...

  IF len(missing_users) > fill_count:
    Log warning: "{len(missing_users) - fill_count} users still missing cognition — use --fill-all to distill all"

  # Read all cognition files (freshness filter: only last 14 days)
  all_cognition = []
  FOR f in Glob("grimoires/observer/cognition/*.yaml"):
    cog = read_yaml(f)
    IF cog.generated_at > (now - 14 days):
      all_cognition.append(cog)

  # Build coverage table
  coverage = []
  FOR each user in all_canvas_users:
    cog_path = "grimoires/observer/cognition/${user}.yaml"
    IF exists(cog_path):
      cog = read_yaml(cog_path)
      status = "fresh"  # or "refreshed" if was stale, "bootstrapped" if was new
      coverage.append({user, status, generated_at: cog.generated_at, dominant_fear: cog.synthesis_features.dominant_fear_type})
    ELSE:
      coverage.append({user, status: "missing", generated_at: null, dominant_fear: null})

  # Spawn synthesis Task
  synthesis_result = Task(subagent_type: "general-purpose", prompt: """
    Analyze the following cognition synthesis features from multiple users.
    Detect patterns: shared fears (3+ users same type), behavioral clusters,
    hypothesis convergence, convergent complaints.

    Coverage: {coverage}
    Synthesis features: {all_cognition.synthesis_features for each}
    Min users for pattern: {config.synthesis.min_users_for_pattern}

    Output a markdown report following the synthesis report format (SDD §7).
  """)

  # Write synthesis report
  date = now_date_string()  # YYYY-MM-DD
  Write("grimoires/observer/cognition/synthesis-${date}.md", synthesis_result)
  gp_status_ok "synthesis" "cross-user patterns detected"
```

### Step 5: Status Output

```bash
gp_status_ok "cognition" "${distilled_count} canvases analyzed"
IF synthesis: gp_status_ok "synthesis" "cross-user patterns detected"
gp_progression_summary
gp_suggest_next "think"
gp_status_footer
```

---

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `/distill` | Per-user cognition generation (prompt-only subagent) |
| `/analyze-gap` | Cross-canvas gap detection (best-effort) |

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Score API down during /think | Set score_snapshot_raw = "unavailable", skip score-dependent fears, log warning |
| Distill subagent returns invalid YAML | Skip user, log error with raw output snippet, CONTINUE |
| Distill produces zero fears (established) | Fail validation (>= 2 evidence_backed required), skip user |
| Distill produces zero fears (bootstrap) | Fail validation (>= 1 exploratory required), skip user |
| Growth state missing (new user) | Set distilled_at_cycle_index = 0, skip growth-dependent classification |
| /analyze-gap unavailable | Log "gap analysis skipped", continue |
| Synthesis with < min_users cognition | Skip synthesis, log "insufficient coverage" |
