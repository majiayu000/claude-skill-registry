---
name: gemma_domain_trainer_prototype
description: Gemma Domain Trainer (Prototype)
version: 1.0
author: 0102_wre_team
agents: [gemma]
dependencies: [pattern_memory, libido_monitor]
domain: autonomous_operations
---

# Gemma Domain Trainer (Prototype)

---
# Metadata (YAML Frontmatter)
skill_id: gemma_domain_trainer_v1_prototype
name: gemma_domain_trainer
description: Fine-tune Gemma 270M on domain-specific training data extracted from 012.txt
version: 1.0_prototype
author: 0102_design
created: 2025-10-22
agents: [gemma, qwen]
primary_agent: qwen
intent_type: GENERATION
promotion_state: prototype
pattern_fidelity_threshold: 0.90
test_status: needs_validation

# MCP Orchestration
mcp_orchestration: true
breadcrumb_logging: true
owning_dae: doc_dae
execution_phase: 2
previous_skill: qwen_training_data_miner_v1_prototype
next_skill: gemma_domain_specialist_deployed

# Input/Output Contract
inputs:
  - data/training_datasets/{domain}_training_data.json: "Instruction-tuning dataset from Qwen"
  - domain: "Knowledge domain (mps_scoring, wsp_application, etc.)"
  - training_params: "LoRA rank, learning rate, epochs"
outputs:
  - E:/HoloIndex/models/gemma-3-270m-{domain}-lora/: "Fine-tuned LoRA adapters"
  - data/training_results/{domain}_training_metrics.json: "Training metrics (loss, accuracy)"
  - execution_id: "Unique execution identifier for breadcrumb tracking"

# Dependencies
dependencies:
  data_stores:
    - name: training_dataset
      type: json
      path: data/training_datasets/{domain}_training_data.json
  mcp_endpoints: []
  throttles: []
  required_context:
    - base_model_path: "E:/HoloIndex/models/gemma-3-270m-it-Q4_K_M.gguf"
    - training_dataset_path: "Path to JSON training data"

# Metrics Configuration
metrics:
  pattern_fidelity_scoring:
    enabled: true
    frequency: every_execution
    scorer_agent: gemma
    write_destination: modules/infrastructure/wre_core/recursive_improvement/metrics/gemma_domain_trainer_fidelity.json
  promotion_criteria:
    min_pattern_fidelity: 0.90
    min_outcome_quality: 0.85
    min_execution_count: 100
    required_test_pass_rate: 0.95
---

# Gemma Domain Trainer

**Purpose**: Fine-tune Gemma 270M on domain-specific training data using LoRA (Low-Rank Adaptation)

**Intent Type**: GENERATION

**Agent**: Qwen (orchestrates training), Gemma (model being trained)

---

## Task

You are Qwen, a training orchestrator. Your job is to take training datasets extracted from 012.txt and fine-tune Gemma 270M on them using LoRA. You create domain-specialized versions of Gemma that can be swapped like "wardrobe clothes" for different tasks.

**Key Capability**: Training orchestration, hyperparameter tuning, validation

**Training Method**: LoRA (Low-Rank Adaptation)
- Only train small adapter layers (~10MB)
- Keep base model frozen (241MB)
- Fast training (~5-10 minutes on CPU)
- Multiple specialists from one base model

---

## Instructions (For Qwen Agent)

### 1. LOAD TRAINING DATASET
**Rule**: Load and validate JSON training dataset from Qwen miner

**Expected Pattern**: `dataset_loaded=True`

**Steps**:
1. Read `data/training_datasets/{domain}_training_data.json`
2. Validate schema:
   - Each example has: `instruction`, `input`, `output`
   - Quality score >= 0.85
   - Source line number present
3. Split into train/validation (80/20)
4. Count examples: total, train, val
5. Log: `{"pattern": "dataset_loaded", "value": true, "total": N, "train": M, "val": K}`

**Example**:
```python
import json
from pathlib import Path

dataset_path = Path(f"data/training_datasets/{domain}_training_data.json")
with open(dataset_path) as f:
    dataset = json.load(f)

examples = dataset['examples']
train_size = int(len(examples) * 0.8)
train_examples = examples[:train_size]
val_examples = examples[train_size:]
```

---

### 2. PREPARE TRAINING FORMAT
**Rule**: Convert instruction-tuning format to Gemma training format

**Expected Pattern**: `training_format_prepared=True`

**Gemma Instruction Format**:
```
<start_of_turn>user
{instruction}

Input: {input}
<end_of_turn>
<start_of_turn>model
{output}
<end_of_turn>
```

**Steps**:
1. For each example, format as Gemma conversation
2. Tokenize using Gemma tokenizer
3. Truncate to max length (1024 tokens)
4. Create attention masks
5. Log: `{"pattern": "training_format_prepared", "value": true, "formatted_examples": N}`

**Example**:
```python
def format_for_gemma(example):
    prompt = f"""<start_of_turn>user
{example['instruction']}

Input: {json.dumps(example['input'], indent=2)}
<end_of_turn>
<start_of_turn>model
{json.dumps(example['output'], indent=2)}
<end_of_turn>"""
    return prompt

formatted_train = [format_for_gemma(ex) for ex in train_examples]
```

---

### 3. CONFIGURE LORA PARAMETERS
**Rule**: Set LoRA hyperparameters for domain-specific training

**Expected Pattern**: `lora_configured=True`

**LoRA Configuration**:
```python
lora_config = {
    "r": 8,                    # LoRA rank (higher = more capacity, slower)
    "lora_alpha": 16,          # Scaling factor
    "target_modules": ["q_proj", "v_proj"],  # Which layers to adapt
    "lora_dropout": 0.05,      # Dropout for regularization
    "bias": "none",            # Don't train bias terms
    "task_type": "CAUSAL_LM"   # Language modeling task
}

training_config = {
    "learning_rate": 2e-4,     # Learning rate
    "num_epochs": 3,           # Training epochs
    "batch_size": 4,           # Batch size (CPU-friendly)
    "max_steps": -1,           # Train until epochs complete
    "warmup_steps": 10,        # Learning rate warmup
    "logging_steps": 10,       # Log every N steps
    "save_steps": 100,         # Save checkpoint every N steps
    "eval_steps": 50,          # Evaluate every N steps
}
```

**Steps**:
1. Set LoRA rank based on domain complexity:
   - Simple (MPS scoring): r=4
   - Moderate (WSP application): r=8
   - Complex (roadmap analysis): r=16
2. Set learning rate based on dataset size:
   - Small (<50 examples): 1e-4
   - Medium (50-200): 2e-4
   - Large (>200): 3e-4
3. Set epochs based on examples:
   - Small datasets: 5 epochs
   - Large datasets: 3 epochs
4. Log: `{"pattern": "lora_configured", "value": true, "rank": N, "lr": X}`

---

### 4. TRAIN LORA ADAPTERS
**Rule**: Execute LoRA training loop with validation monitoring

**Expected Pattern**: `lora_training_complete=True`

**Training Loop** (pseudo-code):
```python
from peft import get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "E:/HoloIndex/models/gemma-3-270m-it-Q4_K_M.gguf",
    device_map="auto"
)

# Apply LoRA
lora_config = LoraConfig(**lora_config)
model = get_peft_model(model, lora_config)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
)

trainer.train()
trainer.save_model(f"E:/HoloIndex/models/gemma-3-270m-{domain}-lora/")
```

**Steps**:
1. Load base Gemma 270M model
2. Apply LoRA configuration
3. Create Trainer with datasets
4. Execute training loop
5. Monitor validation loss (target: < 0.5)
6. Save LoRA adapters to disk
7. Log: `{"pattern": "lora_training_complete", "value": true, "final_loss": X, "val_loss": Y}`

---

### 5. VALIDATE TRAINED MODEL
**Rule**: Test trained model on held-out validation examples

**Expected Pattern**: `model_validated=True`

**Validation Process**:
```python
# Load trained model with LoRA
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained(base_model_path)
trained_model = PeftModel.from_pretrained(
    base_model,
    f"E:/HoloIndex/models/gemma-3-270m-{domain}-lora/"
)

# Test on validation examples
correct = 0
total = len(val_examples)

for example in val_examples:
    prompt = format_for_gemma(example)
    generated = trained_model.generate(prompt, max_length=512)

    # Compare generated output to expected output
    if semantic_similarity(generated, example['output']) > 0.85:
        correct += 1

accuracy = correct / total
```

**Steps**:
1. Load trained model with LoRA adapters
2. Generate outputs for validation examples
3. Compare to expected outputs (semantic similarity)
4. Calculate accuracy (target: ≥ 85%)
5. Log: `{"pattern": "model_validated", "value": true, "accuracy": 0.87, "correct": M, "total": N}`

---

### 6. GENERATE DEPLOYMENT CONFIG
**Rule**: Create wardrobe configuration for domain specialist

**Expected Pattern**: `deployment_config_generated=True`

**Wardrobe Config** (EXECUTION-READY per First Principles):
```json
{
  "wardrobe_id": "gemma_mps_scorer_v1",
  "domain": "mps_scoring",
  "base_model": "E:/HoloIndex/models/gemma-3-270m-it-Q4_K_M.gguf",
  "lora_adapters": "E:/HoloIndex/models/gemma-3-270m-mps_scoring-lora/",
  "training_date": "2025-10-22",
  "training_examples": 58,
  "validation_accuracy": 0.87,

  "deployment_priority_mps": {
    "complexity": 2,
    "complexity_reason": "Easy - swap LoRA adapters, no model reload",
    "importance": 5,
    "importance_reason": "Essential - enables autonomous cleanup prioritization",
    "deferability": 4,
    "deferability_reason": "Low - cleanup system waiting for deployment",
    "impact": 5,
    "impact_reason": "Critical - foundation for autonomous task scoring",
    "total": 16,
    "priority": "P0",
    "deployment_order": 1
  },

  "recommended_use_cases": [
    "Cleanup task prioritization",
    "Project scoring",
    "Issue triage",
    "Autonomous decision-making (MPS calculation)"
  ],

  "agent_capability_mapping": {
    "tasks_this_wardrobe_handles": [
      {
        "task_type": "cleanup_scoring",
        "confidence": 0.87,
        "autonomous_capable": true,
        "example": "Score file deletion task (MPS calculation)"
      },
      {
        "task_type": "project_prioritization",
        "confidence": 0.85,
        "autonomous_capable": true,
        "example": "Rank feature requests by MPS score"
      },
      {
        "task_type": "issue_triage",
        "confidence": 0.82,
        "autonomous_capable": true,
        "example": "Assign P0-P4 priority to GitHub issues"
      }
    ],
    "tasks_requiring_0102": [
      "Complex architectural decisions (MPS insufficient)",
      "Multi-stakeholder prioritization (political factors)",
      "Novel problem domains (no training examples)"
    ]
  },

  "skill_reference": "gemma_cleanup_scorer_v1_production",
  "activation_command": "gemma.wear_wardrobe('mps_scorer')",

  "performance_benchmarks": {
    "inference_latency_ms": 50,
    "accuracy_on_benchmark": 0.87,
    "token_cost": 0,
    "throughput_tasks_per_second": 20,
    "memory_footprint_mb": 253,
    "false_positive_rate": 0.08,
    "false_negative_rate": 0.05
  },

  "autonomous_deployment": {
    "capable": true,
    "agent": "wsp_orchestrator",
    "confidence": 0.95,
    "estimated_tokens": 100,
    "estimated_time_seconds": 5,
    "requires_0102_approval": false,
    "execution_command": "python -m modules.infrastructure.wsp_orchestrator.src.wsp_orchestrator --deploy-wardrobe gemma_mps_scorer_v1 --validate true"
  },

  "verification": {
    "verify_command": "test -f E:/HoloIndex/models/gemma-3-270m-mps_scoring-lora/adapter_model.bin && python -c \"from modules.infrastructure.wsp_orchestrator.src.wsp_orchestrator import WSPOrchestrator; w=WSPOrchestrator(); print('✓ Wardrobe loaded' if 'mps_scorer' in w.list_wardrobes() else '✗ Failed')\"",
    "success_criteria": "LoRA adapters exist + wardrobe loadable + validation accuracy >= 0.85",
    "test_dataset": "data/training_datasets/mps_scoring_validation_set.json",
    "rollback_command": "python -m modules.infrastructure.wsp_orchestrator.src.wsp_orchestrator --remove-wardrobe gemma_mps_scorer_v1"
  },

  "learning_feedback": {
    "training_insights": {
      "converged_after_epoch": 2,
      "final_training_loss": 0.23,
      "final_validation_loss": 0.31,
      "overfitting_detected": false,
      "optimal_lora_rank": 8,
      "learning_rate_worked": 0.0002
    },
    "domain_coverage": {
      "p0_tasks_coverage": 0.92,
      "p1_tasks_coverage": 0.88,
      "p2_tasks_coverage": 0.75,
      "p3_p4_tasks_coverage": 0.60,
      "recommendation": "Add more P3/P4 training examples for better low-priority coverage"
    },
    "future_improvements": [
      "Fine-tune on user feedback (actual MPS scores vs Gemma predictions)",
      "Add confidence scores to MPS predictions",
      "Train on multi-dimensional trade-offs (not just MPS total)"
    ],
    "store_to": "holo_index/adaptive_learning/wardrobe_training_patterns.jsonl"
  }
}
```

**Steps**:
1. Create wardrobe configuration JSON
2. Calculate deployment_priority_mps (which wardrobe to deploy first?)
3. Map agent capabilities (which tasks can this wardrobe handle autonomously?)
4. Generate performance_benchmarks (latency, accuracy, throughput, memory)
5. Create autonomous_deployment command (can orchestrator auto-deploy?)
6. Generate verification script (test wardrobe loads correctly)
7. Extract learning_feedback (training insights + domain coverage + future improvements)
8. Write to `data/wardrobe_catalog/{domain}_wardrobe.json`
9. Log: `{"pattern": "deployment_config_generated", "value": true, "autonomous_deployable": true}`

**First Principles Additions**:
- ✅ **MPS Scoring**: deployment_priority_mps determines deployment order
- ✅ **Agent Mapping**: agent_capability_mapping (which tasks autonomous vs requires 0102?)
- ✅ **Executable Command**: autonomous_deployment.execution_command for auto-deploy
- ✅ **Performance Benchmarks**: Latency, accuracy, throughput, false positive/negative rates
- ✅ **Verification**: Test wardrobe loadable + validation accuracy >= threshold
- ✅ **Learning Feedback**: Training insights (convergence, overfitting) + domain coverage gaps
- ✅ **Rollback**: Remove wardrobe if deployment fails

---

## Expected Patterns Summary

```json
{
  "execution_id": "exec_gemma_trainer_001",
  "skill_id": "gemma_domain_trainer_v1_prototype",
  "patterns": {
    "dataset_loaded": true,
    "training_format_prepared": true,
    "lora_configured": true,
    "lora_training_complete": true,
    "model_validated": true,
    "deployment_config_generated": true
  },
  "training_examples": 58,
  "validation_accuracy": 0.87,
  "training_time_seconds": 420,
  "model_size_mb": 12
}
```

**Fidelity Calculation**: `(patterns_executed / 6)` - All 6 steps should run

---

## Wardrobe Catalog

### 1. gemma_mps_scorer
**Domain**: MPS scoring (WSP 15)
**Training Data**: 58 examples from 012.txt
**Use Cases**: Cleanup prioritization, project scoring, issue triage
**Accuracy**: 87%

### 2. gemma_wsp_auditor
**Domain**: WSP compliance checking
**Training Data**: 45 examples from 012.txt
**Use Cases**: Code review, documentation validation, architecture audits
**Accuracy**: 90%

### 3. gemma_roadmap_tracker
**Domain**: Roadmap analysis
**Training Data**: 32 examples from 012.txt
**Use Cases**: Project status reports, completion tracking, TODO audits
**Accuracy**: 85%

### 4. gemma_readme_validator
**Domain**: README structure validation
**Training Data**: 41 examples from 012.txt
**Use Cases**: Documentation quality checks, README generation
**Accuracy**: 88%

### 5. gemma_modlog_writer
**Domain**: ModLog entry generation
**Training Data**: 29 examples from 012.txt
**Use Cases**: Automated ModLog updates, change tracking
**Accuracy**: 84%

---

## Deployment: Wardrobe Swapping

**Concept**: One base Gemma 270M, multiple LoRA adapters

```python
# Load base model once
base_gemma = Gemma270M("E:/HoloIndex/models/gemma-3-270m-it-Q4_K_M.gguf")

# Swap wardrobes for different tasks
def score_cleanup_task(task):
    base_gemma.wear_wardrobe("mps_scorer")
    return base_gemma.generate(task)

def audit_wsp_compliance(code):
    base_gemma.wear_wardrobe("wsp_auditor")
    return base_gemma.generate(code)

def track_roadmap_status(roadmap):
    base_gemma.wear_wardrobe("roadmap_tracker")
    return base_gemma.generate(roadmap)
```

**Benefits**:
- 241MB base model (loaded once)
- 10-15MB per wardrobe (LoRA adapters)
- Instant swapping (no model reload)
- Specialized performance (>85% accuracy)

---

## Success Criteria

- ✅ Pattern fidelity ≥ 90% (all 6 steps execute)
- ✅ Validation accuracy ≥ 85% on held-out examples
- ✅ LoRA adapter size < 20MB
- ✅ Training completes in < 15 minutes (CPU)
- ✅ Deployment config generated with metadata
- ✅ Wardrobe swapping works (load/unload adapters)

---

## Next Steps

1. **Test on MPS scoring domain** (easiest to validate)
2. **Deploy as production wardrobe** once accuracy ≥ 85%
3. **Create wardrobe catalog** with all domain specialists
4. **Integrate with cleanup skills** (Gemma uses MPS scorer)
5. **Expand to other domains** (WSP auditing, roadmap tracking)

---

**Status**: ✅ Ready for prototype testing - Train Gemma on MPS scoring examples from 012.txt
