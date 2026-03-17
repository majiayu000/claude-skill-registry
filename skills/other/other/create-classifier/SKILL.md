---
name: create-classifier
description: >
  Train task-specific classifiers for the extractor pipeline.
  Supports vision, text, and hybrid classifiers with GRPO training and execution feedback.
  Includes data collection, confidence-based routing, and shadow deployment.
allowed-tools: Bash, Read, Write
triggers:
  - train classifier
  - create classifier
  - classifier training
  - document type classifier
  - ml model training
metadata:
  short-description: Generalized classifier training infrastructure with execution feedback

provides:
  - create-classifier
composes:
  - memory
  - classifier-lab
  - dogpile
  - task-monitor
---

# Create Classifier Skill

> **Purpose**: Training infrastructure for task-specific classifiers that improve extractor pipeline accuracy through ML-based detection instead of regex/heuristics.

## Overview

This skill provides end-to-end infrastructure for creating, training, and deploying classifiers for extraction tasks:

- **Data Collection**: Mine labeled data from successful pipeline runs
- **Training Templates**: Vision, text, and hybrid classifier architectures
- **Execution Feedback**: GRPO-style training with pipeline success as reward
- **Confidence Routing**: Automatic fallback to heuristics when confidence is low
- **Shadow Deployment**: Compare classifier vs heuristics before full rollout

## Success Story: Table Strategy Classifier

The table extraction classifier (S05) achieved:

- **95.07% accuracy** (vs ~75% heuristic baseline)
- **Reduced fallback rate** from ~25% to <10%
- **Faster inference** than multi-strategy attempts

This skill generalizes that success pattern for other extraction tasks.

---

## Supported Classifier Types

### 1. Vision Classifiers

**Use case**: Document-level classification from images

- **Example**: S00 document type detection (arxiv, requirements_spec, legal)
- **Input**: First 3 pages as images (224x224)
- **Architecture**: EfficientNet-B0 or DiT (Document Image Transformer)

### 2. Text Classifiers

**Use case**: Sentence or block-level classification from text

- **Example**: S08 requirement sentence detection
- **Input**: Sentence text + context (headings, modal verbs)
- **Architecture**: BERT-base or RoBERTa

### 3. Hybrid Classifiers

**Use case**: Combined text + layout features

- **Example**: S04 citation vs section header detection
- **Input**: Text + font size + bbox + surrounding context
- **Architecture**: Multi-modal fusion network

---

## Usage

### Step 0: Preflight Assess (Recommended)

Run an initial task/data assessment before training. This recommends classifier family/backbone,
checks class imbalance, and can trigger `/dogpile` research when confidence is low.

```bash
./run.sh assess \
  --task document_type \
  --labels data/labels/document_type.jsonl \
  --dogpile-when-uncertain
```

### Step 0b: Benchmark-First Model Selection (Recommended)

Run benchmark-first selection after assess. This attempts `classifier-lab` first
when configured, then uses internal quick benchmarking as deterministic fallback.
For production training, make classifier-lab mandatory and fail closed on selection.

```bash
./run.sh select-model \
  --labels data/labels/document_type.jsonl \
  --model efficientnet_b0 \
  --candidate-backbones \
    efficientnet_b0,convnextv2_nano.fcmae_ft_in22k_in1k,resnet50 \
  --benchmark-first \
  --classifier-lab-first \
  --require-classifier-lab \
  --require-selection-pass
```

### Step 1: Data Collection

Collect labeled examples from successful pipeline runs:

```bash
./run.sh collect \
  --task document_type \
  --source /path/to/corpus \
  --output data/labels/document_type.jsonl
```

**Output format** (JSONL):

```json
{
  "id": "doc_abc123",
  "task": "document_type",
  "input": {
    "image_paths": ["page_0.png", "page_1.png", "page_2.png"],
    "text_features": { "page_count": 42, "has_formulas": true }
  },
  "label": "arxiv_scientific",
  "confidence": 0.95,
  "source": "successful_extraction"
}
```

### Step 2: Train Classifier

Train using supervised learning or GRPO (with execution feedback):

````bash
# Supervised fine-tuning (SFT)
./run.sh train \
  --config configs/document_type.yaml \
  --mode sft \
  --epochs 20

# GRPO with execution feedback
./run.sh train \
  --config configs/document_type.yaml \
  --mode grpo \
  --feedback-fn validate_pipeline_success

# Iterative train with preflight assess, optional HF augmentation, and holdout gate
./run.sh train-iterative \
  --task document_type \
  --model efficientnet_b0 \
  --labels data/labels/document_type.jsonl \
  --output-dir models/document_type \
  --benchmark-first \
  --classifier-lab-first \
  --require-classifier-lab \
  --require-selection-pass \
  --run-preflight-assess \
  --auto-hf-augment \
  --run-hp-search

# Strict quality gate profile (recommended default)
# - holdout macro-F1 >= 0.90
# - holdout accuracy >= 0.90
# - per-class recall floor >= 0.80 (enforce in evaluator/report gate)

### Step 2b: Train with Docker

Run training in a container (recommended for reproducibility):

```bash
docker-compose up classifier
````

This mounts the corpus and output directories automatically.

````

### Step 3: Evaluate

Compare classifier against heuristic baseline:

```bash
./run.sh evaluate \
  --model models/document_type \
  --baseline heuristic \
  --test-set data/test/document_type.jsonl
````

**Success criteria**:

- Overall accuracy >90%
- Per-class precision >80%
- Inference time <100ms

### Step 4: Shadow Deploy

Run classifier in parallel with heuristics (log differences, no changes to pipeline):

```bash
./run.sh shadow-deploy \
  --model models/document_type \
  --target s00_profile_detector \
  --duration 7d \
  --log-path logs/shadow_deploy.jsonl
```

### Step 5: Deploy

If metrics pass, deploy to production:

```bash
./run.sh deploy \
  --model models/document_type \
  --target extractor \
  --confidence-threshold 0.8
```

---

## Configuration Files

### Document Type Classifier (`configs/document_type.yaml`)

```yaml
task: document_type
type: vision

classes:
  - arxiv_scientific
  - requirements_spec
  - legal_contract
  - general

model:
  architecture: efficientnet_b0
  pretrained: true
  input_size: 224
  num_pages: 3 # First 3 pages

training:
  epochs: 20
  batch_size: 16
  learning_rate: 0.001
  optimizer: adam

confidence:
  threshold: 0.8 # Route to heuristic if below

feedback:
  mode: grpo # or 'sft'
  reward_fn: validate_preset_accuracy
  baseline: heuristic
```

### Requirements Classifier (`configs/requirements.yaml`)

```yaml
task: requirement_detection
type: text

classes:
  - requirement
  - non_requirement

model:
  architecture: bert-base-uncased
  max_length: 256

training:
  epochs: 10
  batch_size: 32
  learning_rate: 2e-5

confidence:
  threshold: 0.9 # High precision needed
```

---

## Architecture Details

### Vision Classifier Template

```python
import timm
import torch.nn as nn

class VisionClassifier(nn.Module):
    def __init__(self, num_classes, backbone="efficientnet_b0"):
        super().__init__()
        self.backbone = timm.create_model(
            backbone,
            pretrained=True,
            num_classes=0
        )
        self.classifier = nn.Linear(
            self.backbone.num_features,
            num_classes
        )
        self.confidence_head = nn.Sequential(
            nn.Linear(self.backbone.num_features, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        features = self.backbone(x)
        logits = self.classifier(features)
        confidence = self.confidence_head(features)
        return logits, confidence
```

### Confidence-Based Routing

```python
class ConfidenceRouter:
    def __init__(self, classifier, heuristic_fn, threshold=0.8):
        self.classifier = classifier
        self.heuristic = heuristic_fn
        self.threshold = threshold

    def predict(self, input_data):
        pred, confidence = self.classifier(input_data)

        if confidence >= self.threshold:
            return {"prediction": pred, "source": "classifier"}
        else:
            # Fallback to heuristic
            return {
                "prediction": self.heuristic(input_data),
                "source": "heuristic",
                "classifier_confidence": confidence  # Log anyway
            }
```

---

## Data Collection Strategy

### Automatic Labeling

Mine labels from successful pipeline outputs:

**S00 (Document Type)**:

- Extract preset from `00_profile.json` → label
- Extract first 3 pages as images → input

**S05 (Table Strategy)**:

- Extract strategy from `05_tables.json` → label
- Extract table region image → input
- Use success/failure as GRPO reward

**S08 (Requirements)**:

- Bootstrap with regex-matched sentences → positive examples
- Random sentences without modal verbs → negative examples
- Manual review of edge cases

### Label Validation

```python
def validate_labels(labels_path, sample_size=100):
    """Manual review of random sample for quality check."""
    labels = load_jsonl(labels_path)
    sample = random.sample(labels, sample_size)

    correct = 0
    for item in sample:
        print(f"Input: {item['input']}")
        print(f"Predicted label: {item['label']}")
        response = input("Correct? (y/n): ")
        if response.lower() == 'y':
            correct += 1

    accuracy = correct / sample_size
    print(f"Label quality: {accuracy:.1%}")
    return accuracy >= 0.95  # Threshold for good labels
```

---

## GRPO Training (Execution Feedback)

### Reward Functions

**S00 Document Type**:

```python
def reward_preset_accuracy(predicted_preset, pdf_path):
    """Reward = 1.0 if pipeline succeeds, 0.0 if fails."""
    result = run_pipeline(pdf_path, preset=predicted_preset)
    return 1.0 if result.success else 0.0
```

**S08 Requirements**:

```python
def reward_requirement_extraction(predicted_requirements, ground_truth):
    """Reward = F1 score vs ground truth."""
    precision = len(predicted & ground_truth) / len(predicted)
    recall = len(predicted & ground_truth) / len(ground_truth)
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1
```

### Training Loop

```python
from trl import GRPOTrainer

trainer = GRPOTrainer(
    model=classifier,
    reward_fn=reward_preset_accuracy,
    baseline_fn=heuristic_preset_detection,
    num_iterations=100,
    batch_size=16
)

trainer.train()
```

---

## Integration Example: S00 Document Type

### Before (Heuristics Only)

```python
def detect_preset(pdf_path):
    # 47 regex patterns for section numbering
    # Formula detection regex
    # Font-size analysis
    # ~85% accuracy, confidence often <0.8
    return {"preset": "arxiv", "confidence": 0.7}
```

### After (Classifier + Fallback)

```python
def detect_preset(pdf_path):
    # Try classifier first
    result = preset_classifier.predict(pdf_path)

    if result["confidence"] >= 0.8:
        return result  # Use classifier
    else:
        # Fallback to heuristics
        return detect_preset_heuristic(pdf_path)
```

**Benefits**:

- Higher accuracy (90%+ vs 85%)
- Faster (single forward pass vs 47 regex patterns)
- Continuous improvement (retrain with production data)

---

## Observability

### Metrics Logged

```json
{
  "timestamp": "2026-02-08T10:53:00Z",
  "task": "document_type",
  "input_id": "doc_abc123",
  "classifier_prediction": "arxiv_scientific",
  "classifier_confidence": 0.92,
  "heuristic_prediction": "general",
  "heuristic_confidence": 0.65,
  "source_used": "classifier",
  "execution_result": "success",
  "inference_time_ms": 45
}
```

### Monitoring Dashboard

Track over time:

- Classifier usage rate (% using classifier vs fallback)
- Accuracy comparison (classifier vs heuristic)
- Inference latency (p50, p95, p99)
- Fallback rate (low confidence → heuristic)

---

## Files

```
create-classifier/
├── SKILL.md                    # This file
├── run.sh                      # CLI wrapper
├── .env.example               # Configuration template
├── scripts/
│   ├── collect_labels.py      # Mine labels from pipeline
│   ├── train_vision.py        # Vision classifier training
│   ├── train_text.py          # Text classifier training
│   ├── evaluate.py            # Evaluation & comparison
│   └── deploy.py              # Generate inference code
├── templates/
│   ├── vision_classifier.py   # EfficientNet/DiT template
│   ├── text_classifier.py     # BERT/RoBERTa template
│   └── hybrid_classifier.py   # Multi-modal template
├── configs/
│   ├── document_type.yaml     # S00 preset detection
│   ├── requirements.yaml      # S08 requirement detection
│   └── citation_filter.yaml   # S04 citation filtering
└── utils/
    ├── data_collection.py     # Dataset utilities
    ├── confidence_routing.py  # Routing logic
    └── shadow_deploy.py       # Parallel testing
```

---

## Dependencies

```toml
[tool.uv.dependencies]
torch = "^2.0.0"
timm = "^0.9.0"              # Vision models
transformers = "^4.30.0"     # Text models
trl = "^0.7.0"               # GRPO training
pillow = "^10.0.0"           # Image processing
pyyaml = "^6.0"
loguru = "^0.7.0"
```

---

## Troubleshooting

### Low Accuracy (<90%)

**Causes**:

- Insufficient training data (need >1000 examples per class)
- Class imbalance (e.g., 90% arxiv, 10% legal)
- Poor label quality

**Solutions**:

- Collect more data from corpus
- Apply class balancing (oversample minority, undersample majority)
- Manual review and relabeling of subset

### Slow Inference (>100ms)

**Causes**:

- Large model (DiT is 85M params)
- CPU inference (no GPU available)

**Solutions**:

- Use smaller model (EfficientNet-B0 is 5M params)
- Quantize to ONNX (2-3x speedup)
- Batch inference (process multiple pages together)
- Cache predictions (don't re-classify same document)

### High Fallback Rate (>30%)

**Causes**:

- Classifier not confident on edge cases
- Threshold too high (>0.9)

**Solutions**:

- Lower confidence threshold (try 0.7)
- Add more diverse training data
- Ensemble multiple models (vote on prediction)

---

## Next Steps

1. **Collect data** for S00 document type classifier
2. **Train baseline** EfficientNet-B0 model
3. **Shadow deploy** for 1 week, compare vs heuristics
4. **Deploy** if accuracy >90%
5. **Repeat** for S08 requirements classifier

---

## References

- [Table Classifier Context](/home/graham/workspace/experiments/extractor/local/docs/CONTEXT.md)
- [S00 Profile Detector](/home/graham/workspace/experiments/extractor/src/extractor/pipeline/steps/s00_profile_detector.py)
- [GRPO Paper](https://arxiv.org/abs/2402.03300)
- [DiT Model](https://huggingface.co/microsoft/dit-base)
