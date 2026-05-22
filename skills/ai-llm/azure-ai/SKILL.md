---
name: azure-ai
description: "Build AI solutions with Azure AI services including OpenAI, Cognitive Services, Document Intelligence, and AI Search. Use for enterprise AI, document processing, and intelligent applications on Azure."
---

# Azure AI Skill

Complete guidance for building, configuring, troubleshooting, and managing Azure AI services.

## Quick Reference

### Service Categories
| Category | Services |
|----------|----------|
| **AI Platform** | Microsoft Foundry (Azure AI Foundry), Azure AI Hub, AI Projects |
| **Generative AI** | Azure OpenAI Service (GPT-4, GPT-4o, o1, DALL-E, Whisper) |
| **Search & RAG** | Azure AI Search (vector, semantic, hybrid, agentic retrieval) |
| **AI Agents** | Azure AI Agent Service, Foundry Agent Service, Multi-agent Orchestration |
| **Document AI** | Document Intelligence (OCR, form extraction, prebuilt models) |
| **Cognitive Services** | Vision, Speech, Language, Translator, Content Safety |
| **ML Platform** | Azure Machine Learning (MLOps, training, deployment) |
| **Governance** | Responsible AI, Content Filtering, Safety Evaluations |

### Common CLI Prefixes
```bash
az cognitiveservices    # Cognitive Services & Azure OpenAI
az search               # Azure AI Search
az ml                   # Azure Machine Learning
az ai                   # Azure AI resources (newer)
```

---

## 1. Microsoft Foundry (Azure AI Foundry)

### Overview
Microsoft Foundry is the unified platform for enterprise AI operations, combining:
- **AI Hub**: Shared infrastructure (connections, compute, policies)
- **AI Projects**: Workspaces for building AI applications
- **Model Catalog**: Pre-trained models from Azure OpenAI, Meta, Mistral, Cohere
- **Prompt Flow**: Visual orchestration for LLM workflows

### Portal Access
- **Foundry (New)**: https://ai.azure.com
- **Foundry (Classic)**: https://ai.azure.com/build (legacy)

### Create AI Hub & Project
```bash
# Create resource group
az group create --name rg-ai-foundry --location eastus

# Create AI Hub (shared infrastructure)
az ml workspace create \
  --name ai-hub-prod \
  --resource-group rg-ai-foundry \
  --kind hub \
  --location eastus

# Create AI Project (linked to hub)
az ml workspace create \
  --name ai-project-chatbot \
  --resource-group rg-ai-foundry \
  --kind project \
  --hub-id /subscriptions/{sub}/resourceGroups/rg-ai-foundry/providers/Microsoft.MachineLearningServices/workspaces/ai-hub-prod
```

### Python SDK Setup
```python
# Install SDK
# pip install azure-ai-projects azure-identity

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize client
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://<hub-name>.api.azureml.ms",
    project_name="ai-project-chatbot"
)

# List models in project
for model in project.models.list():
    print(f"{model.name}: {model.description}")
```

### Connections Management
```bash
# List connections in hub
az ml connection list --workspace-name ai-hub-prod --resource-group rg-ai-foundry

# Create Azure OpenAI connection
az ml connection create \
  --file connection.yml \
  --workspace-name ai-hub-prod \
  --resource-group rg-ai-foundry
```

Connection YAML example:
```yaml
# connection.yml
name: aoai-connection
type: azure_open_ai
target: https://<openai-resource>.openai.azure.com/
api_key: <your-api-key>
api_version: "2024-10-21"
```

---

## 2. Azure OpenAI Service

### Deployment Types
| Type | Use Case | Billing |
|------|----------|---------|
| **Standard** | Development, testing | Pay-per-token |
| **Global Standard** | Production, global routing | Pay-per-token |
| **Provisioned (PTU)** | High-throughput, predictable latency | Reserved capacity |
| **Data Zone** | Data residency requirements | Region-specific |

### Available Models (as of 2024)
- **GPT-4o** (latest multimodal) - Text, images, audio
- **GPT-4 Turbo** - 128k context window
- **GPT-4** - 8k/32k context
- **o1-preview / o1-mini** - Reasoning models
- **DALL-E 3** - Image generation
- **Whisper** - Speech-to-text
- **text-embedding-ada-002** / **text-embedding-3-large** - Embeddings

### Create Azure OpenAI Resource
```bash
# Create Cognitive Services account for OpenAI
az cognitiveservices account create \
  --name openai-prod \
  --resource-group rg-ai \
  --kind OpenAI \
  --sku S0 \
  --location eastus \
  --custom-domain openai-prod

# Deploy a model
az cognitiveservices account deployment create \
  --name openai-prod \
  --resource-group rg-ai \
  --deployment-name gpt-4o-deployment \
  --model-name gpt-4o \
  --model-version "2024-08-06" \
  --model-format OpenAI \
  --sku-name Standard \
  --sku-capacity 10
```

### List Deployments & Models
```bash
# List all deployments
az cognitiveservices account deployment list \
  --name openai-prod \
  --resource-group rg-ai \
  --output table

# List available models in region
az cognitiveservices account list-models \
  --name openai-prod \
  --resource-group rg-ai
```

### Python SDK Usage
```python
# pip install openai

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="<your-key>",
    api_version="2024-10-21",
    azure_endpoint="https://openai-prod.openai.azure.com"
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o-deployment",  # deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing"}
    ],
    max_tokens=500,
    temperature=0.7
)
print(response.choices[0].message.content)

# Embeddings
embedding = client.embeddings.create(
    model="text-embedding-3-large",
    input="The quick brown fox"
)
print(f"Vector dimension: {len(embedding.data[0].embedding)}")

# Image generation
image = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city skyline at sunset",
    size="1024x1024",
    quality="hd"
)
print(image.data[0].url)
```

### Content Filtering
```bash
# View content filter configuration
az cognitiveservices account show \
  --name openai-prod \
  --resource-group rg-ai \
  --query properties.contentFilterConfiguration
```

Configure custom content filter policy:
```python
# Categories: hate, violence, sexual, self-harm
# Severity levels: safe, low, medium, high
filter_config = {
    "hate": {"severity": "medium", "blocking": True},
    "violence": {"severity": "low", "blocking": True},
    "sexual": {"severity": "medium", "blocking": True},
    "self_harm": {"severity": "low", "blocking": True}
}
```

---

## 3. Azure AI Search

### Search Modes
| Mode | Features | Use Case |
|------|----------|----------|
| **Keyword** | BM25 ranking, full-text | Traditional search |
| **Vector** | Embedding similarity | Semantic similarity |
| **Hybrid** | Keyword + Vector | Best of both |
| **Semantic** | Re-ranking with language models | Improved relevance |
| **Agentic Retrieval** | Knowledge store for AI agents | RAG applications |

### Create Search Service
```bash
# Create search service
az search service create \
  --name search-prod \
  --resource-group rg-ai \
  --sku standard \
  --location eastus \
  --partition-count 1 \
  --replica-count 1

# Get admin keys
az search admin-key show \
  --service-name search-prod \
  --resource-group rg-ai

# Get query keys
az search query-key list \
  --service-name search-prod \
  --resource-group rg-ai
```

### Create Vector Index
```python
# pip install azure-search-documents

from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch
)
from azure.core.credentials import AzureKeyCredential

# Initialize client
index_client = SearchIndexClient(
    endpoint="https://search-prod.search.windows.net",
    credential=AzureKeyCredential("<admin-key>")
)

# Define index with vector field
index = SearchIndex(
    name="documents-index",
    fields=[
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(name="title", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(name="category", type=SearchFieldDataType.String, filterable=True, facetable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,  # text-embedding-ada-002
            vector_search_profile_name="vector-profile"
        )
    ],
    vector_search=VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config")
        ],
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ]
    ),
    semantic_search=SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="semantic-config",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=SemanticField(field_name="title"),
                    content_fields=[SemanticField(field_name="content")]
                )
            )
        ]
    )
)

# Create index
index_client.create_or_update_index(index)
```

### Hybrid Search Query
```python
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

search_client = SearchClient(
    endpoint="https://search-prod.search.windows.net",
    index_name="documents-index",
    credential=AzureKeyCredential("<query-key>")
)

# Get query embedding (from Azure OpenAI)
query_embedding = get_embedding("What is machine learning?")

# Hybrid search (keyword + vector)
results = search_client.search(
    search_text="machine learning",
    vector_queries=[
        VectorizedQuery(
            vector=query_embedding,
            k_nearest_neighbors=5,
            fields="content_vector"
        )
    ],
    query_type="semantic",
    semantic_configuration_name="semantic-config",
    top=10
)

for result in results:
    print(f"{result['title']}: {result['@search.score']}")
```

### Agentic Retrieval (Knowledge Store)
```python
# pip install azure-ai-projects

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import AgentKnowledgeStore

# Create knowledge store linked to search index
knowledge_store = project.agents.knowledge_stores.create(
    name="docs-knowledge",
    index_name="documents-index",
    search_endpoint="https://search-prod.search.windows.net",
    semantic_configuration="semantic-config"
)

# Use in agent
agent = project.agents.create(
    name="doc-assistant",
    model="gpt-4o",
    knowledge_store_ids=[knowledge_store.id]
)
```

---

## 4. Azure AI Agents

### Agent Types
| Type | Description | Use Case |
|------|-------------|----------|
| **Foundry Agent** | Managed agent with tools | Chat assistants |
| **Code Interpreter** | Python execution sandbox | Data analysis |
| **File Search** | Document retrieval | RAG applications |
| **Function Calling** | Custom function execution | API integration |
| **Multi-Agent** | Orchestrated agent swarm | Complex workflows |

### Create Basic Agent
```python
# pip install azure-ai-projects azure-ai-agents

from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential

# Initialize
project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint="https://<hub>.api.azureml.ms",
    project_name="my-project"
)

# Create agent with tools
agent = project.agents.create_agent(
    model="gpt-4o",
    name="data-analyst",
    instructions="You are a data analyst. Analyze data and create visualizations.",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ]
)

# Create thread and run
thread = project.agents.create_thread()
message = project.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Analyze the sales data and create a trend chart"
)

run = project.agents.create_run(
    thread_id=thread.id,
    agent_id=agent.id
)

# Wait for completion
import time
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = project.agents.get_run(thread_id=thread.id, run_id=run.id)

# Get response
messages = project.agents.list_messages(thread_id=thread.id)
for msg in messages.data:
    if msg.role == "assistant":
        print(msg.content[0].text.value)
```

### Function Calling Agent
```python
# Define custom functions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

agent = project.agents.create_agent(
    model="gpt-4o",
    name="weather-assistant",
    instructions="Help users with weather information.",
    tools=tools
)

# Handle function calls in run loop
while run.status == "requires_action":
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []

    for call in tool_calls:
        if call.function.name == "get_weather":
            args = json.loads(call.function.arguments)
            result = fetch_weather(args["location"])  # Your function
            tool_outputs.append({
                "tool_call_id": call.id,
                "output": json.dumps(result)
            })

    run = project.agents.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=tool_outputs
    )
```

### Multi-Agent Orchestration
```python
# Supervisor pattern - one agent coordinates others
supervisor = project.agents.create_agent(
    model="gpt-4o",
    name="supervisor",
    instructions="""You are a supervisor coordinating a team:
    - researcher: Finds information
    - writer: Creates content
    - reviewer: Reviews and edits

    Delegate tasks and synthesize results."""
)

researcher = project.agents.create_agent(
    model="gpt-4o",
    name="researcher",
    instructions="You research topics and provide factual information.",
    tools=[{"type": "file_search"}]
)

writer = project.agents.create_agent(
    model="gpt-4o",
    name="writer",
    instructions="You write clear, engaging content based on research."
)

reviewer = project.agents.create_agent(
    model="gpt-4o",
    name="reviewer",
    instructions="You review content for accuracy, clarity, and style."
)

# Orchestration logic handles routing between agents
```

---

## 5. Document Intelligence

### Prebuilt Models
| Model | Use Case |
|-------|----------|
| **read** | General OCR, text extraction |
| **layout** | Tables, figures, structure |
| **invoice** | Invoice data extraction |
| **receipt** | Receipt parsing |
| **id-document** | IDs, passports, driver licenses |
| **business-card** | Contact information |
| **tax documents** | W-2, 1099, etc. |
| **mortgage** | Loan documents |
| **health-insurance** | Insurance cards |
| **contract** | Legal documents |

### Create Document Intelligence Resource
```bash
az cognitiveservices account create \
  --name doc-intel-prod \
  --resource-group rg-ai \
  --kind FormRecognizer \
  --sku S0 \
  --location eastus
```

### Python SDK Usage
```python
# pip install azure-ai-documentintelligence

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint="https://doc-intel-prod.cognitiveservices.azure.com",
    credential=AzureKeyCredential("<key>")
)

# Analyze invoice
with open("invoice.pdf", "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",
        analyze_request=AnalyzeDocumentRequest(bytes_source=f.read())
    )

result = poller.result()

for invoice in result.documents:
    print(f"Vendor: {invoice.fields.get('VendorName', {}).get('content')}")
    print(f"Total: {invoice.fields.get('InvoiceTotal', {}).get('content')}")
    print(f"Date: {invoice.fields.get('InvoiceDate', {}).get('content')}")

    # Line items
    for item in invoice.fields.get("Items", {}).get("valueArray", []):
        print(f"  - {item.get('content')}")

# Layout analysis (tables, figures)
poller = client.begin_analyze_document(
    model_id="prebuilt-layout",
    analyze_request=AnalyzeDocumentRequest(url_source="https://example.com/doc.pdf")
)

result = poller.result()
for table in result.tables:
    print(f"Table: {table.row_count} rows x {table.column_count} cols")
    for cell in table.cells:
        print(f"  [{cell.row_index},{cell.column_index}]: {cell.content}")
```

### Custom Model Training
```python
# Train custom extraction model
training_data = "https://storage.blob.core.windows.net/training-data?sv=..."

poller = client.begin_build_document_model(
    build_request={
        "modelId": "custom-contract-model",
        "description": "Custom contract extraction",
        "azureBlobSource": {
            "containerUrl": training_data
        }
    }
)

model = poller.result()
print(f"Model ID: {model.model_id}")
print(f"Fields: {list(model.doc_types.values())[0].field_schema.keys()}")
```

---

## 6. Cognitive Services

### Vision
```python
# pip install azure-ai-vision-imageanalysis

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

client = ImageAnalysisClient(
    endpoint="https://vision-prod.cognitiveservices.azure.com",
    credential=AzureKeyCredential("<key>")
)

# Analyze image
result = client.analyze(
    image_url="https://example.com/image.jpg",
    visual_features=[
        VisualFeatures.CAPTION,
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS,
        VisualFeatures.DENSE_CAPTIONS,
        VisualFeatures.READ,  # OCR
        VisualFeatures.SMART_CROPS,
        VisualFeatures.PEOPLE
    ]
)

print(f"Caption: {result.caption.text} ({result.caption.confidence:.2f})")
print(f"Tags: {', '.join([t.name for t in result.tags.list])}")
for obj in result.objects.list:
    print(f"Object: {obj.tags[0].name} at {obj.bounding_box}")
```

### Speech
```python
# pip install azure-cognitiveservices-speech

import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="<key>",
    region="eastus"
)

# Speech-to-text
audio_config = speechsdk.AudioConfig(filename="audio.wav")
recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config
)

result = recognizer.recognize_once()
print(f"Recognized: {result.text}")

# Text-to-speech
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

result = synthesizer.speak_text_async("Hello, this is Azure Speech.").get()
audio_data = result.audio_data
```

### Language
```python
# pip install azure-ai-textanalytics

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint="https://language-prod.cognitiveservices.azure.com",
    credential=AzureKeyCredential("<key>")
)

documents = ["Azure AI is amazing! I love using it for my projects."]

# Sentiment analysis
result = client.analyze_sentiment(documents)[0]
print(f"Sentiment: {result.sentiment} ({result.confidence_scores})")

# Key phrase extraction
result = client.extract_key_phrases(documents)[0]
print(f"Key phrases: {result.key_phrases}")

# Entity recognition
result = client.recognize_entities(documents)[0]
for entity in result.entities:
    print(f"Entity: {entity.text} ({entity.category})")

# Language detection
result = client.detect_language(documents)[0]
print(f"Language: {result.primary_language.name}")
```

### Translator
```python
# pip install azure-ai-translation-text

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

client = TextTranslationClient(
    credential=AzureKeyCredential("<key>"),
    region="eastus"
)

# Translate text
result = client.translate(
    body=["Hello, how are you?"],
    to_language=["es", "fr", "de"]
)

for translation in result[0].translations:
    print(f"{translation.to}: {translation.text}")

# Detect language
result = client.detect_language(body=["Bonjour le monde"])
print(f"Detected: {result[0].language} ({result[0].score})")
```

---

## 7. Content Safety

### Categories & Severity Levels
| Category | Description | Severity (0-7) |
|----------|-------------|----------------|
| **Hate** | Discriminatory content | 0=safe, 2=low, 4=medium, 6=high |
| **Violence** | Violent content | 0=safe, 2=low, 4=medium, 6=high |
| **Sexual** | Sexual content | 0=safe, 2=low, 4=medium, 6=high |
| **SelfHarm** | Self-harm content | 0=safe, 2=low, 4=medium, 6=high |

### Create Content Safety Resource
```bash
az cognitiveservices account create \
  --name content-safety-prod \
  --resource-group rg-ai \
  --kind ContentSafety \
  --sku S0 \
  --location eastus
```

### Python SDK Usage
```python
# pip install azure-ai-contentsafety

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint="https://content-safety-prod.cognitiveservices.azure.com",
    credential=AzureKeyCredential("<key>")
)

# Analyze text
request = AnalyzeTextOptions(
    text="Sample text to analyze for safety",
    categories=[
        TextCategory.HATE,
        TextCategory.VIOLENCE,
        TextCategory.SEXUAL,
        TextCategory.SELF_HARM
    ]
)

result = client.analyze_text(request)

for category_result in result.categories_analysis:
    print(f"{category_result.category}: severity {category_result.severity}")

# Check if content should be blocked (threshold-based)
def should_block(result, threshold=4):
    for cat in result.categories_analysis:
        if cat.severity >= threshold:
            return True
    return False

if should_block(result):
    print("Content blocked due to safety concerns")
```

### Image Moderation
```python
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData

# Analyze image
with open("image.jpg", "rb") as f:
    image_data = f.read()

request = AnalyzeImageOptions(
    image=ImageData(content=image_data)
)

result = client.analyze_image(request)
for category in result.categories_analysis:
    print(f"{category.category}: {category.severity}")
```

---

## 8. Azure Machine Learning

### Workspace Management
```bash
# Create ML workspace
az ml workspace create \
  --name ml-workspace-prod \
  --resource-group rg-ai \
  --location eastus

# List workspaces
az ml workspace list --resource-group rg-ai --output table

# Create compute cluster
az ml compute create \
  --name gpu-cluster \
  --type AmlCompute \
  --size Standard_NC6s_v3 \
  --min-instances 0 \
  --max-instances 4 \
  --workspace-name ml-workspace-prod \
  --resource-group rg-ai
```

### Model Registration & Deployment
```python
# pip install azure-ai-ml

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model, ManagedOnlineEndpoint, ManagedOnlineDeployment
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<sub-id>",
    resource_group_name="rg-ai",
    workspace_name="ml-workspace-prod"
)

# Register model
model = ml_client.models.create_or_update(
    Model(
        name="my-classifier",
        path="./model",
        description="Image classification model"
    )
)

# Create online endpoint
endpoint = ManagedOnlineEndpoint(
    name="classifier-endpoint",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint).result()

# Deploy model
deployment = ManagedOnlineDeployment(
    name="blue",
    endpoint_name="classifier-endpoint",
    model=model.id,
    instance_type="Standard_DS3_v2",
    instance_count=1
)
ml_client.online_deployments.begin_create_or_update(deployment).result()

# Set traffic
endpoint.traffic = {"blue": 100}
ml_client.online_endpoints.begin_create_or_update(endpoint).result()
```

### Training Jobs
```python
from azure.ai.ml import command
from azure.ai.ml.entities import Environment

# Define training job
job = command(
    code="./src",
    command="python train.py --epochs ${{inputs.epochs}} --lr ${{inputs.lr}}",
    inputs={
        "epochs": 10,
        "lr": 0.001
    },
    environment=Environment(
        image="mcr.microsoft.com/azureml/pytorch-2.0-cuda11.8:latest"
    ),
    compute="gpu-cluster",
    display_name="training-run"
)

# Submit job
returned_job = ml_client.jobs.create_or_update(job)
print(f"Job URL: {returned_job.studio_url}")

# Monitor job
from azure.ai.ml.entities import Job
status = ml_client.jobs.get(returned_job.name)
print(f"Status: {status.status}")
```

### MLflow Integration
```python
import mlflow
from azure.ai.ml import MLClient

# Set tracking URI
ml_client = MLClient(...)
mlflow_tracking_uri = ml_client.workspaces.get(ml_client.workspace_name).mlflow_tracking_uri
mlflow.set_tracking_uri(mlflow_tracking_uri)

# Log experiment
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_artifact("model.pkl")
    mlflow.sklearn.log_model(model, "model")
```

---

## 9. Observability & Tracing

### Application Insights Integration
```python
# pip install azure-monitor-opentelemetry

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Configure (use connection string from Azure Portal)
configure_azure_monitor(
    connection_string="InstrumentationKey=...;IngestionEndpoint=..."
)

tracer = trace.get_tracer(__name__)

# Create spans for AI operations
with tracer.start_as_current_span("llm-inference") as span:
    span.set_attribute("model", "gpt-4o")
    span.set_attribute("tokens.input", 100)
    span.set_attribute("tokens.output", 250)

    response = call_openai(prompt)

    span.set_attribute("tokens.total", response.usage.total_tokens)
```

### Prompt Flow Tracing
```python
from promptflow.tracing import start_trace

# Enable tracing
start_trace(
    resource_attributes={
        "service.name": "chatbot-service",
        "service.version": "1.0.0"
    }
)

# Traces are automatically captured for:
# - Azure OpenAI calls
# - Azure AI Search queries
# - Custom function calls
```

### Azure AI Evaluation
```python
# pip install azure-ai-evaluation

from azure.ai.evaluation import GroundednessEvaluator, RelevanceEvaluator

# Evaluate response quality
groundedness = GroundednessEvaluator()
relevance = RelevanceEvaluator()

result = groundedness.evaluate(
    query="What is Azure AI?",
    context="Azure AI is Microsoft's cloud AI platform...",
    response="Azure AI provides machine learning and cognitive services."
)
print(f"Groundedness score: {result['groundedness']}")

result = relevance.evaluate(
    query="What is Azure AI?",
    response="Azure AI provides machine learning and cognitive services."
)
print(f"Relevance score: {result['relevance']}")
```

---

## 10. Responsible AI

### Six Principles
1. **Fairness** - AI systems should treat all people fairly
2. **Reliability & Safety** - AI systems should perform reliably and safely
3. **Privacy & Security** - AI systems should be secure and respect privacy
4. **Inclusiveness** - AI systems should empower everyone
5. **Transparency** - AI systems should be understandable
6. **Accountability** - People should be accountable for AI systems

### Content Filtering Configuration
```python
# Azure OpenAI content filter settings
content_filter_config = {
    "prompt": {
        "hate": {"filtering": True, "severity_threshold": "medium"},
        "violence": {"filtering": True, "severity_threshold": "medium"},
        "sexual": {"filtering": True, "severity_threshold": "medium"},
        "self_harm": {"filtering": True, "severity_threshold": "medium"}
    },
    "completion": {
        "hate": {"filtering": True, "severity_threshold": "medium"},
        "violence": {"filtering": True, "severity_threshold": "medium"},
        "sexual": {"filtering": True, "severity_threshold": "medium"},
        "self_harm": {"filtering": True, "severity_threshold": "medium"}
    }
}
```

### Model Evaluation for Bias
```python
from azure.ai.evaluation import HateSpeechEvaluator, ViolenceEvaluator

# Evaluate model outputs for harmful content
hate_evaluator = HateSpeechEvaluator()
violence_evaluator = ViolenceEvaluator()

# Batch evaluation
results = []
for response in model_responses:
    hate_score = hate_evaluator.evaluate(response=response)
    violence_score = violence_evaluator.evaluate(response=response)
    results.append({
        "response": response,
        "hate_score": hate_score,
        "violence_score": violence_score
    })
```

---

## Troubleshooting

### Common Issues

**Authentication Errors**
```bash
# Check logged in identity
az account show

# Re-login
az login

# Use service principal
az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>

# Check role assignments
az role assignment list --assignee <identity>
```

**Quota Exceeded**
```bash
# Check current usage
az cognitiveservices usage list \
  --name openai-prod \
  --resource-group rg-ai

# Request quota increase via Azure Portal > Quotas
```

**Model Not Available**
```bash
# List available models in region
az cognitiveservices account list-models \
  --name openai-prod \
  --resource-group rg-ai \
  --output table

# Check model availability by region
# https://learn.microsoft.com/azure/ai-services/openai/concepts/models
```

**Rate Limiting (429 Errors)**
```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
def call_with_retry():
    return client.chat.completions.create(...)
```

**Search Index Issues**
```bash
# Check index status
az search service show --name search-prod --resource-group rg-ai

# Rebuild index
# Use indexer reset via REST API or SDK
```

### Logging & Diagnostics
```bash
# Enable diagnostic logging
az monitor diagnostic-settings create \
  --name ai-diagnostics \
  --resource /subscriptions/{sub}/resourceGroups/rg-ai/providers/Microsoft.CognitiveServices/accounts/openai-prod \
  --logs '[{"category": "RequestResponse", "enabled": true}]' \
  --workspace /subscriptions/{sub}/resourceGroups/rg-ai/providers/Microsoft.OperationalInsights/workspaces/log-analytics-prod

# Query logs
az monitor log-analytics query \
  --workspace log-analytics-prod \
  --analytics-query "AzureDiagnostics | where ResourceProvider == 'MICROSOFT.COGNITIVESERVICES'"
```

---

## Best Practices

### Cost Optimization
1. Use **Provisioned Throughput (PTU)** for predictable high-volume workloads
2. Implement **caching** for repeated queries
3. Use **smaller models** when possible (GPT-4o-mini vs GPT-4o)
4. Set **max_tokens** appropriately to avoid waste
5. Batch requests when possible

### Security
1. Use **Managed Identities** instead of API keys
2. Store keys in **Azure Key Vault**
3. Enable **Private Endpoints** for network isolation
4. Configure **RBAC** with least privilege
5. Enable **audit logging**

### Performance
1. Deploy to **regions close to users**
2. Use **Global Standard** deployment for automatic routing
3. Implement **retry logic** with exponential backoff
4. Use **streaming** for long responses
5. Pre-compute **embeddings** for known content

### Reliability
1. Deploy across **multiple regions**
2. Implement **circuit breaker** patterns
3. Set up **alerts** for quota and errors
4. Have **fallback models** configured
5. Regular **backup** of custom models and configurations
