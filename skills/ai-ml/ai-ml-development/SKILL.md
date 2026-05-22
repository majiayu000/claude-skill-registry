---
name: ai-ml-development
description: AI and machine learning development with PyTorch, TensorFlow, and LLM integration. Use when building ML models, training pipelines, fine-tuning LLMs, or implementing AI features.
---

# AI & Machine Learning Development

Comprehensive guide for building AI/ML systems from prototyping to production.

## Frameworks Overview

| Framework        | Best For               | Ecosystem                  |
| ---------------- | ---------------------- | -------------------------- |
| **PyTorch**      | Research, flexibility  | Hugging Face, Lightning    |
| **TensorFlow**   | Production, mobile     | TFX, TF Lite, TF.js        |
| **JAX**          | High-performance, TPUs | Flax, Optax                |
| **scikit-learn** | Classical ML           | Simple, batteries-included |

---

## PyTorch

### Model Definition

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvNet(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 8 * 8, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 64 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        return self.fc2(x)
```

### Training Loop

```python
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm

def train_model(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    epochs: int = 10,
    lr: float = 1e-3,
    device: str = "cuda"
) -> dict:
    model = model.to(device)
    optimizer = AdamW(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        model.train()
        for batch in tqdm(train_loader):
            inputs, labels = batch[0].to(device), batch[1].to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        # Validation
        model.eval()
        correct = total = 0
        with torch.no_grad():
            for batch in val_loader:
                inputs, labels = batch[0].to(device), batch[1].to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

        print(f"Epoch {epoch+1}: Val Acc {100.*correct/total:.2f}%")
```

### PyTorch Lightning

```python
import pytorch_lightning as pl
from torchmetrics import Accuracy

class LitModel(pl.LightningModule):
    def __init__(self, model: nn.Module, lr: float = 1e-3):
        super().__init__()
        self.model = model
        self.lr = lr
        self.criterion = nn.CrossEntropyLoss()
        self.accuracy = Accuracy(task="multiclass", num_classes=10)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        loss = self.criterion(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self.model(x)
        self.accuracy(logits, y)
        self.log("val_acc", self.accuracy)

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.lr)
```

---

## Hugging Face Transformers

### Text Classification

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from datasets import load_dataset

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

dataset = load_dataset("imdb")

def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")

tokenized = dataset.map(preprocess, batched=True)

trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        evaluation_strategy="epoch",
    ),
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
)

trainer.train()
```

### Fine-Tuning LLMs with LoRA

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer

model_name = "meta-llama/Llama-2-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj"],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
```

---

## LLM Integration

### OpenAI API

```python
from openai import OpenAI

client = OpenAI()

def chat_completion(messages: list[dict], model: str = "gpt-4") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content

# Function calling
def extract_entities(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": text}],
        tools=[{
            "type": "function",
            "function": {
                "name": "extract_entities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "people": {"type": "array", "items": {"type": "string"}},
                        "places": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
        }],
    )
    return response.choices[0].message.tool_calls[0].function.arguments
```

### Anthropic Claude API

```python
import anthropic

client = anthropic.Anthropic()

def claude_completion(prompt: str, model: str = "claude-3-sonnet-20240229") -> str:
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
```

### LangChain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_template("Summarize: {text}")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"text": "Long document here..."})
```

---

## Vector Databases

### Pinecone

```python
from pinecone import Pinecone

pc = Pinecone(api_key="xxx")
index = pc.Index("my-index")

# Upsert vectors
index.upsert(vectors=[
    {"id": "1", "values": [0.1, 0.2], "metadata": {"text": "..."}},
])

# Query
results = index.query(vector=[0.1, 0.2], top_k=5, include_metadata=True)
```

### ChromaDB (Local)

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

collection.add(
    documents=["Doc 1", "Doc 2"],
    ids=["doc1", "doc2"],
)

results = collection.query(query_texts=["search query"], n_results=5)
```

---

## MLOps

### Model Registry (MLflow)

```python
import mlflow

mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    mlflow.log_params({"lr": 0.001, "epochs": 10})
    mlflow.log_metrics({"accuracy": 0.95})
    mlflow.pytorch.log_model(model, "model")
```

### Model Serving (FastAPI)

```python
from fastapi import FastAPI
from pydantic import BaseModel
import torch

app = FastAPI()
model = torch.load("model.pt")
model.eval()

class PredictionRequest(BaseModel):
    features: list[float]

@app.post("/predict")
async def predict(request: PredictionRequest):
    with torch.no_grad():
        tensor = torch.tensor([request.features])
        output = model(tensor)
        return {"prediction": output.argmax().item()}
```

---

## Best Practices

### Training

- [ ] Experiment tracking (MLflow, W&B)
- [ ] Mixed precision training
- [ ] Gradient accumulation
- [ ] Early stopping
- [ ] Learning rate scheduling

### Deployment

- [ ] Model versioning
- [ ] A/B testing
- [ ] Monitoring for drift
- [ ] Fallback mechanisms
