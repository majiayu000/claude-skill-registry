---
name: "unsloth-training"
description: "Fine-tune LLMs with Unsloth using GRPO or SFT. Supports FP8, vision models, mobile deployment, Docker, packing, GGUF export. Use when: train with GRPO, fine-tune, reward functions, SFT training, FP8 training, vision fine-tuning, phone deployment, docker training, packing, export to GGUF."
---

<objective>
Guide LLM fine-tuning using Unsloth:

1. **GRPO** - RL with reward functions (no labeled outputs needed)
2. **SFT** - Supervised fine-tuning with input/output pairs
3. **Vision** - VLM fine-tuning (Qwen3-VL, Gemma3, Llama 3.2 Vision)

Key capabilities:
- **FP8 Training** - 60% less VRAM, 1.4x faster (RTX 40+, H100)
- **3x Packing** - Automatic 2-5x speedup for mixed-length data
- **Docker** - Official `unsloth/unsloth` image
- **Mobile** - QAT → ExecuTorch → iOS/Android (~40 tok/s)
- **Export** - GGUF, Ollama, vLLM, LM Studio, SGLang
</objective>

<quick_start>
**GRPO with FP8 (60% less VRAM):**
```python
import os
os.environ['UNSLOTH_VLLM_STANDBY'] = "1"  # Shared memory
from unsloth import FastLanguageModel
from trl import GRPOConfig, GRPOTrainer

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen3-8B",
    max_seq_length=2048, load_in_fp8=True, fast_inference=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    use_gradient_checkpointing="unsloth",
)

def correctness_reward(completions, answer, **kwargs):
    return [2.0 if extract_answer(c) == a else 0.0
            for c, a in zip(completions, answer)]

trainer = GRPOTrainer(
    model=model,
    args=GRPOConfig(num_generations=4, beta=0.04, learning_rate=5e-6),
    train_dataset=dataset, reward_funcs=[correctness_reward],
)
trainer.train()
```

**SFT with Packing (2-5x faster):**
```python
from trl import SFTTrainer, SFTConfig

trainer = SFTTrainer(
    model=model, train_dataset=dataset, processing_class=tokenizer,
    args=SFTConfig(
        per_device_train_batch_size=2, num_train_epochs=3,
        learning_rate=2e-4, packing=True,  # 2-5x speedup
    ),
)
trainer.train()
```
</quick_start>

<success_criteria>
A training run is successful when:
- Model loads without OOM errors
- Reward (GRPO) or loss (SFT) shows improvement trend
- Generated outputs match expected format
- Model exported to desired format (LoRA, merged, GGUF)
- Test inference produces reasonable outputs
</success_criteria>

<activation_triggers>
**Explicit triggers:**
- `/unsloth grpo` - GRPO (RL) training
- `/unsloth sft` - SFT training
- `/unsloth fp8` - FP8 training setup
- `/unsloth vision` - VLM fine-tuning
- `/unsloth mobile` - Phone deployment (QAT)
- `/unsloth docker` - Docker container setup
- `/unsloth troubleshoot` - Debug issues

**Natural language:**
- "train with GRPO", "fine-tune", "reward functions"
- "FP8 training", "fp8", "less VRAM"
- "vision fine-tuning", "VLM", "image training"
- "phone deployment", "mobile LLM", "ExecuTorch"
- "docker training", "container", "unsloth docker"
- "packing", "faster training", "500k context"
- "export GGUF", "Ollama", "vLLM", "SGLang"
</activation_triggers>

<file_locations>
**Core references:**
- `references/reward-design.md` - Reward function patterns
- `references/domain-examples.md` - Voice AI, Sales Agent examples
- `references/hyperparameters.md` - GRPOConfig reference
- `references/troubleshooting.md` - Common fixes

**New feature references:**
- `references/fp8-training.md` - FP8 setup, VRAM savings
- `references/deployment.md` - Docker, vLLM, LoRA hot-swap, SGLang
- `references/export-formats.md` - GGUF, Ollama, LM Studio, Dynamic 2.0
- `references/advanced-training.md` - 500K context, packing, checkpoints
- `references/vision-training.md` - VLM fine-tuning
- `references/mobile-deployment.md` - QAT, ExecuTorch, iOS/Android

**Code examples:** `reference/grpo/`, `reference/sft/`
</file_locations>

<core_concepts>
## When to Use GRPO vs SFT

| Method | Use When | Data Needed |
|--------|----------|-------------|
| **GRPO** | Improving reasoning quality | Prompts + verifiable answers |
| **GRPO** | Aligning behavior with preferences | Reward functions |
| **GRPO** | When you can verify correctness | Verifiable outputs |
| **SFT** | Teaching specific output format | Input/output pairs |
| **SFT** | Following new instructions | Conversation examples |
| **SFT** | Learning domain knowledge | Labeled examples |

## Model Selection

| Model | Size | VRAM | Use Case |
|-------|------|------|----------|
| `unsloth/Qwen2.5-0.5B-Instruct` | 0.5B | 5GB | Mobile deployment (~200MB GGUF) |
| `unsloth/Qwen2.5-1.5B-Instruct` | 1.5B | 5GB | Learning/prototyping |
| `Qwen/Qwen2.5-3B-Instruct` | 3B | 8GB | Good balance (recommended start) |
| `unsloth/Qwen2.5-7B-Instruct` | 7B | 16GB | Production quality |
| `unsloth/Phi-4` | 14B | 20GB | Strong reasoning |

## Core Hyperparameters

**GRPO (RL):**
```python
GRPOConfig(
    num_generations=4,        # Completions per prompt (2-8)
    beta=0.04,                # KL penalty (0.01-0.1)
    learning_rate=5e-6,       # 10x smaller than SFT!
    max_completion_length=512,
    max_steps=300,            # Minimum for results
)
```

**SFT:**
```python
TrainingArguments(
    learning_rate=2e-4,       # Standard SFT rate
    num_train_epochs=3,       # 2-4 typical
    per_device_train_batch_size=2,
)
```
</core_concepts>

<reward_functions>
## Reward Function Design

Reward functions are the core of GRPO. They return a list of floats for each completion.

### Pattern 1: Correctness (Primary Signal)

```python
def correctness_reward(completions, answer, **kwargs):
    """
    +2.0 for correct answer, 0.0 otherwise.
    This should be your highest-weighted reward.
    """
    rewards = []
    for completion, true_answer in zip(completions, answer):
        extracted = extract_answer(completion)
        try:
            pred = float(extracted.replace(",", "").strip())
            true = float(true_answer.replace(",", "").strip())
            reward = 2.0 if abs(pred - true) < 0.01 else 0.0
        except ValueError:
            reward = 2.0 if extracted.strip() == str(true_answer).strip() else 0.0
        rewards.append(reward)
    return rewards
```

### Pattern 2: Format Compliance

```python
def format_reward(completions, **kwargs):
    """
    +0.5 for proper XML structure with reasoning and answer tags.
    """
    rewards = []
    for completion in completions:
        has_reasoning = bool(re.search(r"<reasoning>.*?</reasoning>", completion, re.DOTALL))
        has_answer = bool(re.search(r"<answer>.*?</answer>", completion, re.DOTALL))
        if has_reasoning and has_answer:
            rewards.append(0.5)
        elif has_answer:
            rewards.append(0.2)
        else:
            rewards.append(0.0)
    return rewards
```

### Pattern 3: Reasoning Quality

```python
def reasoning_length_reward(completions, **kwargs):
    """
    +0.3 for substantive reasoning (30-200 words).
    """
    rewards = []
    for completion in completions:
        reasoning = extract_reasoning(completion)
        word_count = len(reasoning.split()) if reasoning else 0
        if 30 <= word_count <= 200:
            rewards.append(0.3)
        elif 15 <= word_count < 30:
            rewards.append(0.1)
        else:
            rewards.append(0.0)
    return rewards
```

### Pattern 4: Negative Constraints

```python
def no_hedging_reward(completions, **kwargs):
    """
    -0.3 penalty for uncertainty language.
    """
    hedging = ["i think", "maybe", "perhaps", "possibly", "i'm not sure"]
    rewards = []
    for completion in completions:
        has_hedging = any(phrase in completion.lower() for phrase in hedging)
        rewards.append(-0.3 if has_hedging else 0.0)
    return rewards
```

### Typical Reward Stack

```python
reward_funcs = [
    correctness_reward,      # +2.0 max (primary signal)
    format_reward,           # +0.5 max (structure)
    reasoning_length_reward, # +0.3 max (quality)
    no_hedging_reward,       # -0.3 max (constraint)
]
# Total range: -0.3 to +2.8
```

> **For domain-specific rewards:** See `references/domain-examples.md` for Voice AI, Sales Agent, and Support patterns.
</reward_functions>

<prompt_format>
## Prompt Structure

### System Prompt with XML Tags

```python
SYSTEM_PROMPT = """You are a helpful assistant that thinks step-by-step.

Always respond in this exact format:
<reasoning>
[Your step-by-step thinking process]
</reasoning>
<answer>
[Your final answer - just the number or short response]
</answer>
"""
```

### Extraction Helpers

```python
import re

def extract_answer(text: str) -> str:
    """Extract answer from XML tags"""
    match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_reasoning(text: str) -> str:
    """Extract reasoning from XML tags"""
    match = re.search(r"<reasoning>(.*?)</reasoning>", text, re.DOTALL)
    return match.group(1).strip() if match else ""
```

### Dataset Format

**GRPO (prompt-only):**
```python
dataset = dataset.map(lambda ex: {
    "prompt": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": ex["question"]}
    ],
    "answer": ex["answer"]  # Ground truth for verification
})
```

**SFT (full conversations):**
```python
dataset = dataset.map(lambda ex: {
    "conversations": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": ex["input"]},
        {"role": "assistant", "content": ex["output"]}
    ]
})
```
</prompt_format>

<model_export>
## Save and Deploy

### Save LoRA Only (~100MB)
```python
model.save_lora("grpo_lora")
```

### Merge and Save Full Model
```python
model.save_pretrained_merged(
    "grpo_merged", tokenizer,
    save_method="merged_16bit",
)
```

### Export to GGUF for Ollama
```python
model.save_pretrained_gguf(
    "grpo_gguf", tokenizer,
    quantization_method="q4_k_m",  # Options: q4_k_m, q8_0, q5_k_m
)
```

### Test with Ollama
```bash
# Create Modelfile
cat > Modelfile << EOF
FROM ./grpo_gguf/unsloth.Q4_K_M.gguf
TEMPLATE """{{ .System }}
User: {{ .Prompt }}
Assistant: """
PARAMETER temperature 0.7
EOF

ollama create my-model -f Modelfile
ollama run my-model "Solve: 15 + 27 = ?"
```
</model_export>

<routing>
## Request Routing

**GRPO training:** → GRPOConfig, reward functions, dataset prep
→ Reference: `reference/grpo/basic_grpo.py`

**SFT training:** → SFTTrainer, dataset formatting
→ Reference: `reference/sft/sales_extractor_training.py`

**Reward function design:** → 4 patterns (correctness, format, quality, constraints)
→ Reference: `references/reward-design.md`, `references/domain-examples.md`

**FP8 training:** → 60% VRAM savings, env vars, pre-quantized models
→ Reference: `references/fp8-training.md`

**Docker setup:** → Official image, volumes, Jupyter/SSH
→ Reference: `references/deployment.md`

**Vision fine-tuning:** → FastVisionModel, VLM data format
→ Reference: `references/vision-training.md`

**Mobile deployment:** → QAT, ExecuTorch, iOS/Android
→ Reference: `references/mobile-deployment.md`

**Long context / packing:** → 500K context, 2-5x speedup
→ Reference: `references/advanced-training.md`

**Export formats:** → GGUF methods, Ollama, vLLM, SGLang
→ Reference: `references/export-formats.md`

**Training issues:** → `references/troubleshooting.md`
</routing>

<troubleshooting_quick>
## Quick Troubleshooting

| Symptom | Fix |
|---------|-----|
| Reward not increasing | Wait 300+ steps, then increase learning_rate 2x |
| Reward spiky/unstable | Decrease learning_rate 0.5x, increase beta |
| Model outputs garbage | Increase beta 2-4x, check prompt format |
| Out of memory | Reduce max_completion_length, num_generations=2 |
| No reasoning appearing | Train 500+ steps, use model >= 1.5B |

> **For detailed troubleshooting:** See `references/troubleshooting.md`
</troubleshooting_quick>

<training_checklist>
## Pre-Training Checklist

**GRPO:**
- [ ] Model loads without OOM
- [ ] LoRA configured with `use_gradient_checkpointing="unsloth"`
- [ ] Dataset has `prompt` and `answer` fields
- [ ] At least one reward function defined and tested
- [ ] `num_generations >= 2`
- [ ] `beta` set (0.01-0.1, start at 0.04)
- [ ] `learning_rate` set (1e-6 to 1e-5)
- [ ] At least 300 steps planned

**SFT:**
- [ ] Model loads without OOM
- [ ] Dataset has conversations or text field
- [ ] Chat template applied correctly
- [ ] `learning_rate` ~2e-4
- [ ] 2-4 epochs planned
</training_checklist>

<cost_estimates>
## Cost Estimates

**Training Data Generation:**
- 50 seeds x 10 variations x ~1000 tokens = ~500K tokens
- Claude Sonnet: ~$1.50
- GPT-4o-mini: ~$0.30

**Training Compute:**
- Google Colab T4: Free (30-60 min for 1000 examples)
- RunPod A40 (48GB): ~$0.79/hr

**Total per experiment:** ~$0.50-$1.00 on RunPod
</cost_estimates>

<example_session>
## Example Session

**User:** "I want to train a model that gives concise voice responses"

**Claude:**
1. First, let's set up the model:
```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-3B-Instruct",
    max_seq_length=1024, load_in_4bit=True,
)
```

2. For voice AI, you need brevity rewards. Here's a custom stack:
```python
def brevity_reward(completions, **kwargs):
    """Voice responses under 50 words get +0.5"""
    return [0.5 if len(c.split()) <= 50 else -0.3 for c in completions]

def speakable_reward(completions, **kwargs):
    """Penalize markdown that sounds bad spoken"""
    bad = ["**", "- ", "```", "http"]
    return [-0.2 * sum(1 for b in bad if b in c) for c in completions]

reward_funcs = [correctness_reward, brevity_reward, speakable_reward]
```

3. See `references/domain-examples.md` for complete Voice AI reward patterns.
</example_session>
