---
name: huggingface-transformers
description: Use Hugging Face Transformers for local model inference, embeddings, and fine-tuning. Covers pipelines, model selection, quantization, and optimization. Use when working with local LLMs, embeddings, or custom model training.
---

# Hugging Face Transformers Skill

## Quick Reference

| Task | Approach | Key Class |
|------|----------|-----------|
| Text Generation | `pipeline("text-generation")` | `AutoModelForCausalLM` |
| Classification | `pipeline("text-classification")` | `AutoModelForSequenceClassification` |
| Embeddings | `sentence-transformers` | `SentenceTransformer` |
| NER | `pipeline("ner")` | `AutoModelForTokenClassification` |
| QA | `pipeline("question-answering")` | `AutoModelForQuestionAnswering` |
| Fine-tuning | `Trainer` API | `TrainingArguments` |

## Installation

```bash
# Core transformers
pip install transformers torch

# With all extras
pip install transformers[torch] accelerate

# For embeddings
pip install sentence-transformers

# For quantization
pip install bitsandbytes

# For PEFT/LoRA
pip install peft

# For datasets
pip install datasets
```

## Pipeline API (Fastest Start)

### Text Generation

```python
from transformers import pipeline

# Simple generation
generator = pipeline("text-generation", model="microsoft/DialoGPT-medium")
result = generator("Hello, how are you?", max_length=50, num_return_sequences=1)
print(result[0]["generated_text"])

# With specific model for instruction following
generator = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    device_map="auto",
    torch_dtype="auto"
)

messages = [{"role": "user", "content": "Explain transformers in 2 sentences"}]
response = generator(messages, max_new_tokens=100)
```

### Text Classification

```python
from transformers import pipeline

# Sentiment analysis
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Multi-label classification
classifier = pipeline(
    "text-classification",
    model="facebook/bart-large-mnli",
    top_k=None  # Return all labels with scores
)

# Zero-shot classification
classifier = pipeline("zero-shot-classification")
result = classifier(
    "This is a tutorial about machine learning",
    candidate_labels=["education", "politics", "business"]
)
```

### Named Entity Recognition

```python
from transformers import pipeline

ner = pipeline("ner", aggregation_strategy="simple")
text = "Apple CEO Tim Cook announced new products in Cupertino"
entities = ner(text)

for entity in entities:
    print(f"{entity['word']}: {entity['entity_group']} ({entity['score']:.2f})")
# Apple: ORG (0.99)
# Tim Cook: PER (0.99)
# Cupertino: LOC (0.98)
```

### Question Answering

```python
from transformers import pipeline

qa = pipeline("question-answering")
context = """
Hugging Face is a company that develops tools for building machine learning 
applications. It was founded in 2016 and is headquartered in New York City.
"""
question = "When was Hugging Face founded?"
result = qa(question=question, context=context)
# {'answer': '2016', 'score': 0.98, 'start': 89, 'end': 93}
```

### Summarization

```python
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
text = """Your long document text here..."""
summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
```

## Model and Tokenizer Loading

### Basic Loading

```python
from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM

# Load tokenizer and model separately
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

# For text generation models
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    device_map="auto",
    torch_dtype="auto"
)
```

### Loading with Options

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    torch_dtype=torch.float16,      # Half precision
    device_map="auto",              # Automatic GPU placement
    low_cpu_mem_usage=True,         # Reduce RAM during loading
    trust_remote_code=True,         # For custom architectures
    attn_implementation="flash_attention_2"  # If available
)

tokenizer = AutoTokenizer.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    padding_side="left",            # For batch generation
    use_fast=True                   # Use Rust tokenizer
)
tokenizer.pad_token = tokenizer.eos_token  # Set pad token
```

### Offline Loading

```python
# Download model for offline use
from transformers import AutoModel, AutoTokenizer

model_name = "bert-base-uncased"
save_path = "./models/bert-base"

# Download and save
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
tokenizer.save_pretrained(save_path)
model.save_pretrained(save_path)

# Load offline
tokenizer = AutoTokenizer.from_pretrained(save_path, local_files_only=True)
model = AutoModel.from_pretrained(save_path, local_files_only=True)
```

## Embeddings with Sentence Transformers

### Basic Embeddings

```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Single text
embedding = model.encode("Hello, world!")
print(f"Dimension: {len(embedding)}")  # 384

# Batch encoding
sentences = ["First sentence", "Second sentence", "Third sentence"]
embeddings = model.encode(sentences, show_progress_bar=True)
```

### Semantic Similarity

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-mpnet-base-v2")

query = "How to learn Python?"
documents = [
    "Python tutorial for beginners",
    "Advanced JavaScript patterns",
    "Machine learning with Python",
    "Cooking recipes for dinner"
]

# Encode
query_embedding = model.encode(query, convert_to_tensor=True)
doc_embeddings = model.encode(documents, convert_to_tensor=True)

# Calculate similarity
scores = util.cos_sim(query_embedding, doc_embeddings)[0]

# Rank results
ranked = sorted(zip(documents, scores.tolist()), key=lambda x: x[1], reverse=True)
for doc, score in ranked:
    print(f"{score:.3f}: {doc}")
```

### Embedding Model Selection

| Model | Dim | Use Case |
|-------|-----|----------|
| `all-MiniLM-L6-v2` | 384 | Fast, general purpose |
| `all-mpnet-base-v2` | 768 | Higher quality, balanced |
| `bge-large-en-v1.5` | 1024 | State-of-the-art retrieval |
| `e5-large-v2` | 1024 | Multilingual support |
| `nomic-embed-text-v1` | 768 | Long context (8K tokens) |

### Optimized Embedding Generation

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# Batch processing with optimal settings
embeddings = model.encode(
    large_text_list,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True  # For cosine similarity
)
```

## Text Generation (Advanced)

### Chat-Style Generation

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float16
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Write a haiku about coding"}
]

# Apply chat template
input_ids = tokenizer.apply_chat_template(
    messages,
    return_tensors="pt",
    add_generation_prompt=True
).to(model.device)

# Generate
outputs = model.generate(
    input_ids,
    max_new_tokens=100,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    pad_token_id=tokenizer.eos_token_id
)

response = tokenizer.decode(outputs[0][input_ids.shape[1]:], skip_special_tokens=True)
```

### Streaming Generation

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto")

streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

inputs = tokenizer("Explain quantum computing:", return_tensors="pt").to(model.device)

generation_kwargs = {
    **inputs,
    "streamer": streamer,
    "max_new_tokens": 200,
    "do_sample": True,
    "temperature": 0.7
}

thread = Thread(target=model.generate, kwargs=generation_kwargs)
thread.start()

for text in streamer:
    print(text, end="", flush=True)
```

### Generation Parameters

```python
outputs = model.generate(
    input_ids,
    # Length control
    max_new_tokens=256,
    min_new_tokens=10,
    
    # Sampling strategy
    do_sample=True,
    temperature=0.8,        # Randomness (0.0 = greedy)
    top_k=50,               # Top-k sampling
    top_p=0.95,             # Nucleus sampling
    
    # Repetition control
    repetition_penalty=1.1,
    no_repeat_ngram_size=3,
    
    # Beam search (alternative to sampling)
    # num_beams=4,
    # early_stopping=True,
    
    # Other
    pad_token_id=tokenizer.eos_token_id,
    eos_token_id=tokenizer.eos_token_id
)
```

## Quantization

### BitsAndBytes 4-bit Quantization

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",              # Normal float 4
    bnb_4bit_compute_dtype=torch.float16,    # Computation dtype
    bnb_4bit_use_double_quant=True           # Nested quantization
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    quantization_config=bnb_config,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
```

### 8-bit Quantization

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)
```

### GPTQ Models (Pre-quantized)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load pre-quantized GPTQ model
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Mistral-7B-v0.1-GPTQ",
    device_map="auto",
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained("TheBloke/Mistral-7B-v0.1-GPTQ")
```

### Memory Comparison

| Model (7B) | Precision | VRAM | Quality |
|------------|-----------|------|---------|
| Full | FP32 | ~28GB | 100% |
| Half | FP16 | ~14GB | ~99% |
| 8-bit | INT8 | ~7GB | ~97% |
| 4-bit | NF4 | ~4GB | ~95% |

## Fine-Tuning with Trainer

### Basic Fine-Tuning

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from datasets import load_dataset

# Load dataset
dataset = load_dataset("imdb")

# Load model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Tokenize dataset
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=100,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"]
)

# Train
trainer.train()
```

### Custom Metrics

```python
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1": f1_score(labels, predictions, average="weighted")
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
)
```

## PEFT and LoRA

### LoRA Fine-Tuning

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    load_in_4bit=True,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# LoRA configuration
lora_config = LoraConfig(
    r=16,                          # Rank
    lora_alpha=32,                 # Alpha scaling
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 4,194,304 || all params: 6,742,609,920 || trainable%: 0.06%
```

### Save and Load LoRA Adapters

```python
# Save adapter only (small file)
model.save_pretrained("./lora-adapter")

# Load adapter onto base model
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
model = PeftModel.from_pretrained(base_model, "./lora-adapter")

# Merge adapter into base model (optional)
merged_model = model.merge_and_unload()
merged_model.save_pretrained("./merged-model")
```

### QLoRA (Quantized LoRA)

```python
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
model = get_peft_model(model, lora_config)
```

## Model Selection from Hub

### Finding Models

```python
from huggingface_hub import HfApi, list_models

api = HfApi()

# Search for models
models = list_models(
    filter="text-generation",
    sort="downloads",
    direction=-1,
    limit=10
)

for model in models:
    print(f"{model.id}: {model.downloads:,} downloads")

# Get model info
model_info = api.model_info("meta-llama/Llama-2-7b-hf")
print(f"Tags: {model_info.tags}")
print(f"License: {model_info.cardData.get('license', 'Unknown')}")
```

### Recommended Models by Task

| Task | Small (<3B) | Medium (3-13B) | Large (>13B) |
|------|-------------|----------------|--------------|
| Chat | TinyLlama-1.1B | Phi-3-mini-4k | Llama-3-70B |
| Code | CodeGemma-2B | CodeLlama-7B | DeepSeek-Coder-33B |
| Embeddings | all-MiniLM-L6-v2 | bge-base-en-v1.5 | bge-large-en-v1.5 |
| Classification | DistilBERT | RoBERTa-base | DeBERTa-v3-large |

## Local Inference Optimization

### Batch Processing

```python
from transformers import pipeline
import torch

# Optimal batching for embeddings
pipe = pipeline(
    "feature-extraction",
    model="sentence-transformers/all-MiniLM-L6-v2",
    device=0 if torch.cuda.is_available() else -1
)

texts = ["text1", "text2", "text3", ...]
batch_size = 32
results = []

for i in range(0, len(texts), batch_size):
    batch = texts[i:i + batch_size]
    embeddings = pipe(batch, truncation=True)
    results.extend(embeddings)
```

### torch.compile for Speed

```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Compile for faster inference (PyTorch 2.0+)
model = torch.compile(model, mode="reduce-overhead")
```

### KV-Cache and Attention Optimization

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    device_map="auto",
    torch_dtype="auto",
    attn_implementation="flash_attention_2"  # Faster attention
)

# For multi-turn generation, use past_key_values
outputs = model.generate(
    input_ids,
    max_new_tokens=50,
    use_cache=True,  # Enable KV-cache
    return_dict_in_generate=True
)
past_key_values = outputs.past_key_values

# Continue generation with cached context
new_outputs = model.generate(
    new_input_ids,
    past_key_values=past_key_values,
    max_new_tokens=50
)
```

### Memory-Efficient Inference

```python
from transformers import AutoModelForCausalLM
import torch

# Gradient checkpointing for large models
model = AutoModelForCausalLM.from_pretrained(
    "large-model",
    device_map="auto",
    torch_dtype=torch.float16
)

# Enable for training (saves memory, slower)
model.gradient_checkpointing_enable()

# Inference with no_grad
with torch.no_grad():
    outputs = model.generate(input_ids, max_new_tokens=100)
```

## Best Practices

### 1. Choose the Right Model Size

```python
# Start small, scale up only if needed
MODELS_BY_USE_CASE = {
    "quick_prototype": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "production_chat": "microsoft/Phi-3-mini-4k-instruct",
    "code_generation": "codellama/CodeLlama-7b-hf",
    "embeddings": "sentence-transformers/all-MiniLM-L6-v2"
}
```

### 2. Always Set Device and Dtype

```python
import torch
from transformers import AutoModelForCausalLM

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map="auto" if device == "cuda" else None
)
```

### 3. Handle Tokenizer Edge Cases

```python
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Set pad token for batching
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# For left-padding in generation
tokenizer.padding_side = "left"
```

### 4. Error Handling for Generation

```python
def safe_generate(model, tokenizer, prompt, **kwargs):
    try:
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_new_tokens", 256),
                pad_token_id=tokenizer.eos_token_id,
                **kwargs
            )
        
        response = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )
        return response.strip()
        
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        raise RuntimeError("GPU OOM - try smaller batch or quantized model")
```

### 5. Environment Configuration

```python
import os

# Cache directory
os.environ["HF_HOME"] = "/path/to/cache"
os.environ["TRANSFORMERS_CACHE"] = "/path/to/models"

# Offline mode
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# Disable telemetry
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# Token for gated models
os.environ["HF_TOKEN"] = "your_token_here"
```

## Common Patterns

### Embedding Service

```python
from sentence_transformers import SentenceTransformer
from functools import lru_cache
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: list[str], normalize: bool = True) -> np.ndarray:
        return self.model.encode(
            texts,
            normalize_embeddings=normalize,
            show_progress_bar=len(texts) > 100
        )
    
    @lru_cache(maxsize=10000)
    def embed_cached(self, text: str) -> tuple:
        return tuple(self.embed([text])[0])
```

### LLM Wrapper

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalLLM:
    def __init__(self, model_id: str, quantize: bool = True):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        load_kwargs = {"device_map": "auto", "torch_dtype": torch.float16}
        if quantize:
            from transformers import BitsAndBytesConfig
            load_kwargs["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True)
        
        self.model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate(self, prompt: str, max_tokens: int = 256, **kwargs) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                pad_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )
        
        return self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1]:],
            skip_special_tokens=True
        )
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CUDA OOM | Use 4-bit quantization or smaller model |
| Slow generation | Enable `use_cache=True`, use Flash Attention |
| Truncated output | Increase `max_new_tokens` |
| Repetitive text | Set `repetition_penalty=1.1` |
| Model not found | Check `HF_TOKEN` for gated models |
| Wrong device | Explicitly set `device_map="auto"` |
