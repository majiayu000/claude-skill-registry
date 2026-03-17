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

---

## LLM Application Development

### RAG Architecture (Retrieval-Augmented Generation)

```python
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. Load and chunk documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " "],
)
chunks = text_splitter.split_documents(documents)

# 2. Embed and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./db")

# 3. Create retrieval chain
retriever = vectorstore.as_retriever(
    search_type="mmr",          # Maximal Marginal Relevance
    search_kwargs={"k": 5},
)

prompt = ChatPromptTemplate.from_template("""
Answer based on the following context. If the answer is not in the context, say so.

Context: {context}

Question: {question}
""")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI(model="gpt-4o")
)

result = chain.invoke("What is the refund policy?")
```

### Vector Databases

| Database        | Type        | Best For                          |
| --------------- | ----------- | --------------------------------- |
| **pgvector**    | PostgreSQL extension | Existing Postgres, hybrid queries |
| **Pinecone**    | Managed cloud | Production scale, serverless      |
| **Chroma**      | Local/embedded | Prototyping, small-medium datasets |
| **Weaviate**    | Self-hosted/cloud | Multimodal, GraphQL interface    |
| **Qdrant**      | Self-hosted/cloud | High performance, filtering      |

```python
# pgvector with SQLAlchemy
from pgvector.sqlalchemy import Vector

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    embedding = Column(Vector(1536))  # OpenAI embedding dimension

# Similarity search
from sqlalchemy import text
results = session.execute(text("""
    SELECT content, embedding <=> :query_embedding AS distance
    FROM documents
    ORDER BY embedding <=> :query_embedding
    LIMIT 5
"""), {"query_embedding": str(query_vector)})
```

### Prompt Engineering Patterns

```python
# System prompt pattern
SYSTEM_PROMPT = """You are a helpful assistant that answers questions about {domain}.

Rules:
- Only answer based on provided context
- If uncertain, say "I don't know"
- Cite sources when possible
- Be concise and factual
"""

# Few-shot prompting
FEW_SHOT_PROMPT = """
Classify the sentiment of the following text.

Text: "The product arrived on time and works perfectly!"
Sentiment: positive

Text: "Terrible customer service, waited 3 hours."
Sentiment: negative

Text: "{user_input}"
Sentiment:"""

# Chain-of-thought prompting
COT_PROMPT = """
Solve step by step:
1. Identify the key information
2. Break down the problem
3. Work through each step
4. Provide the final answer

Problem: {problem}
"""
```

### Structured Outputs

```python
# Anthropic Claude structured output
import anthropic
from pydantic import BaseModel

class ExtractedEntity(BaseModel):
    name: str
    type: str  # person, org, location
    confidence: float

class ExtractionResult(BaseModel):
    entities: list[ExtractedEntity]
    summary: str

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Extract entities from: {text}"}],
    # Claude supports tool_use for structured output
    tools=[{
        "name": "extract_entities",
        "description": "Extract named entities from text",
        "input_schema": ExtractionResult.model_json_schema(),
    }],
    tool_choice={"type": "tool", "name": "extract_entities"},
)

# OpenAI structured output
from openai import OpenAI

client = OpenAI()
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": f"Extract entities from: {text}"}],
    response_format=ExtractionResult,
)
result = response.choices[0].message.parsed
```

### Tool Use / Function Calling

```python
# Claude tool use
tools = [
    {
        "name": "search_database",
        "description": "Search the product database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "category": {"type": "string", "enum": ["electronics", "clothing", "books"]},
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
            },
            "required": ["location"],
        },
    },
]

# Agentic loop: call LLM, execute tools, feed results back
while True:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        messages=messages,
        tools=tools,
    )

    if response.stop_reason == "end_turn":
        break

    # Execute tool calls
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{"type": "tool_result", "tool_use_id": block.id, "content": str(result)}],
            })
```

### Claude API / Anthropic SDK Patterns

```python
import anthropic

client = anthropic.Anthropic()

# Basic message
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Explain async/await in Python"},
    ],
)

# Streaming
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Vision (image input)
import base64

with open("screenshot.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "Describe this UI and suggest improvements"},
        ],
    }],
)
```

### LangChain / LlamaIndex

```python
# LangChain LCEL (LangChain Expression Language)
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

chain = (
    ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("user", "{input}"),
    ])
    | llm
    | StrOutputParser()
)

# LlamaIndex for document Q&A
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("data/").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("What are the key findings?")
```

### Evaluation Frameworks

```python
# RAGAS for RAG evaluation
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

result = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
print(result)

# LangSmith for tracing and evaluation
import langsmith

client = langsmith.Client()
# Traces are automatically captured when LANGCHAIN_TRACING_V2=true

# Custom evaluation
def evaluate_response(prediction: str, reference: str) -> dict:
    """Score response quality."""
    # Use LLM-as-judge pattern
    judge_prompt = f"""Rate the following response on a scale of 1-5:
    Reference: {reference}
    Response: {prediction}
    Score (1-5):"""
    score = llm.invoke(judge_prompt)
    return {"score": int(score.content.strip())}
```

### LLM App Architecture Patterns

| Pattern               | Use Case                                   |
| --------------------- | ------------------------------------------ |
| **RAG**               | Q&A over documents, knowledge bases        |
| **Agent**             | Multi-step tasks requiring tool use        |
| **Chain-of-Thought**  | Complex reasoning, math, logic             |
| **Map-Reduce**        | Summarizing long documents                 |
| **Router**            | Directing queries to specialized handlers  |
| **Reflection**        | Self-correcting outputs                    |
| **Multi-Agent**       | Collaborative problem solving              |
