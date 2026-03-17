---
name: azure-ai
description: Comprehensive Azure AI skill for building, configuring, troubleshooting, and managing all Azure AI services. Covers Azure AI Foundry, Azure OpenAI Service, Azure AI Search, Azure AI Agents, Document Intelligence, Cognitive Services (Vision, Speech, Language), Azure Machine Learning, Content Safety, and Responsible AI. Use when working with AI workloads, LLM deployments, vector search, RAG patterns, multi-agent orchestration, or any Azure AI service.
---

# Azure AI Services Skill

Build and manage AI solutions with Azure AI services including Azure OpenAI, AI Search, Document Intelligence, and Cognitive Services.

## Triggers

Use this skill when you see:
- azure ai, azure openai, gpt, openai service
- azure ai search, cognitive search, vector search
- document intelligence, form recognizer
- azure ml, machine learning, mlops
- content safety, responsible ai

## Instructions

### Azure OpenAI Service

#### Deploy Model via CLI

```bash
# Create Azure OpenAI resource
az cognitiveservices account create \
    --name myopenai \
    --resource-group mygroup \
    --kind OpenAI \
    --sku S0 \
    --location eastus

# Deploy a model
az cognitiveservices account deployment create \
    --name myopenai \
    --resource-group mygroup \
    --deployment-name gpt-4 \
    --model-name gpt-4 \
    --model-version "0613" \
    --model-format OpenAI \
    --sku-capacity 10 \
    --sku-name Standard
```

#### Python SDK Usage

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Chat completion
response = client.chat.completions.create(
    model="gpt-4",  # deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=800
)

print(response.choices[0].message.content)
```

#### Embeddings

```python
# Generate embeddings
response = client.embeddings.create(
    model="text-embedding-ada-002",  # deployment name
    input=["Hello world", "How are you?"]
)

embeddings = [item.embedding for item in response.data]
```

### Azure AI Search

#### Create Search Index

```bash
# Create search service
az search service create \
    --name mysearch \
    --resource-group mygroup \
    --sku standard \
    --location eastus
```

```python
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.core.credentials import AzureKeyCredential

# Create index client
index_client = SearchIndexClient(
    endpoint="https://mysearch.search.windows.net",
    credential=AzureKeyCredential(api_key)
)

# Define index with vector search
fields = [
    SearchField(name="id", type=SearchFieldDataType.String, key=True),
    SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="myProfile"
    ),
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(name="myHnsw"),
    ],
    profiles=[
        VectorSearchProfile(
            name="myProfile",
            algorithm_configuration_name="myHnsw",
        ),
    ],
)

index = SearchIndex(
    name="my-index",
    fields=fields,
    vector_search=vector_search
)

index_client.create_or_update_index(index)
```

#### Vector Search Query

```python
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

search_client = SearchClient(
    endpoint="https://mysearch.search.windows.net",
    index_name="my-index",
    credential=AzureKeyCredential(api_key)
)

# Generate query embedding
query_embedding = get_embedding("What is Azure AI?")

# Vector search
vector_query = VectorizedQuery(
    vector=query_embedding,
    k_nearest_neighbors=5,
    fields="content_vector"
)

results = search_client.search(
    search_text=None,
    vector_queries=[vector_query],
    select=["id", "content"]
)

for result in results:
    print(f"Score: {result['@search.score']}, Content: {result['content']}")
```

### Document Intelligence

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint="https://mydocai.cognitiveservices.azure.com/",
    credential=AzureKeyCredential(api_key)
)

# Analyze document
with open("document.pdf", "rb") as f:
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request=f,
        content_type="application/pdf"
    )

result = poller.result()

# Extract text
for page in result.pages:
    for line in page.lines:
        print(line.content)

# Extract tables
for table in result.tables:
    for cell in table.cells:
        print(f"Row {cell.row_index}, Col {cell.column_index}: {cell.content}")
```

### Azure Machine Learning

#### Create Workspace

```bash
# Create ML workspace
az ml workspace create \
    --name myworkspace \
    --resource-group mygroup \
    --location eastus

# Create compute cluster
az ml compute create \
    --name cpu-cluster \
    --type AmlCompute \
    --min-instances 0 \
    --max-instances 4 \
    --size Standard_DS3_v2
```

#### Training Job

```python
from azure.ai.ml import MLClient, command, Input
from azure.ai.ml.entities import Environment
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="...",
    resource_group_name="mygroup",
    workspace_name="myworkspace"
)

# Define job
job = command(
    code="./src",
    command="python train.py --data ${{inputs.training_data}}",
    inputs={
        "training_data": Input(type="uri_folder", path="azureml://datastores/...")
    },
    environment="AzureML-sklearn-1.0@latest",
    compute="cpu-cluster",
    display_name="training-job"
)

# Submit job
returned_job = ml_client.jobs.create_or_update(job)
```

### Content Safety

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory, AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint="https://mycontentsafety.cognitiveservices.azure.com/",
    credential=AzureKeyCredential(api_key)
)

# Analyze text
response = client.analyze_text(
    AnalyzeTextOptions(
        text="Your text here",
        categories=[
            TextCategory.HATE,
            TextCategory.SELF_HARM,
            TextCategory.SEXUAL,
            TextCategory.VIOLENCE
        ]
    )
)

for result in response.categories_analysis:
    print(f"{result.category}: severity {result.severity}")
```

### RAG Pattern Implementation

```python
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

# Initialize clients
openai_client = AzureOpenAI(...)
search_client = SearchClient(...)

def rag_query(user_question: str) -> str:
    # 1. Generate embedding for question
    embedding_response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=user_question
    )
    query_vector = embedding_response.data[0].embedding

    # 2. Search for relevant documents
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=5,
        fields="content_vector"
    )

    search_results = search_client.search(
        search_text=user_question,
        vector_queries=[vector_query],
        top=5
    )

    # 3. Build context from search results
    context = "\n\n".join([doc["content"] for doc in search_results])

    # 4. Generate answer with context
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"Answer based on this context:\n\n{context}"
            },
            {"role": "user", "content": user_question}
        ]
    )

    return response.choices[0].message.content
```

## Best Practices

1. **Security**: Use managed identities and Key Vault for credentials
2. **Rate Limits**: Implement retry logic with exponential backoff
3. **Cost Management**: Monitor token usage and set quotas
4. **Content Safety**: Always filter user inputs and model outputs
5. **Responsible AI**: Follow Microsoft's responsible AI guidelines

## Common Workflows

### Deploy Azure OpenAI
1. Create Azure OpenAI resource
2. Deploy model (GPT-4, embeddings)
3. Configure API access and keys
4. Implement client code with SDK
5. Monitor usage and costs

### Build RAG Solution
1. Set up Azure AI Search with vector index
2. Deploy embedding model in Azure OpenAI
3. Index documents with embeddings
4. Implement retrieval and generation
5. Add content safety filtering
