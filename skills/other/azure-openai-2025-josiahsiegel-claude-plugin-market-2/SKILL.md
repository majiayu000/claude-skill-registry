---
name: azure-openai-2025
description: Azure OpenAI Service 2025 models including GPT-5, GPT-4.1, reasoning models, and Azure AI Foundry integration
---

# Azure OpenAI Service - 2025 Models and Features

Complete knowledge base for Azure OpenAI Service with latest 2025 models including GPT-5, GPT-4.1, reasoning models, and Azure AI Foundry integration.

## Overview

Azure OpenAI Service provides REST API access to OpenAI's most powerful models with enterprise-grade security, compliance, and regional availability.

## Latest Models (2025)

### GPT-5 Series (GA August 2025)

**Registration Required Models:**
- `gpt-5-pro`: Highest capability, complex reasoning
- `gpt-5`: Balanced performance and cost
- `gpt-5-codex`: Optimized for code generation

**No Registration Required:**
- `gpt-5-mini`: Faster, more affordable
- `gpt-5-nano`: Ultra-fast for simple tasks
- `gpt-5-chat`: Optimized for conversational use

### GPT-4.1 Series

- `gpt-4.1`: 1 million token context window
- `gpt-4.1-mini`: Efficient version with 1M context
- `gpt-4.1-nano`: Fastest variant

**Key Improvements:**
- 1,000,000 token context (vs 128K in GPT-4 Turbo)
- Better instruction following
- Reduced hallucinations
- Improved multilingual support

### Reasoning Models

**o4-mini**: Lightweight reasoning model
- Faster inference
- Lower cost
- Suitable for structured reasoning tasks

**o3**: Advanced reasoning model
- Complex problem solving
- Mathematical reasoning
- Scientific analysis

**o1**: Original reasoning model
- General-purpose reasoning
- Step-by-step explanations

**o1-mini**: Efficient reasoning
- Balanced cost and performance

### Image Generation

**GPT-image-1 (2025-04-15)**
- DALL-E 3 successor
- Higher quality images
- Better prompt understanding
- Improved safety filters

### Video Generation

**Sora (2025-05-02)**
- Text-to-video generation
- Realistic and imaginative scenes
- Up to 60 seconds of video
- Multiple camera angles and styles

### Audio Models

**gpt-4o-transcribe**: Speech-to-text powered by GPT-4o
- High accuracy transcription
- Multiple languages
- Speaker diarization

**gpt-4o-mini-transcribe**: Faster, more affordable transcription
- Good accuracy
- Lower latency
- Cost-effective

## Deploying Azure OpenAI

### Create Azure OpenAI Resource

```bash
# Create OpenAI account
az cognitiveservices account create \
  --name myopenai \
  --resource-group MyRG \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --custom-domain myopenai \
  --public-network-access Disabled \
  --identity-type SystemAssigned

# Get endpoint and key
az cognitiveservices account show \
  --name myopenai \
  --resource-group MyRG \
  --query "properties.endpoint" \
  --output tsv

az cognitiveservices account keys list \
  --name myopenai \
  --resource-group MyRG \
  --query "key1" \
  --output tsv
```

### Deploy GPT-5 Model

```bash
# Deploy gpt-5
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name gpt-5 \
  --model-name gpt-5 \
  --model-version latest \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 100 \
  --scale-type Standard

# Deploy gpt-5-pro (requires registration)
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name gpt-5-pro \
  --model-name gpt-5-pro \
  --model-version latest \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 50
```

### Deploy Reasoning Models

```bash
# Deploy o3 reasoning model
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name o3-reasoning \
  --model-name o3 \
  --model-version latest \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 50

# Deploy o4-mini
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name o4-mini \
  --model-name o4-mini \
  --model-version latest \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 100
```

### Deploy GPT-4.1 with 1M Context

```bash
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name gpt-4-1 \
  --model-name gpt-4.1 \
  --model-version latest \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 100
```

### Deploy Image Generation Model

```bash
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name image-gen \
  --model-name gpt-image-1 \
  --model-version 2025-04-15 \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 10
```

### Deploy Sora Video Generation

```bash
az cognitiveservices account deployment create \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name sora \
  --model-name sora \
  --model-version 2025-05-02 \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 5
```

## Using Azure OpenAI Models

### Python SDK (GPT-5)

```python
from openai import AzureOpenAI
import os

# Initialize client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2025-02-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# GPT-5 completion
response = client.chat.completions.create(
    model="gpt-5",  # deployment name
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    max_tokens=1000,
    temperature=0.7,
    top_p=0.95
)

print(response.choices[0].message.content)
```

### Python SDK (o3 Reasoning Model)

```python
# o3 reasoning with chain-of-thought
response = client.chat.completions.create(
    model="o3-reasoning",
    messages=[
        {"role": "system", "content": "You are an expert problem solver. Show your reasoning step-by-step."},
        {"role": "user", "content": "If a train travels 120 km in 2 hours, then speeds up to travel 180 km in the next 2 hours, what is the average speed for the entire journey?"}
    ],
    max_tokens=2000,
    temperature=0.2  # Lower temperature for reasoning tasks
)

print(response.choices[0].message.content)
```

### Python SDK (GPT-4.1 with 1M Context)

```python
# Read a large document
with open('large_document.txt', 'r') as f:
    document = f.read()

# GPT-4.1 can handle up to 1M tokens
response = client.chat.completions.create(
    model="gpt-4-1",
    messages=[
        {"role": "system", "content": "You are a document analysis expert."},
        {"role": "user", "content": f"Analyze this document and provide key insights:\n\n{document}"}
    ],
    max_tokens=4000
)

print(response.choices[0].message.content)
```

### Image Generation (GPT-image-1)

```python
# Generate image with DALL-E 3 successor
response = client.images.generate(
    model="image-gen",
    prompt="A futuristic city with flying cars and vertical gardens, cyberpunk style, highly detailed, 4K",
    size="1024x1024",
    quality="hd",
    n=1
)

image_url = response.data[0].url
print(f"Generated image: {image_url}")
```

### Video Generation (Sora)

```python
# Generate video with Sora
response = client.videos.generate(
    model="sora",
    prompt="A serene lakeside at sunset with birds flying overhead and gentle waves on the shore",
    duration=10,  # seconds
    resolution="1080p",
    fps=30
)

video_url = response.data[0].url
print(f"Generated video: {video_url}")
```

### Audio Transcription

```python
# Transcribe audio file
audio_file = open("meeting_recording.mp3", "rb")

response = client.audio.transcriptions.create(
    model="gpt-4o-transcribe",
    file=audio_file,
    language="en",
    response_format="verbose_json"
)

print(f"Transcription: {response.text}")
print(f"Duration: {response.duration}s")

# Speaker diarization
for segment in response.segments:
    print(f"[{segment.start}s - {segment.end}s] {segment.text}")
```

## Azure AI Foundry Integration

### Model Router (Automatic Model Selection)

```python
from azure.ai.foundry import ModelRouter

# Initialize model router
router = ModelRouter(
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    credential=os.getenv("AZURE_OPENAI_API_KEY")
)

# Automatically select optimal model
response = router.complete(
    prompt="Analyze this complex scientific paper...",
    optimization_goals=["quality", "cost"],
    available_models=["gpt-5", "gpt-5-mini", "gpt-4-1"]
)

print(f"Selected model: {response.model_used}")
print(f"Response: {response.content}")
print(f"Cost: ${response.cost}")
```

**Benefits:**
- Automatic model selection based on prompt complexity
- Balance quality vs cost
- Reduce costs by up to 40% while maintaining quality

### Agentic Retrieval (Azure AI Search Integration)

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Initialize search client
search_client = SearchClient(
    endpoint=os.getenv("SEARCH_ENDPOINT"),
    index_name="documents",
    credential=AzureKeyCredential(os.getenv("SEARCH_KEY"))
)

# Agentic retrieval with Azure OpenAI
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You have access to a document search system."},
        {"role": "user", "content": "What are the company's revenue projections for Q3?"}
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": "Search company documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }],
    tool_choice="auto"
)

# Process tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == "search_documents":
            query = json.loads(tool_call.function.arguments)["query"]
            results = search_client.search(query)
            # Feed results back to model for final answer
```

**Improvements:**
- 40% better on complex, multi-part questions
- Automatic query decomposition
- Relevance ranking
- Citation generation

### Foundry Observability (Preview)

```python
from azure.ai.foundry import FoundryObservability

# Enable observability
observability = FoundryObservability(
    workspace_id=os.getenv("AI_FOUNDRY_WORKSPACE_ID"),
    enable_tracing=True,
    enable_metrics=True
)

# Monitor agent execution
with observability.trace_agent("customer_support_agent") as trace:
    response = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )

    trace.log_tool_call("search_kb", {"query": "refund policy"})
    trace.log_reasoning_step("Retrieved refund policy document")
    trace.log_token_usage(response.usage.total_tokens)

# View in Azure AI Foundry portal:
# - End-to-end trace logs
# - Reasoning steps and tool calls
# - Performance metrics
# - Cost analysis
```

## Capacity and Quota Management

### Check Quota

```bash
# List deployments with usage
az cognitiveservices account deployment list \
  --resource-group MyRG \
  --name myopenai \
  --output table

# Check usage metrics
az monitor metrics list \
  --resource $(az cognitiveservices account show -g MyRG -n myopenai --query id -o tsv) \
  --metric "TokenTransaction" \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-31T23:59:59Z \
  --interval PT1H \
  --aggregation Total
```

### Update Capacity

```bash
# Scale up deployment capacity
az cognitiveservices account deployment update \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name gpt-5 \
  --sku-capacity 200

# Scale down during off-peak
az cognitiveservices account deployment update \
  --resource-group MyRG \
  --name myopenai \
  --deployment-name gpt-5 \
  --sku-capacity 50
```

### Request Quota Increase

1. Navigate to Azure Portal → Azure OpenAI resource
2. Go to "Quotas" blade
3. Select model and region
4. Click "Request quota increase"
5. Provide justification and target capacity

## Security and Networking

### Private Endpoint

```bash
# Create private endpoint
az network private-endpoint create \
  --name openai-private-endpoint \
  --resource-group MyRG \
  --vnet-name MyVNet \
  --subnet PrivateEndpointSubnet \
  --private-connection-resource-id $(az cognitiveservices account show -g MyRG -n myopenai --query id -o tsv) \
  --group-id account \
  --connection-name openai-connection

# Create private DNS zone
az network private-dns zone create \
  --resource-group MyRG \
  --name privatelink.openai.azure.com

# Link to VNet
az network private-dns link vnet create \
  --resource-group MyRG \
  --zone-name privatelink.openai.azure.com \
  --name openai-dns-link \
  --virtual-network MyVNet \
  --registration-enabled false

# Create DNS zone group
az network private-endpoint dns-zone-group create \
  --resource-group MyRG \
  --endpoint-name openai-private-endpoint \
  --name default \
  --private-dns-zone privatelink.openai.azure.com \
  --zone-name privatelink.openai.azure.com
```

### Managed Identity Access

```bash
# Enable system-assigned identity
az cognitiveservices account identity assign \
  --name myopenai \
  --resource-group MyRG

# Grant role to managed identity
PRINCIPAL_ID=$(az cognitiveservices account show -g MyRG -n myopenai --query identity.principalId -o tsv)

az role assignment create \
  --assignee $PRINCIPAL_ID \
  --role "Cognitive Services OpenAI User" \
  --scope /subscriptions/<sub-id>/resourceGroups/MyRG
```

### Content Filtering

```bash
# Configure content filtering
az cognitiveservices account update \
  --name myopenai \
  --resource-group MyRG \
  --set properties.customContentFilter='{
    "hate": {"severity": "medium", "enabled": true},
    "violence": {"severity": "medium", "enabled": true},
    "sexual": {"severity": "medium", "enabled": true},
    "selfHarm": {"severity": "high", "enabled": true}
  }'
```

## Cost Optimization

### Model Selection Strategy

**Use GPT-5-mini or GPT-5-nano for:**
- Simple questions
- Classification tasks
- Content moderation
- Summarization

**Use GPT-5 or GPT-4.1 for:**
- Complex reasoning
- Long-form content generation
- Document analysis
- Code generation

**Use Reasoning Models (o3, o4-mini) for:**
- Mathematical problems
- Scientific analysis
- Step-by-step reasoning
- Logic puzzles

### Implement Caching

```python
# Use semantic cache to reduce duplicate requests
from azure.ai.cache import SemanticCache

cache = SemanticCache(
    similarity_threshold=0.95,
    ttl_seconds=3600
)

# Check cache before API call
cached_response = cache.get(user_query)
if cached_response:
    return cached_response

response = client.chat.completions.create(
    model="gpt-5",
    messages=messages
)

cache.set(user_query, response)
```

### Token Management

```python
import tiktoken

# Count tokens before API call
encoding = tiktoken.get_encoding("cl100k_base")
tokens = len(encoding.encode(prompt))

if tokens > 100000:
    print(f"Warning: Prompt has {tokens} tokens, this will be expensive!")

# Use shorter max_tokens when appropriate
response = client.chat.completions.create(
    model="gpt-5",
    messages=messages,
    max_tokens=500  # Limit output tokens
)
```

## Monitoring and Alerts

### Set Up Cost Alerts

```bash
# Create budget alert
az consumption budget create \
  --budget-name openai-monthly-budget \
  --resource-group MyRG \
  --amount 1000 \
  --category Cost \
  --time-grain Monthly \
  --start-date 2025-01-01 \
  --end-date 2025-12-31 \
  --notifications '{
    "actual_GreaterThan_80_Percent": {
      "enabled": true,
      "operator": "GreaterThan",
      "threshold": 80,
      "contactEmails": ["billing@example.com"]
    }
  }'
```

### Application Insights Integration

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
))

# Log API calls
logger.info("OpenAI API call", extra={
    "custom_dimensions": {
        "model": "gpt-5",
        "tokens": response.usage.total_tokens,
        "cost": calculate_cost(response.usage.total_tokens),
        "latency_ms": response.response_ms
    }
})
```

## Best Practices

✓ **Use Model Router** for automatic cost optimization
✓ **Implement caching** to reduce duplicate requests
✓ **Monitor token usage** and set budgets
✓ **Use private endpoints** for production workloads
✓ **Enable managed identity** instead of API keys
✓ **Configure content filtering** for safety
✓ **Right-size capacity** based on actual demand
✓ **Use Foundry Observability** for monitoring
✓ **Implement retry logic** with exponential backoff
✓ **Choose appropriate models** for task complexity

## References

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/)
- [What's New in Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/whats-new)
- [GPT-5 Announcement](https://azure.microsoft.com/en-us/blog/gpt-5-azure/)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- [Model Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)

Azure OpenAI Service with GPT-5 and reasoning models brings enterprise-grade AI to your applications!
