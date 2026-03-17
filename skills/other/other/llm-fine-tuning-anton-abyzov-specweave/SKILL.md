---
description: "LLM Fine-Tuning expert. Covers LoRA, QLoRA, PEFT, dataset preparation, Hugging Face Trainer/TRL, RLHF, DPO, quantization (GPTQ/AWQ/GGUF), model merging, distributed training with DeepSpeed/FSDP, hardware selection, and production deployment of fine-tuned models. Activates for: fine-tune, fine-tuning, LoRA, QLoRA, PEFT, RLHF, DPO, GPTQ, AWQ, GGUF, LLM training, model training, quantization, DeepSpeed."
model: opus
context: fork
---

# LLM Fine-Tuning

Expert guidance for fine-tuning large language models efficiently. Covers parameter-efficient methods, dataset preparation, training pipelines, alignment techniques, quantization, and production deployment.

## When to Fine-Tune: Decision Framework

### Fine-Tune vs RAG vs Prompt Engineering

| Approach | Best When | Cost | Time | Maintenance |
|----------|-----------|------|------|-------------|
| Prompt Engineering | Behavior is achievable with instructions | Lowest | Minutes | Low |
| RAG | Model needs access to specific knowledge | Medium | Hours | Medium (index updates) |
| Fine-Tuning | Model needs new behavior/style/format | High | Hours-Days | High (retraining) |
| Fine-Tune + RAG | Need both new behavior AND specific knowledge | Highest | Days | Highest |

### Fine-Tuning Decision Checklist

Choose fine-tuning when:
- [ ] Prompt engineering cannot achieve the desired output format or style
- [ ] RAG retrieval adds too much latency or cost for production
- [ ] You need consistent behavior that prompt instructions cannot guarantee
- [ ] You have 500+ high-quality training examples
- [ ] The task is repetitive and well-defined (classification, extraction, formatting)
- [ ] You need to reduce token usage (shorter prompts after fine-tuning)
- [ ] Domain-specific terminology or reasoning patterns are required

Do NOT fine-tune when:
- Prompt engineering or few-shot examples work well enough
- Your data is small (< 100 examples) or low quality
- The knowledge changes frequently (use RAG instead)
- You need the model to access external information (use tools/RAG)

## LoRA (Low-Rank Adaptation)

### How LoRA Works

LoRA freezes the pretrained model weights and injects trainable low-rank decomposition matrices into transformer layers. Instead of updating a weight matrix W (d x d), it learns A (d x r) and B (r x d) where r << d.

### Basic LoRA Configuration

```python
from peft import LoraConfig, get_peft_model, TaskType

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank: 8-64 typical, higher = more capacity
    lora_alpha=32,                 # Scaling factor, usually 2x rank
    lora_dropout=0.05,             # Dropout for regularization
    target_modules=[               # Which layers to adapt
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj",       # MLP (optional)
    ],
    bias="none",                   # "none", "all", or "lora_only"
)

model = get_peft_model(base_model, lora_config)
model.print_trainable_parameters()
# trainable params: 6,553,600 || all params: 6,744,682,496 || trainable%: 0.0971
```

### LoRA Rank Selection Guide

| Rank (r) | Trainable Params | Use Case |
|----------|-----------------|----------|
| 4-8 | Very few | Simple style transfer, format adaptation |
| 16-32 | Moderate | General fine-tuning, most tasks |
| 64-128 | Many | Complex domain adaptation, multilingual |
| 256+ | Large | Approaching full fine-tune quality |

### Target Module Selection

```python
# Find all available modules
from peft import PeftModel
import re

def find_target_modules(model):
    """List all linear layers that can be targeted by LoRA."""
    linear_modules = set()
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):
            # Get the last part of the module name
            names = name.split(".")
            linear_modules.add(names[-1])
    return list(linear_modules)

# Common target modules by model family:
# Llama/Mistral: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
# GPT-NeoX: query_key_value, dense, dense_h_to_4h, dense_4h_to_h
# Falcon: query_key_value, dense, dense_h_to_4h, dense_4h_to_h
```

## QLoRA: Fine-Tuning on Consumer Hardware

QLoRA combines 4-bit quantization with LoRA, enabling fine-tuning of 70B models on a single 48GB GPU.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 (best for LLMs)
    bnb_4bit_compute_dtype=torch.bfloat16, # Compute in bf16
    bnb_4bit_use_double_quant=True,       # Nested quantization saves ~0.4 bits/param
)

# Load model in 4-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer.pad_token = tokenizer.eos_token

# Prepare for k-bit training (freezes, casts, enables gradient checkpointing)
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules="all-linear",  # Shorthand: targets all linear layers
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
```

### Hardware Requirements for QLoRA

| Model Size | VRAM (QLoRA) | VRAM (Full Fine-Tune) | GPU Example |
|-----------|-------------|----------------------|-------------|
| 7-8B | 6-10 GB | 60+ GB | RTX 3090/4090 |
| 13B | 10-16 GB | 100+ GB | RTX 4090/A6000 |
| 34B | 20-28 GB | 250+ GB | A100 40GB |
| 70B | 36-48 GB | 500+ GB | A100 80GB |

## Dataset Preparation

### Instruction Format

```python
from datasets import Dataset

# Alpaca-style format
training_data = [
    {
        "instruction": "Summarize the following text in one sentence.",
        "input": "The quick brown fox jumped over the lazy dog. The dog was sleeping...",
        "output": "A fox jumped over a sleeping dog."
    },
    {
        "instruction": "Translate the following English text to French.",
        "input": "Hello, how are you?",
        "output": "Bonjour, comment allez-vous?"
    },
]

dataset = Dataset.from_list(training_data)
```

### Chat Template Format

```python
# Chat/conversation format (preferred for modern models)
chat_data = [
    {
        "messages": [
            {"role": "system", "content": "You are a medical coding assistant."},
            {"role": "user", "content": "What ICD-10 code for type 2 diabetes?"},
            {"role": "assistant", "content": "The ICD-10 code for type 2 diabetes mellitus is E11."},
        ]
    },
    {
        "messages": [
            {"role": "system", "content": "You are a medical coding assistant."},
            {"role": "user", "content": "Code for acute myocardial infarction?"},
            {"role": "assistant", "content": "The ICD-10 code for acute myocardial infarction is I21."},
        ]
    },
]

dataset = Dataset.from_list(chat_data)

# Apply chat template during tokenization
def format_chat(example):
    text = tokenizer.apply_chat_template(
        example["messages"],
        tokenize=False,
        add_generation_prompt=False,
    )
    return {"text": text}

dataset = dataset.map(format_chat)
```

### Data Quality Checklist

- [ ] Minimum 500 examples (1000+ preferred for robust results)
- [ ] Consistent format across all examples
- [ ] Diverse inputs covering expected use cases
- [ ] Correct and high-quality outputs (garbage in = garbage out)
- [ ] No personally identifiable information (PII)
- [ ] Balanced distribution across categories/topics
- [ ] Deduplicated (no exact or near-duplicates)
- [ ] Train/validation split (90/10 or 80/20)

## Training with Hugging Face TRL

### SFTTrainer (Supervised Fine-Tuning)

```python
from trl import SFTTrainer, SFTConfig

training_args = SFTConfig(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,    # Effective batch size = 4 * 4 = 16
    gradient_checkpointing=True,       # Saves VRAM at cost of ~20% speed
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    weight_decay=0.01,
    max_seq_length=2048,
    packing=True,                      # Pack multiple short examples per sequence
    bf16=True,                         # Use bf16 mixed precision
    logging_steps=10,
    save_strategy="steps",
    save_steps=100,
    eval_strategy="steps",
    eval_steps=100,
    save_total_limit=3,
    load_best_model_at_end=True,
    report_to="wandb",                 # Weights & Biases logging
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    peft_config=lora_config,           # Pass LoRA config directly
)

trainer.train()

# Save the LoRA adapter (small, typically 10-100 MB)
trainer.save_model("./final_adapter")
```

### Training Hyperparameter Guide

| Parameter | Recommended Range | Notes |
|-----------|------------------|-------|
| Learning rate | 1e-5 to 3e-4 | 2e-4 is a safe default for LoRA |
| Epochs | 1-5 | More epochs risk overfitting; monitor eval loss |
| Batch size (effective) | 8-64 | Larger = more stable, use grad accumulation |
| Warmup ratio | 0.03-0.1 | Prevents early training instability |
| Weight decay | 0.01-0.1 | Regularization, 0.01 is safe default |
| Max seq length | 512-4096 | Match your use case; longer = more VRAM |
| LoRA rank | 8-64 | Start with 16, increase if underfitting |

## RLHF and DPO (Alignment)

### Direct Preference Optimization (DPO)

DPO is simpler than full RLHF since it does not require training a separate reward model.

```python
from trl import DPOTrainer, DPOConfig

# Dataset format: each example has a prompt, chosen response, and rejected response
dpo_data = [
    {
        "prompt": "Explain quantum computing simply.",
        "chosen": "Quantum computing uses quantum bits (qubits) that can be 0, 1, or both simultaneously...",
        "rejected": "Quantum computing is a complex field involving superposition and entanglement of quantum states in Hilbert space...",
    },
]
dpo_dataset = Dataset.from_list(dpo_data)

dpo_config = DPOConfig(
    output_dir="./dpo_results",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-6,                # Lower LR for DPO
    beta=0.1,                          # KL penalty strength (0.1-0.5)
    bf16=True,
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    report_to="wandb",
)

dpo_trainer = DPOTrainer(
    model=model,
    args=dpo_config,
    train_dataset=dpo_dataset,
    tokenizer=tokenizer,
    peft_config=lora_config,
)

dpo_trainer.train()
```

### RLHF Pipeline (Full)

```python
from trl import PPOConfig, PPOTrainer, AutoModelForCausalLMWithValueHead

# Step 1: Train a reward model on preference data
# Step 2: Use PPO to optimize the policy model against the reward model

ppo_config = PPOConfig(
    model_name="meta-llama/Llama-3.1-8B-Instruct",
    learning_rate=1e-5,
    batch_size=16,
    mini_batch_size=4,
    ppo_epochs=4,
    kl_penalty="kl",
    target_kl=6.0,
)

model = AutoModelForCausalLMWithValueHead.from_pretrained(ppo_config.model_name)
ppo_trainer = PPOTrainer(config=ppo_config, model=model, tokenizer=tokenizer)

# Training loop
for batch in dataloader:
    query_tensors = batch["input_ids"]
    response_tensors = ppo_trainer.generate(query_tensors, max_new_tokens=256)
    rewards = reward_model(query_tensors, response_tensors)
    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
```

## Quantization Formats

### Comparison

| Format | Bits | Speed | Quality | Use Case |
|--------|------|-------|---------|----------|
| BF16 | 16 | Baseline | Best | Training, high-end inference |
| GPTQ | 4/8 | Fast (GPU) | Very good | GPU deployment |
| AWQ | 4 | Fastest (GPU) | Very good | GPU deployment, best perf |
| GGUF | 2-8 | Good (CPU/GPU) | Varies | llama.cpp, local inference |
| bitsandbytes | 4/8 | Moderate | Good | Training (QLoRA), prototyping |

### GPTQ Quantization

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, GPTQConfig

# Quantize a model to 4-bit GPTQ
quantization_config = GPTQConfig(
    bits=4,
    dataset="c4",                     # Calibration dataset
    group_size=128,                    # Quantization group size
    desc_act=True,                     # Better quality, slightly slower
    sym=True,                          # Symmetric quantization
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=quantization_config,
    device_map="auto",
)

model.save_pretrained("./llama-3.1-8b-gptq-4bit")
```

### AWQ Quantization

```python
from awq import AutoAWQForCausalLM

model = AutoAWQForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")

quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM",                # GEMM or GEMV
}

model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized("./llama-3.1-8b-awq-4bit")
```

### GGUF Conversion (for llama.cpp)

```bash
# Convert HF model to GGUF
python llama.cpp/convert_hf_to_gguf.py \
    ./model-directory \
    --outfile model.gguf \
    --outtype q4_k_m

# Quantization levels:
# q2_k   - 2-bit (smallest, lowest quality)
# q4_0   - 4-bit (fast, decent quality)
# q4_k_m - 4-bit k-quant medium (best balance)
# q5_k_m - 5-bit k-quant medium (good quality)
# q6_k   - 6-bit (high quality)
# q8_0   - 8-bit (near lossless)
```

## Model Merging

Combine multiple fine-tuned models without additional training.

```python
# Using mergekit
# Install: pip install mergekit

# mergekit-config.yaml for TIES merge
"""
models:
  - model: base-model/path
    parameters:
      density: 1.0
      weight: 1.0
  - model: code-adapter/path
    parameters:
      density: 0.5
      weight: 0.7
  - model: math-adapter/path
    parameters:
      density: 0.5
      weight: 0.3

merge_method: ties
base_model: base-model/path
parameters:
  normalize: true
  int8_mask: true
dtype: bfloat16
"""
```

```bash
# Run merge
mergekit-yaml mergekit-config.yaml ./merged-model --cuda
```

### Merge Method Selection

| Method | Best For | Quality |
|--------|----------|---------|
| Linear | Two similar models | Good baseline |
| SLERP | Two models, smooth interpolation | Better for dissimilar |
| TIES | Multiple models, resolve conflicts | Best for 3+ models |
| DARE | Multiple models with pruning | Good for diverse skills |

## Distributed Training

### DeepSpeed ZeRO

```python
# deepspeed_config.json
"""
{
    "bf16": {"enabled": true},
    "zero_optimization": {
        "stage": 2,
        "offload_optimizer": {"device": "cpu", "pin_memory": true},
        "allgather_partitions": true,
        "reduce_scatter": true
    },
    "gradient_accumulation_steps": 4,
    "gradient_clipping": 1.0,
    "train_batch_size": "auto",
    "train_micro_batch_size_per_gpu": "auto"
}
"""

# In SFTConfig
training_args = SFTConfig(
    ...,
    deepspeed="deepspeed_config.json",
)

# Launch
# deepspeed --num_gpus=4 train.py
```

### FSDP (Fully Sharded Data Parallel)

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    ...,
    fsdp="full_shard auto_wrap",
    fsdp_config={
        "fsdp_transformer_layer_cls_to_wrap": "LlamaDecoderLayer",
        "fsdp_backward_prefetch": "backward_pre",
        "fsdp_forward_prefetch": True,
        "fsdp_use_orig_params": True,
        "fsdp_cpu_ram_efficient_loading": True,
        "fsdp_sync_module_states": True,
    },
)

# Launch
# torchrun --nproc_per_node=4 train.py
```

### ZeRO Stage Selection

| Stage | Shards | VRAM Savings | Communication | Use When |
|-------|--------|-------------|---------------|----------|
| ZeRO-1 | Optimizer states | ~4x | Low | 2-4 GPUs, large batch |
| ZeRO-2 | + Gradients | ~8x | Medium | 4-8 GPUs, standard |
| ZeRO-3 | + Parameters | ~Nx | High | Model too large for 1 GPU |
| ZeRO-3 + Offload | + CPU offload | Maximum | Highest | Maximum VRAM savings |

## Evaluation

### Automated Metrics

```python
import evaluate

# Perplexity (lower is better, measures model confidence)
perplexity = evaluate.load("perplexity")
results = perplexity.compute(
    predictions=generated_texts,
    model_id="meta-llama/Llama-3.1-8B",
)

# Task-specific evaluation
from lm_eval import evaluator

results = evaluator.simple_evaluate(
    model="hf",
    model_args="pretrained=./fine-tuned-model",
    tasks=["mmlu", "hellaswag", "arc_challenge"],
    batch_size=8,
)
```

### Catastrophic Forgetting Detection

```python
def evaluate_forgetting(base_model, fine_tuned_model, general_benchmarks):
    """Compare base vs fine-tuned on general tasks to detect forgetting."""
    base_scores = run_benchmarks(base_model, general_benchmarks)
    ft_scores = run_benchmarks(fine_tuned_model, general_benchmarks)

    for task in general_benchmarks:
        delta = ft_scores[task] - base_scores[task]
        if delta < -0.05:  # > 5% degradation
            print(f"WARNING: Forgetting detected on {task}: {delta:.2%}")

    return {"base": base_scores, "fine_tuned": ft_scores}
```

### Prevention Strategies

- Use low LoRA rank (8-16) to limit weight changes
- Short training (1-3 epochs) to avoid overfitting
- Include general-purpose examples in training data (5-10%)
- Use regularization (weight decay, dropout)
- Evaluate on general benchmarks throughout training

## Deployment of Fine-Tuned Models

### Merge and Export LoRA

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Load and merge adapter
model = PeftModel.from_pretrained(base_model, "./final_adapter")
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")

# Push to Hub
merged_model.push_to_hub("my-org/my-fine-tuned-model")
tokenizer.push_to_hub("my-org/my-fine-tuned-model")
```

### Serve with vLLM

```bash
# Install: pip install vllm
# Serve the merged model
vllm serve ./merged_model \
    --dtype bfloat16 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.9 \
    --port 8000

# Or serve with LoRA adapter on the fly
vllm serve meta-llama/Llama-3.1-8B \
    --enable-lora \
    --lora-modules my-adapter=./final_adapter \
    --max-lora-rank 64
```

### Serve with TGI (Text Generation Inference)

```bash
docker run --gpus all --shm-size 1g \
    -v ./merged_model:/model \
    -p 8080:80 \
    ghcr.io/huggingface/text-generation-inference:latest \
    --model-id /model \
    --quantize bitsandbytes-nf4 \
    --max-input-length 2048 \
    --max-total-tokens 4096
```
