---
name: dspy-finetune-bootstrap
version: "1.0.0"
dspy-compatibility: "3.1.2"
description: This skill should be used when the user asks to "fine-tune a DSPy model", "distill a program into weights", "use BootstrapFinetune", "create a student model", "reduce inference costs with fine-tuning", mentions "model distillation", "teacher-student training", or wants to deploy a DSPy program as fine-tuned weights for production efficiency.
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# DSPy BootstrapFinetune Optimizer

## Goal

Distill a DSPy program into fine-tuned model weights for efficient production deployment.

## When to Use

- You have a working DSPy program with a large model
- Need to reduce inference costs
- Want faster responses (smaller model)
- Deploying to resource-constrained environments

## Inputs

| Input | Type | Description |
|-------|------|-------------|
| `program` | `dspy.Module` | Teacher program to distill |
| `trainset` | `list[dspy.Example]` | Training examples |
| `metric` | `callable` | Validation metric (optional) |
| `train_kwargs` | `dict` | Training hyperparameters |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `finetuned_program` | `dspy.Module` | Program with fine-tuned weights |
| `model_path` | `str` | Path to saved model |

## Workflow

### Phase 1: Prepare Teacher Program

```python
import dspy

# Configure with strong teacher model
dspy.configure(lm=dspy.LM("openai/gpt-4o"))

class TeacherQA(dspy.Module):
    def __init__(self):
        self.cot = dspy.ChainOfThought("question -> answer")
    
    def forward(self, question):
        return self.cot(question=question)
```

### Phase 2: Enable Experimental Features & Generate Training Traces

BootstrapFinetune is experimental and requires enabling the flag:

```python
import dspy
from dspy.teleprompt import BootstrapFinetune

# Enable experimental features
dspy.settings.experimental = True

optimizer = BootstrapFinetune(
    metric=lambda gold, pred, trace=None: gold.answer.lower() in pred.answer.lower(),
    train_kwargs={
        'learning_rate': 5e-5,
        'num_train_epochs': 3,
        'per_device_train_batch_size': 4,
        'warmup_ratio': 0.1
    }
)
```

### Phase 3: Fine-tune Student Model

```python
finetuned = optimizer.compile(
    TeacherQA(),
    trainset=trainset
)
```

### Phase 4: Deploy

```python
# Save the fine-tuned model (saves state-only by default)
finetuned.save("finetuned_qa_model.json")

# Load and use (must recreate architecture first)
loaded = TeacherQA()
loaded.load("finetuned_qa_model.json")
result = loaded(question="What is machine learning?")
```

## Production Example

```python
import dspy
from dspy.teleprompt import BootstrapFinetune
from dspy.evaluate import Evaluate
import logging
import os

# Enable experimental features
dspy.settings.experimental = True

logger = logging.getLogger(__name__)

class ClassificationSignature(dspy.Signature):
    """Classify text into categories."""
    text: str = dspy.InputField()
    label: str = dspy.OutputField(desc="Category: positive, negative, neutral")

class TextClassifier(dspy.Module):
    def __init__(self):
        self.classify = dspy.Predict(ClassificationSignature)
    
    def forward(self, text):
        return self.classify(text=text)

def classification_metric(gold, pred, trace=None):
    """Exact label match."""
    gold_label = gold.label.lower().strip()
    pred_label = pred.label.lower().strip() if pred.label else ""
    return gold_label == pred_label

def finetune_classifier(trainset, devset, output_dir="./finetuned_model"):
    """Full fine-tuning pipeline."""
    
    # Configure teacher (strong model)
    dspy.configure(lm=dspy.LM("openai/gpt-4o"))
    
    teacher = TextClassifier()
    
    # Evaluate teacher
    evaluator = Evaluate(devset=devset, metric=classification_metric, num_threads=8)
    teacher_score = evaluator(teacher)
    logger.info(f"Teacher score: {teacher_score:.2%}")

    # Fine-tune (train_kwargs passed to constructor)
    optimizer = BootstrapFinetune(
        metric=classification_metric,
        train_kwargs={
            'learning_rate': 2e-5,
            'num_train_epochs': 3,
            'per_device_train_batch_size': 8,
            'gradient_accumulation_steps': 2,
            'warmup_ratio': 0.1,
            'weight_decay': 0.01,
            'logging_steps': 10,
            'save_strategy': 'epoch',
            'output_dir': output_dir
        }
    )

    finetuned = optimizer.compile(
        teacher,
        trainset=trainset
    )
    
    # Evaluate fine-tuned model
    student_score = evaluator(finetuned)
    logger.info(f"Student score: {student_score:.2%}")

    # Save (state-only as JSON)
    finetuned.save(os.path.join(output_dir, "final_model.json"))

    return {
        "teacher_score": teacher_score,
        "student_score": student_score,
        "model_path": os.path.join(output_dir, "final_model.json")
    }

# For RAG fine-tuning
class RAGClassifier(dspy.Module):
    """RAG pipeline that can be fine-tuned."""
    
    def __init__(self, num_passages=3):
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.classify = dspy.ChainOfThought("context, text -> label")
    
    def forward(self, text):
        context = self.retrieve(text).passages
        return self.classify(context=context, text=text)

def finetune_rag_classifier(trainset, devset):
    """Fine-tune a RAG-based classifier."""

    # Configure retriever and LM
    colbert = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
    dspy.configure(
        lm=dspy.LM("openai/gpt-4o"),
        rm=colbert
    )

    rag = RAGClassifier()

    # Fine-tune (train_kwargs in constructor)
    optimizer = BootstrapFinetune(
        metric=classification_metric,
        train_kwargs={
            'learning_rate': 1e-5,
            'num_train_epochs': 5
        }
    )

    finetuned = optimizer.compile(
        rag,
        trainset=trainset
    )

    return finetuned
```

## Training Arguments Reference

| Argument | Description | Typical Value |
|----------|-------------|---------------|
| `learning_rate` | Learning rate | 1e-5 to 5e-5 |
| `num_train_epochs` | Training epochs | 3-5 |
| `per_device_train_batch_size` | Batch size | 4-16 |
| `gradient_accumulation_steps` | Gradient accumulation | 2-8 |
| `warmup_ratio` | Warmup proportion | 0.1 |
| `weight_decay` | L2 regularization | 0.01 |
| `max_grad_norm` | Gradient clipping | 1.0 |

## Best Practices

1. **Strong teacher** - Use GPT-4 or Claude as teacher
2. **Quality data** - Teacher traces are only as good as training examples
3. **Validate improvement** - Compare student to teacher on held-out set
4. **Start with more epochs** - Fine-tuning often needs 3-5 epochs
5. **Monitor overfitting** - Track validation loss during training

## Limitations

- Requires access to model weights (not API-only models)
- Training requires GPU resources
- Student may not match teacher quality on all inputs
- Fine-tuning takes hours/days depending on data size
- Model size reduction may cause capability loss

## Official Documentation

- **DSPy Documentation**: https://dspy.ai/
- **DSPy GitHub**: https://github.com/stanfordnlp/dspy
- **BootstrapFinetune API**: https://dspy.ai/api/optimizers/BootstrapFinetune/
- **Fine-tuning Guide**: https://dspy.ai/tutorials/classification_finetuning/
