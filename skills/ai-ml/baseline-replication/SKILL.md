/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] SKILL skill for research workflows [ground:given] [conf:0.95] [state:confirmed]
category: research
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic research processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "research",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["SKILL", "research", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

name: baseline-replication
description: "Replicate published ML baseline experiments with exact reproducibility\
  \ (\xB11% tolerance) for Deep Research SOP Pipeline D. Use when validating baselines,\
  \ reproducing experiments, verifying published results, or preparing for novel method\
  \ development."
version: 1.0.0
category: research
tags:
- research
- analysis
- planning
author: ruv
---

# Baseline Replication

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview
Replicates published machine learning baseline methods with exact reproducibility, ensuring results match within ±1% tolerance. This skill implements Deep Research SOP Pipeline D baseline validation, which is a prerequisite for developing novel methods.

## Prerequisites
- Python 3.8+ with PyTorch/TensorFlow
- Docker (for reproducibility)
- Git and Git LFS
- Access to datasets (HuggingFace, academic repositories)

## What This Skill Does
1. **Extracts methodology** from papers and code repositories
2. **Validates datasets** match baseline specifications exactly
3. **Implements baseline** with exact hyperparameters
4. **Runs experiments** with deterministic settings
5. **Validates results** within ±1% statistical tolerance
6. **Creates reproducibility package** tested in fresh Docker environment
7. **Generates Quality Gate 1 validation** checklist

---

## Quick Start (30 minutes)

### Basic Replication
```bash
# 1. Specify baseline to replicate
BASELINE_PAPER="BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2019)"
BASELINE_CODE="https://github.com/google-research/bert"
TARGET_METRIC="Accuracy on SQuAD 2.0"
PUBLISHED_RESULT=0.948

# 2. Run replication workflow
./scripts/replicate-baseline.sh \
  --paper "$BASELINE_PAPER" \
  --code "$BASELINE_CODE" \
  --metric "$TARGET_METRIC" \
  --expected "$PUBLISHED_RESULT"

# 3. Review results
cat output/baseline-bert/replication-report.md
```

Expected output:
```
✓ Paper analyzed: Extracted 47 hyperparameters
✓ Dataset validated: SQuAD 2.0 matches baseline
✓ Implementation complete: 12 BERT layers, 110M parameters
✓ Training complete: 3 epochs, 26.3 GPU hours
✓ Results validated: 0.945 vs 0.948 (within ±1% tolerance)
✓ Reproducibility verified: 3/3 fresh reproductions successful
→ Quality Gate 1: APPROVED
```

---

## Step-by-Step Guide

### Phase 1: Paper Analysis (15 minutes)

#### Extract Methodology
```bash
# Coordinate with researcher agent
./scripts/analyze-paper.sh --paper "arXiv:2103.00020"
```

The script extracts:
- Model architecture (layers, hidden sizes, attention heads)
- Training hyperparameters (learning rate, batch size, warmup)
- Optimization details (optimizer type, weight decay, dropout)
- Dataset specifications (splits, preprocessing, tokenization)
- Evaluation metrics (primary and secondary)

**Output**: `baseline-specification.md` with all extracted details

#### Validate Completeness
```bash
# Check for missing hyperparameters
./scripts/validate-spec.sh baseline-specification.md
```

**Common Missing Details**:
- Learning rate schedule (linear warmup, cosine decay)
- Random seeds (NumPy, PyTorch, Python)
- Hardware specifications (GPU type, memory)
- Framework versions (PyTorch 1.7 vs 1.13 numerical differences)

**If details missing**:
1. Check paper supplements
2. Check official code config files
3. Check GitHub issues
4. Contact authors

---

### Phase 2: Dataset Validation (20 minutes)

#### Coordinate with data-steward Agent
```bash
# Validate dataset matches baseline specs
./scripts/validate-dataset.sh \
  --dataset "SQuAD 2.0" \
  --splits "train:130k,dev:12k" \
  --preprocessing "WordPiece tokenization, max_length=384"
```

**data-steward checks**:
- Exact dataset version (v2.0, not v1.1)
- Sample counts match (training: 130,319 examples)
- Data splits match (80/10/10 vs 90/10)
- Preprocessing matches (lower-casing, accent stripping)
- Checksum validation (SHA256 hashes)

**Output**: `dataset-validation-report.md`

---

### Ph

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/research/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
