---
name: faion-gemini-api-skill
user-invocable: false
description: ""
---

# Google Gemini API Mastery

**Complete Guide to Google Gemini API for Multimodal AI Applications (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Models** | Gemini 2.0 Flash, 1.5 Pro (2M context), 1.5 Flash, Ultra |
| **Multimodal** | Text, images, video (native), audio (native), PDFs, code |
| **Function Calling** | Tool declarations, parallel calls, controlled generation |
| **Code Execution** | Python sandbox, charts, data analysis |
| **Grounding** | Google Search, document retrieval |
| **Caching** | Context caching for cost reduction |
| **Embeddings** | text-embedding-004, multimodal embeddings |
| **Safety** | Harm categories, block thresholds, content filtering |

---

## Model Overview

### Available Models (January 2026)

| Model | Context Window | Strengths | Use Cases |
|-------|----------------|-----------|-----------|
| **Gemini 2.0 Flash** | 1M tokens | Fastest, multimodal, agentic | Real-time apps, agents |
| **Gemini 2.0 Flash Thinking** | 1M tokens | Reasoning, chain-of-thought | Complex reasoning, math |
| **Gemini 1.5 Pro** | 2M tokens | Largest context, balanced | Long documents, codebases |
| **Gemini 1.5 Flash** | 1M tokens | Cost-effective, fast | High-volume, production |
| **Gemini 1.5 Flash-8B** | 1M tokens | Smallest, cheapest | Simple tasks, edge |
| **Gemini Ultra** | 128K tokens | Most capable | Complex multimodal tasks |

### Model Selection Guide

```
Need fastest response? → Gemini 2.0 Flash
Need reasoning? → Gemini 2.0 Flash Thinking
Need largest context? → Gemini 1.5 Pro (2M tokens)
Need cost efficiency? → Gemini 1.5 Flash-8B
Need best quality? → Gemini Ultra
```

---

## Installation & Setup

### Python SDK

```bash
pip install google-generativeai
```

### Authentication

```python
import google.generativeai as genai

# Option 1: API Key (Google AI Studio)
genai.configure(api_key="YOUR_API_KEY")

# Option 2: Environment variable
# export GOOGLE_API_KEY="your-api-key"
genai.configure()
```

### Vertex AI Setup

```bash
# Install Vertex AI SDK
pip install google-cloud-aiplatform

# Authenticate with Google Cloud
gcloud auth application-default login
```

```python
import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(project="your-project-id", location="us-central1")
model = GenerativeModel("gemini-1.5-pro")
```

---

## Basic Text Generation

### Simple Request

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("Explain quantum computing in simple terms")
print(response.text)
```

### With Generation Config

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",  # or "application/json"
    }
)

response = model.generate_content("Write a product description for a smartwatch")
```

### JSON Output

```python
import json

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "price": {"type": "number"},
                "features": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["name", "price"]
        }
    }
)

response = model.generate_content("Create a product listing for wireless earbuds")
product = json.loads(response.text)
```

---

## Streaming

### Text Streaming

```python
model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content(
    "Write a long story about space exploration",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### Chat Streaming

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Tell me about Mars", stream=True)

for chunk in response:
    print(chunk.text, end="")
```

### Async Streaming

```python
import asyncio
import google.generativeai as genai

async def stream_response():
    model = genai.GenerativeModel("gemini-2.0-flash")

    response = await model.generate_content_async(
        "Explain machine learning",
        stream=True
    )

    async for chunk in response:
        print(chunk.text, end="")

asyncio.run(stream_response())
```

---

## Multimodal Input

### Image Analysis

```python
import PIL.Image

model = genai.GenerativeModel("gemini-2.0-flash")

# From file
image = PIL.Image.open("photo.jpg")
response = model.generate_content([
    "Describe this image in detail",
    image
])

# From URL (upload first)
image_file = genai.upload_file("photo.jpg")
response = model.generate_content([
    "What objects are in this image?",
    image_file
])
```

### Multiple Images

```python
image1 = PIL.Image.open("before.jpg")
image2 = PIL.Image.open("after.jpg")

response = model.generate_content([
    "Compare these two images and describe the differences",
    image1,
    image2
])
```

### Video Understanding (Native)

```python
# Upload video file (supports MP4, MPEG, MOV, AVI, etc.)
video_file = genai.upload_file("presentation.mp4")

# Wait for processing
import time
while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = genai.get_file(video_file.name)

# Analyze video
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Summarize the key points of this video presentation",
    video_file
])
print(response.text)

# With timestamps
response = model.generate_content([
    "What happens at the 2:30 mark in this video?",
    video_file
])
```

### Audio Understanding (Native)

```python
# Upload audio file (supports MP3, WAV, AIFF, AAC, OGG, FLAC)
audio_file = genai.upload_file("podcast.mp3")

# Wait for processing
while audio_file.state.name == "PROCESSING":
    time.sleep(5)
    audio_file = genai.get_file(audio_file.name)

# Transcribe and analyze
model = genai.GenerativeModel("gemini-1.5-pro")

# Transcription
response = model.generate_content([
    "Transcribe this audio recording",
    audio_file
])

# Analysis
response = model.generate_content([
    "What are the main topics discussed in this podcast?",
    audio_file
])
```

### PDF Processing

```python
# Upload PDF
pdf_file = genai.upload_file("document.pdf")

model = genai.GenerativeModel("gemini-1.5-pro")

# Summarize
response = model.generate_content([
    "Summarize this document",
    pdf_file
])

# Extract specific information
response = model.generate_content([
    "Extract all dates and deadlines mentioned in this document",
    pdf_file
])

# Q&A over document
response = model.generate_content([
    "What is the total budget mentioned?",
    pdf_file
])
```

### Combined Modalities

```python
image = PIL.Image.open("chart.png")
audio_file = genai.upload_file("explanation.mp3")

response = model.generate_content([
    "This chart shows our Q4 results. Listen to the audio explanation and create a summary report.",
    image,
    audio_file
])
```

---

## Chat Conversations

### Basic Chat

```python
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat()

response = chat.send_message("Hello! I'm learning Python.")
print(response.text)

response = chat.send_message("What should I learn first?")
print(response.text)

response = chat.send_message("Show me an example")
print(response.text)

# Access history
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text}")
```

### Chat with System Instruction

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""You are a helpful Python tutor.
    Always provide code examples.
    Explain concepts step by step.
    Use beginner-friendly language."""
)

chat = model.start_chat()
response = chat.send_message("What are decorators?")
```

### Multimodal Chat

```python
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

# Text message
response = chat.send_message("I'll show you some code screenshots")

# Image message
image = PIL.Image.open("code_screenshot.png")
response = chat.send_message([
    "What's wrong with this code?",
    image
])
```

---

## Function Calling

### Basic Function Calling

```python
def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """Get the current weather in a given location.

    Args:
        location: The city and country, e.g. "London, UK"
        unit: Temperature unit - "celsius" or "fahrenheit"

    Returns:
        Weather information dictionary
    """
    # Simulated response
    return {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "condition": "sunny"
    }

def search_products(query: str, max_results: int = 5) -> list:
    """Search for products in the catalog.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of matching products
    """
    # Simulated response
    return [{"name": f"Product {i}", "price": 10 * i} for i in range(max_results)]

# Create model with tools
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

# Automatic function calling
chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message("What's the weather in Tokyo?")
print(response.text)  # Model called get_current_weather and responded

response = chat.send_message("Find me 3 laptop products")
print(response.text)  # Model called search_products
```

### Manual Function Calling

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[get_current_weather]
)

chat = model.start_chat()
response = chat.send_message("What's the weather in Paris?")

# Check if model wants to call a function
for candidate in response.candidates:
    for part in candidate.content.parts:
        if hasattr(part, 'function_call'):
            fn_call = part.function_call
            print(f"Function: {fn_call.name}")
            print(f"Args: {dict(fn_call.args)}")

            # Execute function
            if fn_call.name == "get_current_weather":
                result = get_current_weather(**dict(fn_call.args))

                # Send result back to model
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn_call.name,
                                response={"result": result}
                            )
                        )]
                    )
                )
                print(response.text)
```

### Parallel Function Calling

```python
# Gemini can call multiple functions in parallel
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[get_current_weather, search_products]
)

chat = model.start_chat(enable_automatic_function_calling=True)

# This may trigger parallel calls
response = chat.send_message(
    "What's the weather in London and search for umbrellas if it's rainy"
)
```

### Tool Config (Controlled Generation)

```python
from google.generativeai.types import content_types

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[get_current_weather, search_products],
    tool_config={
        "function_calling_config": {
            # "AUTO" - model decides
            # "ANY" - must call a function
            # "NONE" - no function calling
            "mode": "ANY",
            # Restrict to specific functions
            "allowed_function_names": ["get_current_weather"]
        }
    }
)
```

---

## Code Execution

### Python Sandbox

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]  # Enable code execution
)

response = model.generate_content(
    "Calculate the first 20 Fibonacci numbers and show the result"
)

# Access executed code and output
for part in response.candidates[0].content.parts:
    if hasattr(part, 'executable_code'):
        print("Code:")
        print(part.executable_code.code)
    if hasattr(part, 'code_execution_result'):
        print("Output:")
        print(part.code_execution_result.output)
```

### Data Analysis

```python
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=["code_execution"]
)

csv_file = genai.upload_file("sales_data.csv")

response = model.generate_content([
    "Analyze this sales data. Calculate averages, find trends, and create a summary.",
    csv_file
])
```

### Chart Generation

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=["code_execution"]
)

response = model.generate_content("""
Create a bar chart showing programming language popularity:
- Python: 35%
- JavaScript: 28%
- Java: 15%
- C++: 12%
- Other: 10%
""")

# The model will generate matplotlib code and return the chart
```

---

## Grounding with Google Search

### Enable Search Grounding

```python
from google.generativeai import GenerativeModel
from google.generativeai.types import Tool

# Create search tool
search_tool = Tool.from_google_search_retrieval(
    google_search_retrieval={
        "dynamic_retrieval_config": {
            "mode": "MODE_DYNAMIC",  # or "MODE_UNSPECIFIED"
            "dynamic_threshold": 0.3  # 0-1, higher = more selective
        }
    }
)

model = GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[search_tool]
)

response = model.generate_content("What are the latest developments in AI in 2026?")
print(response.text)

# Access grounding metadata
if response.candidates[0].grounding_metadata:
    for chunk in response.candidates[0].grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.web.uri}")
        print(f"Title: {chunk.web.title}")
```

### Combining Search with Functions

```python
model = GenerativeModel(
    model_name="gemini-2.0-flash",
    tools=[search_tool, get_current_weather]
)

chat = model.start_chat(enable_automatic_function_calling=True)

response = chat.send_message(
    "What's the weather forecast for Tokyo this week according to recent reports?"
)
```

---

## Context Caching

### Creating a Cache

```python
from google.generativeai import caching

# Upload large document
document = genai.upload_file("large_document.pdf")

# Create cache (minimum 32K tokens)
cache = caching.CachedContent.create(
    model="gemini-1.5-pro",
    display_name="Large document cache",
    system_instruction="You are an expert document analyzer.",
    contents=[document],
    ttl="3600s"  # Time to live: 1 hour
)

print(f"Cache created: {cache.name}")
print(f"Token count: {cache.usage_metadata.total_token_count}")
```

### Using Cached Content

```python
# Create model from cache
model = genai.GenerativeModel.from_cached_content(cache)

# Queries use cached context (faster, cheaper)
response = model.generate_content("Summarize the main points")
print(response.text)

response = model.generate_content("What are the key dates mentioned?")
print(response.text)
```

### Managing Caches

```python
# List caches
for c in caching.CachedContent.list():
    print(f"{c.name}: {c.display_name}")

# Get specific cache
cache = caching.CachedContent.get("cachedContents/xxxxx")

# Update TTL
cache.update(ttl="7200s")  # Extend to 2 hours

# Delete cache
cache.delete()
```

### Cost Savings

```
Regular input: $0.075 / 1M tokens (1.5 Pro)
Cached input:  $0.01875 / 1M tokens (75% cheaper)

Best for:
- Large documents queried multiple times
- System instructions with many examples
- RAG with frequently accessed knowledge bases
```

---

## Embeddings

### Text Embeddings

```python
# Using the embeddings model
result = genai.embed_content(
    model="models/text-embedding-004",
    content="What is machine learning?",
    task_type="RETRIEVAL_DOCUMENT"  # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
)

embedding = result["embedding"]
print(f"Embedding dimension: {len(embedding)}")  # 768
```

### Batch Embeddings

```python
texts = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Python is popular for data science"
]

result = genai.embed_content(
    model="models/text-embedding-004",
    content=texts,
    task_type="RETRIEVAL_DOCUMENT"
)

embeddings = result["embedding"]  # List of embeddings
```

### Task Types

| Task Type | Description | Use Case |
|-----------|-------------|----------|
| `RETRIEVAL_DOCUMENT` | Embed documents for retrieval | Indexing documents |
| `RETRIEVAL_QUERY` | Embed search queries | Search queries |
| `SEMANTIC_SIMILARITY` | Compare text similarity | Deduplication |
| `CLASSIFICATION` | Text classification | Categorization |
| `CLUSTERING` | Group similar texts | Topic modeling |
| `QUESTION_ANSWERING` | Q&A embeddings | Q&A systems |
| `FACT_VERIFICATION` | Verify facts | Fact checking |

### Similarity Search Example

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Index documents
documents = [
    "How to learn Python programming",
    "Best practices for machine learning",
    "Introduction to web development",
    "Guide to cloud computing"
]

doc_embeddings = genai.embed_content(
    model="models/text-embedding-004",
    content=documents,
    task_type="RETRIEVAL_DOCUMENT"
)["embedding"]

# Search
query = "I want to learn AI"
query_embedding = genai.embed_content(
    model="models/text-embedding-004",
    content=query,
    task_type="RETRIEVAL_QUERY"
)["embedding"]

# Find most similar
similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in doc_embeddings]
best_match_idx = np.argmax(similarities)
print(f"Best match: {documents[best_match_idx]}")
```

---

## Safety Settings

### Harm Categories

| Category | Description |
|----------|-------------|
| `HARM_CATEGORY_HARASSMENT` | Harassment content |
| `HARM_CATEGORY_HATE_SPEECH` | Hate speech |
| `HARM_CATEGORY_SEXUALLY_EXPLICIT` | Sexually explicit content |
| `HARM_CATEGORY_DANGEROUS_CONTENT` | Dangerous content |

### Block Thresholds

| Threshold | Description |
|-----------|-------------|
| `BLOCK_NONE` | Always show content |
| `BLOCK_LOW_AND_ABOVE` | Block low probability and above |
| `BLOCK_MEDIUM_AND_ABOVE` | Block medium probability and above (default) |
| `BLOCK_ONLY_HIGH` | Block only high probability |

### Configuring Safety

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)

# Check safety ratings in response
response = model.generate_content("Your prompt")

if response.prompt_feedback.block_reason:
    print(f"Blocked: {response.prompt_feedback.block_reason}")
else:
    for rating in response.candidates[0].safety_ratings:
        print(f"{rating.category}: {rating.probability}")
```

---

## Vertex AI Integration

### Setup

```python
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# Initialize Vertex AI
vertexai.init(project="your-gcp-project", location="us-central1")

# Available locations: us-central1, europe-west4, asia-northeast1
```

### Generate Content

```python
model = GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Explain quantum computing")
print(response.text)
```

### Multimodal with GCS

```python
from vertexai.generative_models import Part

# Using Google Cloud Storage
video_part = Part.from_uri(
    uri="gs://your-bucket/video.mp4",
    mime_type="video/mp4"
)

model = GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Summarize this video",
    video_part
])
```

### Tuned Models

```python
from vertexai.generative_models import GenerativeModel

# Use a tuned model
model = GenerativeModel("projects/your-project/locations/us-central1/endpoints/your-tuned-model")

response = model.generate_content("Your prompt")
```

### Enterprise Features

| Feature | Description |
|---------|-------------|
| **VPC Service Controls** | Network isolation |
| **CMEK** | Customer-managed encryption keys |
| **Audit Logs** | Cloud Audit Logs integration |
| **IAM** | Fine-grained access control |
| **Model Tuning** | Supervised fine-tuning |
| **Evaluation** | Built-in evaluation metrics |

---

## Advanced Patterns

### RAG with Gemini

```python
# 1. Index documents with embeddings
documents = load_documents()  # Your document loader
doc_embeddings = genai.embed_content(
    model="models/text-embedding-004",
    content=[doc.text for doc in documents],
    task_type="RETRIEVAL_DOCUMENT"
)["embedding"]

# 2. Store in vector database (Chroma, Pinecone, etc.)
vector_store.add(doc_embeddings, documents)

# 3. Query
def rag_query(question: str):
    # Get query embedding
    query_emb = genai.embed_content(
        model="models/text-embedding-004",
        content=question,
        task_type="RETRIEVAL_QUERY"
    )["embedding"]

    # Retrieve relevant documents
    relevant_docs = vector_store.similarity_search(query_emb, k=5)

    # Generate answer with context
    model = genai.GenerativeModel("gemini-1.5-pro")
    context = "\n\n".join([doc.text for doc in relevant_docs])

    response = model.generate_content(f"""
    Context: {context}

    Question: {question}

    Answer based on the context above:
    """)

    return response.text
```

### Agent Loop

```python
import json

def run_agent(user_query: str, max_iterations: int = 5):
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        tools=[search_web, get_weather, calculate],
        system_instruction="You are a helpful assistant. Use tools when needed."
    )

    chat = model.start_chat()

    for i in range(max_iterations):
        response = chat.send_message(user_query if i == 0 else "Continue")

        # Check for function calls
        has_function_call = False
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                has_function_call = True
                fn = part.function_call

                # Execute function
                result = execute_function(fn.name, dict(fn.args))

                # Send result back
                chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn.name,
                                response={"result": result}
                            )
                        )]
                    )
                )

        if not has_function_call:
            return response.text

    return "Max iterations reached"
```

### Structured Extraction

```python
from typing import List
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    occupation: str

class ExtractedData(BaseModel):
    people: List[Person]
    locations: List[str]
    dates: List[str]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": ExtractedData.model_json_schema()
    }
)

text = """
John Smith (35), a software engineer from San Francisco, met
Maria Garcia (28), a designer from New York, at a conference
on January 15, 2026.
"""

response = model.generate_content(f"Extract all entities from this text: {text}")
data = ExtractedData.model_validate_json(response.text)
```

---

## Error Handling

### Common Errors

```python
from google.generativeai.types import StopCandidateException, BlockedPromptException

try:
    response = model.generate_content("Your prompt")
    print(response.text)

except BlockedPromptException as e:
    print(f"Prompt blocked: {e}")

except StopCandidateException as e:
    print(f"Generation stopped: {e}")
    # Access partial response
    if e.args and e.args[0].content:
        print(f"Partial: {e.args[0].content.parts[0].text}")

except Exception as e:
    print(f"Error: {e}")
```

### Rate Limits

```python
import time
from google.api_core.exceptions import ResourceExhausted

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except ResourceExhausted:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

---

## Pricing (January 2026)

### Google AI Studio (API Key)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 1.5 Pro | $1.25 (<128K) / $2.50 (>128K) | $5.00 (<128K) / $10.00 (>128K) |
| Gemini 1.5 Flash | $0.075 (<128K) / $0.15 (>128K) | $0.30 (<128K) / $0.60 (>128K) |
| Gemini 1.5 Flash-8B | $0.0375 | $0.15 |

### Context Caching Discount

| Model | Cached Input Price | Savings |
|-------|-------------------|---------|
| Gemini 1.5 Pro | $0.3125 (<128K) | 75% |
| Gemini 1.5 Flash | $0.01875 (<128K) | 75% |

### Free Tier

| Model | Free Requests/Minute | Free Requests/Day |
|-------|---------------------|-------------------|
| Gemini 1.5 Flash | 15 | 1,500 |
| Gemini 1.5 Pro | 2 | 50 |
| Gemini 2.0 Flash | 10 | 1,000 |

---

## Best Practices

### Prompt Engineering

1. **Be specific** - Clear instructions, expected format
2. **Use examples** - Few-shot prompting improves accuracy
3. **System instructions** - Set consistent behavior
4. **Structured output** - Use JSON mode for parsing

### Performance

1. **Choose right model** - Flash for speed, Pro for quality
2. **Use caching** - For repeated large contexts
3. **Batch requests** - When possible
4. **Stream responses** - For better UX

### Cost Optimization

1. **Use Flash models** - 10x cheaper than Pro
2. **Enable caching** - 75% savings on large contexts
3. **Limit output tokens** - Set max_output_tokens
4. **Compress prompts** - Remove unnecessary text

### Security

1. **Never expose API keys** - Use environment variables
2. **Validate inputs** - Sanitize user content
3. **Check safety ratings** - Handle blocked content
4. **Use Vertex AI** - For enterprise compliance

---

## Quick Reference: API Comparison

| Feature | Gemini | OpenAI GPT-4 | Claude |
|---------|--------|--------------|--------|
| Max Context | 2M tokens | 128K tokens | 200K tokens |
| Native Video | Yes | No | No |
| Native Audio | Yes | Via Whisper | No |
| Code Execution | Yes | Via tools | No |
| Search Grounding | Yes | Via tools | Via tools |
| Context Caching | Yes | No | Yes |

---

## Sources

- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Vertex AI Generative AI](https://cloud.google.com/vertex-ai/generative-ai/docs)
- [Google AI Python SDK](https://github.com/google-gemini/generative-ai-python)
- [Gemini Cookbook](https://github.com/google-gemini/gemini-api-cookbook)

---

*Skill: faion-gemini-api-skill v1.0*
*Last updated: 2026-01-18*
