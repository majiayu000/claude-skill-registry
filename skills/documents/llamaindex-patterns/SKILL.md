---
name: llamaindex-patterns
description: LlamaIndex implementation patterns with templates, scripts, and examples for building RAG applications. Use when implementing LlamaIndex, building RAG pipelines, creating vector indices, setting up query engines, implementing chat engines, integrating LlamaCloud, or when user mentions LlamaIndex, RAG, VectorStoreIndex, document indexing, semantic search, or question answering systems.
allowed-tools: Bash, Read, Write, Edit
---

# LlamaIndex Patterns

Comprehensive implementation patterns, templates, and examples for building production-ready RAG (Retrieval-Augmented Generation) applications with LlamaIndex.

## Overview

This skill provides complete, functional implementations for:
- **RAG Pipeline Setup**: End-to-end document indexing and querying
- **Custom Retrievers**: Advanced retrieval strategies with filtering and reranking
- **LlamaCloud Integration**: Managed parsing and hosted indices
- **Chat Engines**: Conversational AI with memory management
- **Multi-Document RAG**: Cross-document reasoning and source attribution

All scripts, templates, and examples are production-ready and fully functional.

## Scripts

### 1. setup-llamaindex.sh
Automated LlamaIndex installation with dependency management and environment setup.

```bash
bash scripts/setup-llamaindex.sh
```

**Features:**
- Detects Python version and virtual environment
- Installs LlamaIndex core and common integrations
- Sets up vector stores (Chroma, Pinecone, Qdrant)
- Configures embedding models (OpenAI, HuggingFace)
- Creates .env template with all required API keys
- Generates requirements.txt for reproducibility
- Creates data and storage directories
- Validates installation

**Output:**
- `.env` file with API key templates
- `requirements.txt` with pinned versions
- `data/` directory for documents
- `storage/` directory for persisted indices
- Installation verification report

### 2. create-index.sh
Create a VectorStoreIndex from documents with progress tracking.

```bash
bash scripts/create-index.sh [data_dir] [storage_dir] [index_name]
```

**Arguments:**
- `data_dir`: Directory containing documents (default: `./data`)
- `storage_dir`: Where to persist the index (default: `./storage`)
- `index_name`: Name for the index (default: `default_index`)

**Features:**
- Loads documents from multiple formats (.txt, .pdf, .md, .csv, .json, .html)
- Configures optimal embedding model
- Shows progress during indexing
- Displays document statistics
- Persists index to disk
- Tests index with sample query
- Provides usage instructions

**Example:**
```bash
bash scripts/create-index.sh ./documents ./indices my_knowledge_base
```

### 3. test-llamaindex.sh
Comprehensive validation tests for LlamaIndex installation and configuration.

```bash
bash scripts/test-llamaindex.sh
```

**Tests:**
- Python 3 installation and version
- LlamaIndex core package and version
- Core imports (VectorStoreIndex, Settings, etc.)
- Environment file existence and configuration
- API key setup (OpenAI, Anthropic, etc.)
- Vector store integrations (Chroma, Pinecone, Qdrant)
- Embedding models (OpenAI, HuggingFace)
- LLM integrations (OpenAI, Anthropic)
- Basic functionality (index creation)
- Data and storage directories

**Output:**
- ✓ for passing tests
- ✗ for critical failures
- ⚠ for warnings
- Exit code 0 for success, 1 for failures

## Templates

### 1. basic-rag-pipeline.py
Complete RAG pipeline implementation with best practices.

**Features:**
- Document loading from directory
- Index creation and persistence
- Query with source attribution
- Interactive chat interface
- Configurable LLM and embedding models
- Error handling and validation

**Key Components:**
```python
class BasicRAGPipeline:
    def load_or_create_index()  # Smart index loading/creation
    def query()                  # Simple question answering
    def query_with_sources()     # Answers with citations
    def chat()                   # Interactive chat mode
```

**Usage:**
```python
from basic_rag_pipeline import BasicRAGPipeline

pipeline = BasicRAGPipeline(
    data_dir="./data",
    storage_dir="./storage",
    model="gpt-4o-mini"
)

pipeline.load_or_create_index()
response = pipeline.query("What is LlamaIndex?")
```

**Use Cases:**
- Document Q&A systems
- Knowledge base queries
- Research assistants
- Documentation search

### 2. custom-retriever.py
Advanced retrieval strategies with filtering, reranking, and hybrid search.

**Retrievers Included:**

**MetadataFilteredRetriever:**
- Filter results by metadata (category, author, date, etc.)
- Multi-tenant applications
- Document versioning
- Access control

**HybridRetriever:**
- Combines semantic search with keyword matching
- Configurable weights for vector vs keyword scores
- Better results for specific terminology
- Handles exact phrase matching

**RerankedRetriever:**
- Two-stage retrieval (broad then narrow)
- Custom scoring with multiple factors
- Recency weighting
- Document quality scoring

**Example:**
```python
from custom_retriever import MetadataFilteredRetriever

retriever = MetadataFilteredRetriever(
    index=index,
    similarity_top_k=10,
    metadata_filters={"category": "technical", "year": 2024}
)

nodes = retriever.retrieve("How to deploy?")
```

**Use Cases:**
- Filtered search (by category, date, author)
- Improved accuracy with hybrid search
- Production systems requiring precise results
- Applications with diverse document types

### 3. llamacloud-integration.py
LlamaCloud managed services integration template.

**Features:**
- LlamaParse for complex document parsing
- Managed index hosting
- Production deployment patterns
- Enterprise-ready architecture

**Components:**

**LlamaParse Integration:**
- Parse complex PDFs with tables/charts
- Multi-column layout handling
- OCR for scanned documents
- Academic paper processing

**Managed Indices:**
- Automatic scaling
- High availability
- Built-in monitoring
- Version control

**Example:**
```python
from llamacloud_integration import LlamaCloudRAG

rag = LlamaCloudRAG(api_key="your_key")
documents = rag.parse_with_llamaparse("complex.pdf")
rag.create_managed_index(documents, "prod-index")
```

**Use Cases:**
- Complex document parsing (PDFs with tables)
- Production RAG applications
- Enterprise deployments
- Scalable knowledge bases

**Note:** Requires LlamaCloud account and `llama-parse` package for full functionality. Template includes fallbacks for development.

## Examples

### 1. question-answering.py
Complete Q&A system with citations and interactive mode.

**Run:**
```bash
python examples/question-answering.py
```

**Features:**
- Automatic sample document creation
- Pre-configured example queries
- Source attribution with relevance scores
- Interactive chat mode
- Streaming responses (advanced)
- Metadata-aware queries

**Demonstrates:**
- Document loading and indexing
- Query engine configuration
- Source node extraction
- Response synthesis modes
- Interactive user interfaces

### 2. chatbot-with-memory.py
Conversational AI with memory management and context awareness.

**Run:**
```bash
python examples/chatbot-with-memory.py
```

**Features:**
- Conversation history tracking
- Context-aware multi-turn dialogues
- Memory summarization
- Session management
- Custom system prompts
- Sample knowledge base creation

**Components:**
```python
class ConversationalChatbot:
    def load_knowledge_base()      # Setup knowledge
    def initialize_chat_engine()   # Configure memory
    def chat()                     # Send/receive messages
    def reset_conversation()       # Clear memory
    def get_conversation_summary() # History summary
    def interactive_mode()         # CLI interface
```

**Commands:**
- `/help` - Show available commands
- `/reset` - Reset conversation memory
- `/summary` - View conversation history
- `/exit` - Exit chatbot

**Use Cases:**
- Customer service chatbots
- Technical support assistants
- Interactive documentation
- Educational tutoring systems

### 3. multi-document-rag.py
Advanced RAG with cross-document reasoning and filtering.

**Run:**
```bash
python examples/multi-document-rag.py
```

**Features:**
- Multiple document handling
- Metadata-based filtering
- Cross-document queries
- Source attribution by document
- Document comparison
- Category-based search

**Components:**
```python
class MultiDocumentRAG:
    def build_index()            # Index multiple docs
    def query_by_category()      # Filtered queries
    def cross_document_query()   # Search all docs
    def compare_documents()      # Compare specific docs
```

**Demonstrates:**
- Document metadata enrichment
- Category-based filtering
- Cross-document reasoning
- Source tracking by document
- Comparative analysis
- Interactive multi-doc search

**Use Cases:**
- Multi-source research
- Document comparison
- Categorized knowledge bases
- Enterprise document search

## Usage Instructions

### Initial Setup

**Step 1: Install Dependencies**
```bash
cd plugins/rag-pipeline/skills/llamaindex-patterns
bash scripts/setup-llamaindex.sh
```

**Step 2: Configure API Keys**
Edit `.env` file:
```bash
OPENAI_API_KEY=YOUR_API_KEY
ANTHROPIC_API_KEY=sk-ant-your-key-here  # Optional
```

**Step 3: Validate Installation**
```bash
bash scripts/test-llamaindex.sh
```

### Building Your First RAG Application

**Option 1: Using Scripts**
```bash
# 1. Add your documents to ./data directory
mkdir -p data
cp /path/to/your/docs/* data/

# 2. Create index
bash scripts/create-index.sh data storage my_index

# 3. Use the index in your code
python -c "
from llama_index.core import StorageContext, load_index_from_storage
storage_context = StorageContext.from_defaults(persist_dir='storage/my_index')
index = load_index_from_storage(storage_context)
response = index.as_query_engine().query('Your question?')
print(response)
"
```

**Option 2: Using Templates**
```bash
# Copy template to your project
cp templates/basic-rag-pipeline.py my_rag_app.py

# Customize and run
python my_rag_app.py
```

**Option 3: Using Examples**
```bash
# Run examples directly
python examples/question-answering.py
python examples/chatbot-with-memory.py
python examples/multi-document-rag.py
```

### Integration Patterns

**For Next.js Applications:**
```python
# Use in API route: app/api/chat/route.ts
# Create Python backend with FastAPI:

from fastapi import FastAPI
from basic_rag_pipeline import BasicRAGPipeline

app = FastAPI()
pipeline = BasicRAGPipeline()
pipeline.load_or_create_index()

@app.post("/query")
async def query(question: str):
    response = pipeline.query(question)
    return {"answer": response}
```

**For FastAPI Projects:**
```python
# Integrate into existing FastAPI app
from contextlib import asynccontextmanager
from basic_rag_pipeline import BasicRAGPipeline

rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_pipeline
    rag_pipeline = BasicRAGPipeline()
    rag_pipeline.load_or_create_index()
    yield

app = FastAPI(lifespan=lifespan)
```

**For Standalone Python Applications:**
```python
# Use directly in your Python code
from basic_rag_pipeline import BasicRAGPipeline

def main():
    pipeline = BasicRAGPipeline(
        data_dir="./knowledge_base",
        storage_dir="./indices"
    )
    pipeline.load_or_create_index()

    while True:
        question = input("Ask: ")
        answer = pipeline.query(question)
        print(f"Answer: {answer}")
```

## Advanced Patterns

### Custom Node Parsing
```python
from llama_index.core.node_parser import SentenceSplitter

node_parser = SentenceSplitter(
    chunk_size=512,      # Smaller chunks for precise retrieval
    chunk_overlap=50,    # Overlap for context continuity
)

index = VectorStoreIndex.from_documents(
    documents,
    node_parser=node_parser
)
```

### Multi-Index Routing
```python
# Use custom retriever template for routing between indices
tech_index = VectorStoreIndex.from_documents(tech_docs)
business_index = VectorStoreIndex.from_documents(business_docs)

# Route queries based on content
if "technical" in query.lower():
    response = tech_index.as_query_engine().query(query)
else:
    response = business_index.as_query_engine().query(query)
```

### Streaming Responses
```python
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("Your question")

for text in streaming_response.response_gen:
    print(text, end="", flush=True)
```

### Persisting and Loading Indices
```python
# Persist
index.storage_context.persist(persist_dir="./storage")

# Load
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

## Production Deployment

### Environment-Specific Configuration
```bash
# Development
export OPENAI_API_KEY=sk-dev-key
export ENVIRONMENT=development

# Production
export OPENAI_API_KEY=sk-prod-key
export ENVIRONMENT=production
export REDIS_URL=redis://prod-cache:6379  # For caching
```

### Monitoring and Observability
```python
# Enable logging
import logging
logging.basicConfig(level=logging.INFO)

# Track usage
from llama_index.core import set_global_handler
set_global_handler("simple")
```

### Error Handling
```python
try:
    response = pipeline.query(question)
except Exception as e:
    logger.error(f"Query failed: {e}")
    response = "I encountered an error. Please try again."
```

### Rate Limiting
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def query_with_rate_limit(question: str):
    return pipeline.query(question)
```

## Performance Optimization

### Caching
```python
# Enable response caching
from llama_index.core.storage.cache import SimpleCache

Settings.cache = SimpleCache()
```

### Batch Processing
```python
# Process multiple queries efficiently
questions = ["Q1", "Q2", "Q3"]
responses = [pipeline.query(q) for q in questions]
```

### Index Optimization
```python
# Use appropriate similarity_top_k
query_engine = index.as_query_engine(
    similarity_top_k=3  # Lower for speed, higher for accuracy
)
```

## Troubleshooting

### API Key Issues
```bash
# Validate environment
bash scripts/test-llamaindex.sh

# Check .env file
cat .env | grep OPENAI_API_KEY
```

### Import Errors
```bash
# Reinstall dependencies
bash scripts/setup-llamaindex.sh

# Verify installation
python -c "import llama_index; print(llama_index.__version__)"
```

### Index Not Loading
```python
# Check storage directory exists
import os
assert os.path.exists("./storage"), "Storage directory not found"

# Verify index files
assert os.path.exists("./storage/docstore.json"), "Index not persisted"
```

### Out of Memory
```python
# Reduce chunk size
node_parser = SentenceSplitter(chunk_size=256)  # Smaller chunks

# Process documents in batches
for batch in document_batches:
    batch_index = VectorStoreIndex.from_documents(batch)
    # Merge indices
```

## References

### Official Documentation
- LlamaIndex Framework: https://developers.llamaindex.ai/python/framework/
- VectorStoreIndex: https://developers.llamaindex.ai/python/framework/understanding/
- Query Engines: https://developers.llamaindex.ai/python/framework/use_cases/q_and_a
- LlamaCloud: https://docs.cloud.llamaindex.ai/

### GitHub Resources
- Examples: https://github.com/run-llama/llama_index/tree/main/docs/examples
- Cookbooks: https://github.com/run-llama/llama_index/tree/main/docs/cookbooks

### Community
- Discord: https://discord.gg/dGcwcsnxhU
- Twitter: @llama_index
- Blog: https://blog.llamaindex.ai/

## Best Practices

1. **Always persist indices** - Avoid rebuilding on every run
2. **Use appropriate chunk sizes** - Balance between context and precision
3. **Add metadata** - Enables filtering and better organization
4. **Monitor token usage** - Track costs in production
5. **Implement error handling** - Graceful degradation for API failures
6. **Cache responses** - Reduce API calls for common queries
7. **Version your indices** - Track changes over time
8. **Test with real data** - Validate with actual use cases
9. **Configure embeddings wisely** - Match model to use case
10. **Document your setup** - Record configurations and decisions
