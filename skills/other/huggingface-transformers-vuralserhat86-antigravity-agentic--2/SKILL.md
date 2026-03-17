---
name: huggingface_transformers
router_kit: AIKit
description: Hugging Face Transformers best practices including model loading, tokenization, fine-tuning workflows, and inference optimization. Use when working with transformer models, fine-tuning LLMs, implementing NLP tasks, or optimizing transformer inference.
metadata:
  skillport:
    category: auto-healed
    tags: [bert, big data, cleaning, csv, data analysis, data engineering, data science, database, etl pipelines, export, gpt, huggingface transformers, import, inference, json, machine learning basics, migration, models, nlp, nosql, numpy, pandas, python data stack, query optimization, reporting, schema design, sql, statistics, transformation, visualization]
---

# Hugging Face Transformers Best Practices

Comprehensive guide to using the Hugging Face Transformers library including model loading, tokenization, fine-tuning workflows, pipeline usage, custom datasets, and deployment optimization.

---

## Quick Reference

**When to use this skill:**
- Loading and using pre-trained transformers (BERT, GPT, T5, LLaMA, etc.)
- Fine-tuning models on custom data
- Implementing NLP tasks (classification, QA, generation, etc.)
- Optimizing inference (quantization, ONNX, etc.)
- Debugging tokenization issues
- Using Hugging Face pipelines
- Deploying transformers to production

**Models covered:**
- Encoders: BERT, RoBERTa, DeBERTa, ALBERT
- Decoders: GPT-2, GPT-Neo, LLaMA, Mistral
- Encoder-Decoders: T5, BART, Flan-T5
- Vision: ViT, CLIP, Stable Diffusion

---

## Part 1: Model Loading Patterns

### Pattern 1: Basic Model Loading

```python
from transformers import AutoModel, AutoTokenizer

# Load model and tokenizer
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# For specific tasks
from transformers import AutoModelForSequenceClassification
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=3  # For 3-class classification
)
```

### Pattern 2: Loading with Specific Configuration

```python
from transformers import AutoConfig, AutoModel

# Modify configuration
config = AutoConfig.from_pretrained("bert-base-uncased")
config.hidden_dropout_prob = 0.2  # Custom dropout
config.attention_probs_dropout_prob = 0.2

# Load model with custom config
model = AutoModel.from_pretrained("bert-base-uncased", config=config)

# Or create model from scratch with config
model = AutoModel.from_config(config)
```

### Pattern 3: Loading Quantized Models (Memory Efficient)

```python
from transformers import AutoModel, BitsAndBytesConfig
import torch

# 8-bit quantization (50% memory reduction)
quantization_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModel.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=quantization_config,
    device_map="auto"  # Automatic device placement
)

# 4-bit quantization (75% memory reduction)
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

model = AutoModel.from_pretrained(
    "meta-llama/Llama-2-13b-hf",
    quantization_config=quantization_config,
    device_map="auto"
)
```

### Pattern 4: Loading from Local Path

```python
# Save model locally
model.save_pretrained("./my-model")
tokenizer.save_pretrained("./my-model")

# Load from local path
model = AutoModel.from_pretrained("./my-model")
tokenizer = AutoTokenizer.from_pretrained("./my-model")
```

---

## Part 2: Tokenization Best Practices

### Critical Tokenization Patterns

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# ✅ CORRECT: All required arguments
tokens = tokenizer(
    text,
    padding=True,  # Pad to longest in batch
    truncation=True,  # Truncate to max_length
    max_length=512,  # Maximum sequence length
    return_tensors="pt"  # Return PyTorch tensors
)

# Access components
input_ids = tokens['input_ids']  # Token IDs
attention_mask = tokens['attention_mask']  # Padding mask
token_type_ids = tokens.get('token_type_ids')  # Segment IDs (BERT)

# ❌ WRONG: Missing critical arguments
tokens = tokenizer(text)  # No padding, truncation, or tensor format!
```

### Batch Tokenization

```python
# Tokenize multiple texts efficiently
texts = ["First text", "Second text", "Third text"]

tokens = tokenizer(
    texts,
    padding=True,  # Pad all to longest in batch
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

# Result shape: [batch_size, max_length]
print(tokens['input_ids'].shape)  # torch.Size([3, max_len_in_batch])
```

### Special Token Handling

```python
# Add special tokens
tokenizer.add_special_tokens({
    'additional_special_tokens': ['[CUSTOM]', '[MARKER]']
})

# Resize model embeddings to match
model.resize_token_embeddings(len(tokenizer))

# Encode with special tokens preserved
text = "Hello [CUSTOM] world"
tokens = tokenizer(text, add_special_tokens=True)

# Decode
decoded = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=False)
```

### Tokenization for Different Tasks

```python
# Text classification (single sequence)
tokens = tokenizer(
    "This movie was great!",
    padding="max_length",
    truncation=True,
    max_length=128,
    return_tensors="pt"
)

# Question answering (pair of sequences)
question = "What is the capital of France?"
context = "France is a country in Europe. Paris is its capital."

tokens = tokenizer(
    question,
    context,
    padding="max_length",
    truncation="only_second",  # Only truncate context
    max_length=384,
    return_tensors="pt"
)

# Text generation (decoder-only models)
prompt = "Once upon a time"
tokens = tokenizer(prompt, return_tensors="pt")
# No padding needed for generation input
```

---

## Part 3: Fine-Tuning Workflows

### Pattern 1: Simple Fine-Tuning with Trainer

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments
)
from datasets import load_dataset

# 1. Load dataset
dataset = load_dataset("glue", "mrpc")

# 2. Load model
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# 3. Tokenize dataset
def tokenize_function(examples):
    return tokenizer(
        examples["sentence1"],
        examples["sentence2"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 4. Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

# 5. Define metrics
from datasets import load_metric
import numpy as np

metric = load_metric("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# 6. Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
    compute_metrics=compute_metrics,
)

# 7. Train
trainer.train()

# 8. Save
trainer.save_model("./fine-tuned-model")
```

### Pattern 2: LoRA Fine-Tuning (Parameter-Efficient)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_8bit=True,  # 8-bit for memory efficiency
    device_map="auto"
)

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,  # LoRA rank
    lora_alpha=32,  # LoRA alpha
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Check trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 4.2M || all params: 6.7B || trainable%: 0.062%

# Train with Trainer (same as before)
# Only LoRA parameters are updated!
```

### Pattern 3: Custom Training Loop

```python
import torch
from torch.utils.data import DataLoader
from transformers import AdamW, get_scheduler

# Prepare dataloaders
train_dataloader = DataLoader(tokenized_datasets["train"], batch_size=16, shuffle=True)
eval_dataloader = DataLoader(tokenized_datasets["validation"], batch_size=16)

# Optimizer
optimizer = AdamW(model.parameters(), lr=2e-5)

# Learning rate scheduler
num_epochs = 3
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=500,
    num_training_steps=num_training_steps
)

# Training loop
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(num_epochs):
    model.train()
    for batch in train_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}

        outputs = model(**batch)
        loss = outputs.loss
        loss.backward()

        optimizer.step()
        lr_scheduler.step()
        optimizer.zero_grad()

    # Evaluation
    model.eval()
    for batch in eval_dataloader:
        batch = {k: v.to(device) for k, v in batch.items()}
        with torch.no_grad():
            outputs = model(**batch)
        # Compute metrics
```

---

## Part 4: Pipeline Usage (High-Level API)

### Text Classification Pipeline

```python
from transformers import pipeline

# Load pipeline
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Single prediction
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Batch prediction
results = classifier([
    "Great service!",
    "Terrible experience",
    "Average quality"
])
```

### Question Answering Pipeline

```python
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

result = qa_pipeline(
    question="What is the capital of France?",
    context="France is a country in Europe. Its capital is Paris, a beautiful city."
)
# {'score': 0.98, 'start': 49, 'end': 54, 'answer': 'Paris'}
```

### Text Generation Pipeline

```python
generator = pipeline("text-generation", model="gpt2")

outputs = generator(
    "Once upon a time",
    max_length=50,
    num_return_sequences=3,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    do_sample=True
)

for output in outputs:
    print(output['generated_text'])
```

### Zero-Shot Classification Pipeline

```python
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

result = classifier(
    "This is a course about Python programming.",
    candidate_labels=["education", "technology", "business", "sports"]
)
# {'sequence': '...', 'labels': ['education', 'technology', ...], 'scores': [0.85, 0.12, ...]}
```

---

## Part 5: Inference Optimization

### Optimization 1: Batch Processing

```python
# ❌ SLOW: Process one at a time
for text in texts:
    output = model(**tokenizer(text, return_tensors="pt"))

# ✅ FAST: Process in batches
batch_size = 32
for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
```

### Optimization 2: Mixed Precision (AMP)

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in dataloader:
    optimizer.zero_grad()

    # Forward pass in mixed precision
    with autocast():
        outputs = model(**batch)
        loss = outputs.loss

    # Backward pass with scaled gradients
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### Optimization 3: ONNX Export

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from optimum.onnxruntime import ORTModelForSequenceClassification

# Export to ONNX
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
model.save_pretrained("./onnx-model", export=True)

# Load ONNX model (faster inference)
ort_model = ORTModelForSequenceClassification.from_pretrained("./onnx-model")

# Inference (2-3x faster)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
inputs = tokenizer("Hello world", return_tensors="pt")
outputs = ort_model(**inputs)
```

### Optimization 4: Dynamic Quantization

```python
import torch

# Quantize model to int8
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},  # Quantize Linear layers
    dtype=torch.qint8
)

# 4x smaller model, 2-3x faster inference on CPU
```

---

## Part 6: Common Issues & Solutions

### Issue 1: CUDA Out of Memory

**Problem:** `RuntimeError: CUDA out of memory`

**Solutions:**

```python
# Solution 1: Reduce batch size
training_args = TrainingArguments(
    per_device_train_batch_size=8,  # Was 32
    gradient_accumulation_steps=4,  # Effective batch = 8*4 = 32
)

# Solution 2: Use gradient checkpointing
model.gradient_checkpointing_enable()

# Solution 3: Use 8-bit model
from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model = AutoModel.from_pretrained("model-name", quantization_config=quantization_config)

# Solution 4: Clear cache
import torch
torch.cuda.empty_cache()
```

### Issue 2: Slow Tokenization

**Problem:** Tokenization is bottleneck

**Solutions:**

```python
# Solution 1: Use fast tokenizers
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased", use_fast=True)

# Solution 2: Tokenize dataset once, cache it
tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    num_proc=4,  # Parallel processing
    remove_columns=dataset.column_names,
    load_from_cache_file=True  # Cache results
)

# Solution 3: Use larger batches for tokenization
tokenizer(
    texts,
    padding=True,
    truncation=True,
    max_length=512,
    return_tensors="pt",
    batched=True,  # Process multiple texts at once
    batch_size=1000
)
```

### Issue 3: Inconsistent Results

**Problem:** Model outputs different results for same input

**Solution:**

```python
# Set seeds for reproducibility
import random
import numpy as np
import torch

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)

# Disable dropout during inference
model.eval()

# Use deterministic generation
outputs = model.generate(
    inputs,
    do_sample=False,  # Greedy decoding
    # OR
    do_sample=True,
    temperature=1.0,
    top_k=50,
    seed=42  # For sampling
)
```

### Issue 4: Attention Mask Errors

**Problem:** `IndexError: index out of range in self`

**Solution:**

```python
# ✅ ALWAYS provide attention mask
tokens = tokenizer(
    text,
    padding=True,
    truncation=True,
    return_tensors="pt",
    return_attention_mask=True  # Explicit (usually default)
)

# Use it in model forward
outputs = model(
    input_ids=tokens['input_ids'],
    attention_mask=tokens['attention_mask']  # Don't forget this!
)

# For custom padding
attention_mask = (input_ids != tokenizer.pad_token_id).long()
```

---

## Part 7: Model-Specific Patterns

### GPT Models (Decoder-Only)

```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set pad token (GPT doesn't have one by default)
tokenizer.pad_token = tokenizer.eos_token

# Generation
input_text = "The future of AI is"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_new_tokens=50,
    num_beams=5,  # Beam search
    early_stopping=True,
    no_repeat_ngram_size=2,  # Prevent repetition
    temperature=0.8,
    top_p=0.9
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### T5 Models (Encoder-Decoder)

```python
from transformers import T5ForConditionalGeneration, T5Tokenizer

model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# T5 expects task prefix
input_text = "translate English to German: How are you?"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(
    **inputs,
    max_length=50
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
# "Wie geht es dir?"
```

### BERT Models (Encoder-Only)

```python
from transformers import BertForMaskedLM, BertTokenizer

model = BertForMaskedLM.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# Masked language modeling
text = "Paris is the [MASK] of France."
inputs = tokenizer(text, return_tensors="pt")

# Get predictions for [MASK]
outputs = model(**inputs)
mask_token_index = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)[1]
mask_token_logits = outputs.logits[0, mask_token_index, :]

# Top 5 predictions
top_5_tokens = torch.topk(mask_token_logits, 5, dim=1).indices[0].tolist()
for token in top_5_tokens:
    print(tokenizer.decode([token]))
# capital, city, center, heart, ...
```

---

## Part 8: Production Deployment

### FastAPI Serving Pattern

```python
from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Load model once at startup
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

class TextInput(BaseModel):
    text: str

@app.post("/classify")
async def classify_text(input: TextInput):
    result = classifier(input.text)[0]
    return {
        "label": result['label'],
        "confidence": result['score']
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Batch Inference Optimization

```python
import asyncio
from typing import List

class BatchPredictor:
    def __init__(self, model, tokenizer, max_batch_size=32):
        self.model = model
        self.tokenizer = tokenizer
        self.max_batch_size = max_batch_size
        self.queue = []
        self.lock = asyncio.Lock()

    async def predict(self, text: str):
        async with self.lock:
            future = asyncio.Future()
            self.queue.append((text, future))

            if len(self.queue) >= self.max_batch_size:
                await self._process_batch()

        return await future

    async def _process_batch(self):
        if not self.queue:
            return

        texts, futures = zip(*self.queue)
        self.queue = []

        # Process batch
        inputs = self.tokenizer(list(texts), padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        results = outputs.logits.argmax(dim=-1).tolist()

        # Return results
        for future, result in zip(futures, results):
            future.set_result(result)
```

---

## Quick Decision Trees

### "Which model should I use?"

```
*Hugging Face Transformers v1.1 - Enhanced*

## 🔄 Workflow

> **Kaynak:** [Hugging Face Course](https://huggingface.co/course) & [Production Guide](https://huggingface.co/docs/transformers/performance)

### Aşama 1: Model Selection
- [ ] **Task**: Görevine en uygun mimariyi seç (Encoder: classification, Decoder: generation).
- [ ] **License**: Modelin ticari kullanım izni (Apache 2.0 vs Llama Community) var mı?
- [ ] **Size**: Parametre sayısı vs performans dengesini kur (7B genellikle yeterli).

### Aşama 2: Optimization pipeline
- [ ] **Quantization**: Inference için 4-bit / 8-bit quantization (BitsAndBytes) kullan.
- [ ] **Batching**: Tek tek değil, batch halinde process et (GPU verimi).
- [ ] **Format**: Production için ONNX veya TensorRT formatına çevir.

### Aşama 3: Deployment
- [ ] **Cache**: Model ağırlıklarını ve tokenizer'ı docker image içine bake etme, volume kullan.
- [ ] **Token Limits**: Context window sınırını aşan inputlar için strateji belirle (chunking).

### Kontrol Noktaları
| Aşama | Doğrulama |
|-------|-----------|
| 1 | Model GPU hafızasına sığıyor mu (OOM hatası)? |
| 2 | Inference süresi (Latency) hedefin altında mı? |
| 3 | Tokenizer ile Model uyumlu mu (aynı vocab)? |
  Classification → BERT, RoBERTa, DeBERTa
  Generation → GPT-2, GPT-Neo, LLaMA
  Translation/Summarization → T5, BART, mT5
  Question Answering → BERT, DeBERTa, RoBERTa

Performance vs Speed?
  Best performance → Large models (355M+ params)
  Balanced → Base models (110M params)
  Fast inference → Distilled models (66M params)
```

### "How should I fine-tune?"

```
Have full dataset control?
  YES → Full fine-tuning or LoRA
  NO → Few-shot prompting

Dataset size?
  Large (>10K examples) → Full fine-tuning
  Medium (1K-10K) → LoRA or full fine-tuning
  Small (<1K) → LoRA or prompt engineering

Compute available?
  Limited → LoRA (4-bit quantized)
  Moderate → LoRA (8-bit)
  High → Full fine-tuning
```

---

## Resources

- **Hugging Face Docs:** https://huggingface.co/docs/transformers/
- **Model Hub:** https://huggingface.co/models
- **PEFT (LoRA):** https://huggingface.co/docs/peft/
- **Optimum:** https://huggingface.co/docs/optimum/
- **Datasets:** https://huggingface.co/docs/datasets/

---

**Skill version:** 1.0.0
**Last updated:** 2025-10-25
**Maintained by:** Applied Artificial Intelligence
