---
name: faion-finetuning-skill
user-invocable: false
description: ""
---

# LLM Fine-tuning Mastery

**Customize Language Models for Domain-Specific Tasks (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Techniques** | Full fine-tuning, LoRA, QLoRA, DoRA |
| **Frameworks** | LLaMA-Factory, Unsloth, Axolotl, TRL |
| **Datasets** | Alpaca, ShareGPT, Conversation, Instruction |
| **Alignment** | SFT, RLHF, DPO, ORPO |
| **Evaluation** | Perplexity, task benchmarks, human eval |
| **Deployment** | GGUF, vLLM, TGI, Ollama |
| **Cost** | GPU selection, cloud pricing, optimization |

---

## Technique Comparison

| Technique | GPU Memory | Speed | Quality | Use Case |
|-----------|------------|-------|---------|----------|
| **Full FT** | 80GB+ | Slow | Best | Large budgets, critical tasks |
| **LoRA** | 16-24GB | Fast | Good | Most production cases |
| **QLoRA** | 8-12GB | Medium | Good | Consumer GPUs, prototyping |
| **DoRA** | 16-24GB | Fast | Better | LoRA successor (2024+) |
| **OpenAI FT** | N/A | Fast | Good | API-only workflows |

---

## LoRA (Low-Rank Adaptation)

### Core Concept

LoRA freezes base model weights and injects small trainable matrices into attention layers.

```
Original weight W (d x k)
         ↓
W' = W + BA  where B (d x r), A (r x k)
         ↓
Only B and A are trained (r << min(d, k))
```

### Key Parameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| **rank (r)** | Adapter matrix rank | 8, 16, 32, 64 |
| **alpha** | Scaling factor | Usually = rank |
| **target_modules** | Layers to adapt | q_proj, v_proj, k_proj, o_proj |
| **dropout** | Regularization | 0.0 - 0.1 |

### Rank Selection Guide

| Rank | Memory | Use Case |
|------|--------|----------|
| 8 | Minimal | Simple tasks, prototyping |
| 16 | Low | General fine-tuning |
| 32 | Medium | Complex tasks |
| 64 | Higher | Maximum quality |
| 128+ | High | Rarely needed |

### Target Modules by Model

| Model | Recommended Modules |
|-------|---------------------|
| **LLaMA/Mistral** | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| **Qwen** | c_attn, c_proj |
| **Phi** | q_proj, k_proj, v_proj, dense |
| **GPT-NeoX** | query_key_value, dense |

---

## QLoRA (Quantized LoRA)

### Memory Savings

QLoRA loads base model in 4-bit precision, trains LoRA adapters in fp16.

| Model Size | Full FT | LoRA (fp16) | QLoRA (4-bit) |
|------------|---------|-------------|---------------|
| 7B | 28GB | 16GB | 6-8GB |
| 13B | 52GB | 28GB | 10-12GB |
| 70B | 280GB | 140GB | 40-48GB |

### Key Components

1. **NF4 Quantization** - 4-bit NormalFloat
2. **Double Quantization** - Quantize quantization constants
3. **Paged Optimizers** - Handle memory spikes
4. **fp16 LoRA** - Full precision adapters

### Configuration

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)
```

---

## OpenAI Fine-tuning API

### Supported Models

| Model | Training Cost | Inference Cost |
|-------|---------------|----------------|
| gpt-4o-mini-2024-07-18 | $3.00/1M tokens | $12.00/1M output |
| gpt-4o-2024-08-06 | $25.00/1M tokens | $100.00/1M output |
| gpt-3.5-turbo-0125 | $0.80/1M tokens | $3.20/1M output |

### Training Data Format

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is LoRA?"}, {"role": "assistant", "content": "LoRA (Low-Rank Adaptation) is..."}]}
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "How to fine-tune?"}, {"role": "assistant", "content": "To fine-tune a model..."}]}
```

### Python API

```python
from openai import OpenAI

client = OpenAI()

# Upload training file
with open("training_data.jsonl", "rb") as f:
    file = client.files.create(file=f, purpose="fine-tune")

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 1.8
    },
    suffix="my-custom-model"
)

# Monitor progress
print(f"Job ID: {job.id}")
print(f"Status: {job.status}")

# List events
events = client.fine_tuning.jobs.list_events(job.id)
for event in events.data:
    print(event.message)

# Use fine-tuned model
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:my-org::abc123",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Best Practices

1. **Minimum 10 examples** - but 50-100+ recommended
2. **Consistent format** - same system prompt across examples
3. **Quality over quantity** - clean, accurate examples
4. **Validation set** - 10-20% for monitoring
5. **Suffix naming** - descriptive, version-tracked

---

## LLaMA-Factory

### Overview

User-friendly framework with WebUI for training LLMs.

### Installation

```bash
git clone https://github.com/hiyouga/LLaMA-Factory.git
cd LLaMA-Factory
pip install -e ".[torch,metrics]"

# Launch WebUI
python src/webui.py
```

### Supported Models

| Family | Models |
|--------|--------|
| **LLaMA** | Llama-2, Llama-3, Llama-3.1, Llama-3.2 |
| **Mistral** | Mistral-7B, Mixtral-8x7B |
| **Qwen** | Qwen-1.5, Qwen-2, Qwen-2.5 |
| **Yi** | Yi-6B, Yi-34B |
| **Phi** | Phi-2, Phi-3, Phi-3.5 |
| **DeepSeek** | DeepSeek-V2, DeepSeek-V3 |

### CLI Training

```bash
# LoRA fine-tuning
llamafactory-cli train \
    --stage sft \
    --model_name_or_path meta-llama/Llama-3.1-8B \
    --dataset alpaca_en \
    --template llama3 \
    --finetuning_type lora \
    --lora_rank 16 \
    --lora_target q_proj,v_proj \
    --output_dir output/llama3-lora \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 4 \
    --learning_rate 5e-5 \
    --num_train_epochs 3 \
    --fp16

# Merge LoRA adapter
llamafactory-cli export \
    --model_name_or_path meta-llama/Llama-3.1-8B \
    --adapter_name_or_path output/llama3-lora \
    --template llama3 \
    --finetuning_type lora \
    --export_dir merged_model
```

### Dataset Formats

**Alpaca Format:**
```json
[
  {
    "instruction": "Summarize the following text",
    "input": "Long text here...",
    "output": "Summary here..."
  }
]
```

**ShareGPT Format:**
```json
[
  {
    "conversations": [
      {"from": "human", "value": "What is AI?"},
      {"from": "gpt", "value": "AI stands for..."}
    ]
  }
]
```

---

## Unsloth

### Overview

2x faster training with 80% less memory using custom CUDA kernels.

### Installation

```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

### Quick Start

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments

# Load model (4-bit)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-1B",
    max_seq_length=2048,
    dtype=None,  # Auto-detect
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",  # 30% less VRAM
    random_state=42,
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    warmup_steps=10,
    max_steps=60,
    learning_rate=2e-4,
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=42,
)

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=training_args,
)

trainer.train()

# Save LoRA
model.save_pretrained("lora_model")
tokenizer.save_pretrained("lora_model")

# Save merged 16-bit
model.save_pretrained_merged("merged_16bit", tokenizer, save_method="merged_16bit")

# Save GGUF for llama.cpp / Ollama
model.save_pretrained_gguf("model_gguf", tokenizer, quantization_method="q4_k_m")
```

### Key Features

| Feature | Benefit |
|---------|---------|
| **RoPE Scaling** | 4x longer context |
| **Gradient Checkpointing** | 30% less VRAM |
| **4-bit Loading** | Train 70B on 48GB |
| **Flash Attention 2** | 2x faster attention |
| **GGUF Export** | Direct Ollama deployment |

---

## Axolotl

### Overview

Advanced framework for complex training scenarios.

### Installation

```bash
pip install axolotl
# Or from source
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install -e ".[flash-attn,deepspeed]"
```

### Configuration (YAML)

```yaml
# config.yaml
base_model: meta-llama/Llama-3.1-8B
model_type: LlamaForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: my_dataset.jsonl
    type: alpaca
    data_files:
      - train.jsonl

dataset_prepared_path: prepared_data
val_set_size: 0.05
output_dir: ./outputs

adapter: lora
lora_r: 32
lora_alpha: 16
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
  - gate_proj
  - down_proj
  - up_proj

sequence_len: 4096
sample_packing: true
pad_to_sequence_len: true

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 2e-4
warmup_ratio: 0.03
weight_decay: 0.01

train_on_inputs: false
group_by_length: false
bf16: auto
fp16: false
tf32: false

gradient_checkpointing: true
flash_attention: true
deepspeed: null

wandb_project: my-finetune
wandb_run_id: run-001
wandb_log_model: false

special_tokens:
  pad_token: "<|end_of_text|>"
```

### Training

```bash
# Single GPU
accelerate launch -m axolotl.cli.train config.yaml

# Multi-GPU (DeepSpeed)
accelerate launch --config_file deepspeed.yaml -m axolotl.cli.train config.yaml

# Inference test
accelerate launch -m axolotl.cli.inference config.yaml --lora_model_dir ./outputs
```

---

## Dataset Preparation

### Format Comparison

| Format | Structure | Use Case |
|--------|-----------|----------|
| **Alpaca** | instruction, input, output | Single-turn tasks |
| **ShareGPT** | conversations array | Multi-turn chat |
| **OpenAI** | messages array | API fine-tuning |
| **Completion** | prompt, completion | Text completion |

### Data Cleaning Pipeline

```python
import json
from datasets import load_dataset

def clean_dataset(raw_data):
    cleaned = []
    seen = set()

    for item in raw_data:
        # Remove duplicates
        key = (item.get("instruction", ""), item.get("output", ""))
        if key in seen:
            continue
        seen.add(key)

        # Filter empty
        if not item.get("output", "").strip():
            continue

        # Filter too short
        if len(item.get("output", "")) < 10:
            continue

        # Filter too long (adjust as needed)
        if len(item.get("output", "")) > 4096:
            continue

        cleaned.append(item)

    return cleaned

# Load and clean
with open("raw_data.json") as f:
    raw = json.load(f)

cleaned = clean_dataset(raw)
print(f"Cleaned: {len(raw)} -> {len(cleaned)}")

# Save
with open("cleaned_data.json", "w") as f:
    json.dump(cleaned, f, indent=2)
```

### Prompt Formatting

```python
def format_alpaca(example):
    """Format for instruction-following."""
    if example.get("input"):
        return f"""### Instruction:
{example['instruction']}

### Input:
{example['input']}

### Response:
{example['output']}"""
    else:
        return f"""### Instruction:
{example['instruction']}

### Response:
{example['output']}"""

def format_chat(example):
    """Format for chat models."""
    messages = []
    for msg in example["conversations"]:
        role = "user" if msg["from"] == "human" else "assistant"
        messages.append({"role": role, "content": msg["value"]})
    return messages
```

### Quality Guidelines

| Criterion | Description |
|-----------|-------------|
| **Accuracy** | Factually correct responses |
| **Consistency** | Same format across examples |
| **Diversity** | Varied instructions and domains |
| **Length** | Appropriate response length |
| **No Toxicity** | Filter harmful content |
| **No PII** | Remove personal information |

---

## Training Configuration

### Hyperparameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| **learning_rate** | Step size | 1e-5 to 5e-4 |
| **batch_size** | Samples per step | 1-8 (per GPU) |
| **epochs** | Full passes | 1-5 |
| **warmup_ratio** | LR warmup | 0.03-0.1 |
| **weight_decay** | Regularization | 0.01-0.1 |
| **max_seq_length** | Token limit | 512-8192 |

### Learning Rate Schedules

| Schedule | Description | Use Case |
|----------|-------------|----------|
| **constant** | Fixed LR | Short training |
| **linear** | Linear decay | General |
| **cosine** | Cosine decay | Best for most cases |
| **cosine_with_restarts** | Multiple cycles | Long training |

### Gradient Accumulation

```python
# Effective batch size = batch_size * gradient_accumulation_steps * num_gpus
# Example: 2 * 4 * 1 = 8 effective batch size
training_args = TrainingArguments(
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
)
```

---

## Evaluation Metrics

### Perplexity

Lower is better. Measures model uncertainty.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def calculate_perplexity(model, tokenizer, text, device="cuda"):
    encodings = tokenizer(text, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**encodings, labels=encodings.input_ids)

    return torch.exp(outputs.loss).item()

# Usage
ppl = calculate_perplexity(model, tokenizer, "Sample text here")
print(f"Perplexity: {ppl:.2f}")
```

### Task-Specific Benchmarks

| Benchmark | Tasks | Metrics |
|-----------|-------|---------|
| **MMLU** | Multi-task knowledge | Accuracy |
| **HellaSwag** | Commonsense reasoning | Accuracy |
| **TruthfulQA** | Factual accuracy | MC1, MC2 |
| **HumanEval** | Code generation | Pass@1, Pass@10 |
| **GSM8K** | Math reasoning | Accuracy |
| **BBH** | Hard tasks | Accuracy |

### Using LM Evaluation Harness

```bash
pip install lm-eval

# Evaluate on multiple benchmarks
lm_eval --model hf \
    --model_args pretrained=./my_model \
    --tasks mmlu,hellaswag,truthfulqa \
    --device cuda:0 \
    --batch_size 8
```

### Human Evaluation

| Aspect | Rating Scale |
|--------|--------------|
| **Fluency** | 1-5 (grammatically correct) |
| **Relevance** | 1-5 (answers the question) |
| **Accuracy** | 1-5 (factually correct) |
| **Helpfulness** | 1-5 (useful response) |

---

## Model Merging

### Merge Strategies

| Method | Description | Use Case |
|--------|-------------|----------|
| **Linear** | Weighted average | Simple blending |
| **SLERP** | Spherical interpolation | Smooth transitions |
| **TIES** | Trimmed sparse averaging | Reduce interference |
| **DARE** | Drop and rescale | Better generalization |

### Using mergekit

```bash
pip install mergekit

# Create merge config (merge.yaml)
```

```yaml
# merge.yaml
slices:
  - sources:
      - model: base_model
        layer_range: [0, 32]
      - model: finetuned_model
        layer_range: [0, 32]
    merge_method: slerp
    base_model: base_model
    parameters:
      t: 0.5

merge_method: slerp
dtype: float16
```

```bash
# Run merge
mergekit-yaml merge.yaml ./merged_output
```

### LoRA Merging

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load LoRA
model = PeftModel.from_pretrained(base_model, "path/to/lora")

# Merge and unload
merged = model.merge_and_unload()

# Save
merged.save_pretrained("merged_model")
```

---

## Alignment Methods

### Supervised Fine-tuning (SFT)

Basic instruction following on curated data.

### RLHF (Reinforcement Learning from Human Feedback)

```
SFT Model → Reward Model → PPO Training → RLHF Model
```

### DPO (Direct Preference Optimization)

Simpler alternative to RLHF. No reward model needed.

```python
from trl import DPOTrainer, DPOConfig

# Dataset format
# {"prompt": "...", "chosen": "preferred response", "rejected": "worse response"}

dpo_config = DPOConfig(
    beta=0.1,  # KL penalty
    learning_rate=5e-7,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
)

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()
```

### ORPO (Odds Ratio Preference Optimization)

2024 method. Even simpler than DPO.

```python
from trl import ORPOTrainer, ORPOConfig

orpo_config = ORPOConfig(
    beta=0.1,
    learning_rate=8e-6,
    per_device_train_batch_size=2,
    num_train_epochs=1,
)

trainer = ORPOTrainer(
    model=model,
    args=orpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)
```

---

## Deployment

### GGUF for llama.cpp / Ollama

```python
# Using Unsloth
model.save_pretrained_gguf("model", tokenizer, quantization_method="q4_k_m")

# Quantization options
# q4_k_m - Good balance (recommended)
# q5_k_m - Better quality
# q8_0 - Highest quality
# q2_k - Smallest size
```

### Create Ollama Model

```dockerfile
# Modelfile
FROM ./model-q4_k_m.gguf

TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

PARAMETER stop "<|start_header_id|>"
PARAMETER stop "<|end_header_id|>"
PARAMETER stop "<|eot_id|>"
```

```bash
ollama create my-model -f Modelfile
ollama run my-model
```

### vLLM Deployment

```bash
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model ./merged_model \
    --port 8000 \
    --tensor-parallel-size 1

# API call
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "merged_model", "prompt": "Hello", "max_tokens": 50}'
```

### Text Generation Inference (TGI)

```bash
docker run --gpus all -p 8080:80 \
    -v $PWD/model:/data \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id /data \
    --max-input-length 4096 \
    --max-total-tokens 8192
```

---

## Cost Optimization

### GPU Selection

| GPU | VRAM | Models | Cloud Cost |
|-----|------|--------|------------|
| **RTX 3090** | 24GB | 7B full, 13B QLoRA | $0.50/hr |
| **RTX 4090** | 24GB | 7B full, 13B QLoRA | $0.75/hr |
| **A10G** | 24GB | 7B full, 13B QLoRA | $1.00/hr |
| **A100 40GB** | 40GB | 13B full, 70B QLoRA | $3.50/hr |
| **A100 80GB** | 80GB | 70B full | $4.50/hr |
| **H100** | 80GB | 70B full (fastest) | $8.00/hr |

### Cost Reduction Strategies

| Strategy | Savings | Trade-off |
|----------|---------|-----------|
| **QLoRA instead of LoRA** | 50-70% VRAM | Slightly slower |
| **Gradient checkpointing** | 30% VRAM | 20% slower |
| **Mixed precision (bf16)** | 50% VRAM | None |
| **Smaller batch + grad accum** | Variable | Same effective batch |
| **Shorter sequences** | Linear | Less context |
| **Fewer epochs** | Linear | Less convergence |

### Cloud Providers

| Provider | GPU Options | Pricing Model |
|----------|-------------|---------------|
| **RunPod** | A100, H100, 4090 | Per hour |
| **Lambda Labs** | A100, H100 | Per hour |
| **Vast.ai** | Various | Auction-based |
| **Google Colab Pro+** | A100, V100 | Monthly ($50) |
| **AWS SageMaker** | p4d, p5 | Per hour |

### Training Time Estimation

```python
def estimate_training_time(
    dataset_size: int,
    batch_size: int,
    gradient_accumulation: int,
    epochs: int,
    tokens_per_second: int = 1000,
    avg_seq_length: int = 512
):
    """Estimate training time in hours."""
    steps = (dataset_size // (batch_size * gradient_accumulation)) * epochs
    total_tokens = steps * batch_size * gradient_accumulation * avg_seq_length
    hours = total_tokens / tokens_per_second / 3600
    return hours

# Example
hours = estimate_training_time(
    dataset_size=10000,
    batch_size=2,
    gradient_accumulation=4,
    epochs=3,
    tokens_per_second=2000,  # A100
)
print(f"Estimated: {hours:.1f} hours")
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **OOM (Out of Memory)** | Reduce batch size, use QLoRA, gradient checkpointing |
| **Loss not decreasing** | Lower LR, check data quality, increase rank |
| **Overfitting** | Add dropout, reduce epochs, more data |
| **Catastrophic forgetting** | Lower LR, use regularization |
| **Slow training** | Use Flash Attention, optimize data loading |
| **NaN loss** | Lower LR, check for bad data, use bf16 |

### Debugging Tips

```python
# Check GPU memory
import torch
print(f"Allocated: {torch.cuda.memory_allocated() / 1e9:.2f} GB")
print(f"Reserved: {torch.cuda.memory_reserved() / 1e9:.2f} GB")

# Monitor training
from transformers import TrainerCallback

class LogCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs:
            print(f"Step {state.global_step}: loss={logs.get('loss', 'N/A'):.4f}")
```

---

## Quick Start Checklist

1. [ ] **Choose technique** - LoRA for most cases, QLoRA for limited GPU
2. [ ] **Prepare dataset** - Clean, format, deduplicate (min 100 examples)
3. [ ] **Select base model** - Llama 3.1, Mistral, Qwen 2.5
4. [ ] **Configure training** - LR 2e-4, rank 16, epochs 3
5. [ ] **Monitor metrics** - Loss, perplexity, validation loss
6. [ ] **Evaluate** - Perplexity, task benchmarks, human eval
7. [ ] **Merge/Export** - GGUF for local, vLLM for serving
8. [ ] **Deploy** - Ollama, vLLM, TGI

---

## References

- [Hugging Face PEFT](https://huggingface.co/docs/peft)
- [TRL Documentation](https://huggingface.co/docs/trl)
- [LLaMA-Factory GitHub](https://github.com/hiyouga/LLaMA-Factory)
- [Unsloth GitHub](https://github.com/unslothai/unsloth)
- [Axolotl GitHub](https://github.com/OpenAccess-AI-Collective/axolotl)
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [DPO Paper](https://arxiv.org/abs/2305.18290)
- [ORPO Paper](https://arxiv.org/abs/2403.07691)

---

## Tools

| Tool | Purpose |
|------|---------|
| [Hugging Face Hub](https://huggingface.co) | Model hosting, datasets |
| [Weights & Biases](https://wandb.ai) | Experiment tracking |
| [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) | Benchmarking |
| [mergekit](https://github.com/arcee-ai/mergekit) | Model merging |
| [Ollama](https://ollama.ai) | Local deployment |
| [vLLM](https://github.com/vllm-project/vllm) | Production serving |

---

*Last updated: 2026-01-18*
*Skill version: 1.0*
