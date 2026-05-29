---
name: growing
description: "Golden path /grow — confirm proposed matches, classify evidence, update confidence, run decay, surface growth changes. Full L4 backpropagation orchestrator."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, Skill
---

# /grow — Growth Loop Orchestrator (L4 Backpropagation)

Operator-confirmed response attribution loop. Reviews proposed matches from `/listen`, classifies signal quality, updates hypothesis confidence, runs decay, and surfaces growth changes.

**All matches require operator confirmation.** Deterministic matches (token/thread) are pre-selected for batch confirm but the operator must explicitly approve. No `--auto` flag.

---

## Arguments

```
/grow                    # Full growth loop for all users
/grow --user <user>      # Single user only
```

---

## Chain

1. **Preflight**: `gp_check_growth_dir`
2. **Per-user loop** (sequential, RLM-isolated):
   - Step 1: Review proposed matches → operator batch-confirm
   - Step 2: Classify signal quality → apply to canonical state
   - Step 3: Hypothesis confidence update
   - Step 4: Decay engine
   - Step 5: Per-user health report
3. **Cross-user**: Step 6 — surface shared patterns

---

## RLM Isolation

`/grow` processes users **one at a time** with a fresh model context per user. Classification prompts (Step 2) MUST only include:
- That user's growth state
- That signal's provenance record

Cross-user context is NEVER included in classification prompts. Reset context between users.

---

## Execution

```bash
source scripts/observer/golden-path-lib.sh
source scripts/observer/growth-state.sh
gp_status_header "grow"

# Clean up orphaned .tmp files from crashed runs (see scripts/staleness.md)
find grimoires/observer/growth/ -name "*.tmp" -mmin +5 -delete 2>/dev/null

if ! gp_check_growth_dir; then
  gp_status_fail "growth" "no growth files — run /listen first"
  gp_status_blocked "run /listen to create growth state from follow-up responses"
  gp_status_footer
  return
fi

cycle_started_at = now_iso8601()
total_confirmed = 0
total_rejected = 0
total_decayed = 0
total_confidence_updated = 0

# Determine user list
IF --user flag provided:
  users = [specified_user]
ELSE:
  users = list_growth_users()  # all *.yaml in growth dir

FOR each user in users (sequential, fresh context per user):
  growth_path = "grimoires/observer/growth/${user}.yaml"
  proposed_path = "grimoires/observer/growth/${user}.proposed_matches.yaml"
  lock_path = "grimoires/observer/growth/${user}.yaml.lock"

  IF NOT exists(growth_path): CONTINUE

  # ==== STEP 1: REVIEW PROPOSED MATCHES ====
  # Check for pending proposed matches
  has_pending = false
  IF exists(proposed_path):
    WITH flock(lock_path):
      proposed_content = read_yaml(proposed_path)
    pending_matches = [m for m in proposed_content.matches if m.status == "pending"]
    IF len(pending_matches) > 0:
      has_pending = true

  IF NOT has_pending:
    # No proposed matches — skip to Step 4 (decay)
    GOTO STEP_4

  # Display ALL pending matches for operator review
  # Pre-select deterministic matches (token/thread) for batch confirm
  # Show non-deterministic matches (keyword/temporal/ambiguous) with evidence for manual review
  FOR each match in pending_matches:
    Display:
      - Match type: {match.match_type} ({match.match_confidence} confidence)
      - Signal snippet: {match.evidence_snippet}
      - Follow-up ID: {match.follow_up_id}
      - Follow-up hypothesis: (look up from growth state)
      - Token: {match.follow_up_token}
      - Pre-selected: YES if match_type in [token, thread], NO otherwise

  # Ask operator to batch-confirm
  # "Which matches do you want to confirm? (token/thread matches are pre-selected)"
  # Operator can: confirm all pre-selected, add/remove individual matches, reject remainder
  confirmed_matches = [operator-confirmed matches]
  rejected_matches = [operator-rejected matches]

  # ==== STEP 2: CLASSIFY SIGNAL QUALITY + APPLY ====
  # RLM ISOLATION: fresh model context with ONLY this user's data
  WITH flock(lock_path):
    growth_content = read_yaml(growth_path)
    proposed_content = read_yaml(proposed_path)

  evidence_list = []

  FOR each match in confirmed_matches:
    follow_up = find_follow_up_by_id(growth_content, match.follow_up_id)
    IF follow_up is null:
      Log: "Follow-up {match.follow_up_id} not found, skipping"
      CONTINUE

    # Idempotency: skip if already applied with same signal
    IF follow_up.outcome == "responded" AND follow_up.match_evidence is not null:
      IF follow_up.match_evidence.signal_id == match.signal_id:
        Log: "Already applied signal {match.signal_id} to {match.follow_up_id}, skipping"
        CONTINUE

    # Retrieve full signal text from provenance
    signal_record = Run: scripts/provenance/query.sh --hash {match.signal_id}
    IF signal_record is null:
      Log: "Provenance record not found for {match.signal_id}, skipping"
      CONTINUE

    # Agent classifies with ONLY this user's hypothesis + this signal
    # Classification prompt includes:
    #   - The hypothesis text from follow_up.hypothesis
    #   - The signal text from provenance
    #   - Ask: Does this signal support, refute, or say nothing about the hypothesis?
    #   - Ask: How strong is the evidence? (high / medium / low)
    #   - Ask: Brief rationale (max 300 chars)
    evidence = {
      signal_id: match.signal_id,
      hypothesis_id: follow_up.hypothesis_ids[0] if follow_up.hypothesis_ids else null,
      direction: <agent_classified>,      # supports | refutes | neutral
      strength: <agent_classified>,        # high | medium | low
      quote_span: match.evidence_snippet,  # display-only, max 200 chars
      quote_hash: sha256(NFC_normalize(match.evidence_snippet)),  # immutable evidence anchor
      rationale: <agent_classified>,       # max 300 chars
      classified_by: "agent",
      classified_at: now_iso8601()
    }

    # Apply to canonical growth state (in-memory, write once at end)
    # Check outcome was pending/unknown before mutating (idempotency)
    IF follow_up.outcome in ["pending", "unknown"]:
      follow_up.outcome = "responded"
      follow_up.response_date = match.signal_timestamp
      follow_up.signal_quality = evidence.strength  # high|medium|low maps to quality
      follow_up.match_evidence = evidence
      follow_up.outcome_at = now_iso8601()

      # Update pattern counters (only on FIRST transition to responded)
      pattern = follow_up.question_pattern
      IF pattern in growth_content.question_patterns:
        growth_content.question_patterns[pattern].responded_count += 1
        quality_numeric = signal_quality_to_numeric(evidence.strength)
        IF quality_numeric is not null:
          growth_content.question_patterns[pattern].signal_quality_sum += quality_numeric
          growth_content.question_patterns[pattern].signal_quality_count += 1
        _recompute_pattern_metrics(growth_content, pattern)

    evidence_list.append(evidence)
    total_confirmed += 1

  # Update proposed match statuses (in-memory)
  FOR m in confirmed_matches: m.status = "confirmed"; m.confirmed_at = now_iso8601()
  FOR m in rejected_matches: m.status = "rejected"
  total_rejected += len(rejected_matches)

  # ==== STEP 3: HYPOTHESIS CONFIDENCE UPDATE ====
  FOR each evidence in evidence_list:
    IF evidence.hypothesis_id is not null:
      growth_content = echo "$growth_content" | growth_update_confidence \
        evidence.hypothesis_id evidence.direction evidence.strength cycle_started_at
      # growth_update_confidence is a pure transformer (stdin→stdout)
      # Gates: stale skip, high-strength-only, neutral skip, per-cycle cap
      total_confidence_updated += 1  # (approximate, function logs actual changes)

  # SINGLE ATOMIC WRITE per user (hold lock once for all mutations)
  WITH flock(lock_path):
    growth_content.last_updated = now_iso8601()
    write_yaml(growth_path + ".tmp", growth_content)
    mv(growth_path + ".tmp", growth_path)
    write_yaml(proposed_path + ".tmp", proposed_content)
    mv(proposed_path + ".tmp", proposed_path)

  STEP_4:
  # ==== STEP 4: DECAY ENGINE ====
  # Read config for decay thresholds
  cycles_to_decaying = config.observer.growth.decay.cycles_to_decaying  # default 3
  cycles_to_stale = config.observer.growth.decay.cycles_to_stale        # default 6

  WITH flock(lock_path):
    content = read_yaml(growth_path)
    modified = growth_run_decay(user, cycles_to_decaying, cycles_to_stale, now_iso8601())
    # growth_run_decay reads from file, returns modified content
    # Count transitions
    FOR each hypothesis:
      IF old_state != new_state:
        total_decayed += 1
    write_yaml(growth_path + ".tmp", modified)
    mv(growth_path + ".tmp", growth_path)

  # ==== STEP 5: PER-USER REPORT ====
  Display for user:
    - Proposed matches: {confirmed} confirmed, {rejected} rejected, {still_pending} still pending
    - Hypotheses: {active} active, {decaying} decaying, {stale} stale
    - Effective patterns: list patterns with effectiveness_score >= 60
    - Ineffective patterns: list patterns with effectiveness_score < 20 and times_used > 0
    - Pending follow-ups: {count} still awaiting response
    - Score deltas: latest if behavioral_signal is true

# END per-user loop

# ==== STEP 6: CROSS-USER PATTERNS + STATUS ====
# Surface cross-user patterns if 3+ users share the same pattern
IF len(users) >= 3:
  # Check if 3+ users share the same effective/ineffective pattern
  # Check if 3+ users have same hypothesis decay trend
  Display any cross-user patterns found

gp_status_ok "matches" "${total_confirmed} confirmed, ${total_rejected} rejected"
gp_status_ok "decay" "${total_decayed} hypotheses transitioned"
gp_status_ok "confidence" "${total_confidence_updated} hypotheses evaluated"
gp_progression_summary
gp_suggest_next "grow"
gp_status_footer
```

---

## Evidence Schema

Evidence is stored at `follow_ups[batch].message_ids[msg].match_evidence` in canonical growth state:

```yaml
match_evidence:
  signal_id: "abc123..."          # Provenance content_hash
  hypothesis_id: "H4"             # First from hypothesis_ids
  direction: supports             # supports | refutes | neutral
  strength: high                  # high | medium | low
  quote_span: "first 200 chars"   # Display-only
  quote_hash: "sha256..."         # sha256(NFC_normalize(quote_span))
  rationale: "User confirms..."   # Max 300 chars
  classified_by: agent
  classified_at: "2026-02-14T..."
```

## Signal Quality Mapping

| strength | quality_numeric | Description |
|----------|----------------|-------------|
| high     | 1.0            | Strong, clear signal |
| medium   | 0.5            | Moderate signal |
| low      | 0.0            | Weak signal |

---

## Truenames Chained

| Truename | Purpose |
|----------|---------|
| `growth-state.sh` | Growth state CRUD + `growth_update_confidence` + `growth_run_decay` |
| `growth-match.sh` | Response attribution (called by /listen, results consumed here) |
| `scripts/provenance/query.sh` | Retrieve provenance records for signal verification |
