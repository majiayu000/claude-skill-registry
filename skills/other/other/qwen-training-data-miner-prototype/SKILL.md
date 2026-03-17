---
name: qwen_training_data_miner_prototype
description: Qwen Training Data Miner (Prototype)
version: 1.0
author: 0102_wre_team
agents: [qwen]
dependencies: [pattern_memory, libido_monitor]
domain: autonomous_operations
---

# Qwen Training Data Miner (Prototype)

---
# Metadata (YAML Frontmatter)
skill_id: qwen_training_data_miner_v1_prototype
name: qwen_training_data_miner
description: Mine 012.txt for domain-specific training examples (MPS scoring, WSP patterns, decision rationale)
version: 1.0_prototype
author: 0102_design
created: 2025-10-22
agents: [qwen]
primary_agent: qwen
intent_type: GENERATION
promotion_state: prototype
pattern_fidelity_threshold: 0.90
test_status: needs_validation

# MCP Orchestration
mcp_orchestration: true
breadcrumb_logging: true
owning_dae: doc_dae
execution_phase: 1
next_skill: gemma_domain_trainer_v1_prototype

# Input/Output Contract
inputs:
  - source_file: "O:/Foundups-Agent/012.txt (98,400 lines)"
  - domain: "Target knowledge domain (mps_scoring, wsp_application, roadmap_analysis, etc.)"
  - pattern_type: "Type of pattern to extract (numeric_examples, decision_trees, rationale_chains)"
  - min_examples: "Minimum number of examples to extract (default: 50)"
outputs:
  - data/training_datasets/{domain}_training_data.json: "Instruction-tuning dataset"
  - data/training_datasets/{domain}_pattern_summary.json: "Pattern analysis metadata"
  - execution_id: "Unique execution identifier for breadcrumb tracking"

# Dependencies
dependencies:
  data_stores:
    - name: 012_scrapbook
      type: text
      path: O:/Foundups-Agent/012.txt
  mcp_endpoints:
    - endpoint_name: holo_index
      methods: [semantic_search]
  throttles: []
  required_context:
    - domain: "Knowledge domain to mine"
    - pattern_regex: "Regex pattern for extraction"

# Metrics Configuration
metrics:
  pattern_fidelity_scoring:
    enabled: true
    frequency: every_execution
    scorer_agent: gemma
    write_destination: modules/infrastructure/wre_core/recursive_improvement/metrics/qwen_training_data_miner_fidelity.json
  promotion_criteria:
    min_pattern_fidelity: 0.90
    min_outcome_quality: 0.85
    min_execution_count: 100
    required_test_pass_rate: 0.95
---

# Qwen Training Data Miner

**Purpose**: Mine 012.txt (0102's decision history) for domain-specific training examples to train Gemma models

**Intent Type**: GENERATION

**Agent**: qwen (1.5B, 32K context - can hold large sections of 012.txt)

---

## Task

You are Qwen, a training data miner. Your job is to read 012.txt (98,400 lines of 0102's decision-making history) and extract high-quality training examples for specific knowledge domains. You create instruction-tuning datasets that Gemma can learn from.

**Key Capability**: Pattern recognition, example extraction, quality filtering

**Domains You Can Mine**:
1. **mps_scoring** - WSP 15 scoring examples with numeric calculations
2. **wsp_application** - How WSPs are applied to real problems
3. **roadmap_analysis** - Project planning, completion tracking
4. **readme_patterns** - Documentation structure, best practices
5. **modlog_updates** - Change documentation patterns
6. **first_principles** - Occam's Razor reasoning chains

---

## Instructions (For Qwen Agent)

### 1. LOAD SOURCE FILE
**Rule**: Read 012.txt in chunks (32K token window)

**Expected Pattern**: `source_loaded=True`

**Steps**:
1. Open `O:/Foundups-Agent/012.txt`
2. Count total lines (should be ~98,400)
3. Calculate chunk size (fit within 32K context)
4. Load first chunk for analysis
5. Log: `{"pattern": "source_loaded", "value": true, "total_lines": 98400, "chunk_size": 5000}`

---

### 2. IDENTIFY DOMAIN PATTERNS
**Rule**: Search for domain-specific patterns using regex and semantic matching

**Expected Pattern**: `domain_patterns_identified=True`

**Domain-Specific Patterns**:

#### MPS Scoring Domain
```python
patterns = [
    r"MPS.*Score:?\s*(\d+)",
    r"Complexity.*(\d)\s*,?\s*Importance.*(\d)\s*,?\s*Deferability.*(\d)\s*,?\s*Impact.*(\d)",
    r"Priority:?\s*(P[0-4])",
    r"MPS.*\(C:(\d),\s*I:(\d),\s*D:(\d),\s*P:(\d)\)"
]
```

#### WSP Application Domain
```python
patterns = [
    r"WSP\s*(\d+).*compliance",
    r"WSP\s*(\d+).*violation",
    r"following\s+WSP\s*(\d+)",
    r"applied\s+WSP\s*(\d+)"
]
```

#### Roadmap Analysis Domain
```python
patterns = [
    r"roadmap.*complete",
    r"roadmap.*incomplete",
    r"roadmap.*needs.*update",
    r"Phase\s*(\d+).*status",
    r"TODO.*implement"
]
```

**Steps**:
1. For target domain, compile regex patterns
2. Scan 012.txt for matching lines
3. Extract context (5 lines before/after match)
4. Store matches with line numbers
5. Log: `{"pattern": "domain_patterns_identified", "value": true, "matches_found": N}`

---

### 3. EXTRACT TRAINING EXAMPLES
**Rule**: Convert matched patterns into instruction-tuning format

**Expected Pattern**: `examples_extracted=True`

**Instruction-Tuning Format**:
```json
{
  "instruction": "Apply WSP 15 MPS scoring to this task",
  "input": {
    "task_description": "Migrate agent_permissions to SQLite",
    "context": "Database consolidation, 21 tests passing, high priority"
  },
  "output": {
    "complexity": 3,
    "complexity_reason": "Moderate - requires schema design + migration",
    "importance": 5,
    "importance_reason": "Essential - blocks other migrations",
    "deferability": 5,
    "deferability_reason": "Cannot defer - P0 priority",
    "impact": 4,
    "impact_reason": "Major - enables autonomous permission system",
    "mps_total": 17,
    "priority": "P0"
  },
  "source": "012.txt:line_5234",
  "quality_score": 0.95
}
```

**Steps**:
1. For each match, extract:
   - **Instruction**: What task is being performed?
   - **Input**: What context/data is provided?
   - **Output**: What is the correct answer/decision?
   - **Source**: Line number for verification
2. Quality filter:
   - Complete examples only (has input + output)
   - Clear reasoning (not ambiguous)
   - Correct format (follows pattern)
3. Assign quality score (0.0-1.0)
4. Log: `{"pattern": "examples_extracted", "value": true, "total_examples": N, "high_quality": M}`

---

### 4. QUALITY FILTERING
**Rule**: Only keep examples with quality_score >= 0.85

**Expected Pattern**: `quality_filtering_applied=True`

**Quality Criteria**:
- ✅ Complete (has instruction + input + output)
- ✅ Clear reasoning (rationale provided)
- ✅ Correct format (matches instruction-tuning schema)
- ✅ Verifiable (can trace back to source line)
- ✅ Unambiguous (single correct interpretation)

**Steps**:
1. Review each extracted example
2. Score on 5 criteria (0.2 per criterion)
3. Filter: keep only if score >= 0.85 (4/5 criteria)
4. Remove duplicates (same input/output pattern)
5. Log: `{"pattern": "quality_filtering_applied", "value": true, "kept": N, "filtered": M}`

---

### 5. GENERATE PATTERN SUMMARY
**Rule**: Analyze extracted examples for meta-patterns

**Expected Pattern**: `pattern_summary_generated=True`

**Summary Metadata**:
```json
{
  "domain": "mps_scoring",
  "total_examples": 73,
  "high_quality_examples": 58,
  "quality_distribution": {
    "0.95-1.0": 23,
    "0.90-0.94": 20,
    "0.85-0.89": 15
  },
  "common_patterns": [
    "P0 tasks: MPS 16-20 (23 examples)",
    "P1 tasks: MPS 13-15 (19 examples)",
    "Complexity 3-4 most common (database migrations, refactoring)"
  ],
  "coverage_analysis": {
    "p0_examples": 23,
    "p1_examples": 19,
    "p2_examples": 12,
    "p3_examples": 3,
    "p4_examples": 1
  },
  "recommended_use": "Train Gemma on MPS scoring for cleanup tasks, project prioritization"
}
```

**Steps**:
1. Count examples by category/pattern
2. Identify common themes
3. Assess coverage (are all cases represented?)
4. Generate training recommendations
5. Log: `{"pattern": "pattern_summary_generated", "value": true}`

---

### 6. WRITE TRAINING DATASET
**Rule**: Output JSON file with instruction-tuning examples

**Expected Pattern**: `training_dataset_written=True`

**Output Format** (EXECUTION-READY per First Principles):
```json
{
  "dataset_id": "mps_scoring_training_v1",
  "created": "2025-10-22T02:30:00Z",
  "source": "012.txt (lines 1-98400)",
  "domain": "mps_scoring",
  "total_examples": 58,
  "quality_threshold": 0.85,

  "domain_priority_mps": {
    "complexity": 2,
    "complexity_reason": "Easy - pattern extraction from 012.txt",
    "importance": 4,
    "importance_reason": "Critical - enables autonomous MPS scoring",
    "deferability": 3,
    "deferability_reason": "Moderate - other wardrobes can be trained first",
    "impact": 5,
    "impact_reason": "Critical - foundation for cleanup automation",
    "total": 14,
    "priority": "P1",
    "training_order": 1
  },

  "examples": [
    {
      "example_id": "mps_001",
      "instruction": "...",
      "input": {...},
      "output": {...},
      "source": "012.txt:line_5234",
      "quality_score": 0.95
    },
    ...
  ],

  "metadata": {
    "pattern_summary": {...},
    "coverage_analysis": {...},
    "recommended_use": "..."
  },

  "recommended_wardrobe_config": {
    "wardrobe_id": "gemma_mps_scorer_v1",
    "lora_rank": 8,
    "learning_rate": 0.0002,
    "epochs": 3,
    "expected_accuracy": 0.87,
    "use_cases": [
      "Cleanup task prioritization",
      "Project scoring",
      "Issue triage"
    ]
  },

  "autonomous_execution": {
    "capable": true,
    "agent": "gemma_domain_trainer_v1",
    "confidence": 0.90,
    "estimated_tokens": 200,
    "estimated_time_seconds": 600,
    "requires_0102_approval": false,
    "execution_command": "python -m modules.infrastructure.wsp_orchestrator.src.wsp_orchestrator --skill gemma_domain_trainer --domain mps_scoring --dataset data/training_datasets/mps_scoring_training_data.json"
  },

  "verification": {
    "verify_command": "test -f data/training_datasets/mps_scoring_training_data.json && jq '.total_examples' data/training_datasets/mps_scoring_training_data.json",
    "success_criteria": "File exists + total_examples >= 50 + quality_threshold >= 0.85",
    "validation_script": "python -c \"import json; d=json.load(open('data/training_datasets/mps_scoring_training_data.json')); assert d['total_examples'] >= 50; assert d['quality_threshold'] >= 0.85; print('✓ Dataset validated')\""
  },

  "learning_feedback": {
    "pattern_extraction_stats": {
      "total_patterns_found": 73,
      "high_quality_kept": 58,
      "filter_rate": 0.79,
      "common_filter_reasons": [
        "Incomplete example (missing rationale) - 8 filtered",
        "Ambiguous input - 5 filtered",
        "Duplicate pattern - 2 filtered"
      ]
    },
    "domain_insights": [
      "P0 tasks: MPS 16-20 (23 examples) - database migrations, critical bugs",
      "P1 tasks: MPS 13-15 (19 examples) - feature requests, refactoring",
      "Complexity 3-4 most common - moderate difficulty tasks"
    ],
    "future_improvements": [
      "Add semantic deduplication (beyond exact match)",
      "Extract negative examples (what NOT to do)",
      "Mine multi-step reasoning chains for complex decisions"
    ],
    "store_to": "holo_index/adaptive_learning/training_data_mining_patterns.jsonl"
  }
}
```

**Destination**: `data/training_datasets/{domain}_training_data.json`

**Steps**:
1. Create directory `data/training_datasets/` if not exists
2. Calculate domain_priority_mps (which domain should be trained first?)
3. Generate recommended_wardrobe_config (LoRA hyperparameters)
4. Write training dataset JSON with all First Principles fields
5. Generate autonomous_execution command (can Gemma trainer auto-execute?)
6. Create verification script (validate dataset quality)
7. Extract learning_feedback (pattern extraction stats + future improvements)
8. Log: `{"pattern": "training_dataset_written", "value": true, "file_size_kb": N, "autonomous_ready": true}`

**First Principles Additions**:
- ✅ **MPS Scoring**: domain_priority_mps determines training order (which wardrobe first?)
- ✅ **Agent Mapping**: autonomous_execution.agent = gemma_domain_trainer_v1
- ✅ **Executable Command**: Can pipe to bash to start training automatically
- ✅ **Verification**: validation_script confirms dataset quality before training
- ✅ **Learning Feedback**: Stores pattern extraction stats for future mining improvements
- ✅ **Recommended Config**: Wardrobe hyperparameters (LoRA rank, learning rate, epochs)

---

## Expected Patterns Summary

```json
{
  "execution_id": "exec_qwen_miner_001",
  "skill_id": "qwen_training_data_miner_v1_prototype",
  "patterns": {
    "source_loaded": true,
    "domain_patterns_identified": true,
    "examples_extracted": true,
    "quality_filtering_applied": true,
    "pattern_summary_generated": true,
    "training_dataset_written": true
  },
  "total_examples_extracted": 73,
  "high_quality_examples": 58,
  "execution_time_ms": 3500
}
```

**Fidelity Calculation**: `(patterns_executed / 6)` - All 6 steps should run

---

## Domain Catalog

### 1. MPS Scoring Domain
**Purpose**: Train Gemma to apply WSP 15 MPS scoring
**Patterns**: Numeric scores, priority mapping, rationale
**Use Cases**: Cleanup prioritization, project planning, issue triage

### 2. WSP Application Domain
**Purpose**: Train Gemma to recognize WSP violations and applications
**Patterns**: WSP references, compliance checks, violation detection
**Use Cases**: Code review, documentation validation, architecture audits

### 3. Roadmap Analysis Domain
**Purpose**: Train Gemma to analyze project roadmaps
**Patterns**: Phase completion, TODO tracking, update detection
**Use Cases**: Project status reports, roadmap audits, completion tracking

### 4. README Patterns Domain
**Purpose**: Train Gemma to validate README structure
**Patterns**: Required sections, format consistency, completeness
**Use Cases**: Documentation quality checks, README generation

### 5. ModLog Updates Domain
**Purpose**: Train Gemma to generate ModLog entries
**Patterns**: Change descriptions, WSP references, rationale
**Use Cases**: Automated ModLog updates, change tracking

### 6. First Principles Domain
**Purpose**: Train Gemma to apply Occam's Razor reasoning
**Patterns**: Problem simplification, root cause analysis, decision trees
**Use Cases**: Debugging, architecture design, problem-solving

---

## Benchmark Test Cases

### Test Set 1: MPS Scoring Extraction (10 cases)
1. Input: "MPS Score: 16" → Expected: Extract as P0 example
2. Input: "Complexity: 3, Importance: 5, Deferability: 2, Impact: 4" → Expected: Calculate MPS = 14
3. Input: "Priority: P1" → Expected: Map to MPS 13-15 range
4. Input: Incomplete example (missing rationale) → Expected: Quality score < 0.85, filtered
5. Input: Duplicate example → Expected: Deduplicated

### Test Set 2: WSP Application Extraction (5 cases)
1. Input: "Following WSP 15 for scoring" → Expected: Extract WSP 15 application example
2. Input: "WSP 64 violation detected" → Expected: Extract violation example
3. Input: "WSP compliance: WSP 3, WSP 50" → Expected: Extract multi-WSP compliance
4. Input: Ambiguous WSP reference → Expected: Quality score < 0.85
5. Input: Clear WSP application with rationale → Expected: Quality score >= 0.90

### Test Set 3: Quality Filtering (5 cases)
1. Input: Complete example with all fields → Expected: Quality score = 1.0
2. Input: Missing rationale → Expected: Quality score = 0.8 (filtered)
3. Input: Ambiguous input → Expected: Quality score = 0.6 (filtered)
4. Input: Clear but partial example → Expected: Quality score = 0.85 (kept)
5. Input: Excellent example with source → Expected: Quality score = 0.95

**Total**: 20 test cases across 3 categories

---

## Success Criteria

- ✅ Pattern fidelity ≥ 90% (all 6 steps execute)
- ✅ Extract ≥ 50 high-quality examples per domain
- ✅ Quality threshold 0.85+ maintained
- ✅ Zero duplicate examples in output
- ✅ All examples have verifiable source (line number)
- ✅ Pattern summary provides actionable insights

---

## Next Phase: Gemma Training

After extraction, examples feed into `gemma_domain_trainer` skill:
1. Load training dataset
2. Fine-tune Gemma 270M on domain examples
3. Validate accuracy on held-out test set
4. Deploy trained model for domain-specific tasks

---

## Wardrobe Concept: Training as a Service

**Different "training wardrobes"** for different knowledge domains:
- `qwen_mps_scorer` - Trained on MPS scoring examples
- `qwen_wsp_auditor` - Trained on WSP compliance examples
- `qwen_roadmap_tracker` - Trained on roadmap analysis examples
- `qwen_readme_validator` - Trained on README patterns

**Each wardrobe**:
- Mines 012.txt for domain-specific patterns
- Trains Gemma on extracted examples
- Deploys as reusable skill
- Evolves as more examples accumulate

**Meta-skill**: `qwen_wardrobe_generator` - Automates creation of new training wardrobes for any domain!

---

**Status**: ✅ Ready for prototype testing - Mine 012.txt for MPS scoring examples first
