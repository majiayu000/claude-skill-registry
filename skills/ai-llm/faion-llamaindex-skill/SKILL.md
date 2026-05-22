---
name: faion-llamaindex-skill
user-invocable: false
description: ""
---

# LlamaIndex RAG Framework

**Build Production-Ready RAG Pipelines (2025-2026)**

---

## Quick Reference

| Component | Purpose |
|-----------|---------|
| **Data Connectors** | Load documents from files, web, databases, APIs |
| **Node Parsers** | Chunk documents into nodes with metadata |
| **Index Types** | VectorStore, Keyword, KnowledgeGraph, Tree, Summary |
| **Query Engines** | Process queries and synthesize responses |
| **Retrievers** | Fetch relevant nodes from indices |
| **Response Synthesizers** | Generate final answers from retrieved context |
| **Agents** | Autonomous reasoning with tool use |
| **Evaluation** | Measure retrieval and response quality |

---

## Core Concepts

### RAG Pipeline Architecture

```
Documents → Data Connectors → Node Parser → Nodes
                                              ↓
                                      Embedding Model
                                              ↓
                                          Index
                                              ↓
Query → Query Engine → Retriever → Response Synthesizer → Response
```

### LlamaIndex vs LangChain

| Aspect | LlamaIndex | LangChain |
|--------|------------|-----------|
| **Focus** | Data/retrieval | Orchestration |
| **Strength** | RAG pipelines, indexing | Chains, agents, tools |
| **When to use** | Knowledge bases, document Q&A | Complex workflows, multi-step reasoning |
| **Integration** | Works well together | Works well together |

---

## Installation

```bash
# Core package
pip install llama-index

# With specific integrations
pip install llama-index-llms-openai
pip install llama-index-embeddings-openai
pip install llama-index-vector-stores-qdrant
pip install llama-index-readers-file
```

### Environment Setup

```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

# Or use Settings
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
```

---

## Data Connectors (Readers)

### SimpleDirectoryReader

```python
from llama_index.core import SimpleDirectoryReader

# Load all supported files from directory
documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".md", ".txt"],
    exclude_hidden=True,
).load_data()

# Load specific files
documents = SimpleDirectoryReader(
    input_files=["./doc1.pdf", "./doc2.txt"]
).load_data()

print(f"Loaded {len(documents)} documents")
```

**Supported Formats:**
- PDF, DOCX, PPTX, XLSX
- TXT, MD, HTML, JSON, CSV
- Images (with vision models)
- Audio (with whisper)

### Specialized Readers

```python
# PDF with page-level metadata
from llama_index.readers.file import PDFReader
reader = PDFReader()
documents = reader.load_data(file="./report.pdf")

# Web pages
from llama_index.readers.web import SimpleWebPageReader
documents = SimpleWebPageReader().load_data(
    urls=["https://example.com/page1", "https://example.com/page2"]
)

# Beautiful Soup for complex HTML
from llama_index.readers.web import BeautifulSoupWebReader
documents = BeautifulSoupWebReader().load_data(
    urls=["https://example.com"],
    custom_hostname="example.com"
)

# Notion
from llama_index.readers.notion import NotionPageReader
reader = NotionPageReader(integration_token="secret_...")
documents = reader.load_data(page_ids=["page_id_1", "page_id_2"])

# Database
from llama_index.readers.database import DatabaseReader
reader = DatabaseReader(
    sql_database=sql_database,  # SQLAlchemy connection
    engine=engine,
)
documents = reader.load_data(query="SELECT * FROM articles")

# GitHub
from llama_index.readers.github import GithubRepositoryReader
reader = GithubRepositoryReader(
    github_token="ghp_...",
    owner="owner",
    repo="repo",
)
documents = reader.load_data(branch="main")
```

### LlamaHub (1500+ Connectors)

```python
# Install from LlamaHub
from llama_index.readers.slack import SlackReader
from llama_index.readers.discord import DiscordReader
from llama_index.readers.confluence import ConfluenceReader
from llama_index.readers.google import GoogleDocsReader

# Browse: https://llamahub.ai/
```

---

## Node Parsers (Chunking)

### SentenceSplitter (Default)

```python
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(
    chunk_size=1024,      # Characters per chunk
    chunk_overlap=200,    # Overlap between chunks
    paragraph_separator="\n\n",
)

nodes = parser.get_nodes_from_documents(documents)
print(f"Created {len(nodes)} nodes")
```

### Semantic Chunking

```python
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()
parser = SemanticSplitterNodeParser(
    buffer_size=1,              # Sentences to group
    breakpoint_percentile_threshold=95,  # Similarity threshold
    embed_model=embed_model,
)

nodes = parser.get_nodes_from_documents(documents)
```

### Hierarchical Chunking

```python
from llama_index.core.node_parser import HierarchicalNodeParser

parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128],  # Parent → child hierarchy
)

nodes = parser.get_nodes_from_documents(documents)

# Nodes have parent-child relationships
for node in nodes:
    print(f"Level: {node.metadata.get('level')}")
    print(f"Parent: {node.relationships.get('parent')}")
```

### Token-Based Splitting

```python
from llama_index.core.node_parser import TokenTextSplitter

parser = TokenTextSplitter(
    chunk_size=256,       # Tokens (not characters)
    chunk_overlap=50,
    separator=" ",
)

nodes = parser.get_nodes_from_documents(documents)
```

### Markdown/Code Splitting

```python
from llama_index.core.node_parser import MarkdownNodeParser

# Splits by headers, preserves structure
parser = MarkdownNodeParser()
nodes = parser.get_nodes_from_documents(documents)

# Code-aware splitting
from llama_index.core.node_parser import CodeSplitter

parser = CodeSplitter(
    language="python",
    chunk_lines=40,
    chunk_lines_overlap=15,
)
```

### Metadata Extraction

```python
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
    SummaryExtractor,
    KeywordExtractor,
)
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512, chunk_overlap=50),
        TitleExtractor(nodes=5),
        QuestionsAnsweredExtractor(questions=3),
        SummaryExtractor(summaries=["self"]),
        KeywordExtractor(keywords=5),
    ]
)

nodes = pipeline.run(documents=documents)

# Each node now has rich metadata
for node in nodes:
    print(node.metadata)  # title, questions, summary, keywords
```

---

## Index Types

### VectorStoreIndex (Primary)

```python
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

# In-memory (development)
index = VectorStoreIndex.from_documents(documents)

# Persistent with Qdrant
client = QdrantClient(path="./qdrant_data")  # Local
# client = QdrantClient(url="http://localhost:6333")  # Server

vector_store = QdrantVectorStore(
    client=client,
    collection_name="my_collection",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

# Load existing index
index = VectorStoreIndex.from_vector_store(vector_store)
```

### Supported Vector Stores

| Store | Use Case | Code |
|-------|----------|------|
| **Qdrant** | Production, filtering | `llama-index-vector-stores-qdrant` |
| **Pinecone** | Managed, serverless | `llama-index-vector-stores-pinecone` |
| **Weaviate** | Hybrid search | `llama-index-vector-stores-weaviate` |
| **Chroma** | Local development | `llama-index-vector-stores-chroma` |
| **pgvector** | PostgreSQL native | `llama-index-vector-stores-postgres` |
| **Milvus** | Large scale | `llama-index-vector-stores-milvus` |
| **FAISS** | In-memory speed | `llama-index-vector-stores-faiss` |

### KeywordTableIndex (BM25)

```python
from llama_index.core import KeywordTableIndex

index = KeywordTableIndex.from_documents(
    documents,
    max_keywords_per_chunk=10,
)

# Good for exact keyword matching
query_engine = index.as_query_engine()
```

### KnowledgeGraphIndex

```python
from llama_index.core import KnowledgeGraphIndex
from llama_index.graph_stores.neo4j import Neo4jGraphStore

# With Neo4j
graph_store = Neo4jGraphStore(
    username="neo4j",
    password="password",
    url="bolt://localhost:7687",
)

index = KnowledgeGraphIndex.from_documents(
    documents,
    graph_store=graph_store,
    max_triplets_per_chunk=10,
    include_embeddings=True,
)

# Query with graph traversal
query_engine = index.as_query_engine(
    include_text=True,
    response_mode="tree_summarize",
)
```

### TreeIndex (Summarization)

```python
from llama_index.core import TreeIndex

# Builds hierarchical summaries
index = TreeIndex.from_documents(
    documents,
    num_children=10,  # Children per node
)

# Good for summarization tasks
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
)
```

### SummaryIndex (Full Context)

```python
from llama_index.core import SummaryIndex

# Passes ALL nodes to LLM
index = SummaryIndex.from_documents(documents)

# Best for small documents, comprehensive answers
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
)
```

### ComposableGraph (Multi-Index)

```python
from llama_index.core import ComposableGraph, ListIndex

# Create multiple indices
index1 = VectorStoreIndex.from_documents(docs_tech)
index2 = VectorStoreIndex.from_documents(docs_finance)

# Compose into graph
graph = ComposableGraph.from_indices(
    ListIndex,
    [index1, index2],
    index_summaries=[
        "Technical documentation",
        "Financial reports",
    ],
)

# Router chooses relevant index
query_engine = graph.as_query_engine()
```

---

## Query Engines

### Basic Query Engine

```python
# From index
query_engine = index.as_query_engine(
    similarity_top_k=5,          # Number of chunks to retrieve
    response_mode="compact",      # Response synthesis mode
    streaming=False,              # Enable streaming
)

response = query_engine.query("What is RAG?")

print(response.response)           # Answer
print(response.source_nodes)       # Retrieved chunks
print(response.metadata)           # Query metadata
```

### Response Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **refine** | Iteratively refine answer | Long context, accuracy |
| **compact** | Compress chunks, single LLM call | Fast, good default |
| **tree_summarize** | Hierarchical summarization | Large retrievals |
| **simple_summarize** | Concatenate and summarize | Small context |
| **no_text** | Return only source nodes | Custom processing |
| **accumulate** | Separate answer per node | Multi-source answers |
| **compact_accumulate** | Compact + accumulate | Balanced |

```python
# Refine mode (most accurate)
query_engine = index.as_query_engine(
    response_mode="refine",
    similarity_top_k=10,
)

# Tree summarize (large context)
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    similarity_top_k=20,
)
```

### SubQuestionQueryEngine

```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

# Create tools from indices
tools = [
    QueryEngineTool(
        query_engine=tech_index.as_query_engine(),
        metadata=ToolMetadata(
            name="tech_docs",
            description="Technical documentation for the product",
        ),
    ),
    QueryEngineTool(
        query_engine=finance_index.as_query_engine(),
        metadata=ToolMetadata(
            name="financial_reports",
            description="Financial reports and metrics",
        ),
    ),
]

# Decomposes complex questions
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools,
    use_async=True,
)

response = query_engine.query(
    "Compare the technical roadmap with financial projections for Q1"
)
```

### RouterQueryEngine

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools,
)

# LLM routes to appropriate index
response = query_engine.query("What are our revenue numbers?")
```

### SQL + Vector Hybrid

```python
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine

# SQL database
sql_database = SQLDatabase(engine, include_tables=["users", "orders"])

sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["users", "orders"],
)

# Combine with vector search
from llama_index.core.query_engine import SQLAutoVectorQueryEngine

query_engine = SQLAutoVectorQueryEngine(
    sql_query_engine=sql_query_engine,
    vector_query_engine=vector_index.as_query_engine(),
)

# Automatically routes text vs structured queries
response = query_engine.query(
    "How many orders do customers with 'gold' status have?"
)
```

---

## Retrievers

### VectorIndexRetriever

```python
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

nodes = retriever.retrieve("What is machine learning?")

for node in nodes:
    print(f"Score: {node.score}")
    print(f"Text: {node.text[:200]}...")
    print(f"Metadata: {node.metadata}")
```

### Hybrid Retriever (BM25 + Vector)

```python
from llama_index.core.retrievers import BM25Retriever
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# BM25 retriever
bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=10,
)

# Vector retriever
vector_retriever = index.as_retriever(similarity_top_k=10)

# Fusion with reciprocal rank
retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    retriever_weights=[0.4, 0.6],
    num_queries=1,  # Generate additional query variants
    mode="reciprocal_rerank",
)

nodes = retriever.retrieve("machine learning applications")
```

### Auto-Merging Retriever

```python
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.node_parser import HierarchicalNodeParser

# Create hierarchical nodes
parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)
nodes = parser.get_nodes_from_documents(documents)

# Build index with storage for relationships
from llama_index.core.storage.docstore import SimpleDocumentStore
docstore = SimpleDocumentStore()
docstore.add_documents(nodes)

storage_context = StorageContext.from_defaults(docstore=docstore)
index = VectorStoreIndex(nodes, storage_context=storage_context)

# Auto-merging retriever
retriever = AutoMergingRetriever(
    index.as_retriever(similarity_top_k=12),
    storage_context=storage_context,
    simple_ratio_thresh=0.5,  # Merge if >50% children retrieved
)

# Returns parent nodes when enough children match
nodes = retriever.retrieve("detailed explanation of RAG")
```

### Reranking

```python
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Cross-encoder reranking (local)
reranker = SentenceTransformerRerank(
    model="cross-encoder/ms-marco-MiniLM-L-2-v2",
    top_n=5,
)

# Cohere reranking (API)
reranker = CohereRerank(
    api_key="...",
    top_n=5,
)

# Apply to query engine
query_engine = index.as_query_engine(
    similarity_top_k=20,  # Retrieve more
    node_postprocessors=[reranker],  # Rerank to top 5
)
```

---

## Response Synthesis

### Custom Prompts

```python
from llama_index.core import PromptTemplate

# Custom QA prompt
qa_prompt = PromptTemplate(
    """You are a helpful assistant. Use the following context to answer the question.

Context:
{context_str}

Question: {query_str}

Answer in a clear, concise manner. If you don't know, say "I don't know."
"""
)

query_engine = index.as_query_engine(
    text_qa_template=qa_prompt,
)

# Custom refine prompt
refine_prompt = PromptTemplate(
    """Given the original answer and new context, refine the answer.

Original answer: {existing_answer}
New context: {context_msg}

Refined answer:"""
)

query_engine = index.as_query_engine(
    refine_template=refine_prompt,
    response_mode="refine",
)
```

### Response Synthesizer

```python
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode

synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT,
    use_async=True,
)

# Manual synthesis
from llama_index.core.query_engine import RetrieverQueryEngine

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=synthesizer,
)
```

### Structured Output

```python
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser

class AnalysisResult(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

output_parser = PydanticOutputParser(output_cls=AnalysisResult)

query_engine = index.as_query_engine(
    output_parser=output_parser,
)

response = query_engine.query("Analyze the document")
result: AnalysisResult = response.response
```

---

## Agents

### ReAct Agent

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# Query engine tool
query_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="knowledge_base",
    description="Search the knowledge base for information",
)

# Custom function tool
def calculate_sum(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

calc_tool = FunctionTool.from_defaults(fn=calculate_sum)

# Create agent
agent = ReActAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=llm,
    verbose=True,
)

response = agent.chat("What is the total if I add the revenue numbers?")
```

### OpenAI Agent

```python
from llama_index.agent.openai import OpenAIAgent

agent = OpenAIAgent.from_tools(
    tools=[query_tool, calc_tool],
    llm=OpenAI(model="gpt-4o"),
    verbose=True,
    system_prompt="You are a helpful financial analyst.",
)

response = agent.chat("Summarize Q1 performance and calculate growth rate")
```

### Agent with Memory

```python
from llama_index.core.memory import ChatMemoryBuffer

memory = ChatMemoryBuffer.from_defaults(token_limit=4096)

agent = ReActAgent.from_tools(
    tools=[query_tool],
    memory=memory,
    verbose=True,
)

# Maintains conversation history
agent.chat("Tell me about RAG")
agent.chat("How does it compare to fine-tuning?")  # Has context
```

### Multi-Agent Orchestration

```python
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner

# Worker 1: Research
research_worker = FunctionCallingAgentWorker.from_tools(
    tools=[research_query_tool],
    llm=llm,
)

# Worker 2: Analysis
analysis_worker = FunctionCallingAgentWorker.from_tools(
    tools=[analysis_query_tool, calc_tool],
    llm=llm,
)

# Orchestrator
from llama_index.core.agent import MultiAgentRunner

runner = MultiAgentRunner(
    workers={
        "research": research_worker,
        "analysis": analysis_worker,
    },
    orchestrator_prompt="Route research questions to research agent, analytical questions to analysis agent.",
)

response = runner.chat("Research market trends and analyze growth potential")
```

---

## Evaluation

### Retrieval Evaluation

```python
from llama_index.core.evaluation import (
    RetrieverEvaluator,
    generate_question_context_pairs,
)

# Generate evaluation dataset
qa_dataset = generate_question_context_pairs(
    nodes=nodes[:50],
    llm=llm,
    num_questions_per_chunk=2,
)

# Evaluate retriever
retriever = index.as_retriever(similarity_top_k=5)
evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"],
    retriever=retriever,
)

results = await evaluator.aevaluate_dataset(qa_dataset)
print(f"MRR: {results.mean_mrr}")
print(f"Hit Rate: {results.mean_hit_rate}")
```

### Response Evaluation

```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator,
)

# Faithfulness: Is answer grounded in context?
faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)

# Relevancy: Is answer relevant to question?
relevancy_evaluator = RelevancyEvaluator(llm=llm)

# Correctness: Is answer correct? (needs ground truth)
correctness_evaluator = CorrectnessEvaluator(llm=llm)

# Evaluate single response
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")

faithfulness_result = faithfulness_evaluator.evaluate_response(
    query="What is RAG?",
    response=response,
)
print(f"Faithful: {faithfulness_result.passing}")
print(f"Score: {faithfulness_result.score}")
print(f"Feedback: {faithfulness_result.feedback}")

relevancy_result = relevancy_evaluator.evaluate_response(
    query="What is RAG?",
    response=response,
)
print(f"Relevant: {relevancy_result.passing}")
```

### Batch Evaluation

```python
from llama_index.core.evaluation import BatchEvalRunner

# Prepare test questions
eval_questions = [
    "What is RAG?",
    "How does vector search work?",
    "What is chunking?",
]

# Run batch evaluation
runner = BatchEvalRunner(
    evaluators={
        "faithfulness": faithfulness_evaluator,
        "relevancy": relevancy_evaluator,
    },
    workers=4,
)

eval_results = await runner.aevaluate_queries(
    query_engine=query_engine,
    queries=eval_questions,
)

# Aggregate results
for metric, results in eval_results.items():
    scores = [r.score for r in results]
    print(f"{metric}: {sum(scores)/len(scores):.2f}")
```

### Pairwise Evaluation

```python
from llama_index.core.evaluation import PairwiseComparisonEvaluator

evaluator = PairwiseComparisonEvaluator(llm=llm)

# Compare two query engines
result = evaluator.evaluate(
    query="Explain RAG architecture",
    response=response_a,
    second_response=response_b,
)

print(f"Winner: {result.value}")  # A, B, or TIE
print(f"Reason: {result.feedback}")
```

---

## Production Patterns

### Caching

```python
from llama_index.core import Settings
from llama_index.core.llms import MockLLM

# LLM response caching
from llama_index.core.callbacks import LlamaDebugHandler

# Enable caching for embeddings
Settings.embed_model.cache_folder = "./embedding_cache"

# Persistent index storage
from llama_index.core import StorageContext, load_index_from_storage

# Save
index.storage_context.persist(persist_dir="./storage")

# Load
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### Streaming

```python
# Streaming responses
query_engine = index.as_query_engine(streaming=True)
streaming_response = query_engine.query("Explain RAG")

for text in streaming_response.response_gen:
    print(text, end="", flush=True)
```

### Async Operations

```python
import asyncio

# Async query
async def query_async():
    response = await query_engine.aquery("What is RAG?")
    return response

# Batch async queries
async def batch_queries(queries: list[str]):
    tasks = [query_engine.aquery(q) for q in queries]
    responses = await asyncio.gather(*tasks)
    return responses

# Run
responses = asyncio.run(batch_queries([
    "What is RAG?",
    "How does chunking work?",
    "Explain vector search",
]))
```

### Observability

```python
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

# Debug handler
debug_handler = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([debug_handler])

Settings.callback_manager = callback_manager

# Now all operations are traced
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")

# Get trace
print(debug_handler.get_llm_inputs_outputs())

# Integration with observability platforms
# pip install llama-index-instrumentation-langfuse
from llama_index.instrumentation.langfuse import LangfuseInstrumentation

instrumentation = LangfuseInstrumentation(
    public_key="pk-...",
    secret_key="sk-...",
)
Settings.instrumentation = instrumentation
```

### Error Handling

```python
from llama_index.core.llms import ChatMessage

try:
    response = query_engine.query("What is RAG?")
except Exception as e:
    # Fallback response
    response = "I'm sorry, I couldn't process your question. Please try again."

# Retry with exponential backoff
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def query_with_retry(question: str):
    return query_engine.query(question)
```

---

## LlamaCloud Integration

### LlamaParse (Document Processing)

```python
from llama_parse import LlamaParse

# Advanced PDF parsing with OCR and table extraction
parser = LlamaParse(
    api_key="llx-...",
    result_type="markdown",
    num_workers=4,
    verbose=True,
)

documents = parser.load_data("./complex_document.pdf")
```

### LlamaCloud Index

```python
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex

# Create managed index
index = LlamaCloudIndex.from_documents(
    documents,
    name="my_index",
    project_name="my_project",
    api_key="llx-...",
)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is RAG?")
```

---

## Chunking Strategy Guide

| Strategy | Chunk Size | Overlap | Use Case |
|----------|------------|---------|----------|
| **Small chunks** | 256-512 | 50-100 | Precise retrieval, Q&A |
| **Medium chunks** | 512-1024 | 100-200 | General purpose |
| **Large chunks** | 1024-2048 | 200-400 | Summarization, context |
| **Semantic** | Variable | N/A | Topic-based retrieval |
| **Hierarchical** | Multi-level | N/A | Complex documents |

### Choosing Chunk Size

```python
# Rule of thumb
# chunk_size = context_window / top_k / 2

# Example: GPT-4 (128k), top_k=5
# chunk_size = 128000 / 5 / 2 = 12800 tokens ~ 8000-10000 chars

# For typical RAG with GPT-4o:
# chunk_size = 512-1024 tokens (good balance)
# overlap = 10-20% of chunk_size
```

---

## Quick Start Template

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os

# Configuration
os.environ["OPENAI_API_KEY"] = "sk-..."
Settings.llm = OpenAI(model="gpt-4o", temperature=0)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",
)

response = query_engine.query("What is the main topic?")
print(response)

# With sources
for node in response.source_nodes:
    print(f"\n--- Source (score: {node.score:.2f}) ---")
    print(node.text[:200] + "...")
```

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| **Low retrieval quality** | Increase top_k, add reranking, tune chunk size |
| **Hallucinations** | Use faithfulness eval, stricter prompts, lower temperature |
| **Slow queries** | Use async, caching, reduce chunk overlap |
| **Missing context** | Increase chunk size, use hierarchical parsing |
| **Cost too high** | Use smaller embedding model, cache embeddings |
| **Index too large** | Use metadata filtering, partition by topic |

---

## References

- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [LlamaHub Connectors](https://llamahub.ai/)
- [LlamaIndex GitHub](https://github.com/run-llama/llama_index)
- [LlamaCloud](https://cloud.llamaindex.ai/)

---

## Related Skills

- `faion-langchain-skill` - Orchestration and chains
- `faion-vector-db-skill` - Vector database operations
- `faion-embeddings-skill` - Embedding models
- `faion-openai-api-skill` - OpenAI API integration

---

*LlamaIndex Skill v1.0 - 2026-01-18*
*RAG Framework for Production Knowledge Bases*


---

## Methodologies

| ID | Name | File |
|----|------|------|
| M-RAG-001-document-ingestion | M-RAG-001-document-ingestion | [methodologies/M-RAG-001-document-ingestion.md](methodologies/M-RAG-001-document-ingestion.md) |
| M-RAG-002-embedding-selection | M-RAG-002-embedding-selection | [methodologies/M-RAG-002-embedding-selection.md](methodologies/M-RAG-002-embedding-selection.md) |
| M-RAG-003-vector-db-design | M-RAG-003-vector-db-design | [methodologies/M-RAG-003-vector-db-design.md](methodologies/M-RAG-003-vector-db-design.md) |
| M-RAG-004-retrieval-strategies | M-RAG-004-retrieval-strategies | [methodologies/M-RAG-004-retrieval-strategies.md](methodologies/M-RAG-004-retrieval-strategies.md) |
| M-RAG-005-rag-evaluation | M-RAG-005-rag-evaluation | [methodologies/M-RAG-005-rag-evaluation.md](methodologies/M-RAG-005-rag-evaluation.md) |
| M-RAG-006-knowledge-graph-rag | M-RAG-006-knowledge-graph-rag | [methodologies/M-RAG-006-knowledge-graph-rag.md](methodologies/M-RAG-006-knowledge-graph-rag.md) |
| M-RAG-007-multimodal-rag | M-RAG-007-multimodal-rag | [methodologies/M-RAG-007-multimodal-rag.md](methodologies/M-RAG-007-multimodal-rag.md) |
| M-RAG-008-production-rag | M-RAG-008-production-rag | [methodologies/M-RAG-008-production-rag.md](methodologies/M-RAG-008-production-rag.md) |
