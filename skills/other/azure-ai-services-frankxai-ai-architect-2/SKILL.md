---
name: Azure AI Services Expert
description: Build AI applications on Azure using Azure OpenAI, Cognitive Services, and ML services with enterprise patterns
version: 1.1.0
last_updated: 2026-01-06
external_version: "Azure OpenAI GPT-5.2"
triggers:
  - Azure OpenAI
  - Azure AI
  - Cognitive Services
  - Azure ML
---

# Azure AI Services Expert

You are an expert in Microsoft Azure AI services, specializing in Azure OpenAI Service for GPT models, Azure AI Services, and Azure Machine Learning.

## Azure OpenAI Service

### Overview
Azure OpenAI provides access to OpenAI models (GPT-4, GPT-4o, DALL-E, Whisper) with Azure's enterprise security, compliance, and regional availability.

### Available Models

| Model | Context | Best For |
|-------|---------|----------|
| **GPT-4o** | 128K | Multimodal, fastest GPT-4 |
| **GPT-4 Turbo** | 128K | Complex reasoning |
| **GPT-4** | 8K/32K | High capability |
| **GPT-3.5 Turbo** | 16K | Fast, cost-effective |
| **text-embedding-ada-002** | 8K | Embeddings |
| **text-embedding-3-large** | 8K | Better embeddings |
| **DALL-E 3** | - | Image generation |
| **Whisper** | - | Speech-to-text |

### Basic Usage

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o",  # Deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain machine learning"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    # Execute function and send result back
```

### Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-large",  # Deployment name
    input="Your text to embed",
    dimensions=1024  # Optional: reduce dimensions
)

embedding = response.data[0].embedding
```

### Vision (GPT-4o)

```python
import base64

def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image('image.jpg')}"
                    }
                }
            ]
        }
    ]
)
```

## Provisioned Throughput Units (PTU)

### When to Use PTU
- Predictable, high-volume workloads
- Guaranteed performance requirements
- Cost optimization at scale

### PTU Sizing

```python
# PTU capacity estimation
def estimate_ptus(
    requests_per_minute: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model: str = "gpt-4o"
) -> int:
    """Estimate PTUs needed for workload"""

    # Tokens per minute per PTU (approximate)
    TPM_PER_PTU = {
        "gpt-4o": 10000,
        "gpt-4-turbo": 8000,
        "gpt-35-turbo": 50000,
    }

    total_tokens_per_minute = requests_per_minute * (avg_input_tokens + avg_output_tokens)
    ptus_needed = total_tokens_per_minute / TPM_PER_PTU[model]

    return max(1, int(ptus_needed * 1.2))  # 20% buffer

# Example: 100 RPM, 500 input tokens, 200 output tokens
estimate_ptus(100, 500, 200, "gpt-4o")  # Returns: 9 PTUs
```

## Azure AI Search (Cognitive Search)

### Vector Search Setup

```python
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)

# Create index with vector field
index = SearchIndex(
    name="documents-index",
    fields=[
        SearchField(name="id", type="Edm.String", key=True),
        SearchField(name="content", type="Edm.String", searchable=True),
        SearchField(
            name="embedding",
            type="Collection(Edm.Single)",
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="vector-profile"
        ),
    ],
    vector_search=VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[
            VectorSearchProfile(name="vector-profile", algorithm_configuration_name="hnsw")
        ]
    )
)

index_client = SearchIndexClient(endpoint, credential)
index_client.create_index(index)
```

### Hybrid Search (Vector + Keyword)

```python
from azure.search.documents.models import VectorizedQuery

search_client = SearchClient(endpoint, "documents-index", credential)

# Get embedding for query
query_embedding = get_embedding("What is machine learning?")

# Hybrid search
results = search_client.search(
    search_text="machine learning",  # Keyword search
    vector_queries=[
        VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=5,
            fields="embedding"
        )
    ],
    select=["id", "content"],
    top=10
)

for result in results:
    print(f"Score: {result['@search.score']}, Content: {result['content'][:100]}")
```

## Azure AI Studio

### Prompt Flow

```yaml
# flow.dag.yaml
inputs:
  question:
    type: string

outputs:
  answer:
    type: string
    reference: ${generate_answer.output}

nodes:
  - name: embed_question
    type: python
    source:
      type: code
      path: embed.py
    inputs:
      text: ${inputs.question}

  - name: search_documents
    type: python
    source:
      type: code
      path: search.py
    inputs:
      embedding: ${embed_question.output}

  - name: generate_answer
    type: llm
    source:
      type: code
      path: prompt.jinja2
    inputs:
      deployment_name: gpt-4o
      context: ${search_documents.output}
      question: ${inputs.question}
```

## Azure Machine Learning

### Training with Azure ML

```python
from azure.ai.ml import MLClient, command, Input
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="...",
    resource_group_name="...",
    workspace_name="..."
)

# Define training job
job = command(
    code="./src",
    command="python train.py --data ${{inputs.data}} --lr ${{inputs.learning_rate}}",
    inputs={
        "data": Input(type="uri_folder", path="azureml://datastores/data/paths/train/"),
        "learning_rate": 0.001,
    },
    environment="AzureML-pytorch-2.0-cuda11.8@latest",
    compute="gpu-cluster",
    experiment_name="llm-finetune"
)

# Submit job
returned_job = ml_client.jobs.create_or_update(job)
```

### Deploy to Managed Endpoint

```python
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
)

# Create endpoint
endpoint = ManagedOnlineEndpoint(
    name="llm-endpoint",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Deploy model
deployment = ManagedOnlineDeployment(
    name="llm-deployment",
    endpoint_name="llm-endpoint",
    model=Model(path="./model"),
    instance_type="Standard_NC24ads_A100_v4",
    instance_count=1,
)
ml_client.online_deployments.begin_create_or_update(deployment).result()
```

## Architecture Patterns

### Enterprise RAG on Azure

```
┌─────────────────────────────────────────────────────────────────┐
│                    AZURE RAG ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User ──▶ Azure Front Door ──▶ API Management                   │
│                                      │                           │
│                                      ▼                           │
│                              Azure Functions                     │
│                                      │                           │
│                    ┌─────────────────┼─────────────────┐        │
│                    ▼                 ▼                 ▼        │
│           ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│           │ Azure OpenAI │  │  AI Search   │  │  Blob Store  │ │
│           │   (GPT-4o)   │  │  (Vectors)   │  │ (Documents)  │ │
│           └──────────────┘  └──────────────┘  └──────────────┘ │
│                                      │                           │
│                                      ▼                           │
│                              Cosmos DB                           │
│                         (Conversation History)                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Bicep/ARM Deployment

```bicep
// main.bicep
param location string = resourceGroup().location
param openaiName string

resource openai 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: openaiName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: openaiName
    publicNetworkAccess: 'Disabled'
  }
}

resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-10-01-preview' = {
  parent: openai
  name: 'gpt-4o'
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-05-13'
    }
  }
  sku: {
    name: 'Standard'
    capacity: 100  // TPM in thousands
  }
}
```

## Pricing

### Azure OpenAI Pricing (per 1K tokens)

| Model | Input | Output |
|-------|-------|--------|
| GPT-4o | $0.005 | $0.015 |
| GPT-4 Turbo | $0.01 | $0.03 |
| GPT-3.5 Turbo | $0.0005 | $0.0015 |
| text-embedding-3-large | $0.00013 | - |

### PTU Pricing
- ~$0.06 per PTU-hour
- Minimum 1 month commitment
- 30%+ savings vs pay-as-you-go at scale

## Security

### Private Endpoints

```bicep
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2023-04-01' = {
  name: '${openaiName}-pe'
  location: location
  properties: {
    subnet: {
      id: subnetId
    }
    privateLinkServiceConnections: [
      {
        name: '${openaiName}-plsc'
        properties: {
          privateLinkServiceId: openai.id
          groupIds: ['account']
        }
      }
    ]
  }
}
```

### Managed Identity

```python
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

# Use managed identity (no API keys!)
credential = DefaultAzureCredential()
token = credential.get_token("https://cognitiveservices.azure.com/.default")

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-02-01",
    azure_ad_token=token.token
)
```

## Content Filtering

```python
# Azure OpenAI has built-in content filtering
# Configure via Azure Portal or API

# Check for filtered content in response
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "..."}]
)

# Content filter results
if hasattr(response.choices[0], 'content_filter_results'):
    filters = response.choices[0].content_filter_results
    if filters.get('hate', {}).get('filtered'):
        print("Content was filtered for hate speech")
```

## Resources

- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure AI Search Docs](https://learn.microsoft.com/azure/search/)
- [Azure ML Docs](https://learn.microsoft.com/azure/machine-learning/)
- [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/)
