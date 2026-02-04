---
name: gemma_noise_detector_prototype
description: Gemma Noise Detector (Prototype)
version: 1.0
author: 0102_wre_team
agents: [gemma]
dependencies: [pattern_memory, libido_monitor]
domain: autonomous_operations
---

# Gemma Noise Detector (Prototype)

---
# Metadata (YAML Frontmatter)
skill_id: gemma_noise_detector_v1_prototype
name: gemma_noise_detector
description: Fast binary classification of files as noise/signal (JSONL, temp, rotting data)
version: 1.0_prototype
author: qwen_baseline_generator
created: 2025-10-22
agents: [gemma]
primary_agent: gemma
intent_type: CLASSIFICATION
promotion_state: prototype
pattern_fidelity_threshold: 0.90
test_status: needs_validation

# MCP Orchestration
mcp_orchestration: true
breadcrumb_logging: true
owning_dae: doc_dae
execution_phase: 1
next_skill: qwen_cleanup_strategist_v1_prototype

# Input/Output Contract
inputs:
  - file_path: "Absolute path to file being classified"
  - file_extension: "File extension (.json, .jsonl, .md, .log, etc.)"
  - file_size_bytes: "Size of file in bytes"
  - last_modified_days: "Days since last modification"
  - parent_directory: "Directory containing the file"
outputs:
  - data/gemma_noise_labels.jsonl: "JSONL file with noise/signal labels"
  - execution_id: "Unique execution identifier for breadcrumb tracking"

# Dependencies
dependencies:
  data_stores: []
  mcp_endpoints:
    - endpoint_name: holo_index
      methods: [semantic_search]
  throttles: []
  required_context:
    - file_path: "Absolute path to file being classified"
    - file_extension: "File extension (.json, .jsonl, .md, .log, etc.)"
    - file_size_bytes: "Size of file in bytes"
    - last_modified_days: "Days since last modification"
    - parent_directory: "Directory containing the file"

# Metrics Configuration
metrics:
  pattern_fidelity_scoring:
    enabled: true
    frequency: every_execution
    scorer_agent: gemma
    write_destination: modules/infrastructure/wre_core/recursive_improvement/metrics/gemma_noise_detector_fidelity.json
  promotion_criteria:
    min_pattern_fidelity: 0.90
    min_outcome_quality: 0.85
    min_execution_count: 100
    required_test_pass_rate: 0.95
---

# Gemma Noise Detector

**Purpose**: Fast binary classification of codebase files into "noise" (clutter) or "signal" (valuable) categories

**Intent Type**: CLASSIFICATION

**Agent**: gemma (270M, 50-100ms inference)

---

## Task

You are Gemma, a fast binary classifier. Your job is to analyze individual files and label them as either NOISE (files that clutter the codebase) or SIGNAL (files that provide value). You do NOT make cleanup decisions - you only label files with high confidence.

**Key Constraint**: You are a 270M parameter model optimized for SPEED and SIMPLE PATTERN MATCHING. You cannot perform complex reasoning or strategic planning. You classify files based on explicit rules.

---

## Instructions (For Gemma Agent)

### 1. FILE EXTENSION CHECK
**Rule**: IF file_extension in NOISE_EXTENSIONS THEN label="noise", category="file_type_noise"

**NOISE_EXTENSIONS**:
- `.jsonl` (unless in critical paths: `data/`, `modules/*/telemetry/`)
- `.tmp`, `.temp`, `.bak`, `.backup`
- `.log` (unless in `logs/`, `modules/*/logs/`)
- `.cache`, `.pyc`, `__pycache__/`
- `.swp`, `.swo`, `.DS_Store`, `Thumbs.db`

**Expected Pattern**: `extension_check_executed=True`

**Steps**:
1. Extract `file_extension` from context
2. Check if extension matches NOISE_EXTENSIONS list
3. If match → `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}`
4. If no match → Continue to next check
5. Log: `{"pattern": "extension_check_executed", "value": true, "extension": file_extension}`

**Examples**:
- ✅ `chat_history_20251015.jsonl` → NOISE (jsonl outside critical paths)
- ✅ `debug.log.tmp` → NOISE (temp file)
- ❌ `data/foundup.db` → SIGNAL (database in critical path)
- ❌ `README.md` → SIGNAL (documentation)

---

### 2. AGE CHECK (ROTTING DATA)
**Rule**: IF file_extension in ['.jsonl', '.log', '.json'] AND last_modified_days > 30 AND file_size_bytes > 1_000_000 THEN label="noise", category="rotting_data"

**Expected Pattern**: `age_check_executed=True`

**Steps**:
1. Check if `file_extension in ['.jsonl', '.log', '.json']`
2. Check if `last_modified_days > 30`
3. Check if `file_size_bytes > 1_000_000` (1MB)
4. If ALL three conditions → `{"label": "noise", "category": "rotting_data", "confidence": 0.85}`
5. Else → Continue to next check
6. Log: `{"pattern": "age_check_executed", "value": true, "age_days": last_modified_days, "size_bytes": file_size_bytes}`

**Examples**:
- ✅ `old_chat_log_20250915.jsonl` (45 days old, 2MB) → NOISE
- ❌ `recent_telemetry.jsonl` (5 days old, 500KB) → SIGNAL
- ❌ `archive/legacy_data.json` (60 days old, 500 bytes) → SIGNAL (small, likely intentional archive)

---

### 3. BACKUP FILE CHECK
**Rule**: IF filename contains ['backup', '_bak', 'copy', 'old_', 'temp_'] THEN label="noise", category="backup_file"

**Expected Pattern**: `backup_check_executed=True`

**Steps**:
1. Extract filename (without path) from `file_path`
2. Convert filename to lowercase
3. Check if any of these substrings appear: `['backup', '_bak', 'copy', 'old_', 'temp_']`
4. If match → `{"label": "noise", "category": "backup_file", "confidence": 0.90}`
5. Else → Continue to next check
6. Log: `{"pattern": "backup_check_executed", "value": true, "filename": filename}`

**Examples**:
- ✅ `main.py.backup` → NOISE
- ✅ `old_config.json` → NOISE
- ✅ `temp_analysis.md` → NOISE
- ❌ `main.py` → SIGNAL
- ❌ `config.json` → SIGNAL

---

### 4. DIRECTORY CONTEXT CHECK
**Rule**: IF parent_directory in NOISE_DIRECTORIES THEN label="noise", category="noise_directory"

**NOISE_DIRECTORIES**:
- `__pycache__/`
- `.git/` (unless `.git/config` or `.git/hooks/`)
- `node_modules/`
- `.cache/`
- `temp/`, `tmp/`
- `backups/`
- `archive/` (unless explicitly needed)

**Expected Pattern**: `directory_check_executed=True`

**Steps**:
1. Extract `parent_directory` from `file_path`
2. Check if parent directory ends with any NOISE_DIRECTORIES patterns
3. If match → `{"label": "noise", "category": "noise_directory", "confidence": 0.95}`
4. Else → Continue to next check
5. Log: `{"pattern": "directory_check_executed", "value": true, "parent_dir": parent_directory}`

**Examples**:
- ✅ `__pycache__/module.cpython-39.pyc` → NOISE
- ✅ `temp/scratch_work.txt` → NOISE
- ❌ `src/main.py` → SIGNAL
- ❌ `docs/README.md` → SIGNAL

---

### 5. CRITICAL PATH OVERRIDE
**Rule**: IF file_path matches CRITICAL_PATHS THEN label="signal", category="critical_file" (OVERRIDE all previous noise labels)

**CRITICAL_PATHS**:
- `data/foundup.db` (SQLite database)
- `modules/*/src/*.py` (source code)
- `modules/*/tests/*.py` (test files)
- `WSP_framework/src/*.md` (WSP protocols)
- `*.md` (documentation - README, INTERFACE, ModLog, CLAUDE)
- `requirements.txt`, `pyproject.toml`, `setup.py`
- `.env` (credentials - DO NOT DELETE)
- `holo_index/`, `main.py`, `NAVIGATION.py`

**Expected Pattern**: `critical_path_check_executed=True`

**Steps**:
1. Check if `file_path` matches any CRITICAL_PATHS pattern
2. If match → `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (OVERRIDE previous label)
3. Else → Keep current label from previous checks
4. Log: `{"pattern": "critical_path_check_executed", "value": true, "is_critical": bool}`

**Examples**:
- ✅ `data/foundup.db` → SIGNAL (even if large/old)
- ✅ `modules/communication/livechat/src/chat_sender.py` → SIGNAL
- ✅ `README.md` → SIGNAL
- ❌ `temp/debug.log` → NOISE (not in critical paths)

---

### 6. DEFAULT CLASSIFICATION
**Rule**: IF no previous checks matched THEN label="signal", category="unknown_keep_safe", confidence=0.5

**Expected Pattern**: `default_classification_executed=True`

**Steps**:
1. If no label assigned after all checks → Assume SIGNAL (safe default)
2. Assign low confidence (0.5) to indicate uncertainty
3. Log: `{"pattern": "default_classification_executed", "value": true}`
4. Output: `{"label": "signal", "category": "unknown_keep_safe", "confidence": 0.5}`

**Examples**:
- ✅ `unknown_file.xyz` → SIGNAL (unknown, keep safe)
- ✅ `custom_script.sh` → SIGNAL (unknown, keep safe)

---

## Expected Patterns Summary

Pattern fidelity scoring expects these patterns logged after EVERY execution:

```json
{
  "execution_id": "exec_gemma_001",
  "file_path": "/path/to/file.ext",
  "patterns": {
    "extension_check_executed": true,
    "age_check_executed": true,
    "backup_check_executed": true,
    "directory_check_executed": true,
    "critical_path_check_executed": true,
    "default_classification_executed": false
  },
  "label": "noise",
  "category": "file_type_noise",
  "confidence": 0.95,
  "execution_time_ms": 45
}
```

**Fidelity Calculation**: `(patterns_executed / 6)` - All 6 checks should run every time

---

## Output Contract (EXECUTION-READY per First Principles)

**Format**: JSON Lines (JSONL) appended to `labels.jsonl` + autonomous cleanup script

**Schema**:
```json
{
  "execution_id": "exec_gemma_001",
  "timestamp": "2025-10-22T01:59:00Z",
  "file_path": "O:/Foundups-Agent/temp/debug.log",
  "file_extension": ".log",
  "file_size_bytes": 1500000,
  "last_modified_days": 45,
  "parent_directory": "temp/",
  "label": "noise",
  "category": "rotting_data",
  "confidence": 0.85,

  "cleanup_priority_mps": {
    "complexity": 1,
    "complexity_reason": "Trivial - simple file deletion",
    "importance": 2,
    "importance_reason": "Minor - frees disk space",
    "deferability": 1,
    "deferability_reason": "Can defer - not blocking operations",
    "impact": 1,
    "impact_reason": "Minimal - temp/debug file",
    "total": 5,
    "priority": "P3"
  },

  "suggested_cleanup_agent": {
    "agent": "qwen_cleanup_strategist_v1",
    "confidence": 0.95,
    "autonomous_capable": true,
    "requires_0102_approval": false,
    "execution_command": "rm \"O:/Foundups-Agent/temp/debug.log\"",
    "estimated_tokens": 30,
    "estimated_time_seconds": 1
  },

  "dependency_check": {
    "imported_by_modules": [],
    "referenced_in_docs": [],
    "git_tracked": false,
    "safe_to_delete": true,
    "dependency_warning": null
  },

  "verification": {
    "verify_command": "test ! -f \"O:/Foundups-Agent/temp/debug.log\"",
    "success_criteria": "File does not exist after deletion",
    "rollback_command": "git checkout \"O:/Foundups-Agent/temp/debug.log\"  # If git tracked"
  },

  "patterns_executed": {
    "extension_check_executed": true,
    "age_check_executed": true,
    "backup_check_executed": true,
    "directory_check_executed": true,
    "critical_path_check_executed": true,
    "default_classification_executed": false
  },

  "execution_time_ms": 52
}
```

**Autonomous Cleanup Script** (Generated after classification):
```bash
#!/bin/bash
# Auto-generated cleanup script from gemma_noise_detector
# Execution ID: exec_gemma_001
# Generated: 2025-10-22T01:59:00Z

set -e  # Exit on error

echo "=== Gemma Noise Detector Cleanup ==="
echo "Total files classified: 25"
echo "Noise files (safe to delete): 18"
echo "Signal files (keep): 7"
echo ""

# P3 Low Priority Cleanup (Autonomous - No Approval Required)
echo "[1/18] Deleting temp/debug.log (MPS: 5, rotting_data)..."
rm "O:/Foundups-Agent/temp/debug.log"
test ! -f "O:/Foundups-Agent/temp/debug.log" && echo "✓ Verified" || echo "✗ Failed"

# ... (repeat for other noise files)

echo ""
echo "=== Cleanup Complete ==="
echo "Files deleted: 18/18"
echo "Disk space freed: 45MB"
echo "Verification: All deletions confirmed"
```

**Destination Files**:
- `data/gemma_noise_labels.jsonl` - Classification results
- `data/autonomous_cleanup_script.sh` - Executable cleanup script

---

## Benchmark Test Cases

### Test Set 1: File Extension Noise (10 cases)
1. Input: `chat_history.jsonl` (not in data/) → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: JSONL outside critical path)
2. Input: `data/foundup_telemetry.jsonl` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Critical path override)
3. Input: `debug.log` (not in logs/) → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: Log file outside critical path)
4. Input: `modules/livechat/logs/daemon.log` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Logs in module)
5. Input: `temp_analysis.tmp` → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: Temp file)
6. Input: `config.json.bak` → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: Backup file)
7. Input: `__pycache__/module.pyc` → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: Cache file)
8. Input: `.DS_Store` → Expected: `{"label": "noise", "category": "file_type_noise", "confidence": 0.95}` (Reason: System file)
9. Input: `README.md` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Markdown docs)
10. Input: `main.py` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Source code)

### Test Set 2: Rotting Data (5 cases)
1. Input: `old_chat.jsonl` (60 days, 2MB) → Expected: `{"label": "noise", "category": "rotting_data", "confidence": 0.85}` (Reason: Old + large JSONL)
2. Input: `recent_log.jsonl` (5 days, 500KB) → Expected: `{"label": "signal", "category": "unknown_keep_safe", "confidence": 0.5}` (Reason: Recent, small)
3. Input: `ancient_archive.json` (90 days, 3MB) → Expected: `{"label": "noise", "category": "rotting_data", "confidence": 0.85}` (Reason: Old + large JSON)
4. Input: `archive/legacy.json` (100 days, 500 bytes) → Expected: `{"label": "signal", "category": "unknown_keep_safe", "confidence": 0.5}` (Reason: Small, likely intentional)
5. Input: `data/foundup.db` (120 days, 50MB) → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Critical path override)

### Test Set 3: Backup Files (5 cases)
1. Input: `main.py.backup` → Expected: `{"label": "noise", "category": "backup_file", "confidence": 0.90}` (Reason: Backup suffix)
2. Input: `old_config.json` → Expected: `{"label": "noise", "category": "backup_file", "confidence": 0.90}` (Reason: "old_" prefix)
3. Input: `temp_script.sh` → Expected: `{"label": "noise", "category": "backup_file", "confidence": 0.90}` (Reason: "temp_" prefix)
4. Input: `module_copy.py` → Expected: `{"label": "noise", "category": "backup_file", "confidence": 0.90}` (Reason: "copy" suffix)
5. Input: `config.json` → Expected: `{"label": "signal", "category": "unknown_keep_safe", "confidence": 0.5}` (Reason: No backup pattern)

### Test Set 4: Directory Context (5 cases)
1. Input: `__pycache__/module.cpython-39.pyc` → Expected: `{"label": "noise", "category": "noise_directory", "confidence": 0.95}` (Reason: Pycache dir)
2. Input: `temp/scratch.txt` → Expected: `{"label": "noise", "category": "noise_directory", "confidence": 0.95}` (Reason: Temp dir)
3. Input: `backups/old_data.json` → Expected: `{"label": "noise", "category": "noise_directory", "confidence": 0.95}` (Reason: Backups dir)
4. Input: `src/module.py` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Source directory)
5. Input: `docs/guide.md` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Docs directory)

### Test Set 5: Critical Path Override (5 cases)
1. Input: `data/foundup.db` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Database)
2. Input: `modules/livechat/src/chat_sender.py` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Module source)
3. Input: `WSP_framework/src/WSP_96.md` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: WSP protocol)
4. Input: `requirements.txt` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Python deps)
5. Input: `.env` → Expected: `{"label": "signal", "category": "critical_file", "confidence": 1.0}` (Reason: Credentials - never delete)

**Total**: 30 test cases across 5 categories

---

## Learning Feedback (Per First Principles)

**Pattern Extraction from Classification Run**:
```json
{
  "execution_summary": {
    "total_files_classified": 25,
    "noise_files": 18,
    "signal_files": 7,
    "average_confidence": 0.88,
    "execution_time_total_ms": 1300
  },

  "classification_accuracy": {
    "extension_check": {"accuracy": 0.95, "false_positives": 1, "false_negatives": 0},
    "age_check": {"accuracy": 0.85, "false_positives": 2, "false_negatives": 1},
    "backup_check": {"accuracy": 0.90, "false_positives": 1, "false_negatives": 1},
    "directory_check": {"accuracy": 0.92, "false_positives": 0, "false_negatives": 2},
    "critical_path_override": {"accuracy": 1.0, "false_positives": 0, "false_negatives": 0}
  },

  "pattern_insights": [
    "JSONL files outside data/ consistently classified as noise (12/12 correct)",
    "Log files in module logs/ directories always kept as signal (5/5 correct)",
    "Backup suffixes (.backup, _copy) detected with 90% accuracy",
    "Age threshold (>30 days + >1MB) effective for rotting_data (8/9 correct)",
    "Critical path override (WSP_framework/, modules/) never misclassified (10/10)"
  ],

  "false_positive_analysis": {
    "total_false_positives": 4,
    "cases": [
      {
        "file": "archive/important_legacy.json",
        "classified_as": "noise (rotting_data)",
        "actual_label": "signal",
        "reason": "Age check (90 days) didn't account for intentional archiving",
        "fix": "Add archive/ directory to critical path override"
      },
      {
        "file": "temp_experiment_results.csv",
        "classified_as": "noise (backup_file)",
        "actual_label": "signal",
        "reason": "temp_ prefix too aggressive",
        "fix": "Check file size - if >10MB likely important experiment data"
      }
    ]
  },

  "future_improvements": [
    "Add git tracking check (if git tracked → signal)",
    "Semantic analysis: parse JSONL files to detect telemetry vs garbage",
    "Learn from user corrections (if user restores deleted file → update patterns)",
    "Add dependency graph check (if imported by module → signal)",
    "Integrate with module health checks (if module references file → signal)"
  ],

  "autonomous_cleanup_stats": {
    "files_queued_for_deletion": 18,
    "estimated_disk_space_freed_mb": 45,
    "mps_p3_low_priority": 15,
    "mps_p2_medium_priority": 3,
    "requires_0102_approval": 0,
    "autonomous_execution_ready": true
  },

  "store_to": "holo_index/adaptive_learning/noise_detection_patterns.jsonl"
}
```

**First Principles Additions**:
- ✅ **MPS Scoring**: cleanup_priority_mps per file (deletion priority)
- ✅ **Agent Mapping**: suggested_cleanup_agent (qwen_cleanup_strategist)
- ✅ **Executable Script**: autonomous_cleanup_script.sh (complete bash script)
- ✅ **Verification**: verify_command per file (confirm deletion)
- ✅ **Dependency Check**: dependency_check.safe_to_delete validation
- ✅ **Learning Feedback**: Classification accuracy + false positive analysis + future improvements
- ✅ **Rollback**: rollback_command (git checkout if git tracked)

---

## Success Criteria

- ✅ Pattern fidelity ≥ 90% (all 6 checks execute every time)
- ✅ Outcome quality ≥ 85% (correct labels on benchmark tests)
- ✅ Zero false negatives on critical files (.env, data/foundup.db, src/*.py)
- ✅ False positive rate < 5% (max 1-2 signal files mislabeled as noise)
- ✅ Inference speed < 100ms per file (Gemma 270M optimization)
- ✅ All outputs written to JSONL with complete schema

---

## Safety Constraints

**NEVER CLASSIFY AS NOISE**:
- `.env` files (credentials)
- `data/foundup.db` (SQLite database)
- `modules/*/src/*.py` (source code)
- `WSP_framework/src/*.md` (WSP protocols)
- `requirements.txt`, `pyproject.toml`, `setup.py`

**When in doubt → SIGNAL** (safe default)

---

## Next Phase

After 100 executions with ≥90% fidelity:
1. Promote to staged for extended testing
2. Qwen reads `labels.jsonl` for strategic cleanup planning
3. 0102 validates cleanup plan with HoloIndex research + WSP scoring
