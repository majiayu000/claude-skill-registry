---
name: ollama-rag
description: Build RAG systems with Ollama local + cloud models. Latest cloud models include DeepSeek-V3.2 (GPT-5 level), Qwen3-Coder-480B (1M context), MiniMax-M2. Use for document Q&A, knowledge bases, and agentic RAG. Covers LangChain, LlamaIndex, ChromaDB, and embedding models.
---

# Ollama RAG Guide

Build RAG systems with Ollama - run locally or use cloud for massive models.

## Ollama Cloud Models (Dec 2025)

Access via `ollama signin` (v0.12+). No local storage needed, privacy preserved.

| Model | Params | Context | Best For |
|-------|--------|---------|----------|
| `deepseek-v3.2:cloud` | 671B | 160K | **GPT-5 level**, reasoning |
| `deepseek-v3.1:671b-cloud` | 671B | 160K | Thinking + non-thinking hybrid |
| `qwen3-coder:480b-cloud` | 480B | **256K-1M** | Agentic coding, repo-scale |
| `minimax-m2:cloud` | 230B (10B active) | 128K | #1 open-source, tools |
| `gpt-oss:120b-cloud` | 120B | 128K | OpenAI open weights |
| `glm-4.6:cloud` | - | - | Code generation |

```bash
# Sign in to access cloud
ollama signin

# Run cloud models
ollama run deepseek-v3.2:cloud
ollama run qwen3-coder:480b-cloud
ollama run minimax-m2:cloud
```

## Local Models (Dec 2025)

### Reasoning Models

| Model | Params | Context | Best For |
|-------|--------|---------|----------|
| `nemotron-3-nano` | 30B (3.6B active) | **1M tokens** | Agents, long docs, code |
| `deepseek-r1` | 7B-671B | 128K | Reasoning, math, code |
| `qwq` | 32B | 32K | Logic, analysis |
| `llama4` | 109B/400B | 128K | General, multimodal |

### Fast/Efficient Models

| Model | Size | RAM | Speed |
|-------|------|-----|-------|
| `llama3.2:3b` | 2GB | 8GB | Very fast |
| `mistral-small-3.1` | 24B | 16GB | Fast |
| `gemma3` | 4B-27B | 8-32GB | Balanced |

### Embedding Models

| Model | Dims | Context | MTEB Score |
|-------|------|---------|------------|
| `snowflake-arctic-embed2` | 1024 | 8K | **67.5** |
| `mxbai-embed-large` | 1024 | 512 | 64.68 |
| `nomic-embed-text` | 768 | 8K | 53.01 |

**Recommendation**: `snowflake-arctic-embed2` for accuracy, `nomic-embed-text` for speed.

## Quick Start

### Cloud (No Local Resources)
```bash
ollama signin
ollama run deepseek-v3.2:cloud  # GPT-5 level
ollama run qwen3-coder:480b-cloud  # 1M context for huge repos
```

### Local
```bash
ollama pull nemotron-3-nano  # 1M context, 24GB VRAM
ollama pull snowflake-arctic-embed2

# Or for lower RAM (8GB)
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

## Stack Options

### Option A: LangChain + ChromaDB (Most Common)

```python
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

# Load and split
loader = PyPDFLoader("document.pdf")
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(loader.load())

# Embed and store
embeddings = OllamaEmbeddings(model="snowflake-arctic-embed2")
vectorstore = Chroma.from_documents(docs, embeddings, persist_directory="./db")

# Query - LOCAL
llm = OllamaLLM(model="nemotron-3-nano")

# Or CLOUD (GPT-5 level, no local resources)
llm = OllamaLLM(model="deepseek-v3.2:cloud")

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
answer = qa.invoke("What is the main topic?")
```

### Option B: LlamaIndex (Better Accuracy)

```python
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings

# Configure
Settings.llm = Ollama(model="nemotron-3-nano", request_timeout=300.0)
Settings.embed_model = OllamaEmbedding(model_name="snowflake-arctic-embed2")

# Load and index
documents = SimpleDirectoryReader("./docs").load_data()
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the key findings")
```

### Option C: Direct Ollama API (Minimal Dependencies)

```python
import ollama
import chromadb

# Embed
def embed(text):
    return ollama.embed(model="nomic-embed-text", input=text)["embeddings"][0]

# Store in ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")
collection.add(ids=["1"], documents=["text"], embeddings=[embed("text")])

# Retrieve and generate
results = collection.query(query_embeddings=[embed("query")], n_results=3)
context = "\n".join(results["documents"][0])

response = ollama.chat(
    model="nemotron-3-nano",
    messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: ..."}]
)
```

## Vector Database Options

| Database | Install | Best For |
|----------|---------|----------|
| ChromaDB | `pip install chromadb` | Simple, embedded |
| FAISS | `pip install faiss-cpu` | Fast similarity |
| Qdrant | `pip install qdrant-client` | Production scale |
| Weaviate | Docker | Full-featured |

## Nemotron 3 Nano Deep Dive

**Why Nemotron for RAG:**
- 1M token context = entire codebases, long documents
- Hybrid Mamba-Transformer = 4x faster inference
- MoE (3.6B active params) = runs on 24GB VRAM
- Apache 2.0 license = commercial use OK

```python
# For very long documents
llm = OllamaLLM(
    model="nemotron-3-nano",
    num_ctx=131072,  # 128K context, increase as needed
    temperature=0.1,  # Lower for factual RAG
)
```

## Hardware Requirements

| Model | RAM | GPU VRAM |
|-------|-----|----------|
| 3B models | 8GB | 4GB |
| 7-8B models | 16GB | 8GB |
| 30B models | 32GB | 24GB |
| 70B+ models | 64GB+ | 48GB+ |

## References

- [Model selection guide](references/model-selection.md)
- [Ollama Library](https://ollama.com/library)
- [Nemotron on Ollama](https://ollama.com/library/nemotron-3-nano)
