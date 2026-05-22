---
name: llamaindex
description: "Build LLM applications with LlamaIndex. Create indexes, query engines, and data connectors. Use for RAG applications, document search, and knowledge base systems."
---

# LlamaIndex Skill

Complete guide for LlamaIndex - data framework for LLM applications.

## Quick Reference

### Core Components
| Component | Description |
|-----------|-------------|
| **Documents** | Data containers |
| **Nodes** | Document chunks |
| **Indices** | Searchable structures |
| **Query Engines** | Question answering |
| **Agents** | Autonomous reasoning |
| **Tools** | Agent capabilities |

---

## 1. Installation

```bash
# Core
pip install llama-index

# With all integrations
pip install llama-index[all]

# Specific integrations
pip install llama-index-llms-openai
pip install llama-index-embeddings-openai
pip install llama-index-vector-stores-chroma
pip install llama-index-readers-file
```

---

## 2. Basic Setup

### Initialize
```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# Configure defaults
Settings.llm = OpenAI(model="gpt-4o", temperature=0.1)
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.chunk_size = 1024
Settings.chunk_overlap = 200
```

### Quick Start
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is the main topic?")
print(response)
```

---

## 3. Document Loading

### File Readers
```python
from llama_index.core import SimpleDirectoryReader

# Load from directory
documents = SimpleDirectoryReader(
    input_dir="./data",
    recursive=True,
    required_exts=[".pdf", ".md", ".txt"]
).load_data()

# Load specific files
documents = SimpleDirectoryReader(
    input_files=["./doc1.pdf", "./doc2.txt"]
).load_data()
```

### Specialized Readers
```python
from llama_index.readers.file import PDFReader, DocxReader
from llama_index.readers.web import SimpleWebPageReader

# PDF
pdf_reader = PDFReader()
documents = pdf_reader.load_data(file="document.pdf")

# Web pages
web_reader = SimpleWebPageReader()
documents = web_reader.load_data(urls=["https://example.com"])

# Database (requires llama-index-readers-database)
from llama_index.readers.database import DatabaseReader
reader = DatabaseReader(uri="postgresql://...")
documents = reader.load_data(query="SELECT * FROM articles")
```

### Create Documents Manually
```python
from llama_index.core import Document

documents = [
    Document(
        text="Content here",
        metadata={"source": "manual", "category": "tech"}
    ),
    Document(
        text="More content",
        metadata={"source": "manual", "category": "science"}
    )
]
```

---

## 4. Indices

### Vector Store Index
```python
from llama_index.core import VectorStoreIndex

# Create from documents
index = VectorStoreIndex.from_documents(documents)

# Save to disk
index.storage_context.persist(persist_dir="./storage")

# Load from disk
from llama_index.core import StorageContext, load_index_from_storage

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### With External Vector Store
```python
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb

# Create Chroma client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("my_collection")

# Create vector store
vector_store = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
```

### Summary Index
```python
from llama_index.core import SummaryIndex

# Good for summarization tasks
index = SummaryIndex.from_documents(documents)
query_engine = index.as_query_engine(response_mode="tree_summarize")
response = query_engine.query("Summarize all documents")
```

### Keyword Table Index
```python
from llama_index.core import KeywordTableIndex

# Good for keyword-based retrieval
index = KeywordTableIndex.from_documents(documents)
```

---

## 5. Query Engines

### Basic Query Engine
```python
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact"
)

response = query_engine.query("What is machine learning?")
print(response)
print(response.source_nodes)  # Retrieved documents
```

### Response Modes
```python
# Refine - iterate through nodes refining answer
query_engine = index.as_query_engine(response_mode="refine")

# Compact - stuff nodes into single prompt
query_engine = index.as_query_engine(response_mode="compact")

# Tree summarize - hierarchical summarization
query_engine = index.as_query_engine(response_mode="tree_summarize")

# Simple summarize - concatenate and summarize
query_engine = index.as_query_engine(response_mode="simple_summarize")

# No text - return nodes only
query_engine = index.as_query_engine(response_mode="no_text")
```

### Streaming
```python
query_engine = index.as_query_engine(streaming=True)

response = query_engine.query("Explain RAG")
for text in response.response_gen:
    print(text, end="", flush=True)
```

### Chat Engine
```python
chat_engine = index.as_chat_engine(chat_mode="condense_question")

# Conversation with memory
response = chat_engine.chat("What is LlamaIndex?")
print(response)

response = chat_engine.chat("How does it compare to LangChain?")
print(response)

# Reset memory
chat_engine.reset()
```

---

## 6. Retrievers

### Basic Retriever
```python
from llama_index.core.retrievers import VectorIndexRetriever

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10
)

nodes = retriever.retrieve("machine learning")
for node in nodes:
    print(f"Score: {node.score}, Text: {node.text[:100]}...")
```

### Hybrid Retriever
```python
from llama_index.core.retrievers import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever

# BM25 (keyword-based)
bm25_retriever = BM25Retriever.from_defaults(
    docstore=index.docstore,
    similarity_top_k=5
)

# Vector retriever
vector_retriever = index.as_retriever(similarity_top_k=5)

# Combine
hybrid_retriever = QueryFusionRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    similarity_top_k=5,
    num_queries=1
)

nodes = hybrid_retriever.retrieve("query")
```

### Auto-Merging Retriever
```python
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.retrievers import AutoMergingRetriever

# Create hierarchical nodes
node_parser = HierarchicalNodeParser.from_defaults(
    chunk_sizes=[2048, 512, 128]
)
nodes = node_parser.get_nodes_from_documents(documents)

# Build index with leaf nodes
leaf_nodes = [n for n in nodes if n.node_type == "leaf"]
index = VectorStoreIndex(leaf_nodes)

# Retriever that auto-merges to parent nodes
retriever = AutoMergingRetriever(
    index.as_retriever(similarity_top_k=6),
    storage_context=index.storage_context
)
```

---

## 7. Node Parsing

### Text Splitters
```python
from llama_index.core.node_parser import (
    SentenceSplitter,
    TokenTextSplitter,
    SemanticSplitterNodeParser
)

# Sentence splitter (default)
splitter = SentenceSplitter(
    chunk_size=1024,
    chunk_overlap=200
)
nodes = splitter.get_nodes_from_documents(documents)

# Token-based
splitter = TokenTextSplitter(
    chunk_size=1024,
    chunk_overlap=200
)

# Semantic (groups by meaning)
from llama_index.embeddings.openai import OpenAIEmbedding
splitter = SemanticSplitterNodeParser(
    embed_model=OpenAIEmbedding(),
    breakpoint_percentile_threshold=95
)
```

### Metadata Extraction
```python
from llama_index.core.extractors import (
    TitleExtractor,
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    KeywordsExtractor
)
from llama_index.core.ingestion import IngestionPipeline

pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=512),
        TitleExtractor(),
        SummaryExtractor(summaries=["self"]),
        KeywordsExtractor(keywords=5)
    ]
)

nodes = pipeline.run(documents=documents)
```

---

## 8. Agents

### Basic Agent
```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool

# Create tool from query engine
query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="knowledge_base",
    description="Useful for answering questions about the documents"
)

# Create agent
agent = ReActAgent.from_tools(
    tools=[query_engine_tool],
    llm=Settings.llm,
    verbose=True
)

response = agent.chat("What are the main topics covered?")
```

### Custom Tools
```python
from llama_index.core.tools import FunctionTool

def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

def search_web(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return f"Search results for: {query}"

multiply_tool = FunctionTool.from_defaults(fn=multiply)
search_tool = FunctionTool.from_defaults(fn=search_web)

agent = ReActAgent.from_tools(
    tools=[multiply_tool, search_tool, query_engine_tool],
    verbose=True
)
```

### Multi-Document Agent
```python
from llama_index.core.tools import QueryEngineTool

# Create tools for each document collection
tools = []
for name, index in document_indices.items():
    tool = QueryEngineTool.from_defaults(
        query_engine=index.as_query_engine(),
        name=f"{name}_tool",
        description=f"Query the {name} documents"
    )
    tools.append(tool)

agent = ReActAgent.from_tools(tools, verbose=True)
```

---

## 9. Evaluation

### Response Evaluation
```python
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    CorrectnessEvaluator
)

# Faithfulness - is response grounded in context?
faithfulness = FaithfulnessEvaluator()
result = faithfulness.evaluate_response(response=response)
print(f"Faithfulness: {result.passing}")

# Relevancy - is response relevant to query?
relevancy = RelevancyEvaluator()
result = relevancy.evaluate_response(query="query", response=response)
print(f"Relevancy: {result.passing}")

# Correctness - compare to reference
correctness = CorrectnessEvaluator()
result = correctness.evaluate(
    query="What is X?",
    response="X is Y",
    reference="X is Y and Z"
)
```

### Retrieval Evaluation
```python
from llama_index.core.evaluation import RetrieverEvaluator

# Create evaluation dataset
eval_questions = ["Question 1?", "Question 2?"]
eval_answers = ["Answer 1", "Answer 2"]

evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"],
    retriever=retriever
)

results = []
for q, a in zip(eval_questions, eval_answers):
    result = evaluator.evaluate(query=q, expected_ids=[...])
    results.append(result)
```

---

## 10. Callbacks and Observability

### Basic Callbacks
```python
from llama_index.core.callbacks import CallbackManager, LlamaDebugHandler

# Debug handler
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager([llama_debug])

Settings.callback_manager = callback_manager

# Now all operations are traced
response = query_engine.query("What is RAG?")

# View trace
print(llama_debug.get_event_pairs())
```

### Custom Callback
```python
from llama_index.core.callbacks.base import BaseCallbackHandler
from llama_index.core.callbacks import CBEventType

class MyCallback(BaseCallbackHandler):
    def on_event_start(self, event_type, payload, **kwargs):
        print(f"Start: {event_type}")

    def on_event_end(self, event_type, payload, **kwargs):
        print(f"End: {event_type}")

callback_manager = CallbackManager([MyCallback()])
```

---

## 11. Common Patterns

### Multi-Index Query
```python
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool

# Multiple indices
tools = [
    QueryEngineTool.from_defaults(
        query_engine=index1.as_query_engine(),
        name="index1",
        description="Contains information about topic 1"
    ),
    QueryEngineTool.from_defaults(
        query_engine=index2.as_query_engine(),
        name="index2",
        description="Contains information about topic 2"
    )
]

# Sub-question engine decomposes complex queries
query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=tools
)

response = query_engine.query("Compare topic 1 and topic 2")
```

### Citation Engine
```python
from llama_index.core.query_engine import CitationQueryEngine

citation_engine = CitationQueryEngine.from_args(
    index,
    similarity_top_k=5,
    citation_chunk_size=512
)

response = citation_engine.query("What is machine learning?")
# Response includes citations: [1], [2], etc.
print(response.source_nodes)  # Cited sources
```

### Router Query Engine
```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

# Route queries to appropriate index
query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=tools
)
```

---

## Best Practices

1. **Chunk wisely** - Balance size and context
2. **Add metadata** - Improve retrieval
3. **Evaluate** - Measure RAG quality
4. **Use streaming** - Better UX
5. **Persist indices** - Avoid recomputation
6. **Hybrid retrieval** - Combine methods
7. **Tune top_k** - Balance recall/precision
8. **Custom prompts** - Domain-specific
9. **Monitor costs** - Track LLM usage
10. **Version indices** - Track data changes
