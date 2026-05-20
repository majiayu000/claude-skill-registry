---
name: llm-fine-tuning
description: LoRA/QLoRA/PEFT fine-tuning workflows, dataset formatting, adapter merging, and eval loops. Covers Hugging Face TRL/PEFT patterns, chat template handling, and common training pitfalls.
---

# LLM Fine-Tuning

## When to Use What

| Method | VRAM (7B) | Quality vs Full FT | When to Use |
|--------|-----------|---------------------|-------------|
| Full fine-tuning | 60-80 GB | Baseline | Unlimited compute, max quality, own the weights |
| LoRA (r=64) | 18-24 GB | 95-99% | Production adapters, multi-tenant serving |
| QLoRA (4-bit + LoRA) | 6-10 GB | 90-97% | Single GPU, prototyping, budget-constrained |
| LoRA (r=8-16) | 14-18 GB | 90-95% | Quick experiments, narrow domain tasks |

**Decision rule**: Start with QLoRA to validate the task is learnable, then move to LoRA r=64 or full FT for production.

## Dataset Formatting

### Instruction Format

```python
def format_instruction(example):
    """Alpaca-style. Works with most base models."""
    return {
        "text": (
            f"### Instruction:\n{example['instruction']}\n\n"
            f"### Input:\n{example.get('input', '')}\n\n"
            f"### Response:\n{example['output']}"
        )
    }
```

### Chat Template Format

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

def format_chat(example):
    """Use the model's native chat template. Always prefer this for instruct models."""
    messages = [
        {"role": "system", "content": example.get("system", "You are a helpful assistant.")},
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["answer"]},
    ]
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}
```

### Dataset Prep Pipeline

```python
from datasets import load_dataset, DatasetDict

def prepare_dataset(path, tokenizer, max_length=2048, test_size=0.05):
    ds = load_dataset("json", data_files=path, split="train")
    ds = ds.map(format_chat, remove_columns=ds.column_names)

    # Filter overlength samples rather than truncating -- avoids training on garbage
    ds = ds.filter(lambda x: len(tokenizer.encode(x["text"])) <= max_length)

    split = ds.train_test_split(test_size=test_size, seed=42)
    return DatasetDict({"train": split["train"], "test": split["test"]})
```

**Gotcha**: Truncating mid-response teaches the model to produce incomplete outputs. Filter or increase `max_length` instead.

## PEFT / LoRA Configuration

### Standard LoRA Config

```python
from peft import LoraConfig, TaskType, get_peft_model

lora_config = LoraConfig(
    r=64,
    lora_alpha=128,           # alpha = 2*r is a solid default
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    task_type=TaskType.CAUSAL_LM,
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()  # Expect 1-3% of total
```

### Target Module Selection

| Model Family | Recommended Targets | Notes |
|-------------|-------------------|-------|
| Llama/Mistral | `q,k,v,o_proj` + `gate,up,down_proj` | All linear layers for best quality |
| GPT-NeoX/Pythia | `query_key_value`, `dense` | Fused QKV attention |
| Phi | `q_proj,k_proj,v_proj,dense` | Check model config for names |

Use `model.named_modules()` to discover the actual layer names if unsure.

## QLoRA Setup

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,       # Nested quantization saves ~0.4 GB/B params
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation="flash_attention_2",
)
model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
```

**Gotcha**: `use_reentrant=False` is mandatory with LoRA + gradient checkpointing. The default (`True`) silently skips gradients for LoRA params.

## Training with SFTTrainer

```python
from trl import SFTTrainer, SFTConfig

training_args = SFTConfig(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,        # Effective batch = 16
    learning_rate=2e-4,                   # LoRA tolerates higher LR than full FT
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    max_seq_length=2048,
    dataset_text_field="text",
    packing=True,                         # Pack short sequences together for efficiency
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    peft_config=lora_config,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model("./final_adapter")
```

## Adapter Merging

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load base + adapter, merge, save full model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
model = PeftModel.from_pretrained(base_model, "./final_adapter")
merged = model.merge_and_unload()

merged.save_pretrained("./merged_model")
tokenizer.save_pretrained("./merged_model")
```

**Gotcha**: Don't merge QLoRA adapters directly onto the quantized base. Load the base in full precision (bf16/fp16) first, then load the adapter, then merge.

## Eval Loop

```python
import torch
from torch.utils.data import DataLoader

def evaluate(model, tokenizer, eval_dataset, max_new_tokens=256):
    model.eval()
    predictions, references = [], []

    for example in eval_dataset:
        prompt = extract_prompt(example["text"])  # Everything before assistant response
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,              # Greedy for reproducible eval
                temperature=1.0,
                pad_token_id=tokenizer.eos_token_id,
            )

        pred = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        predictions.append(pred.strip())
        references.append(extract_response(example["text"]))

    return compute_metrics(predictions, references)
```

## Gotchas and Anti-Patterns

### Chat Template Mismatch
Training with one template, inferring with another, destroys quality. Always save the tokenizer alongside the adapter and use `apply_chat_template` consistently.

### Padding Direction
- **Training**: `tokenizer.padding_side = "right"` (standard for causal LM)
- **Batch inference**: `tokenizer.padding_side = "left"` (so generation starts at the right position)
- Forgetting to switch between train/inference is a silent quality killer

### Common Mistakes
- Setting `lora_alpha = r` instead of `2*r` -- underscales the adapter contribution
- Using `packing=True` without checking that your dataset has many short examples -- wastes compute on padding if examples are already near `max_seq_length`
- Not setting `pad_token` -- many models (Llama) don't have one by default: `tokenizer.pad_token = tokenizer.eos_token`
- Training on the prompt tokens -- use `DataCollatorForCompletionOnly` or mask labels manually
- Evaluating with `do_sample=True` -- introduces variance that makes comparison meaningless
