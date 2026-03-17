---
name: transformers
description: Loading and using pretrained models with Hugging Face Transformers. Use when working with pretrained models from the Hub, running inference with Pipeline API, fine-tuning models with Trainer, or handling text, vision, audio, and multimodal tasks.
---

# Using Hugging Face Transformers

Transformers is the model-definition framework for state-of-the-art machine learning across text, vision, audio, and multimodal domains. It provides unified APIs for loading pretrained models, running inference, and fine-tuning.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Pipeline API](#pipeline-api)
- [Model Loading](#model-loading)
- [Inference Patterns](#inference-patterns)
- [Fine-tuning with Trainer](#fine-tuning-with-trainer)
- [Working with Modalities](#working-with-modalities)
- [Memory and Performance](#memory-and-performance)
- [Best Practices](#best-practices)

## Core Concepts

### The Three Core Classes

Every model in Transformers has three core components:

```python
from transformers import AutoConfig, AutoModel, AutoTokenizer

# Configuration: hyperparameters and architecture settings
config = AutoConfig.from_pretrained("bert-base-uncased")

# Model: the neural network weights
model = AutoModel.from_pretrained("bert-base-uncased")

# Tokenizer/Processor: converts inputs to tensors
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
```

### The `from_pretrained` Pattern

All loading uses `from_pretrained()` which handles downloading, caching, and device placement:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-3.2-1B"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",  # Automatic device placement
)
```

### Auto Classes

Use task-specific Auto classes for the correct model head:

```python
from transformers import (
    AutoModelForCausalLM,          # Text generation (GPT, Llama)
    AutoModelForSeq2SeqLM,         # Encoder-decoder (T5, BART)
    AutoModelForSequenceClassification,  # Classification
    AutoModelForTokenClassification,     # NER, POS tagging
    AutoModelForQuestionAnswering,       # Extractive QA
    AutoModelForMaskedLM,                # BERT-style masked LM
    AutoModelForImageClassification,     # Vision models
    AutoModelForSpeechSeq2Seq,           # Speech recognition
)
```

## Pipeline API

The `pipeline()` function provides high-level inference with minimal code:

### Text Tasks

```python
from transformers import pipeline

# Text generation
generator = pipeline("text-generation", model="Qwen/Qwen2.5-1.5B")
output = generator("The secret to success is", max_new_tokens=50)

# Text classification
classifier = pipeline("sentiment-analysis")
result = classifier("I love this product!")
# [{'label': 'POSITIVE', 'score': 0.9998}]

# Named entity recognition
ner = pipeline("ner", aggregation_strategy="simple")
entities = ner("Hugging Face is based in New York City.")

# Question answering
qa = pipeline("question-answering")
answer = qa(question="What is the capital?", context="Paris is the capital of France.")

# Summarization
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summary = summarizer(long_text, max_length=130, min_length=30)

# Translation
translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
result = translator("Hello, how are you?")
```

### Chat/Conversational

```python
from transformers import pipeline
import torch

pipe = pipeline(
    "text-generation",
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing in simple terms."},
]

response = pipe(messages, max_new_tokens=256)
print(response[0]["generated_text"][-1]["content"])
```

### Vision Tasks

```python
# Image classification
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
result = classifier("path/to/image.jpg")

# Object detection
detector = pipeline("object-detection", model="facebook/detr-resnet-50")
objects = detector("path/to/image.jpg")

# Image segmentation
segmenter = pipeline("image-segmentation", model="facebook/mask2former-swin-base-coco-panoptic")
masks = segmenter("path/to/image.jpg")
```

### Audio Tasks

```python
# Speech recognition
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
text = transcriber("path/to/audio.mp3")

# Audio classification
classifier = pipeline("audio-classification", model="superb/wav2vec2-base-superb-ks")
result = classifier("path/to/audio.wav")
```

### Multimodal Tasks

```python
# Visual question answering
vqa = pipeline("visual-question-answering", model="Salesforce/blip-vqa-base")
answer = vqa(image="image.jpg", question="What color is the car?")

# Image-to-text (captioning)
captioner = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
caption = captioner("image.jpg")

# Document question answering
doc_qa = pipeline("document-question-answering", model="impira/layoutlm-document-qa")
answer = doc_qa(image="document.png", question="What is the total?")
```

## Model Loading

### Device Placement

```python
from transformers import AutoModelForCausalLM
import torch

# Automatic placement across available devices
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

# Specific device
model = AutoModelForCausalLM.from_pretrained(
    "gpt2",
    device_map="cuda:0",
)

# Custom device map for model parallelism
device_map = {
    "model.embed_tokens": 0,
    "model.layers.0": 0,
    "model.layers.1": 1,
    "model.norm": 1,
    "lm_head": 1,
}
model = AutoModelForCausalLM.from_pretrained(model_name, device_map=device_map)
```

### Loading from Local Path

```python
# Save model locally
model.save_pretrained("./my_model")
tokenizer.save_pretrained("./my_model")

# Load from local path
model = AutoModelForCausalLM.from_pretrained("./my_model")
tokenizer = AutoTokenizer.from_pretrained("./my_model")
```

### Trust Remote Code

Some models require executing custom code from the Hub:

```python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    trust_remote_code=True,  # Required for custom architectures
)
```

## Inference Patterns

### Text Generation

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_name = "Qwen/Qwen2.5-3B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Basic generation
inputs = tokenizer("Once upon a time", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# With generation config
outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    repetition_penalty=1.1,
)
```

### Chat Templates

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

# Apply chat template
input_text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)

inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### Getting Embeddings

```python
from transformers import AutoModel, AutoTokenizer
import torch

model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(texts: list[str]) -> torch.Tensor:
    inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    # Mean pooling
    attention_mask = inputs["attention_mask"]
    embeddings = outputs.last_hidden_state
    mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
    sum_embeddings = (embeddings * mask_expanded).sum(1)
    sum_mask = mask_expanded.sum(1).clamp(min=1e-9)
    return sum_embeddings / sum_mask

embeddings = get_embeddings(["Hello world", "How are you?"])
```

### Classification

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

inputs = tokenizer("I love this movie!", return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.softmax(outputs.logits, dim=-1)

labels = model.config.id2label
for idx, prob in enumerate(predictions[0]):
    print(f"{labels[idx]}: {prob:.4f}")
```

## Fine-tuning with Trainer

### Basic Fine-tuning

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
from datasets import load_dataset

# Load data and model
dataset = load_dataset("imdb")
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2,
)

# Tokenize dataset
def tokenize(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized = dataset.map(tokenize, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_steps=100,
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
)

trainer.train()
```

### Pushing to Hub

```python
# Login first: huggingface-cli login

# Push model and tokenizer
model.push_to_hub("my-username/my-fine-tuned-model")
tokenizer.push_to_hub("my-username/my-fine-tuned-model")

# Or use trainer
trainer.push_to_hub()
```

See `reference/fine-tuning.md` for advanced patterns including LoRA, custom data collators, and evaluation metrics.

## Working with Modalities

### Vision Models

```python
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = AutoModelForImageClassification.from_pretrained("google/vit-base-patch16-224")

image = Image.open("image.jpg")
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    predicted_class = outputs.logits.argmax(-1).item()
    print(model.config.id2label[predicted_class])
```

### Audio Models

```python
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch

processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    "openai/whisper-large-v3",
    torch_dtype=torch.float16,
    device_map="auto",
)

# Load audio (use librosa, soundfile, or datasets)
import librosa
audio, sr = librosa.load("audio.mp3", sr=16000)

inputs = processor(audio, sampling_rate=16000, return_tensors="pt")
inputs = inputs.to(model.device)

generated_ids = model.generate(**inputs)
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
```

### Vision-Language Models

```python
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch

model_name = "llava-hf/llava-1.5-7b-hf"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

image = Image.open("image.jpg")
prompt = "USER: <image>\nDescribe this image in detail.\nASSISTANT:"

inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200)
response = processor.decode(outputs[0], skip_special_tokens=True)
```

## Memory and Performance

### Quantization

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

# 4-bit quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    quantization_config=bnb_config,
    device_map="auto",
)

# 8-bit quantization
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    load_in_8bit=True,
    device_map="auto",
)
```

### Flash Attention

```python
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",  # Requires flash-attn package
    device_map="auto",
)
```

### torch.compile

```python
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
model = torch.compile(model, mode="reduce-overhead")
```

### Batched Inference

```python
texts = ["First prompt", "Second prompt", "Third prompt"]
inputs = tokenizer(texts, return_tensors="pt", padding=True).to(model.device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=50)

decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
```

See `reference/advanced-inference.md` for streaming, KV caching, and serving patterns.

## Best Practices

1. **Use bfloat16 over float16**: Better numerical stability on modern GPUs
2. **Set pad token for generation**: `tokenizer.pad_token = tokenizer.eos_token`
3. **Use device_map="auto"**: Let Accelerate handle device placement
4. **Enable Flash Attention**: Significant speedup for long sequences
5. **Batch when possible**: Amortize fixed costs across multiple inputs
6. **Use pipeline for quick prototyping**: Switch to manual control for production
7. **Cache models locally**: Set `HF_HOME` environment variable for model cache location
8. **Check model license**: Verify usage rights before deployment

## References

See `reference/` for detailed documentation:
- `fine-tuning.md` - Advanced fine-tuning patterns with LoRA, PEFT, and custom training
- `advanced-inference.md` - Generation strategies, streaming, and serving
