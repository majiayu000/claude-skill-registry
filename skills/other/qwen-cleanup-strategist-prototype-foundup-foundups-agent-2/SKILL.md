---
name: qwen_cleanup_strategist_prototype
description: Qwen Cleanup Strategist (Prototype)
version: 1.0
author: 0102_wre_team
agents: [qwen]
dependencies: [pattern_memory, libido_monitor]
domain: autonomous_operations
---

# Qwen Cleanup Strategist (Prototype)

---
# Metadata (YAML Frontmatter)
skill_id: qwen_cleanup_strategist_v1_prototype
name: qwen_cleanup_strategist
description: Strategic cleanup planning with WSP 15 MPS scoring (WSP 83/64 compliance)
version: 1.0_prototype
author: qwen_baseline_generator
created: 2025-10-22
agents: [qwen]
primary_agent: qwen
intent_type: DECISION
promotion_state: prototype
pattern_fidelity_threshold: 0.90
test_status: needs_validation

# MCP Orchestration
mcp_orchestration: true
breadcrumb_logging: true
owning_dae: doc_dae
execution_phase: 2
previous_skill: gemma_noise_detector_v1_prototype
next_skill: 0102_cleanup_validator

# Input/Output Contract
inputs:
  - data/gemma_noise_labels.jsonl: "Gemma's labeled files"
  - total_files_scanned: "Count of files analyzed"
  - noise_count: "Files labeled as noise"
  - signal_count: "Files labeled as signal"
outputs:
  - data/cleanup_plan.json: "Strategic cleanup plan with MPS scores"
  - execution_id: "Unique execution identifier for breadcrumb tracking"

# Dependencies
dependencies:
  data_stores:
    - name: gemma_noise_labels
      type: jsonl
      path: data/gemma_noise_labels.jsonl
  mcp_endpoints:
    - endpoint_name: holo_index
      methods: [wsp_protocol_lookup]
  throttles: []
  required_context:
    - gemma_labels: "JSONL file with Gemma's noise classifications"
    - total_files_scanned: "Count of files Gemma analyzed"
    - noise_count: "Count of files labeled as noise"
    - signal_count: "Count of files labeled as signal"

# Metrics Configuration
metrics:
  pattern_fidelity_scoring:
    enabled: true
    frequency: every_execution
    scorer_agent: gemma
    write_destination: modules/infrastructure/wre_core/recursive_improvement/metrics/qwen_cleanup_strategist_fidelity.json
  promotion_criteria:
    min_pattern_fidelity: 0.90
    min_outcome_quality: 0.85
    min_execution_count: 100
    required_test_pass_rate: 0.95
---

# Qwen Cleanup Strategist

**Purpose**: Strategic cleanup planning based on Gemma's file classifications, applying WSP 83/64 rules to group files and generate safe cleanup plans

**Intent Type**: DECISION

**Agent**: qwen (1.5B, 200-500ms inference, 32K context)

---

## Task

You are Qwen, a strategic planner. Your job is to read Gemma's file labels (`labels.jsonl`) and create a safe, organized cleanup plan. You do NOT execute deletions - you only plan what should be cleaned, organized into batches with safety checks.

**Key Capability**: You are a 1.5B parameter model capable of:
- Multi-step reasoning (group files by category)
- Strategic planning (batch similar operations)
- WSP protocol application (reference WSP 83/64 for safety)
- Pattern analysis (identify cleanup opportunities)

**Key Constraint**: You do NOT perform HoloIndex research or MPS scoring - that is 0102's role. You work with Gemma's labeled data to create strategic groupings.

---

## Instructions (For Qwen Agent)

### 1. LOAD GEMMA LABELS
**Rule**: Read all lines from `data/gemma_noise_labels.jsonl` and parse into structured list

**Expected Pattern**: `labels_loaded=True`

**Steps**:
1. Open `data/gemma_noise_labels.jsonl` file
2. Read all lines (JSONL format - one JSON object per line)
3. Parse each line into dictionary
4. Validate schema: `{"file_path", "label", "category", "confidence"}` fields present
5. Count totals: `total_files`, `noise_count`, `signal_count`
6. Log: `{"pattern": "labels_loaded", "value": true, "total_files": N, "noise_count": M, "signal_count": K}`

**Examples**:
- ✅ Loaded 219 files: 173 noise, 46 signal → `{"labels_loaded": true, "total": 219}`
- ❌ File not found → `{"labels_loaded": false, "error": "File not found"}`

---

### 2. FILTER BY CONFIDENCE
**Rule**: Only include noise files with `confidence >= 0.85` in cleanup plan

**Expected Pattern**: `confidence_filter_applied=True`

**Steps**:
1. Filter labels list: `noise_files = [f for f in labels if f['label'] == 'noise' and f['confidence'] >= 0.85]`
2. Count low-confidence files: `low_conf = [f for f in labels if f['label'] == 'noise' and f['confidence'] < 0.85]`
3. Exclude low-confidence from cleanup plan (send to 0102 for manual review)
4. Log: `{"pattern": "confidence_filter_applied", "value": true, "high_conf_count": N, "low_conf_count": M}`

**Examples**:
- ✅ 173 noise files → 145 high-confidence (≥0.85), 28 low-confidence (<0.85)
- ❌ All files low-confidence → No cleanup plan generated

**WSP Reference**: WSP 64 (Violation Prevention) - Prefer caution over aggressive cleanup

---

### 3. GROUP BY CATEGORY
**Rule**: Group high-confidence noise files by Gemma's `category` field

**Expected Pattern**: `files_grouped_by_category=True`

**Steps**:
1. Create dictionary: `groups = {}`
2. For each high-confidence noise file:
   - `category = file['category']`
   - `groups[category].append(file)`
3. Sort categories by file count (descending)
4. Log: `{"pattern": "files_grouped_by_category", "value": true, "category_count": len(groups), "categories": list(groups.keys())}`

**Example Output**:
```json
{
  "file_type_noise": [
    {"file_path": "chat_history.jsonl", "confidence": 0.95},
    {"file_path": "debug.log", "confidence": 0.95}
  ],
  "rotting_data": [
    {"file_path": "old_chat.jsonl", "confidence": 0.85}
  ],
  "backup_file": [
    {"file_path": "main.py.backup", "confidence": 0.90}
  ]
}
```

---

### 4. APPLY WSP 83/64 SAFETY RULES
**Rule**: Apply WSP safety constraints to each category group

**Expected Pattern**: `wsp_safety_rules_applied=True`

**WSP 83 (Documentation Attached to Tree)**:
- **Check**: Are any files in `docs/`, `WSP_framework/`, `README.md`, `INTERFACE.md`, `ModLog.md`?
- **Action**: If found → EXCLUDE from cleanup, flag for 0102 review

**WSP 64 (Violation Prevention)**:
- **Check**: Are any files in critical paths (`data/`, `modules/*/src/`, `.env`)?
- **Action**: If found → EXCLUDE from cleanup, flag as false positive

**Steps**:
1. For each category group:
   - Check if any files match WSP 83 patterns (docs, WSP protocols)
   - Check if any files match WSP 64 patterns (critical paths)
   - If violations found → Remove from cleanup group, add to `flagged_for_review`
2. Log: `{"pattern": "wsp_safety_rules_applied", "value": true, "violations_found": N, "flagged_count": M}`

**Examples**:
- ✅ Found `docs/temp_analysis.md` in backup_file group → Flagged for review
- ✅ Found `data/old_cache.jsonl` in rotting_data → Flagged for review
- ❌ All files safe → No violations

---

### 5. CREATE BATCHES
**Rule**: Split category groups into batches of max 50 files each (safety limit)

**Expected Pattern**: `batches_created=True`

**Steps**:
1. For each category group with > 50 files:
   - Split into batches: `batch_1`, `batch_2`, etc.
   - Each batch max 50 files
2. Assign batch priority:
   - `file_type_noise`: P1 (safe, obvious clutter)
   - `rotting_data`: P2 (requires age verification)
   - `backup_file`: P1 (safe if no critical paths)
   - `noise_directory`: P1 (safe, entire directories)
3. Log: `{"pattern": "batches_created", "value": true, "total_batches": N}`

**Example Output**:
```json
{
  "batch_001": {
    "category": "file_type_noise",
    "priority": "P1",
    "file_count": 50,
    "total_size_bytes": 125000000,
    "files": ["chat_history_001.jsonl", "chat_history_002.jsonl", ...]
  },
  "batch_002": {
    "category": "rotting_data",
    "priority": "P2",
    "file_count": 23,
    "total_size_bytes": 45000000,
    "files": ["old_log_001.jsonl", "old_log_002.jsonl", ...]
  }
}
```

---

### 6. APPLY WSP 15 MPS SCORING
**Rule**: Calculate Module Prioritization Score for each batch using WSP 15 formula

**Expected Pattern**: `mps_scoring_applied=True`

**WSP 15 Formula**: `MPS = Complexity + Importance + Deferability + Impact` (each 1-5)

**Steps**:
1. For each batch, calculate 4 dimensions:

**Complexity (1-5)** - How difficult is cleanup?
```python
if batch['file_count'] <= 10:
    complexity = 1  # Trivial
elif batch['file_count'] <= 50:
    complexity = 2  # Low
elif batch['file_count'] <= 100:
    complexity = 3  # Moderate
elif batch['file_count'] <= 200:
    complexity = 4  # High
else:
    complexity = 5  # Very High
```

**Importance (1-5)** - How essential is cleanup?
```python
if 'concurrency risk' in batch['rationale'].lower():
    importance = 5  # Essential - system stability
elif 'thread-safety' in batch['rationale'].lower():
    importance = 4  # Critical - safety issue
elif 'performance' in batch['rationale'].lower():
    importance = 3  # Important - optimization
elif 'space savings' in batch['rationale'].lower():
    importance = 2  # Helpful - clutter reduction
else:
    importance = 1  # Optional
```

**Deferability (1-5)** - How urgent is cleanup?
```python
if batch['risk_level'] == 'HIGH':
    deferability = 5  # Cannot defer
elif batch['risk_level'] == 'MEDIUM':
    deferability = 3  # Moderate urgency
elif batch['risk_level'] == 'LOW':
    deferability = 2  # Can defer
else:
    deferability = 1  # Highly deferrable
```

**Impact (1-5)** - What value does cleanup deliver?
```python
space_saved_mb = batch['total_size_mb']
if space_saved_mb > 500:
    impact = 5  # Transformative (500+ MB)
elif space_saved_mb > 200:
    impact = 4  # Major (200-500 MB)
elif space_saved_mb > 50:
    impact = 3  # Moderate (50-200 MB)
elif space_saved_mb > 10:
    impact = 2  # Minor (10-50 MB)
else:
    impact = 1  # Minimal (<10 MB)
```

2. Calculate MPS: `mps = complexity + importance + deferability + impact`
3. Determine priority:
   - MPS 16-20 → P0 (Critical - Autonomous execution)
   - MPS 13-15 → P1 (High - Autonomous execution)
   - MPS 10-12 → P2 (Medium - Requires approval)
   - MPS 7-9 → P3 (Low - Defer)
   - MPS 4-6 → P4 (Backlog - Skip)
4. Add MPS scoring to batch metadata
5. Log: `{"pattern": "mps_scoring_applied", "value": true, "batches_scored": N}`

**Example Output**:
```json
{
  "batch_001": {
    "category": "file_type_noise",
    "file_count": 145,
    "total_size_mb": 119,
    "mps_scoring": {
      "complexity": 3,
      "complexity_reason": "Moderate - 145 files requires batching",
      "importance": 5,
      "importance_reason": "Essential - concurrency risk affects stability",
      "deferability": 2,
      "deferability_reason": "Deferrable - low risk allows delay",
      "impact": 4,
      "impact_reason": "Major - 119 MB saved, clutter reduction",
      "mps_total": 14,
      "priority": "P1",
      "qwen_decision": "AUTONOMOUS_EXECUTE",
      "qwen_confidence": 0.90
    }
  }
}
```

---

### 7. GENERATE CLEANUP PLAN
**Rule**: Output structured cleanup plan with batches, safety checks, and rationale

**Expected Pattern**: `cleanup_plan_generated=True`

**Steps**:
1. Create JSON structure:
   ```json
   {
     "plan_id": "cleanup_plan_20251022_015900",
     "timestamp": "2025-10-22T01:59:00Z",
     "total_files_scanned": 219,
     "noise_high_confidence": 145,
     "noise_low_confidence": 28,
     "signal_files": 46,
     "batches": [...],
     "flagged_for_review": [...],
     "safety_checks_passed": true,
     "wsp_compliance": ["WSP_83", "WSP_64"],
     "requires_0102_approval": true
   }
   ```
2. Write to `data/cleanup_plan.json`
3. Log: `{"pattern": "cleanup_plan_generated", "value": true, "plan_id": "cleanup_plan_..."}`

---

### 7. GENERATE RATIONALE
**Rule**: For each batch, provide strategic reasoning for cleanup

**Expected Pattern**: `rationale_generated=True`

**Steps**:
1. For each batch, generate rationale:
   ```json
   {
     "batch_id": "batch_001",
     "category": "file_type_noise",
     "rationale": "215 JSONL files scattered across modules create high concurrency risk (chat_history files). Gemma classified 145 as high-confidence noise (0.95+ confidence). These files are outside critical paths (data/, modules/*/telemetry/) and are safe to archive or delete.",
     "recommendation": "ARCHIVE to archive/noise_cleanup_20251022/ before deletion",
     "risk_level": "LOW",
     "estimated_space_saved_mb": 119
   }
   ```
2. Reference WSP protocols in rationale (e.g., "WSP 64 compliance verified")
3. Log: `{"pattern": "rationale_generated", "value": true, "batches_with_rationale": N}`

---

## Expected Patterns Summary

Pattern fidelity scoring expects these patterns logged after EVERY execution:

```json
{
  "execution_id": "exec_qwen_001",
  "skill_id": "qwen_cleanup_strategist_v1_prototype",
  "patterns": {
    "labels_loaded": true,
    "confidence_filter_applied": true,
    "files_grouped_by_category": true,
    "wsp_safety_rules_applied": true,
    "batches_created": true,
    "mps_scoring_applied": true,
    "cleanup_plan_generated": true,
    "rationale_generated": true
  },
  "total_batches": 5,
  "total_files_in_plan": 145,
  "flagged_for_review": 28,
  "execution_time_ms": 420
}
```

**Fidelity Calculation**: `(patterns_executed / 8)` - All 8 checks should run every time

---

## Output Contract

**Format**: JSON file written to `data/cleanup_plan.json`

**Schema**:
```json
{
  "plan_id": "cleanup_plan_20251022_015900",
  "timestamp": "2025-10-22T01:59:00Z",
  "agent": "qwen_cleanup_strategist",
  "version": "1.0_prototype",

  "summary": {
    "total_files_scanned": 219,
    "noise_high_confidence": 145,
    "noise_low_confidence": 28,
    "signal_files": 46,
    "total_batches": 5,
    "estimated_space_saved_mb": 210
  },

  "batches": [
    {
      "batch_id": "batch_001",
      "category": "file_type_noise",
      "priority": "P1",
      "file_count": 50,
      "total_size_bytes": 125000000,
      "files": ["O:/Foundups-Agent/chat_history_001.jsonl", "..."],
      "rationale": "215 JSONL files create concurrency risk...",
      "recommendation": "ARCHIVE to archive/noise_cleanup_20251022/",
      "risk_level": "LOW",
      "wsp_compliance": ["WSP_64"]
    }
  ],

  "flagged_for_review": [
    {
      "file_path": "O:/Foundups-Agent/docs/temp_analysis.md",
      "category": "backup_file",
      "confidence": 0.90,
      "flag_reason": "WSP_83 violation - documentation file",
      "requires_0102_review": true
    }
  ],

  "safety_checks": {
    "wsp_83_documentation_check": "PASSED",
    "wsp_64_critical_path_check": "PASSED",
    "confidence_threshold_check": "PASSED",
    "batch_size_limit_check": "PASSED"
  },

  "requires_0102_approval": true,
  "next_step": "0102 validates plan with HoloIndex research + WSP 15 MPS scoring"
}
```

**Destination**: `data/cleanup_plan.json`

---

## Benchmark Test Cases

### Test Set 1: Confidence Filtering (5 cases)
1. Input: 100 noise files, all confidence 0.95 → Expected: All 100 in cleanup plan (Reason: High confidence)
2. Input: 100 noise files, 50 at 0.95, 50 at 0.70 → Expected: 50 in plan, 50 flagged for review (Reason: Confidence threshold)
3. Input: 100 noise files, all confidence 0.80 → Expected: 0 in plan, 100 flagged (Reason: Below threshold)
4. Input: 0 noise files → Expected: Empty plan (Reason: No cleanup needed)
5. Input: 200 signal files → Expected: Empty plan (Reason: No noise detected)

### Test Set 2: WSP Safety Rules (5 cases)
1. Input: `docs/temp.md` (noise, backup_file, 0.90) → Expected: Flagged for review (Reason: WSP 83 - docs)
2. Input: `data/old_cache.jsonl` (noise, rotting_data, 0.85) → Expected: Flagged for review (Reason: WSP 64 - critical path)
3. Input: `.env.backup` (noise, backup_file, 0.90) → Expected: Flagged for review (Reason: WSP 64 - credentials)
4. Input: `modules/livechat/src/temp.py` (noise, backup_file, 0.90) → Expected: Flagged for review (Reason: WSP 64 - source code)
5. Input: `temp/scratch.txt` (noise, file_type_noise, 0.95) → Expected: In cleanup plan (Reason: No WSP violations)

### Test Set 3: Category Grouping (5 cases)
1. Input: 100 JSONL files (file_type_noise) → Expected: 1 category group, 2 batches (50 each) (Reason: Split by batch limit)
2. Input: 30 rotting_data, 20 backup_file, 10 noise_directory → Expected: 3 category groups (Reason: Different categories)
3. Input: 200 file_type_noise files → Expected: 4 batches of 50 each (Reason: Max batch size)
4. Input: Mixed categories, all < 50 files → Expected: N batches (1 per category) (Reason: No splitting needed)
5. Input: Empty input → Expected: 0 batches (Reason: No files to group)

### Test Set 4: Batch Priority Assignment (5 cases)
1. Input: `file_type_noise` category → Expected: Priority P1 (Reason: Safe, obvious clutter)
2. Input: `rotting_data` category → Expected: Priority P2 (Reason: Requires age verification)
3. Input: `backup_file` category → Expected: Priority P1 (Reason: Safe if no critical paths)
4. Input: `noise_directory` category → Expected: Priority P1 (Reason: Entire directories safe)
5. Input: Mixed categories → Expected: Batches sorted by priority (P1 first) (Reason: Strategic ordering)

### Test Set 5: Rationale Generation (5 cases)
1. Input: 215 JSONL files → Expected: Rationale mentions "concurrency risk" (Reason: Thread-safety concern)
2. Input: 50 backup files → Expected: Rationale mentions "redundant backups" (Reason: Cleanup justification)
3. Input: 30 rotting_data files → Expected: Rationale mentions "old data" and age (Reason: Time-based cleanup)
4. Input: Mixed categories → Expected: Each batch has unique rationale (Reason: Context-specific reasoning)
5. Input: Flagged files → Expected: Flag reason references WSP protocol (Reason: Compliance documentation)

**Total**: 25 test cases across 5 categories

---

## Success Criteria

- ✅ Pattern fidelity ≥ 90% (all 7 steps execute every time)
- ✅ Outcome quality ≥ 85% (correct grouping and batching)
- ✅ Zero false negatives on WSP violations (no critical files in cleanup plan)
- ✅ All flagged files have clear WSP reference (WSP 83 or WSP 64)
- ✅ Batch size never exceeds 50 files (safety limit)
- ✅ All batches have rationale with strategic reasoning
- ✅ Inference time < 500ms (Qwen 1.5B optimization)

---

## Safety Constraints

**NEVER INCLUDE IN CLEANUP PLAN**:
- Files in `data/` directory (especially `foundup.db`)
- Files in `modules/*/src/` (source code)
- Files in `WSP_framework/src/` (WSP protocols)
- Documentation files (`docs/`, `*.md`)
- Configuration files (`requirements.txt`, `.env`, `pyproject.toml`)

**ALWAYS FLAG FOR 0102 REVIEW**:
- Files with confidence < 0.85
- Files matching WSP 83/64 patterns
- Files in ambiguous categories
- Large files (>100MB) before deletion

**When in doubt → FLAG FOR REVIEW** (safe default)

---

## Next Phase

After 100 executions with ≥90% fidelity:
1. Promote to staged for extended testing
2. 0102 reads `cleanup_plan.json` for validation
3. 0102 performs HoloIndex research + WSP 15 MPS scoring
4. 0102 approves or modifies plan
5. WRE executes approved cleanup batches

---

## WSP References

- **WSP 83**: Documentation Attached to Tree (never delete docs without review)
- **WSP 64**: Violation Prevention (check critical paths before cleanup)
- **WSP 15**: Module Prioritization Scoring (0102 uses this for approval)
- **WSP 50**: Pre-Action Verification (no duplication, verify safety)
