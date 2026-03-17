---
name: HuggingFace Model Trainer
description: Train and fine-tune LLMs using HuggingFace TRL, Transformers, and cloud GPU infrastructure with SFT, DPO, GRPO methods
version: 1.1.0
last_updated: 2026-01-06
external_version: "TRL 0.12+, Transformers 4.47+"
triggers:
  - fine-tuning
  - model training
  - huggingface
  - TRL
  - LoRA
  - PEFT
---

# HuggingFace Model Trainer

You are an expert in training and fine-tuning large language models using HuggingFace's TRL (Transformer Reinforcement Learning), Transformers, and PEFT libraries. You help with dataset preparation, training configuration, GPU selection, and deployment.

## Training Methods Overview

### Method Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINING METHOD SELECTION                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HAVE LABELED DATA?                                             │
│  ├── Yes: Input/Output pairs                                    │
│  │   └── Use SFT (Supervised Fine-Tuning)                       │
│  │                                                               │
│  ├── Yes: Preference pairs (chosen/rejected)                    │
│  │   └── Use DPO (Direct Preference Optimization)               │
│  │                                                               │
│  ├── No: Have a reward function/verifier                        │
│  │   └── Use GRPO (Group Relative Policy Optimization)          │
│  │                                                               │
│  └── No: Just want to continue pretraining                      │
│      └── Use CLM (Causal Language Modeling)                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 1. Supervised Fine-Tuning (SFT)

### When to Use
- You have instruction/response pairs
- Adapting a model to your domain
- Teaching specific output formats

### Basic SFT Script

```python
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# Load model and tokenizer
model_id = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# Load dataset
dataset = load_dataset("your-org/your-dataset", split="train")

# Training configuration
config = SFTConfig(
    output_dir="./sft-output",
    max_seq_length=2048,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-5,
    num_train_epochs=3,
    logging_steps=10,
    save_strategy="epoch",
    bf16=True,  # Use bfloat16 on supported GPUs
)

# Create trainer
trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

# Train
trainer.train()
trainer.save_model("./final-model")
```

### SFT with Chat Template

```python
from trl import SFTTrainer, SFTConfig

# Dataset should have 'messages' column in chat format
# [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

config = SFTConfig(
    output_dir="./chat-sft",
    max_seq_length=4096,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=3,
)

trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    # Automatically applies chat template
)
```

## 2. Direct Preference Optimization (DPO)

### When to Use
- You have preference data (chosen vs rejected responses)
- Aligning model with human preferences
- Improving response quality

### DPO Script

```python
from trl import DPOTrainer, DPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# Load model
model_id = "meta-llama/Llama-3.1-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Dataset needs: prompt, chosen, rejected columns
dataset = load_dataset("your-org/preference-data", split="train")

config = DPOConfig(
    output_dir="./dpo-output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    learning_rate=5e-7,  # Lower LR for DPO
    beta=0.1,  # KL penalty coefficient
    num_train_epochs=1,
    bf16=True,
    logging_steps=10,
)

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()
```

### Preference Data Format

```python
# Required columns: prompt, chosen, rejected
preference_example = {
    "prompt": "Explain quantum computing",
    "chosen": "Quantum computing uses quantum bits...",  # Better response
    "rejected": "Computers are fast machines..."  # Worse response
}
```

## 3. Group Relative Policy Optimization (GRPO)

### When to Use
- You have a reward function or verifier
- Math/code tasks with checkable answers
- RL-based training without paired preferences

### GRPO Script

```python
from trl import GRPOTrainer, GRPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "meta-llama/Llama-3.1-8B-Instruct"
model = AutoModelForCausalLM.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Define reward function
def reward_fn(completions, prompts):
    """Return rewards for each completion"""
    rewards = []
    for completion, prompt in zip(completions, prompts):
        # Example: reward correct math answers
        if verify_math_answer(completion, prompt):
            rewards.append(1.0)
        else:
            rewards.append(-0.5)
    return rewards

config = GRPOConfig(
    output_dir="./grpo-output",
    per_device_train_batch_size=4,
    num_generations=4,  # Generate 4 samples per prompt
    learning_rate=1e-6,
    num_train_epochs=1,
)

trainer = GRPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    reward_fn=reward_fn,
)

trainer.train()
```

## 4. Parameter-Efficient Fine-Tuning (PEFT/LoRA)

### Why Use LoRA
- Train large models on limited GPU memory
- 10-100x fewer trainable parameters
- Fast training, easy to merge or swap adapters

### LoRA Configuration

```python
from peft import LoraConfig, get_peft_model, TaskType

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # Rank (start with 8-32)
    lora_alpha=32,  # Alpha scaling
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

# Apply to model
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 6,553,600 || all params: 8,030,261,248 || trainable%: 0.082
```

### SFT with LoRA

```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

config = SFTConfig(
    output_dir="./lora-sft",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,  # Higher LR for LoRA
    num_train_epochs=3,
    bf16=True,
)

trainer = SFTTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    peft_config=peft_config,  # Pass LoRA config
)

trainer.train()
```

### QLoRA (Quantized LoRA)

```python
from transformers import BitsAndBytesConfig
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
)

# Then apply LoRA as normal
```

## GPU Selection Guide

### Memory Requirements

| Model Size | Full Fine-tune | LoRA | QLoRA |
|------------|---------------|------|-------|
| 7-8B | 60GB+ | 16GB | 8GB |
| 13B | 100GB+ | 24GB | 12GB |
| 34B | 200GB+ | 48GB | 24GB |
| 70B | 400GB+ | 80GB | 48GB |

### GPU Recommendations

```
┌─────────────────────────────────────────────────────────────────┐
│                    GPU SELECTION GUIDE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TASK                    │ RECOMMENDED GPU                       │
│  ────────────────────────┼────────────────────────────────────  │
│  QLoRA 8B               │ RTX 4090 (24GB), A10G                 │
│  QLoRA 70B              │ A100 40GB x2, H100                    │
│  LoRA 8B                │ A100 40GB, A10G x2                    │
│  LoRA 70B               │ A100 80GB x2, H100 x2                 │
│  Full FT 8B             │ A100 80GB x2, H100                    │
│  Full FT 70B            │ H100 x8, A100 80GB x8                 │
│                                                                  │
│  CLOUD PROVIDERS:                                                │
│  - AWS: p4d (A100), p5 (H100)                                   │
│  - GCP: a2-highgpu (A100), a3-highgpu (H100)                   │
│  - Azure: NC A100, ND H100                                      │
│  - Lambda Labs: Most cost-effective for training                │
│  - RunPod: Good spot pricing                                    │
│  - HuggingFace Jobs: Managed training infrastructure            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Dataset Preparation

### Chat Format Dataset

```python
from datasets import Dataset

# Conversation format
conversations = [
    {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is a programming language..."}
        ]
    },
    # More examples...
]

dataset = Dataset.from_list(conversations)
dataset.push_to_hub("your-org/chat-dataset")
```

### Instruction Format

```python
# Alpaca-style format
instruction_data = [
    {
        "instruction": "Summarize the following text",
        "input": "Long text here...",
        "output": "Summary here..."
    }
]

# Or simpler format
simple_data = [
    {
        "prompt": "Question or instruction",
        "completion": "Expected response"
    }
]
```

### Data Quality Tips

```python
# Filter low-quality examples
def filter_quality(example):
    # Remove very short responses
    if len(example["completion"]) < 50:
        return False
    # Remove repetitive content
    if example["completion"].count(example["completion"][:20]) > 3:
        return False
    return True

dataset = dataset.filter(filter_quality)

# Deduplicate
from datasets import concatenate_datasets

def deduplicate(dataset, column="prompt"):
    seen = set()
    indices = []
    for i, example in enumerate(dataset):
        key = example[column]
        if key not in seen:
            seen.add(key)
            indices.append(i)
    return dataset.select(indices)
```

## Training on HuggingFace Jobs

### Using HF Jobs MCP Tool

```python
# If using Claude Code with HF Jobs MCP
# This is submitted via hf_jobs() MCP tool

training_script = '''
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
dataset = load_dataset("your-org/your-dataset", split="train")

config = SFTConfig(
    output_dir="./output",
    max_seq_length=2048,
    per_device_train_batch_size=4,
    num_train_epochs=3,
    bf16=True,
    push_to_hub=True,
    hub_model_id="your-org/fine-tuned-model",
)

trainer = SFTTrainer(model=model, args=config, train_dataset=dataset, tokenizer=tokenizer)
trainer.train()
'''

# Submit via MCP: hf_jobs("uv", {"script": training_script, "gpu": "a100"})
```

### Cost Estimation

```python
# Rough cost estimates for HF Jobs / Cloud GPUs
TRAINING_COSTS = {
    # GPU type: (hourly_rate, tokens_per_hour_8B)
    "a10g": (1.50, 50_000_000),
    "a100_40gb": (3.50, 150_000_000),
    "a100_80gb": (5.00, 200_000_000),
    "h100": (8.00, 400_000_000),
}

def estimate_cost(
    model_size: str,
    dataset_tokens: int,
    epochs: int,
    gpu_type: str = "a100_40gb"
) -> dict:
    rate, throughput = TRAINING_COSTS[gpu_type]
    total_tokens = dataset_tokens * epochs
    hours = total_tokens / throughput
    cost = hours * rate

    return {
        "gpu": gpu_type,
        "estimated_hours": round(hours, 1),
        "estimated_cost": f"${cost:.2f}",
        "total_tokens": f"{total_tokens:,}"
    }

# Example: 10M token dataset, 3 epochs on A100
estimate_cost("8B", 10_000_000, 3, "a100_40gb")
# {'gpu': 'a100_40gb', 'estimated_hours': 0.2, 'estimated_cost': '$0.70', 'total_tokens': '30,000,000'}
```

## GGUF Conversion for Local Deployment

```python
# Convert to GGUF for llama.cpp / Ollama

from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your fine-tuned model
model = AutoModelForCausalLM.from_pretrained("./fine-tuned-model")
tokenizer = AutoTokenizer.from_pretrained("./fine-tuned-model")

# Save in format for conversion
model.save_pretrained("./model-for-gguf", safe_serialization=True)
tokenizer.save_pretrained("./model-for-gguf")

# Then use llama.cpp for conversion:
# python convert_hf_to_gguf.py ./model-for-gguf --outtype q4_k_m
```

### Quantization Options

| Type | Size Reduction | Quality Loss | Use Case |
|------|---------------|--------------|----------|
| f16 | 2x | None | Best quality |
| q8_0 | 4x | Minimal | Good balance |
| q4_k_m | 8x | Small | Production |
| q4_0 | 8x | Moderate | Resource constrained |
| q2_k | 16x | Significant | Extreme constraints |

## Evaluation

### Using lm-eval-harness

```python
# Install: pip install lm-eval

# Command line evaluation
# lm_eval --model hf --model_args pretrained=./fine-tuned-model --tasks hellaswag,arc_easy --batch_size 8

# Programmatic
from lm_eval import evaluator, tasks

results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=./fine-tuned-model",
    tasks=["hellaswag", "arc_easy", "mmlu"],
    batch_size=8,
)

print(results["results"])
```

### Custom Evaluation

```python
def evaluate_on_test_set(model, tokenizer, test_dataset):
    correct = 0
    total = 0

    for example in test_dataset:
        prompt = example["prompt"]
        expected = example["expected"]

        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=100)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if expected.lower() in response.lower():
            correct += 1
        total += 1

    return {"accuracy": correct / total, "total": total}
```

## Best Practices

### Training Checklist

```yaml
before_training:
  - [ ] Validate dataset format and quality
  - [ ] Check GPU memory requirements
  - [ ] Set up monitoring (W&B, TensorBoard)
  - [ ] Configure checkpointing strategy
  - [ ] Test with small subset first

during_training:
  - [ ] Monitor loss curves
  - [ ] Watch for gradient issues
  - [ ] Check learning rate schedule
  - [ ] Validate checkpoints periodically

after_training:
  - [ ] Evaluate on held-out test set
  - [ ] Compare with base model
  - [ ] Test on diverse prompts
  - [ ] Convert to desired format (GGUF, etc.)
  - [ ] Push to Hub with model card
```

### Hyperparameter Guidelines

```python
# SFT defaults
SFT_DEFAULTS = {
    "learning_rate": 2e-5,  # Full fine-tune
    "learning_rate_lora": 2e-4,  # LoRA (higher)
    "batch_size": 4,
    "gradient_accumulation": 4,  # Effective batch = 16
    "epochs": 1-3,
    "warmup_ratio": 0.03,
    "weight_decay": 0.01,
}

# DPO defaults
DPO_DEFAULTS = {
    "learning_rate": 5e-7,  # Much lower
    "beta": 0.1,  # KL penalty
    "epochs": 1,  # Usually 1 is enough
}
```

## Resources

- [TRL Documentation](https://huggingface.co/docs/trl)
- [PEFT Documentation](https://huggingface.co/docs/peft)
- [HuggingFace Hub](https://huggingface.co/models)
- [HuggingFace Jobs](https://huggingface.co/jobs)
- [lm-eval-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) - High-level training framework
