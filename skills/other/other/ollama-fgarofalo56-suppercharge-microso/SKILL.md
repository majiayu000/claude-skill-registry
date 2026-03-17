---
name: ollama
description: "Run local LLMs with Ollama. Configure models, manage resources, and integrate with applications. Use for local AI, private LLM deployments, and offline inference."
---

# Ollama Skill

Complete guide for Ollama - run LLMs locally.

## Quick Reference

### Popular Models
| Model | Size | Use Case |
|-------|------|----------|
| **llama3.2** | 3B/11B | General purpose |
| **mistral** | 7B | Fast, capable |
| **codellama** | 7B/13B/34B | Code generation |
| **phi3** | 3.8B | Compact, fast |
| **gemma2** | 2B/9B/27B | Google's model |
| **qwen2.5** | 0.5B-72B | Multilingual |
| **deepseek-coder** | 6.7B/33B | Code specialist |

### Commands
```bash
ollama run <model>    # Interactive chat
ollama pull <model>   # Download model
ollama list           # List installed
ollama rm <model>     # Remove model
ollama serve          # Start server
```

---

## 1. Installation

### macOS
```bash
# Download from ollama.ai or:
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows
```powershell
# Download installer from ollama.ai
# Or use WSL2 with Linux instructions
```

### Docker
```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# With GPU support
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

---

## 2. Basic Usage

### Run Models
```bash
# Run interactively
ollama run llama3.2

# Run with prompt
ollama run llama3.2 "Explain quantum computing"

# Run specific size
ollama run llama3.2:3b
ollama run llama3.2:11b

# Run with system prompt
ollama run llama3.2 --system "You are a helpful coding assistant"
```

### Model Management
```bash
# Pull model
ollama pull mistral

# List models
ollama list

# Show model info
ollama show llama3.2

# Show model file
ollama show llama3.2 --modelfile

# Copy model
ollama cp llama3.2 my-llama

# Remove model
ollama rm mistral
```

---

## 3. REST API

### Generate Completion
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

### Chat Completion
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false
}'
```

### Streaming
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Write a poem"}],
  "stream": true
}'
```

### Embeddings
```bash
curl http://localhost:11434/api/embed -d '{
  "model": "llama3.2",
  "input": "The quick brown fox"
}'
```

### List Models (API)
```bash
curl http://localhost:11434/api/tags
```

---

## 4. Python Integration

### Official Library
```bash
pip install ollama
```

### Basic Usage
```python
import ollama

# Generate
response = ollama.generate(
    model='llama3.2',
    prompt='What is Python?'
)
print(response['response'])

# Chat
response = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': 'Hello!'}
    ]
)
print(response['message']['content'])
```

### Streaming
```python
# Stream generate
for chunk in ollama.generate(model='llama3.2', prompt='Hello', stream=True):
    print(chunk['response'], end='', flush=True)

# Stream chat
for chunk in ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Write a story'}],
    stream=True
):
    print(chunk['message']['content'], end='', flush=True)
```

### Embeddings
```python
# Single embedding
response = ollama.embed(
    model='llama3.2',
    input='Hello, world!'
)
embedding = response['embeddings'][0]

# Multiple embeddings
response = ollama.embed(
    model='llama3.2',
    input=['Hello', 'World']
)
embeddings = response['embeddings']
```

### Async Support
```python
import asyncio
import ollama

async def main():
    response = await ollama.AsyncClient().chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': 'Hello!'}]
    )
    print(response['message']['content'])

asyncio.run(main())
```

---

## 5. LangChain Integration

### Setup
```python
from langchain_ollama import ChatOllama, OllamaEmbeddings

# Chat model
llm = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

# Embeddings
embeddings = OllamaEmbeddings(model="llama3.2")
```

### Use in Chains
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Explain {topic} simply")
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "machine learning"})
```

---

## 6. Custom Models (Modelfile)

### Basic Modelfile
```dockerfile
# Modelfile
FROM llama3.2

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# Set system prompt
SYSTEM """You are a helpful coding assistant specialized in Python.
Always provide clear, well-commented code examples."""
```

### Create Custom Model
```bash
# Create model from Modelfile
ollama create my-coder -f ./Modelfile

# Run custom model
ollama run my-coder
```

### Advanced Modelfile
```dockerfile
FROM llama3.2:11b

# Model parameters
PARAMETER temperature 0.8
PARAMETER top_k 40
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1
PARAMETER num_ctx 8192
PARAMETER num_predict 2048
PARAMETER stop "<|im_end|>"

# System message
SYSTEM """You are an expert software architect. You provide:
1. Clear architectural recommendations
2. Design pattern suggestions
3. Best practices for scalability
4. Security considerations"""

# Template (for custom formats)
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>"""
```

### Import GGUF Models
```dockerfile
# Import from GGUF file
FROM ./model.gguf

PARAMETER temperature 0.7
SYSTEM "You are a helpful assistant."
```

```bash
ollama create custom-model -f Modelfile
```

---

## 7. Vision Models

### Using Vision
```python
import ollama
import base64

# From file
with open('image.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode()

response = ollama.chat(
    model='llava',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': [image_data]
    }]
)
print(response['message']['content'])
```

### Via API
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llava",
  "messages": [{
    "role": "user",
    "content": "Describe this image",
    "images": ["base64-encoded-image"]
  }]
}'
```

---

## 8. Code Models

### CodeLlama
```bash
# Pull code model
ollama pull codellama

# Or specialized variants
ollama pull codellama:7b-instruct
ollama pull codellama:13b-python
```

### Code Generation
```python
response = ollama.generate(
    model='codellama',
    prompt='''Write a Python function that:
1. Takes a list of numbers
2. Returns the median value
3. Handles empty lists'''
)
print(response['response'])
```

### DeepSeek Coder
```bash
ollama pull deepseek-coder:6.7b
```

```python
response = ollama.chat(
    model='deepseek-coder:6.7b',
    messages=[{
        'role': 'user',
        'content': 'Write a REST API in FastAPI for user management'
    }]
)
```

---

## 9. Performance Tuning

### Context Length
```python
# Increase context window
response = ollama.generate(
    model='llama3.2',
    prompt='Long document here...',
    options={
        'num_ctx': 8192  # Default is 2048
    }
)
```

### GPU Layers
```python
# Control GPU usage
response = ollama.generate(
    model='llama3.2',
    prompt='Hello',
    options={
        'num_gpu': 50  # Number of layers on GPU
    }
)
```

### Parameters
```python
response = ollama.generate(
    model='llama3.2',
    prompt='Creative writing prompt',
    options={
        'temperature': 0.9,      # Creativity (0-2)
        'top_p': 0.95,           # Nucleus sampling
        'top_k': 40,             # Top-k sampling
        'repeat_penalty': 1.1,   # Reduce repetition
        'num_predict': 500,      # Max tokens
        'seed': 42               # Reproducibility
    }
)
```

---

## 10. Server Configuration

### Environment Variables
```bash
# Change host/port
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# Custom model directory
OLLAMA_MODELS=/path/to/models ollama serve

# Limit GPU memory
OLLAMA_GPU_MEMORY=4096 ollama serve
```

### Docker Compose
```yaml
services:
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
  open-webui:
```

---

## 11. Common Patterns

### RAG with Ollama
```python
import ollama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create embeddings
embeddings = OllamaEmbeddings(model="llama3.2")

# Create vector store
vectorstore = Chroma.from_texts(
    texts=["Document 1...", "Document 2..."],
    embedding=embeddings
)

# Query
def rag_query(question: str) -> str:
    # Retrieve relevant docs
    docs = vectorstore.similarity_search(question, k=3)
    context = "\n".join(doc.page_content for doc in docs)

    # Generate answer
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'system', 'content': f'Answer using this context:\n{context}'},
            {'role': 'user', 'content': question}
        ]
    )
    return response['message']['content']
```

### Function Calling
```python
import json

tools = [
    {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
        }
    }
]

response = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'system', 'content': f'You have these tools: {json.dumps(tools)}. Call them by returning JSON with "tool" and "arguments".'},
        {'role': 'user', 'content': 'What is the weather in Paris?'}
    ]
)

# Parse tool call from response
```

### Batch Processing
```python
import ollama
from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    response = ollama.generate(
        model='llama3.2',
        prompt=f"Summarize: {item}"
    )
    return response['response']

items = ["Document 1", "Document 2", "Document 3"]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(process_item, items))
```

---

## 12. Troubleshooting

### Common Issues

**Model not found:**
```bash
# Pull the model first
ollama pull llama3.2

# Check available models
ollama list
```

**Out of memory:**
```bash
# Use smaller model
ollama run llama3.2:3b  # Instead of 11b

# Or reduce context
ollama run llama3.2 --num-ctx 2048
```

**Slow generation:**
```bash
# Check GPU usage
nvidia-smi

# Ensure model fits in VRAM
# Or use quantized versions
ollama pull llama3.2:3b-q4_0
```

**Connection refused:**
```bash
# Start server first
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

---

## Best Practices

1. **Right-size models** - Use smallest that works
2. **Quantization** - Use Q4 for speed
3. **Custom models** - Tune for your use case
4. **Batch requests** - Reduce overhead
5. **Cache responses** - Avoid repeat queries
6. **Monitor resources** - Watch GPU/CPU
7. **Use streaming** - Better UX
8. **Set timeouts** - Handle slow responses
9. **Test prompts** - Iterate on system messages
10. **Keep updated** - New models regularly
