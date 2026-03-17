---
name: model-tracking-protocol
description: MANDATORY tracking protocol for multi-model validation. Creates structured tracking tables BEFORE launching models, tracks progress during execution, and ensures complete results presentation. Use when running 2+ external AI models in parallel. Trigger keywords - "multi-model", "parallel review", "external models", "consensus", "model tracking".
version: 1.0.0
tags: [orchestration, tracking, multi-model, statistics, mandatory]
keywords: [tracking, mandatory, pre-launch, statistics, consensus, results, failures]
---

# Model Tracking Protocol

**Version:** 1.0.0
**Purpose:** MANDATORY tracking protocol for multi-model validation to prevent incomplete reviews
**Status:** Production Ready

## Overview

This skill defines the MANDATORY tracking protocol for multi-model validation. It provides templates and procedures that make proper tracking unforgettable.

**The Problem This Solves:**

Agents often launch multiple external AI models but fail to:
- Create structured tracking tables before launch
- Collect timing and performance data during execution
- Document failures with error messages
- Perform consensus analysis comparing model findings
- Present results in a structured format

**The Solution:**

This skill provides MANDATORY checklists, templates, and protocols that ensure complete tracking. Missing ANY of these steps = INCOMPLETE review.

---

## Table of Contents

1. [MANDATORY Pre-Launch Checklist](#mandatory-pre-launch-checklist)
2. [Tracking Table Templates](#tracking-table-templates)
3. [Per-Model Status Updates](#per-model-status-updates)
4. [Failure Documentation Protocol](#failure-documentation-protocol)
5. [Consensus Analysis Requirements](#consensus-analysis-requirements)
6. [Results Presentation Template](#results-presentation-template)
7. [Common Failures and Prevention](#common-failures-and-prevention)
8. [Integration Examples](#integration-examples)

---

## MANDATORY Pre-Launch Checklist

**You MUST complete ALL items before launching ANY external models.**

This is NOT optional. If you skip this, your multi-model validation is INCOMPLETE.

### Checklist (Copy and Complete)

```
PRE-LAUNCH VERIFICATION (complete before Task calls):

[ ] 1. SESSION_ID created: ________________________
[ ] 2. SESSION_DIR created: ________________________
[ ] 3. Tracking table written to: $SESSION_DIR/tracking.md
[ ] 4. Start time recorded: SESSION_START=$(date +%s)
[ ] 5. Model list confirmed (comma-separated): ________________________
[ ] 6. Per-model timing arrays initialized
[ ] 7. Code context written to session directory
[ ] 8. Tracking marker created: /tmp/.claude-multi-model-active

If ANY item is unchecked, STOP and complete it before proceeding.
```

### Why Pre-Launch Matters

Without pre-launch setup, you will:
- Lose timing data (cannot calculate speed accurately)
- Miss failed model details (no structured place to record)
- Skip consensus analysis (no model list to compare)
- Present incomplete results (no tracking table to populate)

### Pre-Launch Script Template

**CRITICAL CONSENSUS FIX APPLIED:** Use file-based detection instead of environment variables.

```bash
#!/bin/bash
# Run this BEFORE launching any Task calls

# 1. Create unique session
SESSION_ID="review-$(date +%Y%m%d-%H%M%S)-$(head -c 4 /dev/urandom | xxd -p)"
SESSION_DIR="/tmp/${SESSION_ID}"
mkdir -p "$SESSION_DIR"

# 2. Record start time
SESSION_START=$(date +%s)

# 3. Create tracking table
cat > "$SESSION_DIR/tracking.md" << EOF
# Multi-Model Tracking

## Session Info
- Session ID: ${SESSION_ID}
- Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)
- Models Requested: [FILL]

## Model Status

| Model | Agent ID | Status | Start | End | Duration | Issues | Quality | Notes |
|-------|----------|--------|-------|-----|----------|--------|---------|-------|
| [MODEL 1] | | pending | | | | | | |
| [MODEL 2] | | pending | | | | | | |
| [MODEL 3] | | pending | | | | | | |

## Failures

| Model | Failure Type | Error Message | Retry? |
|-------|--------------|---------------|--------|

## Consensus

| Issue | Model 1 | Model 2 | Model 3 | Agreement |
|-------|---------|---------|---------|-----------|

EOF

# 4. Initialize timing arrays
declare -A MODEL_START_TIMES
declare -A MODEL_END_TIMES
declare -A MODEL_STATUS

# 5. Create tracking marker file (CRITICAL FIX)
# This allows hooks to detect that tracking is active
echo "$SESSION_DIR" > /tmp/.claude-multi-model-active

echo "Pre-launch setup complete. Session: $SESSION_ID"
echo "Directory: $SESSION_DIR"
echo "Tracking table: $SESSION_DIR/tracking.md"
```

### Strict Mode (Optional)

For stricter enforcement, set:

```bash
export CLAUDE_STRICT_TRACKING=true
```

When enabled, hooks will BLOCK execution if tracking is not set up, rather than just warning.

---

## Tracking Table Templates

### Template A: Simple Model Tracking (3-5 models)

```markdown
| Model | Status | Time | Issues | Quality | Cost |
|-------|--------|------|--------|---------|------|
| claude-embedded | pending | - | - | - | FREE |
| x-ai/grok-code-fast-1 | pending | - | - | - | - |
| qwen/qwen3-coder:free | pending | - | - | - | FREE |
```

**Update as each completes:**

```markdown
| Model | Status | Time | Issues | Quality | Cost |
|-------|--------|------|--------|---------|------|
| claude-embedded | success | 32s | 8 | 95% | FREE |
| x-ai/grok-code-fast-1 | success | 45s | 6 | 87% | $0.002 |
| qwen/qwen3-coder:free | timeout | - | - | - | - |
```

### Template B: Detailed Model Tracking (6+ models)

```markdown
## Model Execution Status

### Summary
- Total Requested: 8
- Completed: 0
- In Progress: 0
- Failed: 0
- Pending: 8

### Detailed Status

| # | Model | Provider | Status | Start | Duration | Issues | Quality | Cost | Error |
|---|-------|----------|--------|-------|----------|--------|---------|------|-------|
| 1 | claude-embedded | Anthropic | pending | - | - | - | - | FREE | - |
| 2 | x-ai/grok-code-fast-1 | X-ai | pending | - | - | - | - | - | - |
| 3 | qwen/qwen3-coder:free | Qwen | pending | - | - | - | - | FREE | - |
| 4 | google/gemini-3-pro | Google | pending | - | - | - | - | - | - |
| 5 | openai/gpt-5.1-codex | OpenAI | pending | - | - | - | - | - | - |
| 6 | mistralai/devstral | Mistral | pending | - | - | - | - | FREE | - |
| 7 | deepseek/deepseek-r1 | DeepSeek | pending | - | - | - | - | - | - |
| 8 | anthropic/claude-sonnet | Anthropic | pending | - | - | - | - | - | - |
```

### Template C: Session-Based Tracking File

Create this file at `$SESSION_DIR/tracking.md`:

```markdown
# Multi-Model Validation Tracking
Session: ${SESSION_ID}
Started: ${TIMESTAMP}

## Pre-Launch Verification
- [x] Session directory created: ${SESSION_DIR}
- [x] Tracking table initialized
- [x] Start time recorded: ${SESSION_START}
- [x] Model list: ${MODEL_LIST}

## Model Status

| Model | Status | Start | Duration | Issues | Quality |
|-------|--------|-------|----------|--------|---------|
| claude | pending | - | - | - | - |
| grok | pending | - | - | - | - |
| gemini | pending | - | - | - | - |

## Failures
(populated as failures occur)

## Consensus
(populated after all complete)
```

### Update Protocol

As each model completes, IMMEDIATELY update:

1. Status: `pending` -> `in_progress` -> `success`/`failed`/`timeout`
2. Duration: Calculate from start time
3. Issues: Number of issues found
4. Quality: Percentage if calculable
5. Error: If failed, brief error message

**DO NOT wait until all models finish.** Update as each completes.

---

## Per-Model Status Update Protocol

### IMMEDIATELY After Each Model Completes

Do NOT wait until all models finish. Update tracking AS EACH COMPLETES.

### Update Script

```bash
# Call this when each model completes
update_model_status() {
  local model="$1"
  local status="$2"
  local issues="${3:-0}"
  local quality="${4:-}"
  local error="${5:-}"

  local end_time=$(date +%s)
  local start_time="${MODEL_START_TIMES[$model]}"
  local duration=$((end_time - start_time))

  # Update arrays
  MODEL_END_TIMES["$model"]=$end_time
  MODEL_STATUS["$model"]="$status"

  # Log update to session tracking file
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - Model: $model, Status: $status, Duration: ${duration}s" >> "$SESSION_DIR/execution.log"

  # Update tracking table (append to tracking.md)
  echo "| $model | $status | ${duration}s | $issues | ${quality:-N/A} | ${error:-} |" >> "$SESSION_DIR/tracking.md"

  # Track performance in global statistics
  if [[ "$status" == "success" ]]; then
    track_model_performance "$model" "success" "$duration" "$issues" "$quality"
  else
    track_model_performance "$model" "$status" "$duration" 0 ""
  fi
}

# Usage examples:
update_model_status "claude-embedded" "success" 8 95
update_model_status "x-ai/grok-code-fast-1" "success" 6 87
update_model_status "some-model" "timeout" 0 "" "Exceeded 120s limit"
update_model_status "other-model" "failed" 0 "" "API 500 error"
```

### Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Not started | Wait |
| `in_progress` | Currently executing | Monitor |
| `success` | Completed successfully | Collect results |
| `failed` | Error during execution | Document error |
| `timeout` | Exceeded time limit | Note timeout |
| `cancelled` | User cancelled | Note cancellation |

### Real-Time Progress Display

Show user progress as models complete:

```
Model Status (3/5 complete):
✓ claude-embedded (32s, 8 issues)
✓ x-ai/grok-code-fast-1 (45s, 6 issues)
✓ qwen/qwen3-coder:free (52s, 5 issues)
⏳ openai/gpt-5.1-codex (in progress, 60s elapsed)
⏳ google/gemini-3-pro (in progress, 48s elapsed)
```

---

## Failure Documentation Protocol

**EVERY failed model MUST be documented with:**
1. Model name
2. Failure type (timeout, API error, parse error, etc.)
3. Error message (exact or summarized)
4. Whether retry was attempted

### Failure Report Template

```markdown
## Failed Models Report

### Model: x-ai/grok-code-fast-1
- **Failure Type:** API Error
- **Error Message:** "500 Internal Server Error from OpenRouter"
- **Retry Attempted:** Yes, 1 retry, same error
- **Impact:** Review results based on 3/4 models instead of 4
- **Recommendation:** Check OpenRouter status, retry later

### Model: google/gemini-3-pro
- **Failure Type:** Timeout
- **Error Message:** "Exceeded 120s limit, response incomplete"
- **Retry Attempted:** No, time constraints
- **Impact:** Lost Gemini perspective, consensus based on remaining models
- **Recommendation:** Extend timeout to 180s for this model
```

### Failure Categorization

| Category | Common Causes | Recovery |
|----------|---------------|----------|
| **Timeout** | Model slow, large input, network latency | Retry with extended timeout |
| **API Error** | Provider down, rate limit, auth issue | Wait and retry, check API status |
| **Parse Error** | Malformed response, encoding issue | Retry, simplify prompt |
| **Auth Error** | Invalid API key, expired token | Check credentials |
| **Context Limit** | Input too large for model | Reduce context, split task |
| **Rate Limit** | Too many requests | Wait, implement backoff |

### Failure Summary Table

Always include this in final results:

```markdown
## Execution Summary

| Metric | Value |
|--------|-------|
| Models Requested | 8 |
| Successful | 5 (62.5%) |
| Failed | 3 (37.5%) |

### Failed Models

| Model | Failure | Recoverable? | Action |
|-------|---------|--------------|--------|
| grok-code-fast-1 | API 500 | Yes - retry later | Check OpenRouter status |
| gemini-3-pro | Timeout | Yes - extend limit | Use 180s timeout |
| deepseek-r1 | Auth Error | No - check key | Verify API key valid |
```

### Writing Failures to Session Directory

```bash
# Document failure immediately when it occurs
document_failure() {
  local model="$1"
  local failure_type="$2"
  local error_msg="$3"
  local retry_attempted="${4:-No}"

  cat >> "$SESSION_DIR/failures.md" << EOF

### Model: $model
- **Failure Type:** $failure_type
- **Error Message:** "$error_msg"
- **Retry Attempted:** $retry_attempted
- **Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

EOF

  echo "Failure documented: $model ($failure_type)" >&2
}

# Usage:
document_failure "x-ai/grok-code-fast-1" "API Error" "500 Internal Server Error" "Yes, 1 retry"
```

---

## Consensus Analysis Requirements

**After ALL models complete (or max wait time), you MUST perform consensus analysis.**

This is NOT optional. Even with 2 successful models, compare their findings.

### Minimum Viable Consensus (2 models)

With only 2 models, consensus is simple:
- **AGREE**: Both found the same issue
- **DISAGREE**: Only one found the issue

```markdown
| Issue | Model 1 | Model 2 | Consensus |
|-------|---------|---------|-----------|
| SQL injection | Yes | Yes | AGREE |
| Missing validation | Yes | No | Model 1 only |
| Weak hashing | No | Yes | Model 2 only |
```

### Standard Consensus (3-5 models)

```markdown
| Issue | Claude | Grok | Gemini | Agreement |
|-------|--------|------|--------|-----------|
| SQL injection | Yes | Yes | Yes | UNANIMOUS (3/3) |
| Missing validation | Yes | Yes | No | STRONG (2/3) |
| Rate limiting | Yes | No | No | DIVERGENT (1/3) |
```

### Extended Consensus (6+ models)

For 6+ models, add summary statistics:

```markdown
## Consensus Summary

- **Unanimous Issues (100%):** 3 issues
- **Strong Consensus (67%+):** 5 issues
- **Majority (50%+):** 2 issues
- **Divergent (<50%):** 4 issues

## Top 5 by Consensus

1. [6/6] SQL injection in search - FIX IMMEDIATELY
2. [6/6] Missing input validation - FIX IMMEDIATELY
3. [5/6] Weak password hashing - RECOMMENDED
4. [4/6] Missing rate limiting - CONSIDER
5. [3/6] Error handling gaps - INVESTIGATE
```

### Consensus Analysis Script

```bash
# Perform consensus analysis on all model findings
analyze_consensus() {
  local session_dir="$1"
  local num_models="$2"

  echo "## Consensus Analysis" > "$session_dir/consensus.md"
  echo "" >> "$session_dir/consensus.md"
  echo "Based on $num_models model reviews:" >> "$session_dir/consensus.md"
  echo "" >> "$session_dir/consensus.md"

  # Read all review files and extract issues
  # (simplified - actual implementation would parse review markdown)
  for review in "$session_dir"/*-review.md; do
    echo "Processing: $review"
    # Extract issues, compare, categorize by agreement level
  done

  # Calculate consensus levels
  echo "### Consensus Levels" >> "$session_dir/consensus.md"
  echo "" >> "$session_dir/consensus.md"
  echo "- UNANIMOUS: All $num_models models agree" >> "$session_dir/consensus.md"
  echo "- STRONG: ≥67% of models agree" >> "$session_dir/consensus.md"
  echo "- MAJORITY: ≥50% of models agree" >> "$session_dir/consensus.md"
  echo "- DIVERGENT: <50% of models agree" >> "$session_dir/consensus.md"
}
```

### NO Consensus Analysis = INCOMPLETE Review

If you present results without a consensus comparison, your review is INCOMPLETE.

**Minimum Requirements:**
- ✅ Compare findings across ALL successful models
- ✅ Categorize by agreement level (unanimous, strong, majority, divergent)
- ✅ Prioritize issues by consensus + severity
- ✅ Document in `$SESSION_DIR/consensus.md`

---

## Results Presentation Template

**Your final output MUST include ALL of these sections.**

### Required Output Format

```markdown
## Multi-Model Review Complete

### Execution Summary

| Metric | Value |
|--------|-------|
| Session ID | review-20251224-143052-a3f2 |
| Session Directory | /tmp/review-20251224-143052-a3f2 |
| Models Requested | 5 |
| Successful | 4 (80%) |
| Failed | 1 (20%) |
| Total Duration | 68s (parallel) |
| Sequential Equivalent | 245s |
| Speedup | 3.6x |

### Model Performance

| Model | Time | Issues | Quality | Status | Cost |
|-------|------|--------|---------|--------|------|
| claude-embedded | 32s | 8 | 95% | Success | FREE |
| x-ai/grok-code-fast-1 | 45s | 6 | 87% | Success | $0.002 |
| qwen/qwen3-coder:free | 52s | 5 | 82% | Success | FREE |
| openai/gpt-5.1-codex | 68s | 7 | 89% | Success | $0.015 |
| mistralai/devstral | - | - | - | Timeout | - |

### Failed Models

| Model | Failure | Error |
|-------|---------|-------|
| mistralai/devstral | Timeout | Exceeded 120s limit |

### Top Issues by Consensus

1. **[UNANIMOUS]** SQL injection in search endpoint
   - Flagged by: claude, grok, qwen, gpt-5 (4/4)
   - Severity: CRITICAL
   - Action: FIX IMMEDIATELY

2. **[UNANIMOUS]** Missing input validation
   - Flagged by: claude, grok, qwen, gpt-5 (4/4)
   - Severity: CRITICAL
   - Action: FIX IMMEDIATELY

3. **[STRONG]** Weak password hashing
   - Flagged by: claude, grok, gpt-5 (3/4)
   - Severity: HIGH
   - Action: RECOMMENDED

### Detailed Reports

- Session directory: /tmp/review-20251224-143052-a3f2
- Consolidated review: /tmp/review-20251224-143052-a3f2/consolidated-review.md
- Individual reviews: /tmp/review-20251224-143052-a3f2/{model}-review.md
- Tracking data: /tmp/review-20251224-143052-a3f2/tracking.md
- Consensus analysis: /tmp/review-20251224-143052-a3f2/consensus.md

### Statistics Saved

- Performance data logged to: ai-docs/llm-performance.json
```

### Missing Section Detection

Before presenting, verify ALL sections are present:

```bash
verify_output_complete() {
  local output="$1"

  local required=(
    "Execution Summary"
    "Model Performance"
    "Top Issues"
    "Detailed Reports"
    "Statistics"
  )

  local missing=()
  for section in "${required[@]}"; do
    if ! echo "$output" | grep -q "$section"; then
      missing+=("$section")
    fi
  done

  if [ ${#missing[@]} -gt 0 ]; then
    echo "ERROR: Missing required sections: ${missing[*]}" >&2
    return 1
  fi

  return 0
}
```

**Checklist before presenting results:**

- [ ] Execution Summary (models requested/successful/failed)
- [ ] Model Performance table (per-model times and quality)
- [ ] Failed Models section (if any failed)
- [ ] Top Issues by Consensus (prioritized list)
- [ ] Detailed Reports (session directory, file paths)
- [ ] Statistics confirmation (llm-performance.json updated)

---

## Common Failures and Prevention

### Failure 1: No Tracking Table Created

**Symptom:** Results presented as prose, not structured data

**What went wrong:**
```
"I ran 5 models. 3 succeeded and found various issues."
(No table, no structure)
```

**Prevention:**
- Always run pre-launch script FIRST
- Create `$SESSION_DIR/tracking.md` before Task calls
- Populate table as models complete

**Detection:** SubagentStop hook warns if no tracking found

### Failure 2: Timing Not Recorded

**Symptom:** "Duration: unknown" or missing speed stats

**What went wrong:**
```bash
# Launched models without recording start time
Task: reviewer1
Task: reviewer2
# No SESSION_START, cannot calculate duration!
```

**Prevention:**
```bash
# ALWAYS do this first
SESSION_START=$(date +%s)
MODEL_START_TIMES["model1"]=$SESSION_START
```

**Detection:** Hook checks for timing data in output

### Failure 3: Failed Models Not Documented

**Symptom:** "2 of 8 succeeded" with no failure details

**What went wrong:**
```
"Launched 8 models. 2 succeeded."
(No info on why 6 failed)
```

**Prevention:**
```bash
# Immediately when model fails
document_failure "model-name" "Timeout" "Exceeded 120s" "No"
```

**Detection:** Hook checks for failure section when success < total

### Failure 4: No Consensus Analysis

**Symptom:** Individual model results listed without comparison

**What went wrong:**
```
"Model 1 found: A, B, C
 Model 2 found: B, D, E"
(No comparison: which issues do they agree on?)
```

**Prevention:**
- After all complete, ALWAYS run consolidation
- Create consensus table comparing findings
- Prioritize by agreement level

**Detection:** Hook checks for consensus keywords

### Failure 5: Statistics Not Saved

**Symptom:** No record in ai-docs/llm-performance.json

**What went wrong:**
```bash
# Forgot to call tracking functions
# No record of this session
```

**Prevention:**
```bash
# ALWAYS call these
track_model_performance "model" "status" duration issues quality
record_session_stats total success failed parallel sequential speedup
```

**Detection:** Hook checks file modification time

### Prevention Checklist

Before presenting results, verify:

```
[ ] Tracking table exists at $SESSION_DIR/tracking.md
[ ] Tracking table is populated with all model results
[ ] All model times recorded (or "timeout"/"failed" noted)
[ ] All failures documented in $SESSION_DIR/failures.md
[ ] Consensus analysis performed in $SESSION_DIR/consensus.md
[ ] Results match required output format
[ ] Statistics saved to ai-docs/llm-performance.json
[ ] Session directory contains all artifacts
```

---

## Integration Examples

### Example 1: Complete Multi-Model Review Workflow

```bash
#!/bin/bash
# Full multi-model review with complete tracking

# ============================================================================
# PHASE 1: PRE-LAUNCH (MANDATORY)
# ============================================================================

# 1. Create unique session
SESSION_ID="review-$(date +%Y%m%d-%H%M%S)-$(head -c 4 /dev/urandom | xxd -p)"
SESSION_DIR="/tmp/${SESSION_ID}"
mkdir -p "$SESSION_DIR"

# 2. Record start time
SESSION_START=$(date +%s)

# 3. Create tracking table
cat > "$SESSION_DIR/tracking.md" << EOF
# Multi-Model Validation Tracking

## Session: $SESSION_ID
Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Model Status
| Model | Status | Duration | Issues | Quality |
|-------|--------|----------|--------|---------|
EOF

# 4. Initialize timing arrays
declare -A MODEL_START_TIMES
declare -A MODEL_END_TIMES

# 5. Create tracking marker
echo "$SESSION_DIR" > /tmp/.claude-multi-model-active

# 6. Write code context
git diff > "$SESSION_DIR/code-context.md"

echo "Pre-launch complete. Session: $SESSION_ID"

# ============================================================================
# PHASE 2: MODEL EXECUTION (Parallel Task calls)
# ============================================================================

# Record start times for each model
MODEL_START_TIMES["claude-embedded"]=$(date +%s)
MODEL_START_TIMES["x-ai/grok-code-fast-1"]=$(date +%s)
MODEL_START_TIMES["qwen/qwen3-coder:free"]=$(date +%s)

# Launch all models in single message (parallel execution)
# (These would be actual Task calls in practice)
echo "Launching 3 models in parallel..."

# ============================================================================
# PHASE 3: RESULTS COLLECTION (as each completes)
# ============================================================================

# Update status immediately after each completes
update_model_status() {
  local model="$1" status="$2" issues="${3:-0}" quality="${4:-}"
  local end_time=$(date +%s)
  local duration=$((end_time - MODEL_START_TIMES["$model"]))

  echo "| $model | $status | ${duration}s | $issues | ${quality:-N/A} |" >> "$SESSION_DIR/tracking.md"
  track_model_performance "$model" "$status" "$duration" "$issues" "$quality"
}

# Example completions
update_model_status "claude-embedded" "success" 8 95
update_model_status "x-ai/grok-code-fast-1" "success" 6 87
update_model_status "qwen/qwen3-coder:free" "timeout"

# ============================================================================
# PHASE 4: CONSENSUS ANALYSIS (MANDATORY)
# ============================================================================

# Consolidate and compare findings
echo "Performing consensus analysis..."
# (Would launch consolidation agent here)

# ============================================================================
# PHASE 5: STATISTICS & PRESENTATION
# ============================================================================

# Calculate session stats
PARALLEL_TIME=52  # max of all durations
SEQUENTIAL_TIME=129  # sum of all durations
SPEEDUP=2.5

# Record session
record_session_stats 3 2 1 "$PARALLEL_TIME" "$SEQUENTIAL_TIME" "$SPEEDUP"

# Present results
cat << RESULTS
## Multi-Model Review Complete

Session: $SESSION_ID
Directory: $SESSION_DIR

Models: 3 requested, 2 successful, 1 failed

See tracking table: $SESSION_DIR/tracking.md
See consensus: $SESSION_DIR/consensus.md
Statistics saved to: ai-docs/llm-performance.json
RESULTS

# Cleanup marker
rm -f /tmp/.claude-multi-model-active
```

### Example 2: Minimal 2-Model Comparison

```bash
# Simplest viable multi-model validation

# Pre-launch
SESSION_ID="review-$(date +%s)"
SESSION_DIR="/tmp/$SESSION_ID"
mkdir -p "$SESSION_DIR"
SESSION_START=$(date +%s)
echo "$SESSION_DIR" > /tmp/.claude-multi-model-active

# Launch
echo "Launching Claude + Grok..."
# Task: claude-embedded
# Task: PROXY_MODE grok

# Track
track_model_performance "claude" "success" 32 8 95
track_model_performance "grok" "success" 45 6 87

# Consensus
echo "Issues both found: SQL injection, missing validation" > "$SESSION_DIR/consensus.md"

# Stats
record_session_stats 2 2 0 45 77 1.7

# Cleanup
rm -f /tmp/.claude-multi-model-active
```

### Example 3: Handling Failures

```bash
# Multi-model with failure handling

# Pre-launch (same as Example 1)
# ... setup code ...

# Launch 4 models
# ... Task calls ...

# Model 1: Success
update_model_status "claude" "success" 32 8 95

# Model 2: Success
update_model_status "grok" "success" 45 6 87

# Model 3: Timeout
update_model_status "gemini" "timeout"
document_failure "gemini" "Timeout" "Exceeded 120s limit" "No"

# Model 4: API Error
update_model_status "gpt5" "failed"
document_failure "gpt5" "API Error" "500 from OpenRouter" "Yes, 1 retry"

# Proceed with 2 successful models
if [ "$SUCCESS_COUNT" -ge 2 ]; then
  echo "Proceeding with $SUCCESS_COUNT successful models"
  # Consensus with partial data
else
  echo "ERROR: Only $SUCCESS_COUNT succeeded, need minimum 2"
fi
```

---

## Integration with Other Skills

### With `multi-model-validation`

The `multi-model-validation` skill defines the execution patterns (4-Message Pattern, parallel execution, proxy mode). This skill (`model-tracking-protocol`) defines the tracking infrastructure.

**Use together:**
```yaml
skills: orchestration:multi-model-validation, orchestration:model-tracking-protocol
```

**Workflow:**
1. Read `multi-model-validation` for execution patterns
2. Read `model-tracking-protocol` for tracking setup
3. Pre-launch (tracking protocol)
4. Execute (validation patterns)
5. Track (protocol updates)
6. Present (protocol templates)

### With `quality-gates`

Use quality gates to ensure tracking is complete before proceeding:

```bash
# After tracking setup, verify completeness
if [ ! -f "$SESSION_DIR/tracking.md" ]; then
  echo "QUALITY GATE FAILED: No tracking table"
  exit 1
fi

# Before presenting results, verify all sections present
verify_output_complete "$OUTPUT" || exit 1
```

### With `todowrite-orchestration`

Track progress through multi-model phases:

```
TodoWrite:
1. Pre-launch setup (tracking protocol)
2. Launch models (validation patterns)
3. Collect results (tracking updates)
4. Consensus analysis (protocol requirement)
5. Present results (protocol template)
```

---

## Quick Reference

### File-Based Tracking Marker (CONSENSUS FIX)

**Create marker after pre-launch setup:**
```bash
echo "$SESSION_DIR" > /tmp/.claude-multi-model-active
```

**Check if tracking active (in hooks):**
```bash
if [[ -f /tmp/.claude-multi-model-active ]]; then
  SESSION_DIR=$(cat /tmp/.claude-multi-model-active)
  [[ -f "$SESSION_DIR/tracking.md" ]] && echo "Tracking active"
fi
```

**Remove marker when done:**
```bash
rm -f /tmp/.claude-multi-model-active
```

### Pre-Launch Commands

```bash
SESSION_ID="review-$(date +%Y%m%d-%H%M%S)-$(head -c 4 /dev/urandom | xxd -p)"
SESSION_DIR="/tmp/${SESSION_ID}"
mkdir -p "$SESSION_DIR"
SESSION_START=$(date +%s)
echo "$SESSION_DIR" > /tmp/.claude-multi-model-active
```

### Tracking Commands

```bash
update_model_status "model" "status" issues quality
document_failure "model" "type" "error" "retry"
track_model_performance "model" "status" duration issues quality
record_session_stats total success failed parallel sequential speedup
```

### Verification Commands

```bash
verify_output_complete "$OUTPUT"
[ -f "$SESSION_DIR/tracking.md" ] && echo "Tracking exists"
[ -f ai-docs/llm-performance.json ] && echo "Statistics saved"
```

---

## Summary

This skill provides MANDATORY tracking infrastructure for multi-model validation:

1. **Pre-Launch Checklist** - 8 items to complete before launching models
2. **Tracking Tables** - Templates for 3-5 models and 6+ models
3. **Status Updates** - Per-model completion tracking
4. **Failure Documentation** - Required format for all failures
5. **Consensus Analysis** - Comparing findings across models
6. **Results Template** - Required output format
7. **Common Failures** - Prevention strategies
8. **Integration Examples** - Complete workflows

**Key Innovation:** File-based tracking marker (`/tmp/.claude-multi-model-active`) allows hooks to detect active tracking without relying on environment variables.

**Use this skill when:** Running 2+ external AI models in parallel for validation, review, or consensus analysis.

**Missing tracking = INCOMPLETE validation.**
