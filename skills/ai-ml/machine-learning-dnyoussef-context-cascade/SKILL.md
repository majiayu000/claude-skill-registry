/*============================================================================*/
/* MACHINE-LEARNING SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: machine-learning
version: 2.0.0
description: |
  [assert|neutral] Comprehensive machine learning development with training, evaluation, and deployment capabilities. Use when training models, developing ML pipelines, or deploying machine learning systems. [ground:given] [conf:0.95] [state:confirmed]
category: platforms
tags:
- ml
- deep-learning
- training
- evaluation
- deployment
author: SPARC System
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute machine-learning workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic platforms processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "machine-learning",
  category: "platforms",
  version: "2.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["machine-learning", "platforms", "workflow"],
  context: "user needs machine-learning capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## When NOT to Use This Skill

- Simple data preprocessing without model training
- Statistical analysis that does not require ML models
- Rule-based systems without learning components
- Operations that do not involve model training or inference

## Success Criteria
- [assert|neutral] Model training convergence: Loss decreasing consistently [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Validation accuracy: Meeting or exceeding baseline targets [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Training time: Within expected bounds for dataset size [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] GPU utilization: >80% during training [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Model export success: 100% successful saves [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Inference latency: <100ms for real-time applications [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Edge Cases & Error Handling

- **GPU Memory Overflow**: Reduce batch size, use gradient accumulation, or mixed precision
- **Divergent Training**: Implement learning rate scheduling, gradient clipping
- **Data Pipeline Failures**: Validate data integrity, handle missing/corrupted files
- **Version Mismatches**: Lock dependency versions, use containerization
- **Checkpoint Corruption**: Save multiple checkpoints, validate before loading
- **Distributed Training Failures**: Handle node failures, implement fault tolerance

## Guardrails & Safety
- [assert|emphatic] NEVER: train on unvalidated or uncleaned data [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate model outputs before deployment [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: implement reproducibility (random seeds, version pinning) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: expose training data in model artifacts or logs [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: monitor for bias and fairness issues [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: implement model versioning and rollback capabilities [ground:policy] [conf:0.98] [state:confirmed]

## Evidence-Based Validation

- Verify hardware availability: Check GPU/TPU status before training
- Validate data quality: Run data integrity checks and statistics
- Monitor training: Track loss curves, gradients, and metrics
- Test model performance: Evaluate on held-out test set
- Benchmark inference: Measure latency and throughput under load


# Machine Learning Development Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Complete workflow for machine learning model development, training, evaluation, and deployment.

## When to Use

Auto-trigger when detecting:
- "train model", "machine learning", "ML pipeline"
- "deep learning", "neural network", "model training"
- "data preprocessing", "feature engineering"
- "model evaluation", "hyperparameter tuning"
- "model deployment", "ML ops"

## Capabilities

### 1. Data Pipeline
- Data preprocessing and cleaning
- Feature engineering and selection
- Data augmentation
- Train/validation/test splitting
- Data versioning with DVC

### 2. Model Training
- Neural network architectures
- Hyperparameter optimization
- Transfer learning
- Distributed training
- Training monitoring and logging

### 3. Model Evaluation
- Multi-metric evaluation
- Cross-validation
- Confusion matrices and ROC curves
- Fairness and bias detection
- Performance benchmarking

### 4. Model Deployment
- Model serialization and versioning
- API endpoint creation
- Containerization
- Monitoring and logging
- A/B testing support

## Agent Workflow

```javascript
// Auto-spawned agents for ML development
Task("ML Researcher", "Research SOTA models and best practices for [task]", "researcher")
Task("

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
  pattern: "skills/platforms/machine-learning/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "machine-learning-{session_id}",
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

[commit|confident] <promise>MACHINE_LEARNING_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
