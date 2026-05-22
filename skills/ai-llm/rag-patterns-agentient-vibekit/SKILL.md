---
name: rag-patterns
version: "1.0"
description: >
  Vertex AI RAG Engine integration patterns for grounding agent responses in private data sources including corpus management, retrieval tool creation, and citation extraction.
  PROACTIVELY activate for: (1) RAG pipeline integration and Vertex AI RAG Engine setup, (2) corpus creation and document ingestion, (3) retrieval tool configuration and grounding metadata parsing.
  Triggers: "add rag", "rag pipeline", "vertex ai search"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# RAG Patterns: Vertex AI RAG Engine Integration

## Core Principles

Retrieval-Augmented Generation (RAG) grounds AI agent responses in authoritative data sources, dramatically reducing hallucinations and enabling agents to answer questions about private, domain-specific information not in their training data.

**Vertex AI RAG Engine** provides a managed service for the complete RAG pipeline: ingestion, embedding, indexing, retrieval, and citation generation.

## RAG Process Overview

### The 5-Stage RAG Pipeline

```
1. INGEST
   └─> Upload documents (PDF, TXT, HTML, etc.) to GCS

2. TRANSFORM & CHUNK
   └─> Split documents into semantic chunks (typically 500-1000 tokens)

3. EMBED
   └─> Generate vector embeddings for each chunk using embedding model

4. INDEX
   └─> Store embeddings in vector database (Vertex AI RAG Corpus)

5. RETRIEVE & GENERATE
   └─> At query time:
       a. Embed user query
       b. Find semantically similar chunks (vector search)
       c. Pass chunks to LLM as context
       d. Generate grounded response with citations
```

## Corpus Management (Required Pattern)

### Creating a RAG Corpus

```python
"""
Create and manage Vertex AI RAG corpus for private knowledge base.
"""
import os
from google.cloud import aiplatform
from google.cloud.aiplatform import rag

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

aiplatform.init(project=PROJECT_ID, location=LOCATION)

async def create_rag_corpus(
    display_name: str,
    description: str
) -> rag.RagCorpus:
    """
    Create a new RAG corpus for knowledge base.

    Args:
        display_name: Human-readable name for the corpus
        description: Purpose and content description

    Returns:
        Created RagCorpus instance
    """
    # Create corpus
    corpus = rag.RagCorpus.create(
        display_name=display_name,
        description=description,
        # Optional: Configure embedding model
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-004"
        )
    )

    print(f"Created corpus: {corpus.name}")
    print(f"Resource name: {corpus.resource_name}")

    return corpus
```

### Listing Existing Corpora

```python
def list_rag_corpora() -> list[rag.RagCorpus]:
    """
    List all RAG corpora in the project.

    Returns:
        List of RagCorpus instances
    """
    corpora = rag.RagCorpus.list()

    for corpus in corpora:
        print(f"Name: {corpus.display_name}")
        print(f"ID: {corpus.name}")
        print(f"Description: {corpus.description}")
        print("---")

    return list(corpora)
```

### Deleting a Corpus

```python
def delete_rag_corpus(corpus_name: str) -> None:
    """
    Delete a RAG corpus.

    Args:
        corpus_name: Full resource name of corpus
                     Format: projects/{project}/locations/{location}/ragCorpora/{corpus_id}
    """
    corpus = rag.RagCorpus(corpus_name)
    corpus.delete()
    print(f"Deleted corpus: {corpus_name}")
```

## Document Ingestion (Required Pattern)

### Upload Documents from Google Cloud Storage

```python
from google.cloud.aiplatform import rag
from google.cloud.aiplatform.rag.utils import resources

async def import_files_to_corpus(
    corpus_name: str,
    gcs_uris: list[str],
    chunk_size: int = 1024,
    chunk_overlap: int = 200
) -> None:
    """
    Import documents from GCS into RAG corpus.

    Args:
        corpus_name: Full resource name of target corpus
        gcs_uris: List of GCS URIs (gs://bucket/path/file.pdf)
        chunk_size: Size of text chunks in tokens (default 1024)
        chunk_overlap: Overlap between chunks in tokens (default 200)

    Example:
        await import_files_to_corpus(
            corpus_name="projects/my-proj/locations/us-central1/ragCorpora/123",
            gcs_uris=[
                "gs://my-bucket/docs/manual.pdf",
                "gs://my-bucket/docs/guide.pdf"
            ]
        )
    """
    corpus = rag.RagCorpus(corpus_name)

    # Import files with chunking configuration
    response = rag.import_files(
        corpus_name=corpus.resource_name,
        paths=gcs_uris,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        max_embedding_requests_per_min=1000  # Rate limiting
    )

    print(f"Import started. Imported {len(gcs_uris)} files.")
    print(f"Response: {response}")
```

### Upload Local Files (via GCS)

```python
from google.cloud import storage
import asyncio

async def upload_local_files_to_rag(
    corpus_name: str,
    local_file_paths: list[str],
    gcs_bucket: str,
    gcs_prefix: str = "rag-docs/"
) -> None:
    """
    Upload local files to GCS, then import to RAG corpus.

    Args:
        corpus_name: RAG corpus resource name
        local_file_paths: Paths to local files
        gcs_bucket: GCS bucket name (without gs://)
        gcs_prefix: Prefix path in bucket for uploaded files

    Example:
        await upload_local_files_to_rag(
            corpus_name="projects/.../ragCorpora/123",
            local_file_paths=["./docs/manual.pdf", "./docs/faq.txt"],
            gcs_bucket="my-rag-bucket",
            gcs_prefix="company-docs/"
        )
    """
    # Initialize GCS client
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(gcs_bucket)

    gcs_uris = []

    # Upload each file to GCS
    for local_path in local_file_paths:
        filename = os.path.basename(local_path)
        gcs_path = f"{gcs_prefix}{filename}"

        blob = bucket.blob(gcs_path)
        blob.upload_from_filename(local_path)

        gcs_uri = f"gs://{gcs_bucket}/{gcs_path}"
        gcs_uris.append(gcs_uri)
        print(f"Uploaded {filename} to {gcs_uri}")

    # Import into RAG corpus
    await import_files_to_corpus(corpus_name, gcs_uris)
```

### Listing Files in Corpus

```python
def list_corpus_files(corpus_name: str) -> None:
    """
    List all files in a RAG corpus.

    Args:
        corpus_name: Full resource name of corpus
    """
    corpus = rag.RagCorpus(corpus_name)
    files = rag.list_files(corpus_name=corpus.resource_name)

    for file in files:
        print(f"File: {file.display_name}")
        print(f"  URI: {file.rag_file_source.gcs_source.uris}")
        print(f"  Status: {file.state}")
        print("---")
```

## ADK Agent Integration (Production Pattern)

### Creating RAG Tool for Agent

```python
from google import genai
from google.genai import types
from google.cloud.aiplatform import rag

async def create_rag_agent(
    corpus_name: str,
    system_instruction: str
) -> types.LlmAgent:
    """
    Create ADK agent with RAG retrieval capabilities.

    Args:
        corpus_name: Full resource name of RAG corpus
        system_instruction: Agent's system prompt

    Returns:
        LlmAgent with RAG tool

    Example:
        agent = await create_rag_agent(
            corpus_name="projects/.../ragCorpora/123",
            system_instruction="You are a helpful assistant that answers questions about our company policies."
        )
    """
    client = genai.Client(vertexai=True)

    # Create RAG retrieval tool
    rag_tool = types.Tool.from_retrieval(
        retrieval=types.VertexRagStore(
            rag_resources=[
                types.RagResource(
                    rag_corpus=corpus_name
                )
            ],
            similarity_top_k=10,  # Number of chunks to retrieve
            vector_distance_threshold=0.3  # Relevance threshold (0-1)
        )
    )

    # Create agent with RAG tool
    agent = types.LlmAgent(
        model="gemini-2.0-flash-exp",
        system_instruction=system_instruction,
        tools=[rag_tool]
    )

    return agent
```

### Configuring Retrieval Parameters

```python
def create_advanced_rag_tool(
    corpus_names: list[str],
    top_k: int = 10,
    distance_threshold: float = 0.3
) -> types.Tool:
    """
    Create RAG tool with advanced configuration.

    Args:
        corpus_names: List of corpus resource names (can search multiple)
        top_k: Number of chunks to retrieve (1-50)
        distance_threshold: Similarity threshold (0.0-1.0, lower = more similar)

    Returns:
        Configured RAG tool

    Retrieval Parameters Guide:
    - top_k=5: Fast, focused (best for specific queries)
    - top_k=10: Balanced (recommended)
    - top_k=20: Comprehensive (best for broad queries)

    - distance_threshold=0.2: Very strict (high precision, low recall)
    - distance_threshold=0.3: Balanced (recommended)
    - distance_threshold=0.5: Lenient (high recall, lower precision)
    """
    rag_resources = [
        types.RagResource(rag_corpus=corpus)
        for corpus in corpus_names
    ]

    rag_tool = types.Tool.from_retrieval(
        retrieval=types.VertexRagStore(
            rag_resources=rag_resources,
            similarity_top_k=top_k,
            vector_distance_threshold=distance_threshold
        )
    )

    return rag_tool
```

## Citation Extraction (Critical Pattern)

### Parsing Grounding Metadata

```python
from google import genai
from google.genai import types

async def query_rag_agent_with_citations(
    agent: types.LlmAgent,
    query: str
) -> dict[str, any]:
    """
    Query RAG agent and extract citations from grounding metadata.

    Args:
        agent: RAG-enabled agent
        query: User query

    Returns:
        Dictionary with response text and citations

    Example:
        result = await query_rag_agent_with_citations(
            agent=my_rag_agent,
            query="What is our return policy?"
        )

        print(result["response"])
        for citation in result["citations"]:
            print(f"Source: {citation['uri']}")
            print(f"Excerpt: {citation['text']}")
    """
    client = genai.Client(vertexai=True)

    # Create chat with agent
    chat = client.aio.chats.create(agent=agent)
    response = await chat.send_message(query)

    # Extract grounding metadata
    citations = []

    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]

        if hasattr(candidate, 'grounding_metadata'):
            metadata = candidate.grounding_metadata

            # Extract grounding supports (sources)
            if hasattr(metadata, 'grounding_supports'):
                for support in metadata.grounding_supports:
                    # Each support references a chunk from the corpus
                    citation = {
                        "uri": support.segment.uri if hasattr(support, 'segment') else None,
                        "text": support.segment.text if hasattr(support, 'segment') else None,
                        "start_index": support.start_index,
                        "end_index": support.end_index,
                        "confidence": support.confidence_score if hasattr(support, 'confidence_score') else None
                    }
                    citations.append(citation)

    return {
        "response": response.text,
        "citations": citations
    }
```

### Formatting Citations for User Display

```python
def format_response_with_citations(
    response_text: str,
    citations: list[dict]
) -> str:
    """
    Format RAG response with inline citations.

    Args:
        response_text: Generated response
        citations: List of citation dictionaries

    Returns:
        Formatted response with citation markers

    Example:
        Input:
          response_text = "Our return policy allows 30-day returns."
          citations = [{"uri": "gs://bucket/policy.pdf", "text": "..."}]

        Output:
          "Our return policy allows 30-day returns. [1]

           Sources:
           [1] policy.pdf: '30-day return policy for all items...'"
    """
    formatted = response_text

    # Add citation markers
    formatted += "\n\n**Sources:**\n"

    for idx, citation in enumerate(citations, start=1):
        source_name = citation.get("uri", "Unknown").split("/")[-1]
        excerpt = citation.get("text", "")[:100]  # First 100 chars

        formatted += f"[{idx}] {source_name}: '{excerpt}...'\n"

    return formatted
```

## RAG Quality Optimization

### Chunking Strategy

**Best Practices**:

```python
# Default (good for most use cases)
chunk_size = 1024  # tokens
chunk_overlap = 200  # tokens

# Technical documentation (shorter, precise chunks)
chunk_size = 512
chunk_overlap = 100

# Long-form content (books, articles)
chunk_size = 1536
chunk_overlap = 300

# FAQ-style content (question-answer pairs)
chunk_size = 256
chunk_overlap = 0  # No overlap needed
```

**Guidelines**:
- Larger chunks: More context, but less precise retrieval
- Smaller chunks: More precise, but may lose context
- Overlap: Prevents important information from being split

### Retrieval Tuning

```python
# Precise, factual queries (high precision)
rag_tool = create_advanced_rag_tool(
    corpus_names=[corpus],
    top_k=5,
    distance_threshold=0.2  # Strict
)

# Exploratory queries (high recall)
rag_tool = create_advanced_rag_tool(
    corpus_names=[corpus],
    top_k=20,
    distance_threshold=0.5  # Lenient
)
```

### Corpus Organization

**Option 1: Single Large Corpus**
- All documents in one corpus
- Simple management
- Good for homogeneous content

**Option 2: Multiple Domain-Specific Corpora**
- Separate corpus per domain (engineering, sales, legal)
- Better retrieval precision
- Easier to update specific domains

```python
# Query multiple corpora
engineering_corpus = "projects/.../ragCorpora/engineering-123"
sales_corpus = "projects/.../ragCorpora/sales-456"

rag_tool = create_advanced_rag_tool(
    corpus_names=[engineering_corpus, sales_corpus],
    top_k=10
)
```

## Complete RAG Integration Example

### End-to-End Implementation

```python
"""
Complete example: Create RAG agent for company documentation.
"""
import asyncio
from google.cloud import aiplatform
from google.cloud.aiplatform import rag
from google import genai
from google.genai import types

async def setup_company_docs_rag_agent() -> types.LlmAgent:
    """
    Set up RAG agent for company documentation Q&A.

    Steps:
    1. Create RAG corpus
    2. Upload documents
    3. Create agent with RAG tool
    4. Test with sample queries

    Returns:
        Configured RAG agent
    """
    # Step 1: Create corpus
    print("Creating RAG corpus...")
    corpus = await create_rag_corpus(
        display_name="Company Documentation",
        description="Employee handbook, policies, and procedures"
    )

    # Step 2: Upload documents
    print("Uploading documents...")
    await upload_local_files_to_rag(
        corpus_name=corpus.resource_name,
        local_file_paths=[
            "./docs/employee_handbook.pdf",
            "./docs/it_policies.pdf",
            "./docs/benefits_guide.pdf"
        ],
        gcs_bucket="my-company-docs",
        gcs_prefix="rag-corpus/"
    )

    # Wait for indexing (typically 2-5 minutes for small corpora)
    print("Waiting for indexing to complete...")
    await asyncio.sleep(180)  # 3 minutes

    # Step 3: Create RAG agent
    print("Creating RAG agent...")
    agent = await create_rag_agent(
        corpus_name=corpus.resource_name,
        system_instruction="""
        You are a helpful HR assistant for our company.

        Answer employee questions about:
        - Company policies and procedures
        - Benefits and compensation
        - IT policies and support

        **Critical Instructions:**
        - ONLY answer using information from the retrieved documents
        - If information isn't in the documents, say "I don't have that information"
        - ALWAYS cite your sources by mentioning the document name
        - Be concise but comprehensive
        """
    )

    # Step 4: Test queries
    print("\nTesting agent...")
    test_queries = [
        "What is the vacation policy?",
        "How do I reset my password?",
        "What health insurance options are available?"
    ]

    for query in test_queries:
        result = await query_rag_agent_with_citations(agent, query)
        print(f"\nQ: {query}")
        print(f"A: {result['response']}")
        print(f"Citations: {len(result['citations'])} sources")

    return agent

# Run setup
if __name__ == "__main__":
    agent = asyncio.run(setup_company_docs_rag_agent())
    print("\nRAG agent ready for production use!")
```

## Anti-Patterns to Avoid

### Not Extracting Citations
```python
# BAD: Ignoring grounding metadata
response = await chat.send_message(query)
return response.text  # No citations!

# GOOD: Always extract and display citations
result = await query_rag_agent_with_citations(agent, query)
return format_response_with_citations(result["response"], result["citations"])
```

### Uploading Unsupported File Types
```python
# BAD: Trying to upload binary formats without conversion
await import_files_to_corpus(
    corpus_name=corpus,
    gcs_uris=["gs://bucket/data.xlsx"]  # Not directly supported!
)

# GOOD: Convert to supported formats (PDF, TXT, HTML)
# Supported: PDF, TXT, HTML, MD
```

### No Rate Limiting on Large Imports
```python
# BAD: Importing thousands of files at once
await import_files_to_corpus(
    corpus_name=corpus,
    gcs_uris=[f"gs://bucket/doc{i}.pdf" for i in range(10000)]  # Too many!
)

# GOOD: Batch imports with rate limiting
batch_size = 100
for i in range(0, len(all_uris), batch_size):
    batch = all_uris[i:i + batch_size]
    await import_files_to_corpus(corpus_name=corpus, gcs_uris=batch)
    await asyncio.sleep(60)  # Rate limit
```

### Using RAG for Real-Time Data
```python
# BAD: Expecting RAG to have live data
query = "What is the current stock price?"  # RAG has static docs!

# GOOD: Use function calling tool for real-time data
stock_tool = create_stock_price_tool()  # API call
```

## When to Use This Skill

Activate this skill when:
- Integrating RAG into ADK agents
- Setting up Vertex AI RAG Engine
- Creating and managing RAG corpora
- Implementing citation extraction
- Troubleshooting RAG retrieval quality
- Optimizing chunking and retrieval parameters

## Integration Points

This skill **depends on**:
- `adk-fundamentals`: Agent structure for RAG integration
- `vertex-ai-sdk`: Model configuration
- `agentient-python-core/pydantic-v2-strict`: Schema definitions
- `agentient-python-core/async-patterns`: Async corpus operations

This skill **enables**:
- Knowledge-grounded agents
- Private data Q&A systems
- Citation-backed responses

## Related Resources

For deeper understanding:
- **Vertex AI RAG Overview**: https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview
- **RAG Quickstart**: https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart
- **ADK + RAG GitHub Example**: https://github.com/arjunprabhulal/adk-vertex-ai-rag-engine
- **RAG Developer Guide**: https://developers.googleblog.com/en/vertex-ai-rag-engine-a-developers-tool/
- **Weaviate on Vertex AI RAG**: https://weaviate.io/blog/google-rag-api
